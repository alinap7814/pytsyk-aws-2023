from remediator.src.investigator import Investigate

import unittest
from unittest.mock import patch
from os import environ
from botocore.response import StreamingBody
from io import BytesIO
import logging


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
        'POLICIES_TABLE': 'test-policy-table',
        'ACCOUNTS_TABLE': 'remediator-dev-accountsTable-5T5ARII5OQZQ',
        'REMEDIATOR_ROLE': 'remediator-$Region-role-dev'
    }
)
class TestInvestigate(unittest.TestCase):

    def test_event_name(self):
        expected_return = 'testEvent'
        test_event = {'detail': {'eventName': 'testEvent'}}
        event_name = Investigate(test_event).event_name()
        self.assertEqual(event_name, expected_return)

    def test_event_source(self):
        expected_return = 'testSource'
        test_event = {
            'source': 'testSource',
            'detail': {
                'eventName': 'testEvent'
            }
        }
        event_source = Investigate(test_event).event_source()
        self.assertEqual(event_source, expected_return)

    def test_request_parameters(self):
        expected_return = 'testRequestParameters'
        test_event = {
            'source': 'testSource',
            'detail': {
                'eventName': 'testEvent',
                'requestParameters': 'testRequestParameters'

            }
        }
        request_parameters = Investigate(test_event).request_parameters()
        self.assertEqual(request_parameters, expected_return)

    def test_evaluate(self):
        test_dict = {'Nested': {'notCode': [1, 2], 'Code': 'list(range(4,8))'}}
        expected_return = {'Nested': {'notCode': [1, 2], 'Code': [4, 5, 6, 7]}}
        iterable = Investigate.iterable_ops(test_dict, evaluate=True)
        self.assertDictEqual(iterable, expected_return)

    @ patch('remediator.src.investigator.Investigate.event_source')
    @ patch('remediator.src.investigator.Investigate.event_name')
    @ patch('remediator.src.investigator.resource')
    def test_policy(self, mocked_resource, mocked_event_name, mocked_event_source):
        test_event = {}
        mocked_event_name.return_value = 'testEvent'
        mocked_event_source.return_value = 'testSource'
        expected_return = {'Remediations': 'aRemediation'}
        mocked_resource('dynamoDb').Table().get_item.return_value = {
            'Item': {'Remediations': 'aRemediation'}
        }
        remediation = Investigate(test_event, 'resource_type').policy()
        self.assertDictEqual(remediation, expected_return)
        mocked_resource().Table().get_item.assert_called_with(
            Key={'ResourceType': 'resource_type', 'EventSource': 'testSource'}
        )

    @patch('remediator.src.investigator.Investigate.policy')
    def test_remediations(self, mocked_policy):
        test_event = {}
        expected_return = {'TestBucketName': 'test-bucket-name'}
        substitutions = {
            'BucketName': 'test-bucket-name'
        }
        mocked_policy.return_value = {
            'Remediations': "{'TestBucketName': '$BucketName'}"}
        remediation = Investigate(test_event).remediations(substitutions)
        self.assertEqual(remediation, expected_return)

    def test_iterable_ops_capitalize(self):
        expected_return = {'ADict': {'NestedDict': True},
                           'NestedDictList': [{'ADict': True}]}
        test_dict = {'aDict':
                     {'nestedDict': True},
                     'nestedDictList': [{'aDict': True}]
                     }
        titled_dict = Investigate.iterable_ops(test_dict, capitalize=True)
        self.assertDictEqual(titled_dict, expected_return)

    def test_convert_remove_empties(self):
        expected_return = [
            {'Parent': {
                'ChildFoo': [
                    {'Item': {'GrandChildBar': 'anItem'}},
                    {'GrandChildFoo': True},
                    {'GrandChild': False}
                ]}}
        ]
        test_iterable = [{
            'Parent': {
                'Child': {},
                'ChildFoo': [
                    {'Item': {'GrandChildBar': 'anItem'}},
                    {'GrandChildFoo': True},
                    {'GrandChild': False}
                ]
            }
        }]
        clean_iterable = Investigate.iterable_ops(
            test_iterable, remove_empties=True)
        self.assertListEqual(clean_iterable, expected_return)

    def test_is_exempt(self, ):
        test_tags = [{'Key': 'Exempt', 'Value': 'True'}]
        is_exempt = Investigate.is_exempt(test_tags)
        self.assertTrue(is_exempt)

    def test_iterable_ops_lookup(self):
        expected_return = [{'FindThis': 'True'}]
        test_iterable = [{
            'Parent': {
                'Child': {},
                'ChildFoo': [
                    {'Item': {'GrandChildFoo': 'anItem'}},
                    {'GrandChildFoo': True},
                    {'GrandChild': False}
                ],
                'ChildBar': {
                    'GrandChildBar': {'FindThis': 'True'}
                }
            }
        }]
        find = Investigate.value_finder(test_iterable, 'GrandChildBar')
        self.assertListEqual(list(find), expected_return)

    def test_nested_keys(self):
        expected_return = ['Parent', 'Child']
        test_dict = {
            'Parent': {
                'Child': {}
            }
        }
        keys = list(Investigate.nested_keys(test_dict))
        self.assertListEqual(keys, expected_return)

    def test_get_value(self):
        expected_return = {'ThisValue': 'true'}
        keys = ['Parent', 'Child']
        test_dict = {
            'Parent': {
                'Child': {
                    'ThisValue': 'true'
                }
            }
        }
        value = Investigate.get_value(test_dict, keys)
        self.assertDictEqual(value, expected_return)

    def test_iterable_ops_convert(self):
        from decimal import Decimal
        expected_return = {'Quantity': 1}
        test_iterable = {'Quantity': Decimal('1')}
        updated = Investigate.iterable_ops(test_iterable, to_int=True)
        self.assertDictEqual(updated, expected_return)

    def test_add_key_value(self):
        test_value = 'appended'
        mappings = ['iter', 'bar', 'new']
        # ['iter']['bar']['new']
        test_iterable = {
            'iter': {
                'bar': {
                    'foo': 'stays'
                },
                'other': ''
            }
        }
        expected_return = {
            'iter': {
                'bar': {
                    'foo': 'stays',
                    'new': 'appended'
                },
                'other': ''
            }
        }
        new = Investigate.add_key_value(test_iterable, mappings, test_value)
        self.assertDictEqual(new, expected_return)

    @ patch('remediator.src.investigator.resource')
    def test_reader(
            self,
            mocked_resource
    ):
        expected_return = 'test'
        streaming_body = StreamingBody(BytesIO(b'test'), len('test'))
        mocked_resource.return_value.Object.return_value.get.return_value = {
            'Body': streaming_body
        }
        content = Investigate.reader(
            'remediator-execution-template-dev', 'template.yml')
        self.assertEqual(content, expected_return)

    @patch.dict(environ, {'REMEDIATOR_ROLE': 'remediator-us-east-1-role-update-policy'})
    def test_is_cloudformation(self):
        test_event = {
            'detail': {
                'userAgent': 'cloudformation.amazonaws.com',
            }
        }
        is_cloudformation = Investigate(test_event).is_cloudformation()
        self.assertTrue(is_cloudformation)

    @ patch('remediator.src.investigator.Connector.connect')
    @ patch('remediator.src.investigator.Connector.call')
    def test_wait_for_stack(
        self,
        mocked_call,
        mocked_connect
    ):
        mocked_call.return_value = {'Stacks': [
            {'StackStatus': 'Create_Complete'}]}
        Investigate(None).wait_for_stack('test-stack')
        mocked_call.assert_called_with(
            'describe_stacks', {'StackName': 'test-stack'})
        mocked_connect().get_waiter.assert_called_with('stack_create_complete')

    def test_find_words(self):
        expected_return = ['THIS', 'THAT', 'ThisOne']
        prefix = '$'
        test_string = 'find $THIS, $THAT also $ThisOne'
        words = Investigate.find_words(test_string, prefix)
        self.assertListEqual(words, expected_return)

    @ patch('remediator.src.investigator.resource')
    def test_account(self, mocked_resource):
        test_event = {
            'account': '000000000000'
        }
        mocked_resource('dynamoDb').Table().get_item.return_value = {
            'Item': {'Remediations': 'aRemediation'}
        }
        account = Investigate(test_event).account()
        self.assertIsInstance(account, dict)

    @ patch('remediator.src.investigator.Connector.call')
    def test_remediation_tags(self, mocked_call):
        test_event = {
            'account': '563014625035',
            'region': 'us-east-1',
            'detail': {'eventID': 'testEventId'}
        }
        Investigate(test_event).remediation_tags('role', 'Delete')
        mocked_call.assert_called_with('tag_resources', {'ResourceARNList': ['role'], 'Tags': {
                                       'RemediationType': 'Delete', 'RemediationId': 'testEventId'}})

    def test_dynamodb_deserializer(self):
        expected_return = {'string': 'test', 'list': ['listItem', 'listItem2']}
        item = {
            'string': {'S': 'test'},
            'list': {'L': [{'S': 'listItem'}, {'S': 'listItem2'}]}
        }
        deserialized = Investigate.iterable_ops(item, dynamo_deserialize=True)
        self.assertEqual(expected_return, deserialized)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
