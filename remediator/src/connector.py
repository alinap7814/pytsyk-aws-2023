import boto3
from os import environ
from botocore.exceptions import ClientError
import logging
from string import Template
from botocore.config import Config


'''
    Class returns a boto3 client or resource object with credentials
    environment variables:
        - REMEDIATOR_ROLE, the name of the role to assume
    args:
        - account number, the account number to get credentials
'''


class Connector:

    def __init__(self, event, abstraction, service):
        self.event = event
        self.abstraction = abstraction
        self.service = service

    '''
        gets credentials from a role
        args: None
        returns:
            dictionary with credentials
                {
                    'AccessKeyId': 'testAccessKeyId',
                    'SecretAccessKey': 'testSecretAccessKey',
                    'SessionToken': 'testSessionToken',
                    'Expiration': 'expirationDateTime'
                }
    '''

    def __credentials(self) -> dict:
        logging.info({'getting credentials'})
        region_name = self.event['region']
        role_name: str = environ['REMEDIATOR_EXECUTION_ROLE']
        role_name = Template(role_name).substitute(Region=region_name)
        logging.debug({'role_name': role_name})
        account_number: str = self.event['account']
        logging.debug({'account_number': account_number})
        event_id: str = self.event['detail']['eventID']
        # constructs the role arn
        role_arn: str = \
            f"arn:aws:iam::{account_number}:role/{role_name}"
        # gets response from AWS
        try:
            response: dict = boto3.client('sts').assume_role(
                RoleArn=role_arn,
                RoleSessionName=event_id
            )
            # gets the credential key
            return response['Credentials']
        except ClientError as client_error:
            logging.error({'boto_error': client_error.response})
            return client_error.response

    '''
        connects to AWS with credentials from tole
        args:
            - abstraction, client or resource
            - service: AWS service
        returns:
            boto3 object
    '''

    def connect(self):
        logging.info('connection to AWS')
        credentials: dict = self.__credentials()
        region_name = self.event['region']
        boto_config = Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        try:
            connection: object = getattr(boto3, self.abstraction)(
                self.service,
                region_name=region_name,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                config=boto_config
            )
            return connection
        except ClientError as client_error:
            logging.error({'boto_error': client_error.response})
            return client_error.response

    def call(self, method, kwargs):
        logging.info(
            f'*** {self.abstraction}.{self.service}.{method} ***'.upper())
        try:
            response = getattr(self.connect(), method)(**kwargs)
            logging.debug({'response': response})
            return response
        except ClientError as client_error:
            client_error_response = client_error.response
            logging.error({'boto_error': client_error_response})
            error_code = client_error_response['Error']['Code']
            if error_code == 'AccessDenied':
                raise Exception(f'*** {error_code.upper()} ***')
            return client_error.response
