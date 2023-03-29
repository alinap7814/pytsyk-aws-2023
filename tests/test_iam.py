import resource
from remediator.src.iam import Iam

import unittest
from unittest.mock import patch, call
from os import environ
import datetime
from dateutil.tz import tzutc


# sets logging format


put_role_policy_event = {
    'version': '0',
    'id': '5ba1f93a-a18a-aab1-89c8-6399b24eb92e',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.iam',
    'account': '000000000000',
    'time': '2022-04-02T00:19:19Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
            'eventVersion': '1.08',
            'userIdentity': {
                'type': 'AssumedRole',
                'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
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
                            'creationDate': '2022-04-01T23:58:29Z',
                            'mfaAuthenticated': 'false'
                        }
                },
                'invokedBy': 'cloudformation.amazonaws.com'
            },
        'eventTime': '2022-04-02T00:19:19Z',
        'eventSource': 'iam.amazonaws.com',
        'eventName': 'PutRolePolicy',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'cloudformation.amazonaws.com',
        'userAgent': 'cloudformation.amazonaws.com',
        'requestParameters': {
                'roleName': 'remediator-test-integration-exemptRole-2KNUCHVJPC8A',
                'policyName': 'compliant',
                'policyDocument': '{"Version":"2012-10-17","Statement":[{"Action":["logs:PutLogEvents"],"Resource":"arn:aws:lambda:us-east-1:000000000000:function:remediator-function-dev","Effect":"Allow"}]}'
                },
        'responseElements': None,
        'requestID': 'b305fdd1-0ca9-4839-b6fc-a27ab0bacd4d',
        'eventID': '1c038bae-b09f-4f23-96dd-14f039312a53',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': True,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management'
    }
}
put_role_policy_event_violating = {
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
            'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
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
            'policyDocument': '{"Version":"2012-10-17","Statement":[{"Action":"logs:*","Resource":"*","Effect":"Allow"}]}'
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

create_policy_event = {
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
            'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
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
                    'creationDate': '2022-03-14T19:59:29Z',
                    'mfaAuthenticated': 'false'
                }
            }
        },
        'eventTime': '2022-03-14T20:03:19Z',
        'eventSource': 'iam.amazonaws.com',
        'eventName': 'CreatePolicy',
        'awsRegion': 'us-east-1',
        'sourceIPAddress': 'AWS Internal',
        'userAgent': 'AWS Internal',
        'requestParameters': {
            'policyName': 'test-policy',
            'policyDocument': '{"Version": "2012-10-17","Statement": [{"Sid": "VisualEditor0","Effect": "Allow","Action": ["ec2:DescribeInstances"],"Resource": "*"}]}',
            'tags': []
        },
        'responseElements': {
            'policy': {
                'policyName': 'test-policy',
                'policyId': 'testPolicyId',
                'arn': 'arn:aws:iam::000000000000:policy/test-policy',
                'path': '/',
                'defaultVersionId': 'v1',
                'attachmentCount': 0,
                'permissionsBoundaryUsageCount': 0,
                'isAttachable': True,
                'createDate': 'Mar 14, 2022 8:03:19 PM',
                'updateDate': 'Mar 14, 2022 8:03:19 PM',
                'tags': []
            }
        },
        'requestID': '3ac2f82e-cf92-4ca6-879c-c20969740dd9',
        'eventID': 'ec592896-5b8a-4b6f-b4ae-a88f08df6ba0',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': True,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management',
        'sessionCredentialFromConsole': 'true'
    }
}

create_policy_version_event = {
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
        'eventID': 'a8915cc1-9015-4177-9d59-9d6144867695',
        'readOnly': False,
        'eventType': 'AwsApiCall',
        'managementEvent': False,
        'recipientAccountId': '000000000000',
        'eventCategory': 'Management',
        'sessionCredentialFromConsole': 'true'
    }
}

put_role_policy_event_with_wildcards = {
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
            'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
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
            'policyDocument': '{"Version":"2012-10-17","Statement":[{"Action":["s3:Descibe*", "s3:PutObject"],"Resource": ["arn:aws:s3:::a-bucket/", "arn:aws:s3:::a-bucket/*"],"Effect":"Allow"}]}'
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

put_role_policy_event_with_wildcards_violation = {
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
            'principalId': 'testPrincipalId:leonardo.bautista@accenture.com',
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
            'policyDocument': '{"Version":"2012-10-17","Statement":[{"Action":["s3:*", "s3:PutObject"],"Resource": ["*", "arn:aws:s3:::a-bucket/*"],"Effect":"Allow"}]}'
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


@ patch.dict(
    environ, {
        'REMEDIATOR_ROLE': 'remediator-us-east-1-role-refactor', 'POLICIES_TABLE': 'remediator-iam-policiesTable-KUR7H7EKM4HZ'
    }
)
class TestIam(unittest.TestCase):

    @ patch('remediator.src.iam.Investigate.remediations')
    def test__policy_remediations(
        self,
        mocked_remediations
    ):
        expected_return = ([{'Inspect': True}], [{'Exeptions': True}])
        mocked_remediations.return_value = {
            'Inspections': [{'Inspect': True}],
            'Exceptions': [{'Exeptions': True}]
        }
        remediations = Iam(put_role_policy_event)._Iam__policy_remediations()
        self.assertTupleEqual(remediations, expected_return)

    @ patch('remediator.src.iam.Iam._Iam__policy_remediations')
    def test__policy_violations_false(
        self,
        mocked_remediation
    ):
        expected_return = ([], 'exceptions')
        mocked_remediation.return_value = (
            [{'WildCardInActionAndResource': '*'}],
            'exceptions'
        )
        policy_violations = Iam(
            put_role_policy_event)._Iam__policy_violations()
        self.assertTupleEqual(policy_violations, expected_return)

    @ patch('remediator.src.iam.Iam._Iam__policy_remediations')
    def test__policy_violations_true(
        self,
        mocked_remediation
    ):
        expected_return = (
            [{'Action': 'logs:*', 'Effect': 'Allow', 'Resource': '*'}],
            'exeption')
        mocked_remediation.return_value = (
            [{'WildCardInActionAndResource': '*'}],
            'exeption'
        )
        policy_violations = Iam(
            put_role_policy_event_violating)._Iam__policy_violations()
        self.assertTupleEqual(policy_violations, expected_return)

    def test__is_exempt_true(self):
        test_exceptions = [{'Key': 'Exempt', 'Value': True}]
        requestor_tags = [
            {'Key': 'Exempt', 'Value': True},
            {'Key': 'aKey', 'Value': True}
        ]
        is_exempt = Iam(put_role_policy_event)._Iam__is_exempt(
            test_exceptions, requestor_tags)
        self.assertTrue(is_exempt)

    def test__is_exempt_false(self):
        test_exceptions = [{'Key': 'Exempt', 'Value': True}]
        requestor_tags = [
            {'Key': 'Exempt', 'Value': False},
            {'Key': 'aKey', 'Value': True}
        ]
        is_exempt = Iam(put_role_policy_event)._Iam__is_exempt(
            test_exceptions, requestor_tags)
        self.assertFalse(is_exempt)

    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Investigate.request_parameters')
    def test__role_tags(
        self,
        mocked_parameters,
        mocked_call
    ):
        expected_return = [{'Key': 'test', 'Value': 'tag'}]
        mocked_parameters.return_value = {
            'roleName': 'test-role'}
        mocked_call.return_value = {'Tags': [{'Key': 'test', 'Value': 'tag'}]}
        role_tags = Iam(put_role_policy_event)._Iam__role_tags()
        self.assertListEqual(role_tags, expected_return)

    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Investigate.request_parameters')
    def test__role_no_tags(
        self,
        mocked_parameters,
        mocked_call
    ):
        mocked_parameters.return_value = {
            'roleName': 'test-role'}
        mocked_call.return_value = {'Tags': []}
        role_tags = Iam(put_role_policy_event)._Iam__role_tags()
        self.assertFalse(role_tags)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.iam.Iam._Iam__role_tags')
    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=True)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_exempt(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_call,
        mocked_role_tags,
        mocked_account
    ):
        expected_return = (
            'exempt',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )
        mocked_role_tags.return_value = [{'Key': 'Exempt', 'Value': 'True'}]
        mocked_violations.return_value = (
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            [{'Tags': [{'Key': 'Exempt', 'Value': 'True'}]}]
        )
        remediation = Iam(put_role_policy_event).iam_policy()
        mocked_exempt.assert_called_with(
            [{'Key': 'Exempt', 'Value': 'True'}],
            [{'Key': 'Exempt', 'Value': 'True'}]
        )
        mocked_call.assert_not_called()
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.iam.Iam._Iam__role_tags')
    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Investigate.request_parameters')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=False)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_no_violations(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_request_parameters,
        mocked_call,
        mocked_role_tags,
        mocked_account
    ):
        expected_return = (None, [], 'policy')
        mocked_role_tags.return_value = [{'Key': 'Exempt', 'Value': 'True'}]
        mocked_violations.return_value = (
            [],
            [{'Tags': [{'Key': 'Exempt', 'Value': 'True'}]}]
        )
        remediation = Iam(put_role_policy_event).iam_policy()
        mocked_exempt.assert_called_with(
            [{'Key': 'Exempt', 'Value': 'True'}],
            [{'Key': 'Exempt', 'Value': 'True'}]
        )
        mocked_call.assert_not_called()
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.iam.Iam._Iam__role_tags')
    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Investigate.request_parameters')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=False)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_put_role(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_request_parameters,
        mocked_call,
        mocked_role_tags,
        mocked_account
    ):
        expected_return = (
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )
        mocked_role_tags.return_value = [{'Key': 'akey', 'Value': 'aValue'}]
        mocked_request_parameters.return_value = {
            'roleName': 'test-role',
            'policyName': 'test-policy'
        }
        mocked_violations.return_value = (
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            [{'Tags': [{'Key': 'Exempt', 'Value': True}]}]
        )
        remediation = Iam(put_role_policy_event).iam_policy()
        mocked_exempt.assert_called_with(
            [{'Key': 'Exempt', 'Value': True}],
            [{'Key': 'akey', 'Value': 'aValue'}])
        mocked_call.assert_called_with(
            'delete_role_policy',
            {'RoleName': 'test-role', 'PolicyName': 'test-policy'}
        )
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.connector.Connector.call')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=False)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_create_policy(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_call,
        mocked_account
    ):
        expected_return = (
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )
        mocked_violations.return_value = (
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            [{'Tags': [{'Key': 'Exempt', 'Value': True}]}]
        )
        remediation = Iam(create_policy_event).iam_policy()
        mocked_call.assert_called_with(
            'delete_policy',
            {'PolicyArn': 'arn:aws:iam::000000000000:policy/test-policy'}
        )
        mocked_exempt.assert_called_with(
            [{'Key': 'Exempt', 'Value': True}],
            []
        )
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.iam.Iam._Iam__policy_tags')
    @ patch('remediator.src.connector.Connector.call')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=False)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_create_policy_version(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_call,
        policy_tags,
        mocked_account
    ):
        policy_tags.return_value = [{'Key': 'akey', 'Value': 'aValue'}]
        expected_return = (
            'delete',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )
        mocked_violations.return_value = (
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            [{'Tags': [{'Key': 'Exempt', 'Value': True}]}]
        )
        mocked_call.return_value = {
            'Versions':
            [
                {'VersionId': 'v7', 'IsDefaultVersion': True, 'CreateDate': datetime.datetime(
                    2022, 3, 14, 23, 7, 53, tzinfo=tzutc())},
                {'VersionId': 'v6', 'IsDefaultVersion': False, 'CreateDate': datetime.datetime(
                    2022, 3, 14, 22, 48, 20, tzinfo=tzutc())}
            ]
        }
        remediation = Iam(create_policy_version_event).iam_policy()
        mocked_exempt.assert_called_with(
            [{'Key': 'Exempt', 'Value': True}],
            [{'Key': 'akey', 'Value': 'aValue'}]
        )
        mocked_call.assert_has_calls([
            call('list_policy_versions', {
                 'PolicyArn': 'arn:aws:iam::000000000000:policy/test-policy'}),
            call('set_default_policy_version', {
                 'PolicyArn': 'arn:aws:iam::000000000000:policy/test-policy', 'VersionId': 'v6'}),
            call('delete_policy_version', {'PolicyArn': 'arn:aws:iam::000000000000:policy/test-policy', 'VersionId': 'v7'})]
        )
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.connector.Connector.call')
    @ patch('remediator.src.iam.Investigate.request_parameters')
    def test__policy_tags(
        self,
        mocked_request_parameters,
        mocked_call
    ):
        mocked_request_parameters.return_value = {
            'policyArn': 'anArn'
        }
        policy_tags = Iam(create_policy_version_event)._Iam__policy_tags()
        mocked_call.assert_called_with(
            'list_policy_tags',
            {'PolicyArn': 'anArn'}
        )

    @ patch('remediator.src.iam.Iam._Iam__policy_remediations')
    def test__policy_violations_wildcards_false(
        self,
        mocked_remediation
    ):
        expected_return = ([], 'exceptions')
        mocked_remediation.return_value = (
            [{'WildCardInActionAndResource': '*'}],
            'exceptions'
        )
        policy_violations = Iam(
            put_role_policy_event_with_wildcards)._Iam__policy_violations()
        self.assertTupleEqual(policy_violations, expected_return)

    @ patch('remediator.src.iam.Iam._Iam__policy_remediations')
    def test__policy_violations_wildcards_true(
        self,
        mocked_remediation
    ):
        expected_return = (
            [{'Action': ['s3:*', 's3:PutObject'],
              'Resource': ['*', 'arn:aws:s3:::a-bucket/*'],
              'Effect': 'Allow'}], 'exceptions')
        mocked_remediation.return_value = (
            [{'WildCardInActionAndResource': '*'}],
            'exceptions'
        )
        policy_violations = Iam(
            put_role_policy_event_with_wildcards_violation)._Iam__policy_violations()
        self.assertTupleEqual(policy_violations, expected_return)

    @ patch('remediator.src.iam.Iam._Iam__policy_remediations')
    def test__policy_violations_wildcards_true(
        self,
        mocked_remediation
    ):
        expected_return = (
            [{'Action': ['s3:*', 's3:PutObject'],
              'Resource': ['*', 'arn:aws:s3:::a-bucket/*'],
              'Effect': 'Allow'}], 'exceptions')
        mocked_remediation.return_value = (
            [{'WildCardInActionAndResource': '*'}],
            'exceptions'
        )
        policy_violations = Iam(
            put_role_policy_event_with_wildcards_violation)._Iam__policy_violations()
        self.assertTupleEqual(policy_violations, expected_return)

    @ patch('remediator.src.iam.Investigate.account', return_value={'Remediate': False})
    @ patch('remediator.src.iam.Iam._Iam__role_tags')
    @ patch('remediator.src.iam.Connector.call')
    @ patch('remediator.src.iam.Iam._Iam__is_exempt', return_value=False)
    @ patch('remediator.src.iam.Iam._Iam__policy_violations')
    def test_policy_account_not_remediate(
        self,
        mocked_violations,
        mocked_exempt,
        mocked_call,
        mocked_role_tags,
        mocked_account
    ):
        expected_return = (
            'Notification',
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            'policy'
        )
        mocked_role_tags.return_value = [{'Key': 'aKey', 'Value': 'aValue'}]
        mocked_violations.return_value = (
            [{'Effect': 'Allow', 'Action': ['ec2:*'], 'Resource': '*'}],
            [{'Tags': [{'Key': 'Exempt', 'Value': 'True'}]}]
        )
        remediation = Iam(put_role_policy_event).iam_policy()
        mocked_call.assert_not_called()
        self.assertTupleEqual(remediation, expected_return)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
