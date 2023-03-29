from botocore.exceptions import ClientError
from remediator.src.investigator import Investigate


from string import Template
from typing import Tuple
from boto3 import resource, client
from os import environ
from datetime import datetime
from json import dumps
import logging
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from copy import deepcopy


class Reporter(Investigate):

    def __init__(self, event: dict, remediation_type, violations=None, resource_type=None):
        self.event: dict = event
        self.remediation_type = remediation_type
        self.violations = violations
        self.resource_type = resource_type

    '''
        puts item in remediation table.
        args: None
        returns: None
    '''

    def archive(self) -> None:
        logging.info('adding remediation to table')
        # set table resource
        table: object = resource('dynamodb').Table(
            environ['REMEDIATION_TABLE'])
        # sets current time in iso format
        now: datetime = datetime.utcnow().isoformat()
        logging.debug({'now': now})
        # dict to add to remediation table
        remediation: dict = {
            'RemediationId': self.event['detail']['eventID'],
            'RemediationDate': now,
            'RemediationType': self.remediation_type.title(),
            'Account': self.event['account'],
            'Violations': self.violations,
            'Event': self.event
        }
        logging.info({'remediation': remediation})
        table.put_item(Item=remediation)
        return

    '''
        gets email parameters from policy table. parameters are text and
        attachment location
        args: none
        returns:
            - recipient, the email address to send email
            - email_text, formated text to email
            - attachment, attachment to email if avail

    '''

    def get_user_email(self):
        user = None
        user_identity = self.event['detail']['userIdentity']
        logging.debug({'user_identity': user_identity})
        # gets principal id from event, id in event 'text:someone@something.com'
        principal_id: str = user_identity['principalId']
        logging.info({'principal_id': principal_id})
        if '@' in principal_id:
            # get recipient from recipient id, splits by ':' then gets last item
            user = f"{principal_id.split(':')[-1]}"
        else:
            # ****CHANGE TO ACCOUNTS TABLE******
            user = self.account().get('Contact')
        logging.debug({'user': user})
        return user

    def __principal(self):
        return self.get_user_email().split('.')[0].title()

    def __default_email_text(self):
        raw_body = (
            'Hello $Principal,\n'
            'The following request:\n\t$RequestParameters\n'
            'Violated ACP policy thus the remediatort performed ($RemediationType)\n.'
            'The violations are:\n\t$Violations'
        )
        substitutions = {
            'Principal': self.__principal(),
            'RequestParameters': self.request_parameters(),
            'RemediationType': self.remediation_type,
            'Violations': self.violations
        }
        body = Template(raw_body).substitute(substitutions)
        return body

    def __email_policy(self):
        email_policy: dict = self.policy(['Email']).get('Email', {})
        logging.debug({'email_policy': email_policy})
        raw_email_body_text = email_policy.get('Text')
        logging.debug({'raw_email_body_text': raw_email_body_text})
        if raw_email_body_text:
            substitutions = {
                'principal': self.__principal(),
                'remediationType': self.remediation_type,
                'violations': self.violations
            }
            substitution_keys = Investigate.find_words(
                raw_email_body_text, '$')
            logging.debug({'substitution_keys': substitution_keys})
            for email_substitution_key, _ in deepcopy(substitutions).items():
                logging.debug(
                    {'email_substitution_key': email_substitution_key})
                if email_substitution_key not in substitution_keys:
                    logging.debug(
                        {'not_substitution_key': email_substitution_key})
                    del substitutions[email_substitution_key]
            logging.debug({'substitutions': substitutions})
            for substitution_key in substitution_keys:
                logging.debug({'substitution_key': substitution_key})
                substitution_value = list(Investigate.value_finder(
                    self.event, substitution_key))
                logging.debug({'substitution_value': substitution_value})
                if substitution_value:
                    substitution_value = substitution_value[0]
                    substitutions.update(
                        {substitution_key: substitution_value})
                else:
                    if substitutions.get(substitution_key):
                        continue
                    string_to_remove = f'${substitution_key}'
                    logging.debug({'string_to_remove': string_to_remove})
                    raw_email_body_text = \
                        raw_email_body_text.replace(string_to_remove, '')
            logging.debug({'raw_email_body_text': raw_email_body_text})
            logging.debug({'substitutions': substitutions})
            email_policy['Text'] = \
                Template(raw_email_body_text).substitute(substitutions)
        else:
            email_policy['Text'] = self.__default_email_text()
        logging.debug({'email_policy': email_policy})
        return email_policy

    '''
        sends email to recipient in the event using ses raw email
        args: None
        return: None
    '''

    def send(self) -> None:
        user_email = self.get_user_email()
        if not user_email:
            logging.info('no user email')
            return
        logging.info('sending email')
        email_policy = self.__email_policy()
        email_text = email_policy['Text']
        attachment_location = email_policy.get('Attachment')
        email_sender: str = environ['EMAIL_SENDER']
        logging.info({'email_sender': email_sender})
        email_domain: str = environ['EMAIL_DOMAIN_SOURCE']
        logging.info({'email_sender': email_sender})
        email_source = f"{email_sender}@{email_domain}"
        logging.info({'email_source': email_source})
        event_name = self.event_name()
        logging.debug({'event_name': event_name})
        message = MIMEMultipart()
        message['Subject'] = f'Remediator {event_name} - {self.remediation_type}'
        message['From'] = email_source
        message['To'] = user_email
        email_body = MIMEText(email_text)
        message.attach(email_body)
        if attachment_location:
            attachment = Investigate.reader(
                environ['POLICIES_BUCKET'], attachment_location)
            email_attachment = MIMEApplication(attachment)
            email_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=f'{event_name}.pdf'
            )
            message.attach(email_attachment)
        logging.info(f'sending email to {user_email}')
        try:
            client('ses').send_raw_email(
                RawMessage={
                    'Data': message.as_bytes()
                }
            )
        except ClientError as client_error:
            logging.error({'boto3_error': client_error.response})
        return email_body.as_string()
    '''
        sends email and puts item in remediation table
        args: none
        return: none
    '''

    def report(self):
        self.archive()
        self.send()
