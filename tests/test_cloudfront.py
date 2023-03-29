from remediator.src.cloudfront import Cloudfront

import unittest
from unittest.mock import patch, call
from os import environ
from decimal import Decimal


create_distribution_with_tags_event = {
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
            "accessKeyId": "TESTACCESSKEYID",
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
                    "creationDate": "2022-03-20T12:34:53Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-20T13:22:59Z",
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
                                "domainName": "deleteme-compliantbucket-izek8iwcndao.s3.amazonaws.com",
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E1FJQZYXTDFUQD"
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
                    "callerReference": "b40928d9-4bdb-e132-a603-d6b6ff1ffe5b",
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
            "location": "https://cloudfront.amazonaws.com/2020-05-31/distribution/testDistributionId",
            "distribution": {
                "aRN": "arn:aws:cloudfront::000000000000:distribution/testDistributionId",
                "id": "testDistributionId",
                "lastModifiedTime": "Mar 20, 2022 1:22:59 PM",
                "activeTrustedSigners": {
                    "quantity": 0,
                    "enabled": False
                },
                "domainName": "d31mbgtrc2csig.cloudfront.net",
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
                                "domainName": "deleteme-compliantbucket-izek8iwcndao.s3.amazonaws.com",
                                "connectionTimeout": 10,
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E1FJQZYXTDFUQD"
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
                    "callerReference": "b40928d9-4bdb-e132-a603-d6b6ff1ffe5b",
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
            "eTag": "E3U1DUD4AHF6P6"
        },
        "requestID": "fe0f4235-b22f-4315-9ff3-68b146dd177b",
        "eventID": "8bc83e3e-8365-4fc1-bc15-5be6d9ce876f",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "apiVersion": "2020_05_31",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "eventCategory": "Management"
    }
}

update_distribution_event = {
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
            "accessKeyId": "testAccesKey",
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
                    "creationDate": "2022-03-16T20:29:10Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-16T20:29:29Z",
        "eventSource": "cloudfront.amazonaws.com",
        "eventName": "UpdateDistribution",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "AWS Internal",
        "userAgent": "AWS Internal",
        "requestParameters": {
            "id": "EMKKSKR0PSVWI",
            "ifMatch": "E23C4I9Z8DACE2",
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
                            "domainName": "deleteme-compliantbucket-1weu4f25vurqh.s3.amazonaws.com",
                            "connectionTimeout": 10,
                            "s3OriginConfig": {
                                "originAccessIdentity": "origin-access-identity/cloudfront/E1FT2YGHTCWK8R"
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
                "callerReference": "ab7f36bc-7c02-14d6-046d-d2d6cce0e164",
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
                "enabled": False,
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
        "responseElements": {
            "distribution": {
                "aRN": "arn:aws:cloudfront::000000000000:distribution/EMKKSKR0PSVWI",
                "id": "EMKKSKR0PSVWI",
                "lastModifiedTime": "Mar 16, 2022 8:29:29 PM",
                "activeTrustedSigners": {
                    "quantity": 0,
                    "enabled": False
                },
                "domainName": "d2860c44dqgktj.cloudfront.net",
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
                                "domainName": "deleteme-compliantbucket-1weu4f25vurqh.s3.amazonaws.com",
                                "connectionTimeout": 10,
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E1FT2YGHTCWK8R"
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
                    "callerReference": "ab7f36bc-7c02-14d6-046d-d2d6cce0e164",
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
                    "enabled": False,
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
            "eTag": "E34LY589P3SLJG"
        },
        "requestID": "f0de29f7-6dac-4063-9363-a7b11e85fc3d",
        "eventID": "5ec15821-d0bd-4e9e-b6e8-d245d31145b9",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "apiVersion": "2020_05_31",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "eventCategory": "Management",
        "sessionCredentialFromConsole": "True"
    }
}

create_distribution_with_tags_event_compliant = {
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
            "accessKeyId": "TESTACCESSKEYID",
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
                    "creationDate": "2022-03-20T12:34:53Z",
                    "mfaAuthenticated": "False"
                }
            },
            "invokedBy": "cloudformation.amazonaws.com"
        },
        "eventTime": "2022-03-20T13:22:59Z",
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
                                "domainName": "deleteme-compliantbucket-izek8iwcndao.s3.amazonaws.com",
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E1FJQZYXTDFUQD"
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
                            'enabled': True,
                            'quantity': 1,
                            'items': ['self']
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
                    "callerReference": "b40928d9-4bdb-e132-a603-d6b6ff1ffe5b",
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
            "location": "https://cloudfront.amazonaws.com/2020-05-31/distribution/testDistributionId",
            "distribution": {
                "aRN": "arn:aws:cloudfront::000000000000:distribution/testDistributionId",
                "id": "testDistributionId",
                "lastModifiedTime": "Mar 20, 2022 1:22:59 PM",
                "activeTrustedSigners": {
                    "quantity": 0,
                    "enabled": False
                },
                "domainName": "d31mbgtrc2csig.cloudfront.net",
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
                                "domainName": "deleteme-compliantbucket-izek8iwcndao.s3.amazonaws.com",
                                "connectionTimeout": 10,
                                "s3OriginConfig": {
                                    "originAccessIdentity": "origin-access-identity/cloudfront/E1FJQZYXTDFUQD"
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
                    "callerReference": "b40928d9-4bdb-e132-a603-d6b6ff1ffe5b",
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
            "eTag": "E3U1DUD4AHF6P6"
        },
        "requestID": "fe0f4235-b22f-4315-9ff3-68b146dd177b",
        "eventID": "8bc83e3e-8365-4fc1-bc15-5be6d9ce876f",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "apiVersion": "2020_05_31",
        "managementEvent": True,
        "recipientAccountId": "000000000000",
        "eventCategory": "Management"
    }
}


@patch.dict(
    environ, {
        'REMEDIATOR_ROLE': 'remediator-us-east-1-role-refactor',
        'POLICIES_TABLE': 'remediator-dev-policiesTable-AHDESW6FFINI'
    }
)
class TestCloudfront(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     resource_patch = patch('remediator.src.investigator.resource')
    #     account_patch = patch('remediator.src.investigator.account')
    #     call_patch = patch('remediator.src.cloudfront.Connector.call')
    #     cls.resource = resource_patch.start()
    #     cls.call = call_patch.start()
    #     cls.account = account_patch.start()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.resource = None
    #     cls.call = None

    @ patch('remediator.src.cloudfront.Investigate.remediations')
    def test__distribution_policy(
        self,
        mocked_remediations
    ):
        expected_return = ([{'Inspect': {'Value': True, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners', 'enabled']}, 'Update': {'Value': {'items': [
                           'self'], 'enabled': True, 'quantity': 1}, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners']}}], [{'Tags': [{'Value': 'True', 'Key': 'Exempt'}]}])
        mocked_remediations.return_value = {'Exceptions': [{'Tags': [{'Value': 'True', 'Key': 'Exempt'}]}], 'Inspections': [{'Inspect': {'Value': True, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners', 'enabled']}, 'Update': {
            'Value': {'items': ['self'], 'enabled': True, 'quantity': Decimal('1')}, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners']}}]}
        remediations = \
            Cloudfront(
                create_distribution_with_tags_event
            )._Cloudfront__distribution_policy()
        self.assertTupleEqual(remediations, expected_return)

    @ patch('remediator.src.cloudfront.Connector.call')
    def test__tags_none(
        self,
        mocked_call
    ):
        mocked_call.return_value = {
            'Tags': {'Items': []}
        }
        tags = Cloudfront(
            create_distribution_with_tags_event)._Cloudfront__tags()
        self.assertFalse(tags)

    @ patch('remediator.src.cloudfront.Connector.call')
    def test__tags(
        self,
        mocked_call
    ):
        expected_return = [
            {'Key': 'Exempt', 'Value': 'True'},
            {'Key': 'test', 'Value': 'ok'}
        ]
        mocked_call.return_value = {
            'Tags': {'Items': [
                {'Key': 'Exempt', 'Value': 'True'},
                {'Key': 'test', 'Value': 'ok'}
            ]}
        }
        tags = Cloudfront(
            create_distribution_with_tags_event)._Cloudfront__tags()
        self.assertListEqual(tags, expected_return)

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__tags')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_policy')
    def test__distibution_violation(
            self,
            mocked_distibution_policy,
            mocked_tags
    ):
        expected_return = (False, [{'distributionConfig': {'defaultCacheBehavior': {'trustedSigners': {'enabled': False}}}}], {'distributionConfig': {'origins': {'quantity': 1, 'items': [{'customHeaders': {'items': [], 'quantity': 0}, 'domainName': 'deleteme-compliantbucket-izek8iwcndao.s3.amazonaws.com', 's3OriginConfig': {'originAccessIdentity': 'origin-access-identity/cloudfront/E1FJQZYXTDFUQD'}, 'originPath': '', 'id': 'only-origin'}]}, 'aliases': {'items': [], 'quantity': 0}, 'defaultCacheBehavior': {'functionAssociations': {'quantity': 0, 'items': []}, 'minTTL': 0, 'defaultTTL': 31536000, 'lambdaFunctionAssociations': {'items': [], 'quantity': 0}, 'fieldLevelEncryptionId': '', 'trustedSigners': {'items': ['self'], 'enabled': True, 'quantity': 1}, 'maxTTL': 31536000, 'trustedKeyGroups': {'enabled': False, 'quantity': 0, 'items': []}, 'allowedMethods': {'items': ['GET', 'HEAD', 'OPTIONS'], 'quantity': 3, 'cachedMethods': {'items': ['GET', 'HEAD'], 'quantity': 2}}, 'smoothStreaming': False, 'targetOriginId': 'only-origin',
                           'viewerProtocolPolicy': 'redirect-to-https', 'compress': True, 'forwardedValues': {'cookies': {'whitelistedNames': {'quantity': 0, 'items': []}, 'forward': 'none'}, 'queryString': False, 'headers': {'quantity': 0, 'items': []}, 'queryStringCacheKeys': {'quantity': 0, 'items': []}}}, 'callerReference': 'b40928d9-4bdb-e132-a603-d6b6ff1ffe5b', 'webACLId': '', 'defaultRootObject': 'index.html', 'customErrorResponses': {'quantity': 1, 'items': [{'responsePagePath': '/index.html', 'errorCachingMinTTL': 300, 'responseCode': '200', 'errorCode': 404}]}, 'enabled': True, 'cacheBehaviors': {'quantity': 0, 'items': []}, 'httpVersion': 'http1.1', 'comment': 'HIDDEN_DUE_TO_SECURITY_REASONS', 'restrictions': {'geoRestriction': {'restrictionType': 'none', 'items': [], 'quantity': 0}}, 'logging': {'includeCookies': False, 'prefix': '', 'bucket': '', 'enabled': False}, 'viewerCertificate': {'cloudFrontDefaultCertificate': True, 'minimumProtocolVersion': 'SSLv3'}, 'priceClass': 'PriceClass_All', 'originGroups': {'quantity': 0, 'items': []}}})
        mocked_distibution_policy.return_value = ([{'Inspect': {'Value': True, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners', 'enabled']}, 'Update': {'Value': {'items': [
            'self'], 'enabled': True, 'quantity': 1}, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners']}}], [{'Tags': [{'Value': 'True', 'Key': 'Exempt'}]}])
        mocked_tags.return_value = [
            {'Key': 'Exempt', 'Value': 'False'},
            {'Key': 'test', 'Value': 'ok'}
        ]
        distibution_violations = Cloudfront(
            create_distribution_with_tags_event)._Cloudfront__distribution_violations()
        self.assertTupleEqual(expected_return, distibution_violations)

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__tags')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_policy')
    def test__distribution_violation_no_violations(
            self,
            mocked_distibution_policy,
            mocked_tags
    ):
        expected_return = (False, [], {})
        mocked_distibution_policy.return_value = ([{'Inspect': {'Value': True, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners', 'enabled']}, 'Update': {'Value': {'items': [
            'self'], 'enabled': True, 'quantity': 1}, 'Map': ['distributionConfig', 'defaultCacheBehavior', 'trustedSigners']}}], [{'Tags': [{'Value': 'True', 'Key': 'Exempt'}]}])
        mocked_tags.return_value = [
            {'Key': 'Exempt', 'Value': 'False'},
            {'Key': 'test', 'Value': 'ok'}
        ]
        distibution_violations = Cloudfront(
            create_distribution_with_tags_event_compliant)._Cloudfront__distribution_violations()
        self.assertTupleEqual(expected_return, distibution_violations)

    @ patch('remediator.src.cloudfront.Connector.call')
    def test__distribution_kwargs(
        self,
        mocked_call
    ):
        expected_return = {
            'Id': 'testDistributionId',
            'IfMatch': 'aTag',
            'DistributionConfig': 'test'
        }
        test_config = {'distributionConfig': 'test'}
        mocked_call.return_value = {
            'ETag': 'aTag'
        }
        kwargs = Cloudfront(
            create_distribution_with_tags_event
        )._Cloudfront__distribution_kwargs(test_config)
        self.assertDictEqual(kwargs, expected_return)

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_kwargs')
    @ patch('remediator.src.cloudfront.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.cloudfront.Connector.call')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_violations')
    def test_distribution(
        self,
        mocked_distribution_violation,
        mocked_call,
        mocked_account,
        mocked_kwargs
    ):
        mocked_distribution_violation.return_value = (
            False,
            ['violation'],
            {'distributionConfig': 'aDistributionConfig'}
        )
        mocked_kwargs.return_value = {
            'Id': 'testDistributionId',
            'IfMatch': 'aTag',
            'DistributionConfig': 'test',
            'distributionConfig': 'aDistributionConfig'
        }
        expected_resource_type = 'distribution'
        expected_remediation_type = 'update'
        expected_violations = ['violation']
        remediation_type, violations, resource_type = Cloudfront(
            create_distribution_with_tags_event).distribution()
        self.assertEqual(remediation_type, expected_remediation_type)
        self.assertEqual(violations, expected_violations)
        self.assertEqual(resource_type, expected_resource_type)
        mocked_call.assert_called_with('update_distribution', {
                                       'Id': 'testDistributionId', 'IfMatch': 'aTag', 'DistributionConfig': 'test', 'distributionConfig': 'aDistributionConfig'})

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_kwargs')
    @ patch('remediator.src.cloudfront.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.cloudfront.Connector.call')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_violations')
    def test_distribution_compliant(
        self,
        mocked_distribution_violation,
        mocked_call,
        mocked_account,
        mocked_kwargs
    ):
        mocked_distribution_violation.return_value = (
            False,
            [],
            {}
        )
        expected_resource_type = 'distribution'
        expected_remediation_type = None
        expected_violations = []
        remediation_type, violations, resource_type = Cloudfront(
            create_distribution_with_tags_event).distribution()
        self.assertEqual(remediation_type, expected_remediation_type)
        self.assertEqual(violations, expected_violations)
        self.assertEqual(resource_type, expected_resource_type)
        mocked_kwargs.assert_not_called()
        mocked_call.assert_not_called()

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_kwargs')
    @ patch('remediator.src.cloudfront.Investigate.account', return_value={'Remediate': False})
    @ patch('remediator.src.cloudfront.Connector.call')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_violations')
    def test_distribution_no_remediate(
        self,
        mocked_distribution_violation,
        mocked_call,
        mocked_account,
        mocked_kwargs
    ):
        mocked_distribution_violation.return_value = (
            False,
            ['violation'],
            {'distributionConfig': 'aDistributionConfig'}
        )
        expected_resource_type = 'distribution'
        expected_remediation_type = 'Notification'
        expected_violations = ['violation']
        remediation_type, violations, resource_type = Cloudfront(
            create_distribution_with_tags_event).distribution()
        self.assertEqual(remediation_type, expected_remediation_type)
        self.assertEqual(violations, expected_violations)
        self.assertEqual(resource_type, expected_resource_type)
        mocked_kwargs.assert_not_called()
        mocked_call.assert_not_called()

    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_kwargs')
    @ patch('remediator.src.cloudfront.Investigate.account', return_value={'Remediate': True})
    @ patch('remediator.src.cloudfront.Connector.call')
    @patch('remediator.src.cloudfront.Cloudfront._Cloudfront__distribution_violations')
    def test_distribution_exempt(
        self,
        mocked_distribution_violation,
        mocked_call,
        mocked_account,
        mocked_kwargs
    ):
        mocked_distribution_violation.return_value = (
            True,
            ['violation'],
            {'distributionConfig': 'aDistributionConfig'}
        )
        expected_resource_type = 'distribution'
        expected_remediation_type = 'Exempt'
        expected_violations = ['violation']
        remediation_type, violations, resource_type = Cloudfront(
            create_distribution_with_tags_event).distribution()
        self.assertEqual(remediation_type, expected_remediation_type)
        self.assertEqual(violations, expected_violations)
        self.assertEqual(resource_type, expected_resource_type)
        mocked_kwargs.assert_not_called()
        mocked_call.assert_not_called()


if __name__ == '__main__':
    unittest.main()
