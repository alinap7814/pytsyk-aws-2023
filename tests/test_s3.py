from remediator.src.s3 import S3

import unittest
from unittest.mock import patch
from os import environ


import json

put_bucket_policy_event = {
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

create_bucket_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.s3',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "AssumedRole",
            "principalId": "testPrincipalId:leonardo.bautista@accenture.com",
            "arn": "arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista@accenture.com",
            "accountId": "000000000000",
            "accessKeyId": "testAccessKey",
            "sessionContext": {
                "sessionIssuer": {
                    "type": "Role",
                    "principalId": "testPrincipalId",
                    "arn": "arn:aws:iam::000000000000:role/LP-Admin",
                    "accountId": "000000000000",
                    "userName": "LP-Admin"
                },
                "webIdFederationData": {},
                "attributes": {
                    "creationDate": "2022-03-15T15:04:08Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-15T15:14:01Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "CreateBucket",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "bucketName": "test-remediator-bucket",
            "Host": "test-remediator-bucket.s3.amazonaws.com",
            "x-amz-acl": "private"
        },
        "responseElements": None,
        "additionalEventData": {
            "SignatureVersion": "SigV4",
            "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
            "bytesTransferredIn": 0,
            "AuthenticationMethod": "AuthHeader",
            "x-amz-id-2": "JTAEB/Lwgf/hf5ks2tcKPYxv6MjEOdGCL77Vcjns+/cuNDLqvKybR3b4w3x0E91174I+yQrWgzo=",
            "bytesTransferredOut": 0
        },
        "requestID": "testRequestId",
        "eventID": "121e0ca9-c7f6-4584-8159-af4416169d39",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "vpcEndpointId": "testVpcEndpointId",
        "eventCategory": "Management"
    }
}

delete_bucket_policy = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.s3',
    'account': '000000000000',
    'time': '2022-03-15T15:14:26Z',
    'region': 'us-east-1',
    'resources': [],
    'detail': {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "AssumedRole",
            "principalId": "testPrincipalId:leonardo.bautista@accenture.com",
            "arn": "arn:aws:sts::000000000000:assumed-role/LP-Admin/leonardo.bautista@accenture.com",
            "accountId": "000000000000",
            "accessKeyId": "testAccessKey",
            "sessionContext": {
                "sessionIssuer": {
                    "type": "Role",
                    "principalId": "testPrincipalId",
                    "arn": "arn:aws:iam::000000000000:role/LP-Admin",
                    "accountId": "000000000000",
                    "userName": "LP-Admin"
                },
                "webIdFederationData": {},
                "attributes": {
                    "creationDate": "2022-03-15T15:05:43Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-15T15:13:01Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "DeleteBucketPolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "bucketName": "test-remediator-bucket",
            "Host": "test-remediator-bucket.s3.us-east-1.amazonaws.com",
            "policy": ""
        },
        "responseElements": None,
        "additionalEventData": {
            "SignatureVersion": "SigV4",
            "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
            "bytesTransferredIn": 0,
            "AuthenticationMethod": "AuthHeader",
            "x-amz-id-2": "K/yscJjcQo+pBsF7GHKDNf5e4zq6VzMyHxA6kAihkTk3eShhpm/B3eOZFGGtVwDz5er4vP7+U74=",
            "bytesTransferredOut": 0
        },
        "requestID": "testRequestId",
        "eventID": "60e8aa9e-0a0c-4ec6-8923-1e0f83b31a2d",
        "readOnly": False,
        "resources": [
            {
                "accountId": "000000000000",
                "type": "AWS::S3::Bucket",
                "ARN": "arn:aws:s3:::test-remediator-bucket"
            }
        ],
        "eventType": "AwsApiCall",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "vpcEndpointId": "vpce-00dc1369",
        "eventCategory": "Management"
    }
}


@patch.dict(environ, {'REMEDIATOR_ROLE': 'remediator-us-east-1-role-update-policy', 'POLICIES_TABLE': 'remediator-update-policy-policiesTable-1R8XQUIO9NSKU'})
class TestS3(unittest.TestCase):

    @ patch('remediator.src.s3.Investigate.remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    def test__bucket_remediations(self, mocked_bucket_name, mocked_remediations):
        expected_return = ('statement', 'exceptions')
        mocked_remediations.return_value = {
            'PolicyStatements': 'statement', 'Exceptions': 'exceptions'}
        mocked_bucket_name.return_value = 'test-remediator-bucket'
        remediations = S3(create_bucket_event)._S3__bucket_remediations()
        self.assertTupleEqual(remediations, expected_return)

    def test__bucket_name(self):
        expected_return = 'test-remediator-bucket'
        bucket_name = S3(create_bucket_event)._S3__bucket_name()
        self.assertEqual(bucket_name, expected_return)

    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.Connector.call')
    def test__current_bucket_policy_false(self, mocked_call, mocked_bucket_name):
        mocked_call.return_value = {'Error': {'Code': 'NoSuchBucketPolicy'}}
        mocked_bucket_name.return_value = 'test-remediator-bucket'
        bucket_policy = S3(create_bucket_event)._S3__current_bucket_policy()
        self.assertFalse(bucket_policy)
        mocked_call.assert_called_with(
            'get_bucket_policy', {'Bucket': 'test-remediator-bucket'})

    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.Connector.call')
    def test__current_bucket_policy(self, mocked_call, mocked_bucket_name):
        expected_return = {'BucketPolicy': 'aBucketPolicy'}
        mocked_bucket_name.return_value = 'test-remediator-bucket'
        mocked_call.return_value = {
            'Policy': {'BucketPolicy': 'aBucketPolicy'}}
        bucket_policy = S3(create_bucket_event)._S3__current_bucket_policy()
        self.assertDictEqual(bucket_policy, expected_return)
        mocked_call.assert_called_with(
            'get_bucket_policy', {'Bucket': 'test-remediator-bucket'})

    @ patch('remediator.src.s3.S3._S3__bucket_tags')
    def test__is_exempt_false_no_tags(
            self,
            mocked_bucket_tags
    ):
        mocked_bucket_tags.return_value = {'Error': {'anError': True}}
        is_exempt = S3(create_bucket_event)._S3__is_exempt([{'Error': {}}])
        self.assertFalse(is_exempt)

    @ patch('remediator.src.s3.S3._S3__bucket_tags')
    def test__is_exempt_false_with_tags(
            self,
            mocked_bucket_tags
    ):
        mocked_bucket_tags.return_value = {'TagSet': [
            {'Key': 'aKey', 'Value': 'aValue'}]}
        is_exempt = S3(create_bucket_event)._S3__is_exempt(
            [{'Tags': [{'Key': 'Exempt', 'Value': True}]}])
        self.assertFalse(is_exempt)

    @ patch('remediator.src.s3.S3._S3__bucket_tags')
    def test__is_exempt_true(
            self,
            mocked_bucket_tags
    ):
        mocked_bucket_tags.return_value = {'TagSet': [
            {'Value': True, 'Key': 'Exempt'}]}
        is_exempt = S3(create_bucket_event)._S3__is_exempt(
            [{'Tags': [{'Key': 'Exempt', 'Value': True}]}])
        self.assertTrue(is_exempt)

    @ patch('remediator.src.s3.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.s3.S3._S3__is_exempt', return_value=False)
    @ patch('remediator.src.s3.Connector.call')
    @ patch('remediator.src.s3.S3._S3__bucket_remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.S3._S3__current_bucket_policy')
    def test_bucket_policy_remediation_no_current_policy(
            self,
            mocked_policy,
            mocked_bucket_name,
            mocked_bucket_remediations,
            mocked_call,
            mocked_exempt,
            mocked_account
    ):
        expected_return = (
            'update',
            {'Version': '2012-10-17', 'Statement': [True]},
            'bucket'
        )
        mocked_bucket_remediations.return_value = ({'Ssl': True}, None)
        mocked_bucket_name.return_value = 'test-remediator-bucket'
        mocked_policy.return_value = False
        remediation = S3(create_bucket_event).bucket_policy_remediation()
        self.assertTupleEqual(remediation, expected_return)
        mocked_call.assert_called_with(
            'put_bucket_policy', {
                'Bucket': 'test-remediator-bucket',
                'Policy': '{"Version": "2012-10-17", "Statement": [true]}'
            }
        )

    @ patch('remediator.src.s3.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.s3.S3._S3__is_exempt', return_value=False)
    @ patch('remediator.src.s3.Connector.call')
    @ patch('remediator.src.s3.S3._S3__bucket_remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.S3._S3__current_bucket_policy')
    def test_bucket_policy_remediation_current_policy_violation(
            self,
            mocked_policy,
            mocked_bucket_name,
            mocked_bucket_remediations,
            mocked_call,
            mocked_exempt,
            mocked_account
    ):
        mocked_bucket_remediations.return_value = (
            {'ARequiredStatement': {'MustHave': {'Has': True}}},
            None
        )
        mocked_bucket_name.return_value = 'deleteme-bucket-oejicsaz5mth'
        mocked_policy.return_value = json.dumps({
            'Version': '2012-10-17',
            'Statement': [{'Statement': [{'DoesHave': {'Has': True}}]}]
        })
        remediation = S3(create_bucket_event).bucket_policy_remediation()
        mocked_call.assert_called_with(
            'put_bucket_policy', {
                'Bucket': 'deleteme-bucket-oejicsaz5mth',
                'Policy': '{"Version": "2012-10-17", "Statement": '
                '[{"Statement": [{"DoesHave": {"Has": true}}]}, '
                '{"MustHave": {"Has": true}}]}'}
        )

    @ patch('remediator.src.s3.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.s3.S3._S3__is_exempt', return_value=False)
    @ patch('remediator.src.s3.Connector.call')
    @ patch('remediator.src.s3.S3._S3__bucket_remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.S3._S3__current_bucket_policy')
    def test_bucket_policy_remediation_current_policy_no_violation(
            self,
            mocked_policy,
            mocked_bucket_name,
            mocked_bucket_remediations,
            mocked_call,
            mocked_exempt,
            mocked_account
    ):
        mocked_bucket_remediations.return_value = (
            {
                'ForceSSLOnlyAccess': {
                    'Resource': [
                        'arn:aws:s3:::test-remediation-bucket',
                        'arn:aws:s3:::test-remediation-bucket/*'
                    ],
                    'Condition': {
                        'Bool': {'aws:SecureTransport': 'false'}},
                    'Effect': 'Deny', 'Action': 's3:*', 'Principal':  '*'}},
            None
        )
        mocked_bucket_name.return_value = 'deleteme-bucket-oejicsaz5mth'
        mocked_policy.return_value = json.dumps({
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Deny',
                    'Principal': '*',
                    'Action': 's3:*',
                    'Resource': [
                        'arn:aws:s3:::test-remediation-bucket',
                        'arn:aws:s3:::test-remediation-bucket/*'
                    ],
                    'Condition': {'Bool': {'aws:SecureTransport': 'false'}}}]
        })
        S3(create_bucket_event).bucket_policy_remediation()
        mocked_call.assert_not_called()

    @ patch('remediator.src.s3.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.s3.S3._S3__is_exempt', return_value=True)
    @ patch('remediator.src.s3.Connector.call')
    @ patch('remediator.src.s3.S3._S3__bucket_remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.S3._S3__current_bucket_policy')
    def test_bucket_policy_remediation_exempt(
            self,
            mocked_policy,
            mocked_bucket_name,
            mocked_bucket_remediations,
            mocked_call,
            mocked_exempt,
            mocked_account
    ):
        expected_return = ('Exempt', {'Version': '2012-10-17', 'Statement': [{'Resource': ['arn:aws:s3:::test-remediation-bucket', 'arn:aws:s3:::test-remediation-bucket/*'], 'Condition': {
                           'Bool': {'aws:SecureTransport': 'false'}}, 'Effect': 'Deny', 'Action': 's3:*', 'Principal': '*'}]}, 'bucket')
        mocked_bucket_remediations.return_value = (
            {'ForceSSLOnlyAccess': {'Resource': ['arn:aws:s3:::test-remediation-bucket', 'arn:aws:s3:::test-remediation-bucket/*'], 'Condition': {
                'Bool': {'aws:SecureTransport': 'false'}}, 'Effect': 'Deny', 'Action': 's3:*', 'Principal': '*'}},
            None
        )
        mocked_bucket_name.return_value = 'deleteme-bucket-oejicsaz5mth'
        mocked_policy.return_value = False
        remediation = S3(create_bucket_event).bucket_policy_remediation()
        mocked_call.assert_not_called()
        mocked_bucket_name.assert_not_called()
        self.assertTupleEqual(remediation, expected_return)

    @ patch('remediator.src.s3.Investigate.wait_for_stack')
    @ patch('remediator.src.s3.S3._S3__bucket_tags')
    def test_waiter_no_tag(
        self,
        mocked_tags,
        mocked_wait_for_stack,
    ):
        mocked_tags.return_value = {'Error': {}}
        S3(create_bucket_event).waiter()
        mocked_wait_for_stack.assert_not_called()

    @ patch('remediator.src.s3.Investigate.wait_for_stack')
    @ patch('remediator.src.s3.S3._S3__bucket_tags')
    def test_waiter_no_stack_name(
        self,
        mocked_tags,
        mocked_wait_for_stack,
    ):
        mocked_tags.return_value = {'TagSet': [
            {'Key': 'aKey', 'Value': 'aValeu'}]}
        S3(create_bucket_event).waiter()
        mocked_wait_for_stack.assert_not_called()

    @ patch('remediator.src.s3.S3.bucket_policy_remediation')
    @ patch('remediator.src.s3.S3.waiter')
    @ patch('remediator.src.s3.Investigate.is_cloudformation', return_value=True)
    def test_remediate_cloudformation(
        self,
        mocked_is_cloudformation,
        mocked_waiter,
        mocked_policy_remediation
    ):
        S3(create_bucket_event).remediate()
        mocked_waiter.assert_called()
        mocked_policy_remediation.assert_called()

    @ patch('remediator.src.s3.Investigate.account', return_value={'Remediate': False})
    @ patch('remediator.src.s3.S3._S3__is_exempt', return_value=False)
    @ patch('remediator.src.s3.Connector.call')
    @ patch('remediator.src.s3.S3._S3__bucket_remediations')
    @ patch('remediator.src.s3.S3._S3__bucket_name')
    @ patch('remediator.src.s3.S3._S3__current_bucket_policy')
    def test_bucket_policy_remediation_false(
            self,
            mocked_policy,
            mocked_bucket_name,
            mocked_bucket_remediations,
            mocked_call,
            mocked_exempt,
            mocked_account
    ):
        expected_return = ('Notification', {'Version': '2012-10-17', 'Statement': [{'Resource': ['arn:aws:s3:::test-remediation-bucket', 'arn:aws:s3:::test-remediation-bucket/*'], 'Condition': {
                           'Bool': {'aws:SecureTransport': 'false'}}, 'Effect': 'Deny', 'Action': 's3:*', 'Principal': '*'}]}, 'bucket')
        mocked_bucket_remediations.return_value = (
            {'ForceSSLOnlyAccess': {'Resource': ['arn:aws:s3:::test-remediation-bucket', 'arn:aws:s3:::test-remediation-bucket/*'], 'Condition': {
                'Bool': {'aws:SecureTransport': 'false'}}, 'Effect': 'Deny', 'Action': 's3:*', 'Principal': '*'}},
            None
        )
        mocked_bucket_name.return_value = 'deleteme-bucket-oejicsaz5mth'
        mocked_policy.return_value = False
        remediation = S3(create_bucket_event).bucket_policy_remediation()
        mocked_call.assert_not_called()
        mocked_bucket_name.assert_not_called()
        self.assertTupleEqual(remediation, expected_return)

    # def test__tag_bucket(self):


if __name__ == '__main__':
    unittest.main(warnings='ignore')
