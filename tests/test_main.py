from remediator.__main__ import handler

import unittest
from unittest.mock import patch
from os import environ


iam_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.iam',
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
            "accessKeyId": "testAccessId",
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
                    "creationDate": "2022-03-20T22:05:42Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-20T22:41:42Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "PutRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "roleName": "deleteme-role-151W0040UAQZ7",
            "policyName": "non-compliant",
            "policyDocument": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Action\":[\"logs:*\",\"logs:PutLogEvents\"],\"Resource\":\"*\",\"Effect\":\"Allow\"}]}"
        },
        "responseElements": None,
        "requestID": "bbb47a62-b22e-4066-a93b-a4724725ee21",
        "eventID": "93ed8e4c-b0aa-4d27-b818-c2258ea42628",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "managementEvent": False,
        "recipientAccountId": "000000000000",
        "eventCategory": "Management"
    }
}

cloudfront_event = {
    'version': '0',
    'id': 'testEventId',
    'detail-type': 'AWS API Call via CloudTrail',
    'source': 'aws.cloudfront',
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
            "accessKeyId": "testAccessId",
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
                    "creationDate": "2022-03-20T22:05:42Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-20T22:42:13Z",
        "eventSource": "cloudfront.amazonaws.com",
        "eventName": "CreateDistributionWithTags",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "distributionConfigWithTags": {
                "distributionConfig": {
                    "origins": {
                        "quantity": 1,
                        "items": [
                            {
                                "customHeaders": {
                                    "items": [],
                                    "quantity": 0
                                },
                                "domainName": "deleteme-compliantbucket-1ar7nzg3imzd1.s3.amazonaws.com",
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E3CIF3IC2SKBZS"
                                },
                                "originPath": "",
                                "id": "only-origin"
                            }
                        ]
                    },
                    "aliases": {
                        "items": [],
                        "quantity": 0
                    },
                    "defaultCacheBehavior": {
                        "functionAssociations": {
                            "quantity": 0,
                            "items": []
                        },
                        "minTTL": 0,
                        "defaultTTL": 31536000,
                        "lambdaFunctionAssociations": {
                            "items": [],
                            "quantity": 0
                        },
                        "fieldLevelEncryptionId": "",
                        "trustedSigners": {
                            "items": [],
                            "enabled": False,
                            "quantity": 0
                        },
                        "maxTTL": 31536000,
                        "trustedKeyGroups": {
                            "enabled": False,
                            "quantity": 0,
                            "items": []
                        },
                        "allowedMethods": {
                            "items": [
                                "GET",
                                "HEAD",
                                "OPTIONS"
                            ],
                            "quantity": 3,
                            "cachedMethods": {
                                "items": [
                                    "GET",
                                    "HEAD"
                                ],
                                "quantity": 2
                            }
                        },
                        "smoothStreaming": False,
                        "targetOriginId": "only-origin",
                        "viewerProtocolPolicy": "redirect-to-https",
                        "compress": True,
                        "forwardedValues": {
                            "cookies": {
                                "whitelistedNames": {
                                    "quantity": 0,
                                    "items": []
                                },
                                "forward": "none"
                            },
                            "queryString": False,
                            "headers": {
                                "quantity": 0,
                                "items": []
                            },
                            "queryStringCacheKeys": {
                                "quantity": 0,
                                "items": []
                            }
                        }
                    },
                    "callerReference": "c590658b-b145-cc96-349b-fb4e31ee63ce",
                    "webACLId": "",
                    "defaultRootObject": "index.html",
                    "customErrorResponses": {
                        "quantity": 1,
                        "items": [
                            {
                                "responsePagePath": "/index.html",
                                "errorCachingMinTTL": 300,
                                "responseCode": "200",
                                "errorCode": 404
                            }
                        ]
                    },
                    "enabled": True,
                    "cacheBehaviors": {
                        "quantity": 0,
                        "items": []
                    },
                    "httpVersion": "http1.1",
                    "comment": "HIDDEN_DUE_TO_SECURITY_REASONS",
                    "restrictions": {
                        "geoRestriction": {
                            "restrictionType": "none",
                            "items": [],
                            "quantity": 0
                        }
                    },
                    "logging": {
                        "includeCookies": False,
                        "prefix": "",
                        "bucket": "",
                        "enabled": False
                    },
                    "viewerCertificate": {
                        "cloudFrontDefaultCertificate": True,
                        "minimumProtocolVersion": "SSLv3"
                    },
                    "priceClass": "PriceClass_All",
                    "originGroups": {
                        "quantity": 0,
                        "items": []
                    }
                },
                "tags": {
                    "items": []
                }
            }
        },
        "responseElements": {
            "location": "https://cloudfront.amazonaws.com/2020-05-31/distribution/E24U8WV64JHNM3",
            "distribution": {
                "aRN": "arn:aws:cloudfront::000000000000:distribution/E24U8WV64JHNM3",
                "id": "E24U8WV64JHNM3",
                "lastModifiedTime": "Mar 20, 2022 10:42:12 PM",
                "activeTrustedSigners": {
                    "quantity": 0,
                    "enabled": False
                },
                "domainName": "d1jwj5rqj4ovjt.cloudfront.net",
                "activeTrustedKeyGroups": {
                    "quantity": 0,
                    "enabled": False
                },
                "inProgressInvalidationBatches": 0,
                "status": "InProgress",
                "distributionConfig": {
                    "origins": {
                        "quantity": 1,
                        "items": [
                            {
                                "connectionAttempts": 3,
                                "customHeaders": {
                                    "quantity": 0
                                },
                                "oacSigningBehavior": "never",
                                "domainName": "deleteme-compliantbucket-1ar7nzg3imzd1.s3.amazonaws.com",
                                "connectionTimeout": 10,
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E3CIF3IC2SKBZS"
                                },
                                "originShield": {
                                    "enabled": False
                                },
                                "originPath": "",
                                "id": "only-origin"
                            }
                        ]
                    },
                    "aliases": {
                        "quantity": 0
                    },
                    "defaultCacheBehavior": {
                        "functionAssociations": {
                            "quantity": 0
                        },
                        "minTTL": 0,
                        "defaultTTL": 31536000,
                        "lambdaFunctionAssociations": {
                            "quantity": 0
                        },
                        "fieldLevelEncryptionId": "",
                        "trustedSigners": {
                            "enabled": False,
                            "quantity": 0
                        },
                        "maxTTL": 31536000,
                        "trustedKeyGroups": {
                            "enabled": False,
                            "quantity": 0
                        },
                        "allowedMethods": {
                            "items": [
                                "HEAD",
                                "GET",
                                "OPTIONS"
                            ],
                            "quantity": 3,
                            "cachedMethods": {
                                "items": [
                                    "HEAD",
                                    "GET"
                                ],
                                "quantity": 2
                            }
                        },
                        "smoothStreaming": False,
                        "targetOriginId": "only-origin",
                        "viewerProtocolPolicy": "redirect-to-https",
                        "compress": True,
                        "forwardedValues": {
                            "cookies": {
                                "forward": "none"
                            },
                            "queryString": False,
                            "headers": {
                                "quantity": 0
                            },
                            "queryStringCacheKeys": {
                                "quantity": 0
                            }
                        }
                    },
                    "callerReference": "c590658b-b145-cc96-349b-fb4e31ee63ce",
                    "staging": False,
                    "webACLId": "",
                    "defaultRootObject": "index.html",
                    "customErrorResponses": {
                        "quantity": 1,
                        "items": [
                            {
                                "responsePagePath": "/index.html",
                                "errorCachingMinTTL": 300,
                                "responseCode": "200",
                                "errorCode": 404
                            }
                        ]
                    },
                    "enabled": True,
                    "cacheBehaviors": {
                        "quantity": 0
                    },
                    "continuousDeploymentPolicyId": "",
                    "httpVersion": "http1.1",
                    "comment": "HIDDEN_DUE_TO_SECURITY_REASONS",
                    "restrictions": {
                        "geoRestriction": {
                            "restrictionType": "none",
                            "quantity": 0
                        }
                    },
                    "logging": {
                        "includeCookies": False,
                        "prefix": "",
                        "bucket": "",
                        "enabled": False
                    },
                    "isIPV6Enabled": True,
                    "viewerCertificate": {
                        "cloudFrontDefaultCertificate": True,
                        "certificateSource": "cloudfront",
                        "minimumProtocolVersion": "TLSv1"
                    },
                    "priceClass": "PriceClass_All",
                    "originGroups": {
                        "quantity": 0
                    }
                }
            },
            "eTag": "E20NMCTGXL3Q96"
        },
        "requestID": "39d5b302-d104-43f5-a0da-a73c25012d55",
        "eventID": "a8a74f41-7d6a-445c-885b-f786dcfcc209",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "apiVersion": "2020_05_31",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "eventCategory": "Management"
    }
}

s3_event = {
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
            "accessKeyId": "testAccessId",
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
                    "creationDate": "2022-03-20T22:05:42Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-20T22:41:41Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "CreateBucket",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "bucketName": "deleteme-noncompliantbucket-p0hco4yi701k",
            "Host": "deleteme-noncompliantbucket-p0hco4yi701k.s3.amazonaws.com",
            "x-amz-acl": "private"
        },
        "responseElements": None,
        "additionalEventData": {
            "SignatureVersion": "SigV4",
            "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
            "bytesTransferredIn": 0,
            "AuthenticationMethod": "AuthHeader",
            "x-amz-id-2": "gB4xnbeZ6QGPg1z6u08tQjbjnQicR751poMPL2r+Nl8Z8Vk/2CiTLhNejXDYYVcjVTACB0Yh7eg=",
            "bytesTransferredOut": 0
        },
        "requestID": "RAQ57VCJ7TVZ424Y",
        "eventID": "7c16ff45-26ed-4972-98dc-331bcbf2a430",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "vpcEndpointId": "vpce-00dc1369",
        "eventCategory": "Management"
    }
}

s3_event_from_remediator = {
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
        'userIdentity': {
            'sessionContext': {
                'sessionIssuer': {
                    'userName': 'remediator-role'
                }
            }
        },
        "eventTime": "2022-03-20T22:41:41Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "CreateBucket",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "cloudformation.amazonaws.com",
        "userAgent": "cloudformation.amazonaws.com",
        "requestParameters": {
            "bucketName": "deleteme-noncompliantbucket-p0hco4yi701k",
            "Host": "deleteme-noncompliantbucket-p0hco4yi701k.s3.amazonaws.com",
            "x-amz-acl": "private"
        },
        "responseElements": None,
        "additionalEventData": {
            "SignatureVersion": "SigV4",
            "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
            "bytesTransferredIn": 0,
            "AuthenticationMethod": "AuthHeader",
            "x-amz-id-2": "gB4xnbeZ6QGPg1z6u08tQjbjnQicR751poMPL2r+Nl8Z8Vk/2CiTLhNejXDYYVcjVTACB0Yh7eg=",
            "bytesTransferredOut": 0
        },
        "requestID": "RAQ57VCJ7TVZ424Y",
        "eventID": "7c16ff45-26ed-4972-98dc-331bcbf2a430",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "vpcEndpointId": "vpce-00dc1369",
        "eventCategory": "Management"
    }
}

dynamo_db_event = {
    'Records': [
        {
            'eventID': '858c50a2da8e612ba84236e86726edeb',
            'eventName': 'MODIFY',
            'eventVersion': '1.1',
            'eventSource': 'aws:dynamodb',
            'awsRegion': 'us-east-1',
            'dynamodb': {
                'ApproximateCreationDateTime': 1661966388.0,
                'Keys': {
                    'AccountNumber': {
                        'S': '000000000000'
                    }
                },
                'NewImage': {
                    'RuleState': {
                        'S': 'DISABLED'
                    },
                    'Remediate': {
                        'BOOL': True
                    },
                    'AdministrationManaged': {
                        'BOOL': True
                    },
                    'Regions': {
                        'L': [{
                            'S': 'us-east-2'
                        }]
                    },
                    'AccountNumber': {
                        'S': '000000000000'
                    },
                    'Contact': {
                        'S': 'other.contact@accenture.com'
                    },
                    'Name': {
                        'S': 'operations'
                    }
                },
                'OldImage': {
                    'RuleState': {
                        'S': 'ENABLED'
                    },
                    'Remediate': {
                        'BOOL': True
                    },
                    'AdministrationManaged': {
                        'BOOL': True
                    },
                    'Regions': {
                        'L': [{
                            'S': 'us-east-2'
                        }]
                    },
                    'AccountNumber': {
                        'S': '000000000000'
                    },
                    'Contact': {
                        'S': 'leonardo.bautista@accenture.com'
                    },
                    'Name': {
                        'S': 'operations'
                    }
                },
                'SequenceNumber': '181900000000012964442789',
                'SizeBytes': 315,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            },
            'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/remediator-dev-accountsTable-1X14PDT5E5E5J/stream/2022-08-31T17:16:15.489'
        }
    ]
}


@ patch.dict(environ, {
    'REMEDIATOR_ROLE': 'remediator-us-east-1-role-refactor',
    'APP_NAME': 'remediator',
    'EMAIL_DOMAIN_SOURCE': 'hk.aabglaunchpad.com',
    'EMAIL_SENDER': 'remediator',
    'REMEDIATION_TABLE': 'remediator-refactor-remediationTable-MUC8GHHTG075',
    'POLICIES_BUCKET': 'remediator-refactor-policiesbucket-t8o5o3ilchbd',
    'POLICIES_TABLE': 'remediator-refactor-policiesTable-EF17U0LY8G59',
    'ADMINISTRATION_STACK_NAME': 'test-administration-stack',
    'ADMINISTRATION_ROLE_ARN': 'test-administration-role-arn',
    'ADMINISTRATION_ACCOUNT_ID': '000000000000',
    'ENVIRONMENT': 'dev'
})
class TestMain(unittest.TestCase):

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.Iam')
    def test_handler_iam(
        self,
        mocked_iam,
        mocked_reporter
    ):
        mocked_iam().remediate.return_value = ('delete', 'anUpdate', 'policy')
        handler(iam_event, None)
        mocked_iam().remediate.assert_called_once()
        mocked_reporter().report.assert_called()

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.Cloudfront')
    def test_handler_cloudfront(
        self,
        mocked_cloudfront,
        mocked_reporter
    ):
        mocked_cloudfront().remediate.return_value = (
            'update', 'aViolation', 'distribution')
        handler(cloudfront_event, None)
        mocked_reporter().report.assert_called()

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.S3')
    def test_handler_s3(
        self,
        mocked_s3,
        mocked_reporter
    ):
        mocked_s3().remediate.return_value = (
            'update', 'aViolation', 'distribution')
        handler(s3_event, None)
        mocked_reporter().report.assert_called()

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.S3')
    def test_handler_exempt_no_violations(
        self,
        mocked_s3,
        mocked_reporter
    ):
        mocked_s3().remediate.return_value = (
            None, [], 'distribution')
        handler(s3_event, None)
        mocked_reporter().report.assert_not_called()

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.S3')
    def test_handler_no_violations(
        self,
        mocked_s3,
        mocked_reporter
    ):
        mocked_s3().remediate.return_value = (
            None, [], 'distribution')
        handler(s3_event, None)
        mocked_reporter().report.assert_not_called()

    @ patch('remediator.__main__.Reporter')
    @ patch('remediator.__main__.Accounts')
    def test_handler_accounts(
        self,
        mocked_accounts,
        mocked_reporter
    ):
        handler(dynamo_db_event, None)
        mocked_accounts().operations.assert_called()
        mocked_reporter().report.assert_not_called()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
