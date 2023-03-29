from remediator.src.connector import Connector


import unittest
from os import environ
from unittest.mock import patch
from botocore.exceptions import ClientError



@patch.dict(environ, {'REMEDIATOR_EXECUTION_ROLE': 'remediator-$Region-role-dev'})
class TestConnector(unittest.TestCase):

    @patch('remediator.src.connector.boto3')
    def test__credentials(self, mocked_boto):
        test_abstraction = 'client'
        test_service = 's3'
        test_event = {
            'account': 'testAccount',
            'id': 'testId',
            'region': 'testRegion',
            'detail': {'eventID': 'testEventId'}
        }
        expected_return = {
            'AccessKeyId': 'testAccessKeyId',
            'SecretAccessKey': 'testSecretAccessKey',
            'SessionToken': 'testSessionToken',
            'Expiration': 'expirationDateTime'
        }
        mocked_boto.client('sts').assume_role.return_value = {
            'Credentials': {
                'AccessKeyId': 'testAccessKeyId',
                'SecretAccessKey': 'testSecretAccessKey',
                'SessionToken': 'testSessionToken',
                'Expiration': 'expirationDateTime'
            },
            'AssumedRoleUser': {
                'AssumedRoleId': 'testAccessKeyId:testId',
                'Arn': 'arn:aws:sts::000000000000:assumed-role/remediator-role-dev/testId'
            },
            'ResponseMetadata': {
                'RequestId': 'testRequestId',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'testRequestId',
                    'content-type': 'text/xml',
                    'content-length': '1146',
                    'date': 'Wed, 13 Oct 2021 17:15:06 GMT'
                }, 'RetryAttempts': 0
            }
        }
        connector = Connector(test_event, test_abstraction, test_service)
        credentials = connector._Connector__credentials()
        mocked_boto.client('sts').assume_role.assert_called_with(
            RoleArn='arn:aws:iam::testAccount:role/remediator-testRegion-role-dev', RoleSessionName='testEventId')
        self.assertDictEqual(credentials, expected_return)

    @patch('remediator.src.connector.boto3.client')
    def test__credentials_error(self, mocked_client):
        test_abstraction = 'client'
        test_service = 's3'
        test_event = {
            'account': 'testAccount',
            'id': 'testId',
            'region': 'testRegion',
            'detail': {'eventID': 'testEventId'}
        }
        mocked_client('sts').assume_role.side_effect = [
            ClientError(
                error_response={'Error': {"Code": "aCode"}},
                operation_name='assume_role'
            )
        ]
        expected_return = {'Error': {'Code': 'aCode'}}
        connector = Connector(test_event, test_abstraction, test_service)
        credentials = connector._Connector__credentials()
        self.assertDictEqual(credentials, expected_return)

    @ patch('remediator.src.connector.Config')
    @ patch('remediator.src.connector.Connector._Connector__credentials')
    @ patch('remediator.src.connector.boto3')
    def test_connection_resource(
        self,
        mocked_boto3,
        mocked_credentials,
        mocked_config
    ):
        test_abstraction = 'resource'
        test_service = 's3'
        test_event = {
            'account': 'testAccount',
            'id': 'testId',
            'region': 'testRegion'
        }
        mocked_credentials.return_value = {
            'AccessKeyId': 'testAccessKeyId',
            'SecretAccessKey': 'testSecretAccessKey',
            'SessionToken': 'testSessionToken',
            'Expiration': 'expirationDateTime'
        }
        connector = Connector(test_event, test_abstraction, test_service)
        mocked_config.return_value = 'test_config'
        connector.connect()
        mocked_boto3.resource.assert_called_with(
            's3',
            region_name='testRegion',
            aws_access_key_id='testAccessKeyId',
            aws_secret_access_key='testSecretAccessKey',
            aws_session_token='testSessionToken',
            config='test_config'
        )

    @ patch('remediator.src.connector.Config')
    @ patch('remediator.src.connector.Connector._Connector__credentials')
    @ patch('remediator.src.connector.boto3')
    def test_connection_client(
        self,
        mocked_boto3,
        mocked_credentials,
        mocked_config
    ):
        test_abstraction = 'client'
        test_service = 's3'
        test_event = {
            'account': 'testAccount',
            'id': 'testId',
            'region': 'testRegion'
        }
        mocked_credentials.return_value = {
            'AccessKeyId': 'testAccessKeyId',
            'SecretAccessKey': 'testSecretAccessKey',
            'SessionToken': 'testSessionToken',
            'Expiration': 'expirationDateTime'
        }
        mocked_config.return_value = 'test_config'
        connector = Connector(test_event, test_abstraction, test_service)
        s3 = connector.connect()
        mocked_boto3.client.assert_called_with(
            's3',
            region_name='testRegion',
            aws_access_key_id='testAccessKeyId',
            aws_secret_access_key='testSecretAccessKey',
            aws_session_token='testSessionToken',
            config='test_config'
        )


if __name__ == '__main__':
    unittest.main(warnings='ignore')
