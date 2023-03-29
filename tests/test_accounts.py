import logging
from os import environ
from unittest.mock import patch, call
import unittest
from remediator.src.accounts import Accounts
from botocore.exceptions import ClientError



test_event_modify_regions = {
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
                            'S': 'regionToAdd'
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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
                            'S': 'regionToDelete'
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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

test_event_modify_contact_rule_state = {
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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

test_event_modify_rule_state = {
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
                        'S': 'leonardo.bautista@accenture.com'
                    },
                    'Name': {
                        'S': 'operations'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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

test_event_modify_contact = {
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
                        'S': 'other.contact@accenture.com'
                    },
                    'Name': {
                        'S': 'operations'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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

test_event_insert = {
    'Records': [
        {
            'eventID': 'fec4feb631d8696e94a60e5d04a75ab2',
            'eventName': 'INSERT',
            'eventVersion': '1.1',
            'eventSource': 'aws:dynamodb',
            'awsRegion': 'us-east-1',
            'dynamodb': {
                'ApproximateCreationDateTime': 1661975184.0,
                'Keys': {
                    'AccountNumber': {
                            'S': '000000000000'
                    }
                },
                'NewImage': {
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
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
                    }
                },
                'SequenceNumber': '182000000000012983119324',
                'SizeBytes': 170,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            },
            'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/remediator-dev-accountsTable-1X14PDT5E5E5J/stream/2022-08-31T17:16:15.489'
        }
    ]
}

test_event_remove = {
    'Records': [{
        'eventID': 'c5c1b619bb6692d20b2bd66ec498b2a9',
                'eventName': 'REMOVE',
                'eventVersion': '1.1',
                'eventSource': 'aws:dynamodb',
                'awsRegion': 'us-east-1',
                'dynamodb': {
                    'ApproximateCreationDateTime': 1662005342.0,
                    'Keys': {
                        'AccountNumber': {
                            'S': '000000000000'
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
                            }, {
                                'S': 'us-east-1'
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
                    'SequenceNumber': '1708900000000030931563383',
                    'SizeBytes': 180,
                    'StreamViewType': 'NEW_AND_OLD_IMAGES'
                },
                'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/remediator-dev-accountsTable-1X14PDT5E5E5J/stream/2022-08-31T17:16:15.489'
                }]
}

test_event_multiple = {
    'Records': [
        {
            'eventID': 'fec4feb631d8696e94a60e5d04a75ab2',
            'eventName': 'INSERT',
            'eventVersion': '1.1',
            'eventSource': 'aws:dynamodb',
            'awsRegion': 'us-east-1',
            'dynamodb': {
                'ApproximateCreationDateTime': 1661975184.0,
                'Keys': {
                    'AccountNumber': {
                        'S': '0'
                    }
                },
                'NewImage': {
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
                        'S': '0'
                    },
                    'Contact': {
                        'S': 'leonardo.bautista@accenture.com'
                    },
                    'Name': {
                        'S': 'accountToCreate'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
                    }
                },
                'SequenceNumber': '182000000000012983119324',
                'SizeBytes': 170,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            },
            'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/remediator-dev-accountsTable-1X14PDT5E5E5J/stream/2022-08-31T17:16:15.489'
        },
        {
            'eventID': 'c5c1b619bb6692d20b2bd66ec498b2a9',
            'eventName': 'REMOVE',
            'eventVersion': '1.1',
            'eventSource': 'aws:dynamodb',
            'awsRegion': 'us-east-1',
            'dynamodb': {
                'ApproximateCreationDateTime': 1662005342.0,
                'Keys': {
                    'AccountNumber': {
                            'S': '1'
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
                        }, {
                            'S': 'us-east-1'
                        }]
                    },
                    'AccountNumber': {
                        'S': '1'
                    },
                    'Contact': {
                        'S': 'leonardo.bautista@accenture.com'
                    },
                    'Name': {
                        'S': 'accountToRemove'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
                    }
                },
                'SequenceNumber': '1708900000000030931563383',
                'SizeBytes': 180,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            },
            'eventSourceARN': 'arn:aws:dynamodb:us-east-1:000000000000:table/remediator-dev-accountsTable-1X14PDT5E5E5J/stream/2022-08-31T17:16:15.489'
        },
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
                        'S': '2'
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
                            'S': 'regionToAdd'
                        }]
                    },
                    'AccountNumber': {
                        'S': '2'
                    },
                    'Contact': {
                        'S': 'other.contact@accenture.com'
                    },
                    'Name': {
                        'S': 'accountToModify'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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
                            'S': 'regionToDelete'
                        }]
                    },
                    'AccountNumber': {
                        'S': '2'
                    },
                    'Contact': {
                        'S': 'leonardo.bautista@accenture.com'
                    },
                    'Name': {
                        'S': 'operations'
                    },
                    'ExecutionRoleName': {
                        'S': 'LaunchPadOperationsStackSetExecutionRole'
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

test_event_put_object = {
    'Records': [
        {
            'eventVersion': '2.1',
            'eventSource': 'aws:s3',
            'awsRegion': 'us-east-1',
            'eventTime': '2022-09-01T23:07:54.843Z',
            'eventName': 'ObjectCreated:Put',
            'userIdentity': {
                'principalId': 'AWS:pincipal:aPerson'
            },
            'requestParameters': {
                'sourceIPAddress': ''
            },
            'responseElements': {
                'x-amz-request-id': 'KJDKFH5Z45NWQ9MH',
                'x-amz-id-2': 'ohRdRaHGYMkb5hluoLfWGIb3VpvgbUuKpfhdzq+tcNnT3a4Q0GkJrlcb/f1ZrO2fZrkKIN1J4OBZRlSUxetLHHExncuD8kzk'
            },
            's3': {
                's3SchemaVersion': '1.0',
                'configurationId': 'fb66eef3-b19f-4467-9cd7-3f0c7daeb772',
                'bucket': {
                    'name': 'remediator-execution-template-dev',
                    'ownerIdentity': {
                            'principalId': 'A2KP8MBIHHULUM'
                    },
                    'arn': 'arn:aws:s3:::remediator-execution-template-dev'
                },
                'object': {
                    'key': 'template.yml',
                    'size': 4880,
                    'eTag': 'f2160019e1aaa9b7106b3af41330a699',
                    'sequencer': '0063113B4AC8D362B4'
                }
            }
        }
    ]
}

test_object_created = {
    'Records': [
        {
            'eventVersion': '2.1',
            'eventSource': 'aws:s3',
            'awsRegion': 'us-east-1',
            'eventTime': '2022-09-09T23:22:43.401Z',
            'eventName': 'ObjectCreated:Put',
            'userIdentity': {
                'principalId': 'AWS:testPrincipalId:leonardo.bautista@accenture.com'
            },
            'requestParameters': {
                'sourceIPAddress': '67.205.203.115'
            },
            'responseElements': {
                'x-amz-request-id': 'EGVQS1HBRTKA9WSR',
                'x-amz-id-2': 'zI0Zb4zaJhn3B2KM3m7Oz0gilsjWQEbZGERo34ibqB0yTKBOTKM000Zqxrwems5cQ1/rmJzNmUY02CyfS1bPj7Hwt6B1bnSmeP2J+yoPDeM='
            },
            's3': {
                's3SchemaVersion': '1.0',
                'configurationId': 'fb66eef3-b19f-4467-9cd7-3f0c7daeb772',
                'bucket': {
                    'name': 'remediator-execution-template-dev',
                    'ownerIdentity': {
                            'principalId': 'testPrincipalId'
                    },
                    'arn': 'arn:aws:s3:::remediator-execution-template-dev'
                },
                'object': {
                    'key': 'template.yml',
                    'size': 4880,
                    'eTag': 'f2160019e1aaa9b7106b3af41330a699',
                    'sequencer': '00631BCAC349214E2C'
                }
            }
        }
    ]
}
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s | %(lineno)s - '
    '%(message)s', level=logging.DEBUG)
# suppress loggers of chatty packages
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.action').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.factory').setLevel(logging.CRITICAL)


@patch.dict(
    environ,
    {
        'ADMINISTRATION_STACK_NAME': 'remediator-dev',
        'ADMINISTRATION_ROLE_ARN': 'arn:aws:iam::000000000000:role/LaunchPadOperationsStackSetAdministrationRole',
        'APP_NAME': 'remediator',
        'ENVIRONMENT': 'dev',
        'ADMINISTRATION_ACCOUNT_ID': '000000000000',
        'EXECUTION_TEMPLATE_BUCKET_NAME': 'remediator-execution-template-dev',
        'ACCOUNTS_TABLE': 'remediator-dev-accountsTable-1X14PDT5E5E5J'
    }
)
class TestAccounts(unittest.TestCase):

    def test_create_cloudformation_parameters(
        self
    ):
        expected_return = [
            {'ParameterKey': 'aKey', 'ParameterValue': 'aValue'}]
        test_parameters = {'aKey': 'aValue'}
        cloudformation_parameters = Accounts.create_cloudformation_parameters(
            test_parameters)
        self.assertListEqual(cloudformation_parameters, expected_return)

    def test_create_cloudformation_parameters_use_previous_value(
        self
    ):
        expected_return = [
            {'ParameterKey': 'aKey', 'UsePreviousValue': True}]
        test_parameters = {'aKey': None}
        cloudformation_parameters = Accounts.create_cloudformation_parameters(
            test_parameters)
        self.assertListEqual(cloudformation_parameters, expected_return)

    def test_get_stack_set_name(self):
        expected_return = 'remediator-operations-dev'
        stack_set_name = \
            Accounts(test_event_insert).get_stack_set_name('operations')
        self.assertEqual(stack_set_name, expected_return)

    @ patch('remediator.src.accounts.client')
    @ patch('remediator.src.accounts.Investigate.reader')
    def test_stack_set_operation_create(
        self,
        mocked_reader,
        mocked_client
    ):
        expected_return = {'remediator-operations-dev': None}
        mocked_reader.return_value = 'test_template'
        mocked_client('cloudformation').create_stack_set.return_value = {
            'StackSetId': 'aStackSetId'
        }
        stack_name_operation_id = Accounts(test_event_insert).stack_set_operation(
            'operations',
            'create',
            'ENABLED',
            'LaunchPadOperationsStackSetExecutionRole',
            'leonardo.bautista@accenture.com',
        )
        mocked_client('cloudformation').create_stack_set.assert_called_with(
            StackSetName='remediator-operations-dev',
            UsePreviousTemplate=True,
            Parameters=[
                {
                    'ParameterKey': 'administrationAccountId',
                    'ParameterValue': '000000000000'
                },
                {
                    'ParameterKey': 'environment',
                    'ParameterValue': 'dev'
                },
                {
                    'ParameterKey': 'ruleState',
                    'ParameterValue': 'ENABLED'
                },
                {
                    'ParameterKey': 'appName',
                    'ParameterValue': 'remediator'
                }
            ],
            AdministrationRoleARN='arn:aws:iam::000000000000:role/LaunchPadOperationsStackSetAdministrationRole',
            ExecutionRoleName='LaunchPadOperationsStackSetExecutionRole',
            Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
            Tags=[
                {'Key': 'AdmnistrationAccount', 'Value': '000000000000'},
                {'Key': 'Contact', 'Value': 'leonardo.bautista@accenture.com'}
            ]
        )
        self.assertDictEqual(stack_name_operation_id, expected_return)

    @ patch('remediator.src.accounts.client')
    @ patch('remediator.src.accounts.Investigate.reader')
    def test_stack_set_operation_delete(
        self,
        mocked_reader,
        mocked_client
    ):
        expected_return = {'remediator-operations-dev': None}
        mocked_client('cloudformation').delete_stack_set.return_value = {}
        stack_name_operation_id = Accounts(test_event_insert).stack_set_operation(
            'operations', 'delete')
        mocked_client('cloudformation').delete_stack_set.assert_called_with(
            StackSetName='remediator-operations-dev'
        )
        mocked_reader.assert_not_called()
        self.assertDictEqual(stack_name_operation_id, expected_return)

    @ patch('remediator.src.accounts.client')
    @ patch('remediator.src.accounts.Investigate.reader')
    def test_stack_set_operation_update(
        self,
        mocked_reader,
        mocked_client
    ):
        expected_return = {'remediator-operations-dev': 'aOperationId'}
        mocked_client('cloudformation').update_stack_set.return_value = {
            'OperationId': 'aOperationId'
        }
        stack_name_operation_id = Accounts(test_event_modify_contact).stack_set_operation(
            'operations',
            'update',
            'ENABLED',
            'LaunchPadOperationsStackSetExecutionRole',
            'leonardo.bautista@accenture.com',
        )
        mocked_client('cloudformation').update_stack_set.assert_called_with(
            StackSetName='remediator-operations-dev',
            UsePreviousTemplate=True,
            Parameters=[
                {
                    'ParameterKey': 'administrationAccountId',
                    'ParameterValue': '000000000000'
                },
                {
                    'ParameterKey': 'environment',
                    'ParameterValue': 'dev'
                },
                {
                    'ParameterKey': 'ruleState',
                    'ParameterValue': 'ENABLED'
                },
                {
                    'ParameterKey': 'appName',
                    'ParameterValue': 'remediator'
                }
            ],
            AdministrationRoleARN='arn:aws:iam::000000000000:role/LaunchPadOperationsStackSetAdministrationRole',
            ExecutionRoleName='LaunchPadOperationsStackSetExecutionRole',
            Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
            Tags=[
                {'Key': 'AdmnistrationAccount', 'Value': '000000000000'},
                {'Key': 'Contact', 'Value': 'leonardo.bautista@accenture.com'}
            ]
        )
        self.assertDictEqual(stack_name_operation_id, expected_return)
        mocked_reader.assert_not_called()

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.client')
    def test_stack_instances_operation_insert(
        self,
        mocked_client,
        mocked_stack_set_operation
    ):
        expected_return = [
            {'remediator-operations-dev': 'createStackInstanceId'}
        ]
        mocked_client('cloudformation').create_stack_instances.return_value = \
            {'OperationId': 'createStackInstanceId'}
        stack_name_operation_id = Accounts(
            test_event_insert).stack_instances_operation(0)
        mocked_stack_set_operation.assert_called_with(
            account_name='operations',
            operation='create',
            rule_state='ENABLED',
            execution_role='LaunchPadOperationsStackSetExecutionRole',
            contact='leonardo.bautista@accenture.com',
            get_template=True
        )
        mocked_client().create_stack_instances.assert_called_with(
            StackSetName='remediator-operations-dev',
            Accounts=['000000000000'],
            Regions=['us-east-2'],
            OperationPreferences={
                'RegionConcurrencyType': 'PARALLEL',
                'MaxConcurrentPercentage': 100,
                'FailureTolerancePercentage': 25
            }
        )
        self.assertListEqual(stack_name_operation_id, expected_return)

    @ patch('remediator.src.accounts.Accounts.stack_set_operations_waiter')
    @ patch('remediator.src.accounts.client')
    def test_stack_instances_operation_delete_error(
        self,
        mocked_client,
        mocked_stack_set_operations_waiter
    ):
        expected_return = [
            {'remediator-operations-dev': 'deleteStackInstanceId'}
        ]
        mocked_client('cloudformation').delete_stack_instances.side_effect = [
            ClientError(
                error_response={
                    'Error': {
                        'Type': 'Sender',
                        'Code': 'OperationInProgressException',
                        'Message': 'Another Operation on StackSet arn:aws:cloudformation:us-east-1:000000000000:stackset/remediator-operations-dev:e7df894d-1a32-4435-9d6c-4266f8df1323 is in progress: operation-id-inprogess'
                    }},
                operation_name='delete_stack_instances'),
            {'OperationId': 'deleteStackInstanceId'}
        ]
        stack_name_operation_id = Accounts(
            test_event_remove).stack_instances_operation(0)
        mocked_stack_set_operations_waiter.assert_called_with(
            [{'remediator-operations-dev': 'operation-id-inprogess'}])
        self.assertListEqual(stack_name_operation_id, expected_return)

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.client')
    def test_stack_instances_operation_modify_regions(
        self,
        mocked_client,
        mocked_stack_set_operation
    ):
        expected_return = [
            {'remediator-operations-dev': 'deleteStackInstanceId'},
            {'remediator-operations-dev': 'createStackInstanceId'}
        ]
        mocked_client().create_stack_instances.return_value = \
            {'OperationId': 'createStackInstanceId'}
        mocked_client().delete_stack_instances.return_value = \
            {'OperationId': 'deleteStackInstanceId'}
        stack_name_operation_ids = Accounts(
            test_event_modify_regions).stack_instances_operation(0)
        mocked_stack_set_operation.assert_not_called()
        mocked_client().create_stack_instances.assert_called_with(
            StackSetName='remediator-operations-dev',
            Accounts=['000000000000'],
            Regions=['regionToAdd'],
            OperationPreferences={
                'RegionConcurrencyType': 'PARALLEL',
                'MaxConcurrentPercentage': 100,
                'FailureTolerancePercentage': 25
            }
        )
        mocked_client().delete_stack_instances.assert_called_with(
            StackSetName='remediator-operations-dev',
            Accounts=['000000000000'],
            Regions=['regionToDelete'],
            OperationPreferences={
                'RegionConcurrencyType': 'PARALLEL',
                'MaxConcurrentPercentage': 100,
                'FailureTolerancePercentage': 25
            },
            RetainStacks=False
        )
        self.assertListEqual(stack_name_operation_ids, expected_return)

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_stack_instances_operation_modify_contact_rule_state(
        self,
        mocked_operation_id,
        mocked_stack_set_operation
    ):
        Accounts(
            test_event_modify_contact_rule_state).stack_instances_operation(0)
        mocked_stack_set_operation.assert_called_with(
            'operations', 'update', 'DISABLED', 'LaunchPadOperationsStackSetExecutionRole', 'other.contact@accenture.com')
        mocked_operation_id.assert_not_called()

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_stack_instances_operation_modify_rule_state(
        self,
        mocked_operation_id,
        mocked_stack_set_operation
    ):
        operation_ids = Accounts(
            test_event_modify_rule_state).stack_instances_operation(0)
        mocked_stack_set_operation.assert_called_with(
            'operations', 'update', 'DISABLED', 'LaunchPadOperationsStackSetExecutionRole', 'leonardo.bautista@accenture.com')
        mocked_operation_id.assert_not_called()

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_stack_instances_operation_modify_contact(
        self,
        mocked_operation_id,
        mocked_stack_set_operation
    ):
        mocked_stack_set_operation.return_value = 'updateStackSetOperationId'
        operation_ids = Accounts(
            test_event_modify_contact).stack_instances_operation(0)
        mocked_stack_set_operation.assert_called_with(
            'operations', 'update', 'ENABLED', 'LaunchPadOperationsStackSetExecutionRole', 'other.contact@accenture.com')
        mocked_operation_id.assert_not_called()

    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_stack_instances_operation_remove(
        self,
        mocked_operation_id,
        mocked_stack_set_operation
    ):
        operation_ids = Accounts(
            test_event_remove).stack_instances_operation(0)
        mocked_stack_set_operation.assert_not_called()
        mocked_operation_id.assert_called_with(
            'operations', '000000000000',
            ['us-east-2', 'us-east-1'],
            'delete'
        )

    @ patch('remediator.src.accounts.Accounts.update_stack_set_template')
    @ patch('remediator.src.accounts.Accounts.stack_set_operations_waiter')
    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_operations_dynamo(
        self,
        mocked_stack_set_instance_operation,
        mocked_stack_set_operation,
        mocked_stack_set_operations_waiter,
        mocked_update_stack_set_template
    ):
        mocked_stack_set_operation.side_effect = [
            {'accountToCreate': None},
            {'accountToUpdate': 'accountToUpdateId'},
            {'accountToDelete': None}
        ]
        mocked_stack_set_instance_operation.side_effect = [
            {'stackSetToCreate': 'stackSetToCreateId'},
            {'stackSetToRemove': 'stackSetToRemoveId'},
            {'stackSetToModifyDelete': 'accountToModifyDeleteId'},
            {'accountToModifyCreate': 'accountToModifyCreateId'}
        ]
        Accounts(test_event_multiple).operations()
        mocked_stack_set_operation.assert_has_calls(
            [
                call(account_name='accountToCreate', operation='create', rule_state='ENABLED',
                     execution_role='LaunchPadOperationsStackSetExecutionRole', contact='leonardo.bautista@accenture.com', get_template=True),
                call('accountToModify', 'update', 'DISABLED', 'LaunchPadOperationsStackSetExecutionRole',
                     'other.contact@accenture.com'),
                call('accountToRemove', 'delete')
            ]
        )
        mocked_stack_set_operations_waiter.assert_called_with(
            [
                {'stackSetToCreate': 'stackSetToCreateId'},
                {'stackSetToRemove': 'stackSetToRemoveId'},
                {'accountToUpdate': 'accountToUpdateId'},
                {'stackSetToModifyDelete': 'accountToModifyDeleteId'},
                {'accountToModifyCreate': 'accountToModifyCreateId'}
            ]
        )
        self.assertEqual(mocked_stack_set_instance_operation.call_count, 4)
        self.assertEqual(mocked_stack_set_operation.call_count, 3)
        mocked_update_stack_set_template.assert_not_called()

    @ patch('remediator.src.accounts.sleep')
    @ patch('remediator.src.accounts.client')
    def test_stack_set_operations_waiter(
        self,
        mocked_client,
        mocked_sleep
    ):
        test_operations = [
            {'failed-stack': 'failed-operation-id'},
            {'succesful-stack': 'succesful-operation-id'},
            {'running-stack': 'running-operation-id'},
            {'stack-no-operation': None},
        ]
        mocked_client().describe_stack_set_operation.side_effect = [
            {'StackSetOperation': {'Status': 'FAILED'}},
            {'StackSetOperation': {'Status': 'SUCCEEDED'}},
            {'StackSetOperation': {'Status': 'RUNNING'}},
            {'StackSetOperation': {'Status': 'SUCCEEDED'}},
        ]
        Accounts(test_event_multiple).stack_set_operations_waiter(
            test_operations
        )
        mocked_client().describe_stack_set_operation.assert_has_calls(
            [
                call(StackSetName='failed-stack',
                     OperationId='failed-operation-id'),
                call(StackSetName='succesful-stack',
                     OperationId='succesful-operation-id'),
                call(StackSetName='running-stack',
                     OperationId='running-operation-id'),
                call(StackSetName='running-stack',
                     OperationId='running-operation-id')
            ]

        )
        self.assertEqual(mocked_sleep.call_count, 1)

    @ patch('remediator.src.accounts.client')
    @ patch('remediator.src.accounts.resource')
    @ patch('remediator.src.accounts.Investigate.reader')
    def test_update_stack_set_template(
        self,
        mocked_reader,
        mocked_resource,
        mocked_client
    ):
        mocked_resource('dynamodb').Table().scan.return_value = {'Items': [{
            'Name': 'operations',
            'RuleState': 'DISABLED',
            'ExecutionRoleName': 'LaunchPadOperationsStackSetExecutionRole',
            'Contact': 'leonardo.bautista@accenture.com'
        }]}
        mocked_client('cloudformation').update_stack_set.return_value = {
            'OperationId': 'test-id'
        }
        mocked_reader.return_value = 'aTemplate'
        Accounts(test_object_created).update_stack_set_template()
        mocked_client('cloudformation').update_stack_set.assert_called_with(
            StackSetName='remediator-operations-dev',
            Parameters=[
                {'ParameterKey': 'administrationAccountId',
                 'ParameterValue': '000000000000'},
                {'ParameterKey': 'environment', 'ParameterValue': 'dev'},
                {'ParameterKey': 'ruleState', 'ParameterValue': 'DISABLED'},
                {'ParameterKey': 'appName', 'ParameterValue': 'remediator'}],
            AdministrationRoleARN='arn:aws:iam::000000000000:role/LaunchPadOperationsStackSetAdministrationRole',
            ExecutionRoleName='LaunchPadOperationsStackSetExecutionRole',
            Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
            Tags=[{'Key': 'AdmnistrationAccount', 'Value': '000000000000'},
                  {'Key': 'Contact', 'Value': 'leonardo.bautista@accenture.com'}],
            TemplateBody='aTemplate')

    @ patch('remediator.src.accounts.Accounts.update_stack_set_template')
    @ patch('remediator.src.accounts.Accounts.stack_set_operations_waiter')
    @ patch('remediator.src.accounts.Accounts.stack_set_operation')
    @ patch('remediator.src.accounts.Accounts.stack_instance_operation')
    def test_operations_s3(
        self,
        mocked_stack_set_instance_operation,
        mocked_stack_set_operation,
        mocked_stack_set_operations_waiter,
        mocked_update_stack_set_template
    ):
        mocked_update_stack_set_template.return_value = [{
            'accountToUpdate': 'accountToUpdateId'}]
        Accounts(test_event_put_object).operations()

        mocked_stack_set_operations_waiter.assert_called_with(
            [{'accountToUpdate': 'accountToUpdateId'}]
        )
        mocked_stack_set_operation.assert_not_called()
        mocked_stack_set_instance_operation.assert_not_called()


if __name__ == '__main__':
    unittest.main(warnings=False)
