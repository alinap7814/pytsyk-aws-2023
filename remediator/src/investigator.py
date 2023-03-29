from typing import Generator


from boto3 import resource
from boto3.dynamodb.types import TypeDeserializer
from copy import deepcopy
from string import Template
from os import environ
import operator
from functools import reduce
from decimal import Decimal
import logging
from ast import literal_eval
from remediator.src.connector import Connector
from botocore.exceptions import ClientError

'''
    object to get common information need for remediations. the methods get information 
    from the event, dynamodb 
    some methods manipulate iterables
    - args:
        - event, aws cloudwatch event 
    
'''


class Investigate:

    def __init__(self, event: dict, resource_type=None):
        self.event: dict = event
        self.resource_type = resource_type

    '''
        gets the event name from the cloudwatch event
        args: self
        Returns: string 
    '''

    def event_name(self) -> str:
        event_name = self.event['detail']['eventName']
        logging.info({'event_name': event_name})
        return event_name

    '''
        gets the service name from the cloudwatch event source key
        args: self
        Returns: string 
    '''

    def event_source(self) -> str:
        event_source = self.event['source'].split('.')[-1]
        logging.info({'event_source': event_source})
        return event_source

    '''
     gets the request parameters of the event, the request parameters are the
     specific for the resource creation/update/delete
     args: self 
     returns:
        - dictionary with the parameters
    '''

    def request_parameters(self) -> dict:
        request_parameters: dict = self.event['detail']['requestParameters']
        logging.info({'request_parameters': request_parameters})
        return request_parameters
    '''
        gets the policy document from the dynamodb policy table
        args:
            - self
            - attribute_to_get: optional key of the document to get the value
        returns: policy document
    '''

    def policy(self, attributes_to_get: list = None) -> dict:
        logging.info('getting policy from table')
        policies_table: object = resource(
            'dynamodb').Table(environ['POLICIES_TABLE'])
        # sets kwargs
        kwargs = {
            'Key': {
                'ResourceType': self.resource_type,
                'EventSource': self.event_source()
            }
        }
        # checks if attributes to get is specified
        if attributes_to_get:
            kwargs.update({'AttributesToGet': attributes_to_get})
        # get item from dynamodb
        logging.debug({'kwargs': kwargs})
        try:
            response = policies_table.get_item(**kwargs)
            logging.debug({'response': response})
            return response.get('Item', {})
        except ClientError as client_error:
            logging.error(client_error.response)
            exit()

    '''
        gets value for the remediation key of the policy document. Some remediations
        will have dynamic values that can be substituted
        args:
            - self
            - substitutions(dict), optional, dictionary with string to substitute
                ie {'BucketName' : 'bucket-name'}
        returns:
            remediations, dictionary from table
    '''

    def remediations(self, substitutions: dict = False):
        logging.debug({'substitutions': substitutions})
        logging.info('getting remediations from table')
        # gets remediation from
        item_to_get: str = 'Remediations'
        logging.debug({'item_to_get': item_to_get})
        remediations: dict = self.policy([item_to_get])
        logging.debug({'remediations': remediations})
        remediation_items = remediations[item_to_get]
        logging.debug({'remediation_items': remediation_items})
        if substitutions:
            remediation_items = \
                literal_eval(Template(str(remediation_items)
                                      ).substitute(**substitutions))
        return remediation_items

    '''
        itertates throught a list of dictionaries or a dictionary to perform
        action depending on arguments. useful when using
        request parameters as kwargs to aws apis.
        args:
            - iterable, dict or list
        kwargs:
            - capitalize, to capitalize keys in iterable
            - remove_empties, delete keys with empty dict
            - to_int, converts bool to int
            - remove_key, key to remove from dict recursively 
            - evaluate, evaluates string as code
        returns


    '''
    @staticmethod
    def iterable_ops(
        iterable: list or dict,
        remove_empties: bool = False,
        capitalize: bool = False,
        to_int: bool = False,
        remove_key: str = False,
        evaluate: bool = False,
        dynamo_deserialize: bool = False
    ) -> list or dict:
        # dictionary with items from the arguments
        kwargs: dict = {
            'iterable': iterable,
            'remove_empties': remove_empties,
            'capitalize': capitalize,
            'to_int': to_int,
            'remove_key': remove_key,
            'evaluate': evaluate
        }
        # copy of iterable
        iterable_copy = deepcopy(iterable)
        # checks if iterable is a dictionary
        if isinstance(iterable, dict):
            # loops throught the keys of the dict
            for key in iterable_copy.keys():
                try:
                    # checks if action is to evaluate
                    if evaluate:
                        # checks if key is a sting
                        if isinstance(iterable[key], str):
                            # evaluates string as python code
                            iterable[key] = eval(iterable[key])
                    # check if action is to remove a key from the dict
                    if remove_key:
                        # gets items from key to remove
                        items = iterable[key].get(remove_key)
                        # removes key from dict
                        if items:
                            iterable[key] = items
                    # checks if action is to replace bool
                    if to_int:
                        if not isinstance(iterable[key], bool):
                            iterable[key] = int(iterable[key])
                    if remove_empties:
                        if iterable[key] == {}:
                            del iterable[key]
                            continue
                # check if operat
                    if capitalize:
                        # set key as title case
                        title_key: str = f'{key[0].upper()}{key[1:]}'
                        # replaces key in dict
                        iterable[title_key] = iterable.pop(key)
                        key = title_key
                    if dynamo_deserialize:
                        deserializer = TypeDeserializer()
                        deserialized_value = \
                            deserializer.deserialize(iterable_copy[key])
                        iterable[key] = deserialized_value
                except Exception as e:
                    pass
                if isinstance(iterable[key], dict):
                    kwargs['iterable'] = iterable[key]
                    Investigate.iterable_ops(**kwargs)
                elif isinstance(iterable[key], list):
                    for item in iterable[key]:
                        kwargs['iterable'] = item
                        Investigate.iterable_ops(**kwargs)
        if isinstance(iterable, list):
            for item in iterable:
                kwargs['iterable'] = item
                Investigate.iterable_ops(**kwargs)
        return iterable

    '''
        checks security groups for exceptions
        args: tags
        returns: boolean
    '''
    @ staticmethod
    def is_exempt(tags: list):
        # checks if has tags
        if tags:
            # loops through tags
            for tag in tags:
                # checks if key exempt with value true exist
                if tag.get('Key') == 'Exempt' and tag.get('Value') == 'True':
                    return True
        return False

    '''
        finds values of key in nested dictionary or list
        args:
            - iterable, dict or list
            - lookup, key to find
        returns: generator with findings
    '''
    def value_finder(iterable: dict, lookup: str) -> Generator:
        # checks if iterable is a list
        if isinstance(iterable, list):
            # loops through list
            for item in iterable:
                # calls function to get dics
                for find in Investigate.value_finder(item, lookup):
                    yield find
        elif isinstance(iterable, dict):
            # checks if lookup is in iterable
            if lookup in iterable:
                yield iterable[lookup]
            # loops through values of dict
            for value in iterable.values():
                for find in Investigate.value_finder(value, lookup):
                    yield find

    '''
        gets all nested keys of a dictionary
        args: dictionary
        return: list of keys
    '''
    @staticmethod
    def nested_keys(dictionary: dict) -> list:
        for key, value in dictionary.items():
            yield key
            if type(value) is dict:
                for k in Investigate.nested_keys(value):
                    yield k

    '''
        gets values from a dictionary from a list of keys
        args:
            - from_, dict to look up
            - keys, list of keys to slice dictionary
        return: value from dict
    '''
    @staticmethod
    def get_value(from_: dict, keys: list):
        return reduce(operator.getitem, keys, from_)

    '''
        decodes decimal obj, to use in json.dumps as default
        args: object
        return: object as int
    '''
    @staticmethod
    def decimal_decoder(obj):
        if isinstance(obj, Decimal):
            return int(obj)
        raise TypeError
    '''
        adds key to a nested dictionary
        args:
            iterable, dictionary to add key to
            mappings, list of indeces to get to nested 
            value, any value to add to dict
    '''
    @staticmethod
    def add_key_value(iterable: dict, mappings: list, value: any) -> dict:
        # called get value to get location to add dict
        Investigate.get_value(
            iterable, mappings[:-1])[mappings[-1]] = value
        return iterable

    def reader(s3_bucket, s3_object_location):
        logging.debug(
            {'s3_bucket': s3_bucket, 's3_object_location': s3_object_location})
        s3_object = resource('s3').Object(s3_bucket, s3_object_location)
        s3_object.wait_until_exists()
        response = s3_object.get()
        body = response['Body'].read()
        try:
            return body.decode()
        except Exception as e:
            logging.debug(e)
            return body

    def is_cloudformation(self):
        logging.info('checking if cloudformation')
        user_agent = self.event['detail']['userAgent']
        if user_agent == 'cloudformation.amazonaws.com':
            return True
        return False

    def wait_for_stack(self, stack_name):
        logging.info(f'waiting for stack {stack_name}')
        connector = Connector(self.event, 'client', 'cloudformation')
        cloudformation_kwargs = {
            'StackName': stack_name
        }
        stack = \
            connector.call('describe_stacks', cloudformation_kwargs)[
                'Stacks'][0]
        logging.debug({'stack': stack})
        stack_status = stack['StackStatus']
        stack_operation = stack_status.split('_')[0].lower()
        waiter_arg = f"stack_{stack_operation}_complete"
        waiter = connector.connect().get_waiter(waiter_arg)
        waiter.wait(**cloudformation_kwargs)

    def find_words(string_, prefix):
        words = []
        raw_words = \
            [word for word in string_.split() if word.startswith(prefix)]
        logging.debug({'raw_words': raw_words})
        for raw_word in raw_words:
            word = ''.join([letter for letter in raw_word if letter.isalpha()])
            words.append(word)
        return words

    '''
        gets the account document from the accounts table
        args:
            - self
            - attribute_to_get: optional key of the document to get the value
        returns: policy document
    '''

    def account(self) -> dict:
        logging.info('getting policy from table')
        policies_table: object = resource(
            'dynamodb').Table(environ['ACCOUNTS_TABLE'])
        # sets kwargs
        kwargs = {
            'Key': {
                'AccountNumber': self.event['account']
            }
        }
        # get item from dynamodb
        logging.debug({'kwargs': kwargs})
        response = policies_table.get_item(**kwargs)
        logging.debug({'response': response})
        return response.get('Item', {})

    def remediation_tags(self, resource_arn, remediation_type):
        logging.info('tagging resource')
        connector = Connector(self.event, 'client', 'resourcegroupstaggingapi')
        remediation_id = self.event['detail']['eventID']
        kwargs = {
            'ResourceARNList': [resource_arn],
            'Tags': {
                'RemediationType': remediation_type,
                'RemediationId': remediation_id
            }
        }
        connector.call('tag_resources', kwargs)
