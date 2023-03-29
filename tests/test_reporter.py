from remediator.src.reporter import Reporter

import unittest
from unittest.mock import patch
from os import environ


test_event_no_email = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.iam',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
        'eventVersion': '1.08',
        'userIdentity': {
            'type': 'AssumedRole',
            'principalId': 'testPrincipalKey:leonardo.bautista|accenture.com',
            'arn': 'arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista|accenture.com',
            'accountId': '000000000000',
            'accessKeyId': 'testAccessKey',
            'sessionContext': {
                'sessionIssuer': {
                    'type': 'Role',
                    'principalId': 'testPrincipalKey',
                    'arn': 'arn:aws:iam::000000000000:role/LP-Admin',
                    'accountId': '000000000000',
                    'userName': 'LP-Admin'
                },
                'webIdFederationData': {},
                'attributes': {
                    'creationDate': '2022-03-15T12:58:57Z',
                    'mfaAuthenticated': 'false'
                }
            }
        },
        'eventTime': '2022-03-15T13:26:50Z',
        'eventSource': 'iam.amazonaws.com',
        'eventName': 'CreatePolicyVersion',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'AWS Internal',
        'userAgent': 'AWS Internal',
        'requestParameters': {
            'policyArn': 'arn:aws:iam::000000000000:policy/test-policy',
            'policyDocument': '{"Version": "2012-10-17","Statement": ["Effect": "Allow","Action": ["ec2:*","iam:*"],"Resource": "*"}]}',
            'setAsDefault': True
        },
        'responseElements': {
            'policyVersion': {
                'versionId': 'v11',
                'isDefaultVersion': True,
                'createDate': 'Mar 15, 2022 1:26:50 PM'
            }
        },
        'requestID': 'e05b6ea6-7eff-4a6d-a899-1e44f6a87302',
        'eventID': 'a8915cc1-9015-4177-9d59-9d6144867695',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': False,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management',
        'sessionCredentialFromConsole': 'true'
    }
}

test_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.iam',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
        'eventVersion': '1.08',
        'userIdentity': {
            'type': 'AssumedRole',
            'principalId': 'testPrincipalKey:leonardo.bautista@accenture.com',
            'arn': 'arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista@accenture.com',
            'accountId': '000000000000',
            'accessKeyId': 'testAccessKey',
            'sessionContext': {
                'sessionIssuer': {
                    'type': 'Role',
                    'principalId': 'testPrincipalKey',
                    'arn': 'arn:aws:iam::000000000000:role/LP-Admin',
                    'accountId': '000000000000',
                    'userName': 'LP-Admin'
                },
                'webIdFederationData': {},
                'attributes': {
                    'creationDate': '2022-03-15T12:58:57Z',
                    'mfaAuthenticated': 'false'
                }
            }
        },
        'eventTime': '2022-03-15T13:26:50Z',
        'eventSource': 'iam.amazonaws.com',
        'eventName': 'CreatePolicyVersion',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'AWS Internal',
        'userAgent': 'AWS Internal',
        'requestParameters': {
            'policyArn': 'arn:aws:iam::000000000000:policy/test-policy',
            'policyDocument': '{"Version": "2012-10-17","Statement": ["Effect": "Allow","Action": ["ec2:*","iam:*"],"Resource": "*"}]}',
            'setAsDefault': True
        },
        'responseElements': {
            'policyVersion': {
                'versionId': 'v11',
                'isDefaultVersion': True,
                'createDate': 'Mar 15, 2022 1:26:50 PM'
            }
        },
        'requestID': 'e05b6ea6-7eff-4a6d-a899-1e44f6a87302',
        'eventID': 'testEventId',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': False,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management',
        'sessionCredentialFromConsole': 'true'
    }
}

test_bucket_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.s3',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
            'eventVersion': '1.08',
            'userIdentity': {
                'type': 'AssumedRole',
                'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
                'arn': 'arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista@accenture.com',
                'accountId': '000000000000',
                'accessKeyId': 'testAcccessKey',
                'sessionContext': {
                        'sessionIssuer': {
                            'type': 'Role',
                                    'principalId': 'testPrincipalId',
                                    'arn': 'arn:aws:iam::000000000000:role/LP-Admin',
                                    'accountId': '000000000000',
                                    'userName': 'LP-Admin'
                        },
                    'webIdFederationData': {},
                    'attributes': {
                            'creationDate': '2022-03-15T15:04:08Z',
                            'mfaAuthenticated': 'False'
                    }
                },
                'invokedBy': 'cloudformation.amazonaws.com'
            },
        'eventTime': '2022-03-15T15:14:26Z',
        'eventSource': 's3.amazonaws.com',
        'eventName': 'PutBucketPolicy',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'cloudformation.amazonaws.com',
        'userAgent': 'cloudformation.amazonaws.com',
        'requestParameters': {
                'bucketPolicy': {
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Condition': {
                            'Bool': {
                                'aws:SecureTransport': 'False'
                            }
                        },
                        'Action': ['s3:*'],
                        'Resource': ['arn:aws:s3:::test-remediator-bucket', 'arn:aws:s3:::test-remediator-bucket/*'],
                        'Effect': 'Deny',
                        'Principal': '*'
                    }]
                },
                'bucketName': 'test-remediator-bucket',
                'Host': 'test-remediator-bucket.s3.us-east-1.amazonaws.com',
                'policy': ''
            },
        'responseElements': None,
        'additionalEventData': {
                'SignatureVersion': 'SigV4',
                'CipherSuite': 'ECDHE-RSA-AES128-GCM-SHA256',
                'bytesTransferredIn': 246,
                'AuthenticationMethod': 'AuthHeader',
                'x-amz-id-2': '24z7PTPi5wP2rit595yl77TDs/B+bCcdYhRb8hyZfZ/upWg7rQOrF4EMHVV5cmeOVZVARXm+7xE=',
                'bytesTransferredOut': 0
                },
        'requestID': 'testRequestId',
        'eventID': 'testEventId',
        'readOnly': False,
        'resources': [{
            'accountId': '000000000000',
            'type': 'AWS::S3::Bucket',
            'ARN': 'arn:aws:s3:::test-remediator-bucket'
        }],
        'eventType': 'AwsApiCall',
        'managementEvent': True,
        'recipientAccountId': '000000000000',
        'vpcEndpointId': 'testVpcEndpointId',
        'eventCategory': 'Management'
    }
}

# @ removed to test no email address
test_policy_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.iam',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
        'eventVersion': '1.08',
        'userIdentity': {
            'type': 'AssumedRole',
            'principalId': 'testPrincipalId:leonardo.bautista.accenture.com',
            'arn': 'arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista@accenture.com',
            'accountId': '000000000000',
            'accessKeyId': 'testAccessKeyId',
            'sessionContext': {
                'sessionIssuer': {
                    'type': 'Role',
                    'principalId': 'testPrincipalId',
                    'arn': 'arn:aws:iam::000000000000:role/LP-Admin',
                    'accountId': '000000000000',
                    'userName': 'LP-Admin'
                },
                'webIdFederationData': {},
                'attributes': {
                    'creationDate': '2022-03-16T18:17:01Z',
                    'mfaAuthenticated': 'false'
                }
            },
            'invokedBy': 'cloudformation.amazonaws.com'
        },
        'eventTime': '2022-03-16T18:18:05Z',
        'eventSource': 'iam.amazonaws.com',
        'eventName': 'PutRolePolicy',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'cloudformation.amazonaws.com',
        'userAgent': 'cloudformation.amazonaws.com',
        'requestParameters': {
            'roleName': 'deleteme-role-17OOPQ13JLKB3',
            'policyName': 'compliant',
            'policyDocument': '{"Version":"2012-10-17","Statement":[{"Action":["logs:*"],"Resource":"arn:aws:lambda:us-east-1:000000000000:function:remediator-function-dev","Effect":"Allow"}]}'
        },
        'responseElements': None,
        'requestID': '21e6455e-a3cb-4bad-bcd6-3f0c2905a654',
        'eventID': 'a374154d-64d8-4265-b7cd-b4507fb3e5b6',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': True,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management'
    }
}


@patch.dict(
    environ,
    {
        'EMAIL_DOMAIN_SOURCE': 'hk.aabglaunchpad.com',
        'EMAIL_SENDER': 'remediator',
        'REMEDIATION_TABLE': 'remediator-refactor-remediationTable-MUC8GHHTG075',
        'POLICIES_BUCKET': 'remediator-refactor-policiesbucket-t8o5o3ilchbd',
        'POLICIES_TABLE': 'remediator-refactor-policiesTable-EF17U0LY8G59',
        'CONTACTS_TABLE': 'remediator-contactsTable-DOT2HWTO47O9'
    }
)
class TestReporter(unittest.TestCase):

    @ patch('remediator.src.reporter.datetime')
    @ patch('remediator.src.reporter.resource')
    def test_archive(
        self,
        mocked_resource,
        mocked_datetime
    ):
        mocked_response = {}
        mocked_datetime.utcnow().isoformat.return_value = '1978-06-21T00:00:00.000000'
        Reporter(
            test_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        ).archive()
        mocked_resource('dynamodb').Table().put_item.assert_called_with(Item={
            'RemediationId': 'testEventId',
            'RemediationDate': '1978-06-21T00:00:00.000000',
            'RemediationType': 'Delete',
            'Account': '000000000000',
            'Violations': [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'Event': test_event
        })

    @ patch('remediator.src.reporter.resource')
    def test_get_user_email(
        self,
        mocked_resource
    ):
        expected_return = 'leonardo.bautista@accenture.com'
        user = Reporter(
            test_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        ).get_user_email()
        self.assertEqual(user, expected_return)
        mocked_resource.assert_not_called()

    @ patch('remediator.src.reporter.Investigate.account')
    def test_get_user_email_no_email_in_event(
        self,
        mocked_account
    ):
        mocked_account.return_value = {
            'Contact': 'leonardo.bautista@accenture.com'}
        expected_return = 'leonardo.bautista@accenture.com'
        user = Reporter(
            test_event_no_email,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        ).get_user_email()
        self.assertEqual(user, expected_return)

    def test__principal(self):
        expected_return = 'Leonardo'
        principal = Reporter(
            test_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )._Reporter__principal()
        self.assertEqual(principal, expected_return)

    def test__default_email_text(
        self,
    ):
        request_parameters = test_bucket_event['detail']['requestParameters']
        expected_return = (
            'Hello Leonardo,\n'
            f'The following request:\n\t{request_parameters}\n'
            'Violated ACP policy thus the remediatort performed (delete)\n.'
            'The violations are:\n\tviolations'
        )
        email_body = Reporter(
            test_bucket_event,
            'delete',
            'violations',
            'policy'
        )._Reporter__default_email_text()
        self.assertEqual(email_body, expected_return)

    @ patch('remediator.src.reporter.Reporter._Reporter__default_email_text')
    @patch('remediator.src.investigator.resource')
    def test__email_policy_no_text(
        self,
        mocked_resource,
        mocked_default_email_text
    ):
        expected_return = {
            'Text': 'Hello Leonardo,  LP-Admin',
            'Attachment': '007_033_034_036_039 IAM Policies.pdf'
        }
        mocked_default_email_text.return_value = 'Hello Leonardo,  LP-Admin'
        mocked_resource('dynamoDb').Table().get_item.return_value = {
            'Item': {
                'Email': {
                    'Attachment': '007_033_034_036_039 IAM Policies.pdf'
                }
            }
        }
        email_policy = Reporter(
            test_bucket_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )._Reporter__email_policy()
        self.assertDictEqual(email_policy, expected_return)

    @patch('remediator.src.investigator.resource')
    def test__email_policy(
        self,
        mocked_resource,
    ):
        expected_return = {
            'Text': 'Hello Leonardo,  LP-Admin',
            'Attachment': '007_033_034_036_039 IAM Policies.pdf'
        }
        mocked_resource('dynamoDb').Table().get_item.return_value = {
            'Item': {
                'Email': {
                    'Text': 'Hello $principal, $notFound $userName',
                    'Attachment': '007_033_034_036_039 IAM Policies.pdf'
                }
            }
        }
        email_policy = Reporter(
            test_bucket_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )._Reporter__email_policy()
        self.assertDictEqual(email_policy, expected_return)

    @patch('remediator.src.investigator.resource')
    @ patch('remediator.src.reporter.client')
    @ patch('remediator.src.reporter.MIMEMultipart.as_bytes')
    def test_send(
        self,
        mocked_multipart,
        mocked_client,
        mocked_resource
    ):
        expected_return = (
            'Content-Type: text/plain; charset="us-ascii"\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n\n'
            'Hello Leonardo,  LP-Admin'
        )
        mocked_resource('dynamoDb').Table().get_item.return_value = {
            'Item': {
                'Email': {
                    'Text': 'Hello $principal, $notFound $userName'
                }
            }
        }
        mocked_multipart.return_value = 'testData'
        body_sent = Reporter(
            test_bucket_event,
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        ).send()
        mocked_client('ses').send_raw_email.assert_called_with(
            RawMessage={'Data': 'testData'})
        self.assertEqual(body_sent, expected_return)

    @ patch('remediator.src.reporter.Reporter.send')
    @ patch('remediator.src.reporter.Reporter.archive')
    def test_report(self, mocked_put, mocked_email):
        Reporter('testEvent', 'update', None).report()
        mocked_email.assert_called_once()
        mocked_put.assert_called_once()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
