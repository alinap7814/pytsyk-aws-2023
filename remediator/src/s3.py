from email import policy
from remediator.src.connector import Connector
from remediator.src.investigator import Investigate
from remediator.src.reporter import Reporter


from boto3 import client
import json
import os
from botocore.exceptions import ClientError
from copy import Error, deepcopy
import logging

'''
    object to interact with s3 service..
    Inheratance:
        - Connector, to interact with AWS
        - Investigate, sets of methods to get information from several sources
    - args:
        - event, aws cloudwatch event

'''


class S3(Connector, Investigate):

    def __init__(self, event):
        self.event = event
        self.service = 's3'
        self.abstraction = 'client'
        self.resource_type = 'bucket'
    '''
        construct force ssl statement
    '''

    def __bucket_remediations(self):
        bucket_name = self.__bucket_name()
        remediations = self.remediations({'BucketName': bucket_name})
        return remediations['PolicyStatements'], remediations['Exceptions']

    def __bucket_name(self) -> str:
        bucket_name = self.request_parameters()['bucketName']
        logging.debug({'bucket_name': bucket_name})
        return bucket_name

    def __current_bucket_policy(self):
        kwargs = {'Bucket': self.__bucket_name()}
        response = self.call('get_bucket_policy', kwargs)
        return response.get('Policy', False)

    def __bucket_tags(self):
        logging.debug('getting bucket tags')
        bucket_tags = \
            self.call('get_bucket_tagging', {'Bucket': self.__bucket_name()})
        logging.debug({'bucket_tags': bucket_tags})
        return bucket_tags

    def __is_exempt(self, exceptions):
        for exception in exceptions:
            exception_tags = exception.get('Tags', [])
        bucket_tags = self.__bucket_tags().get('TagSet')
        if bucket_tags:
            return [x for x in exception_tags if x in bucket_tags]
        return False

    # def __tag_bucket(self):
        # self.call('put_bucket_policy', put_bucket_policy_kwargs)

    def bucket_policy_remediation(self):
        violation = None
        remediation_type = None
        policy_statements, exceptions = self.__bucket_remediations()
        logging.debug(policy_statements)
        logging.debug(exceptions)
        is_exempt = self.__is_exempt(exceptions)
        logging.info({'is_exempt': is_exempt})
        remediate = self.account()['Remediate']
        bucket_policy = {'Version': '2012-10-17', 'Statement': []}
        current_policy = self.__current_bucket_policy()
        current_policy = json.loads(current_policy) \
            if current_policy else current_policy
        if not remediate:
            remediation_type = 'Notification'
        elif is_exempt:
            remediation_type = 'Exempt'
        else:
            remediation_type = 'update'
        for statement_name, statement in policy_statements.items():
            logging.debug(statement)
            if not current_policy:
                bucket_policy['Statement'].append(statement)
                violation = bucket_policy
            else:
                current_policy_statements = current_policy['Statement']
                logging.debug(current_policy_statements)
                for current_policy_statement in current_policy_statements:
                    try:
                        current_policy_statement.pop('Sid')
                        logging.debug('removed sid')
                    except Exception:
                        pass
                if statement not in current_policy_statements:
                    logging.info(f"{statement_name} not in current policy")
                    current_policy_statements.append(statement)
                    bucket_policy = current_policy
                    violation = bucket_policy
                    remediation_type = 'update'
        if violation and remediate and not is_exempt:
            put_bucket_policy_kwargs = {
                'Bucket': self.__bucket_name(),
            }
            put_bucket_policy_kwargs['Policy'] = json.dumps(bucket_policy)
            self.call('put_bucket_policy', put_bucket_policy_kwargs)
        return remediation_type, violation, self.resource_type

    def waiter(self):
        stack_name = None
        bucket_tags = self.__bucket_tags().get('TagSet')
        logging.debug({'bucket_tags': bucket_tags})
        if not bucket_tags:
            return
        for bucket_tag in bucket_tags:
            logging.debug({'bucket_tag': bucket_tag})
            if bucket_tag['Key'] == 'aws:cloudformation:stack-name':
                stack_name = bucket_tag['Value']
        if stack_name:
            logging.info('waiting for stack')
            self.wait_for_stack(stack_name)

    def remediate(self):
        is_cloudformation = self.is_cloudformation()
        logging.debug({'is_cloudformation': is_cloudformation})
        if is_cloudformation:
            self.waiter()
        return self.bucket_policy_remediation()
