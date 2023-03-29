from remediator.src.connector import Connector
from remediator.src.investigator import Investigate
from distutils.util import strtobool
from functools import reduce

import logging


'''
    object to interact with cloudfront service
    Inheratance:
        - Connector, to interact with AWS
        - Investigate, sets of methods to get information from several sources
    - args:
        - event, aws cloudwatch event

'''


class Cloudfront(Connector, Investigate):

    def __init__(self, event: dict):
        self.event = event
        self.service = 'cloudfront'
        self.abstraction = 'client'
        self.resource_type = 'distribution'

    '''
        gets remediations for cloudfront distribution
        args: self
        returns: tuple
            - default_cache_behavior
            - exceptions
    '''

    def __distribution_policy(self) -> tuple:
        remediations: dict = self.remediations()
        logging.debug({'remediations': remediations})
        inspections = remediations['Inspections']
        logging.debug({'inspections': inspections})
        inspections: list = Investigate.iterable_ops(
            remediations['Inspections'], to_int=True)
        logging.debug({'inspections': inspections})
        exceptions: dict = remediations['Exceptions']
        logging.debug({'exceptions': exceptions})
        return inspections, exceptions

    '''
        checks if distributions has violations by getting the remediations from
        table and matching with the event
        args: self
        return: violating keys, list of keys to map to config
    '''

    def __distribution_violations(self) -> tuple:
        violations = []
        event_distribution_config = \
            {
                'distributionConfig':
                    list(Investigate.value_finder(
                        self.event, 'distributionConfig'))[0]
            }
        logging.debug({'event_distribution_config': event_distribution_config})
        # sets remediation config ignores exeptions
        inspections, exceptions = self.__distribution_policy()
        for exception in exceptions:
            exception_tags = exception.get('Tags', [])
        requestor_tags = self.__tags()
        is_exempt = True if self.__is_exempt(exception_tags, requestor_tags) \
            else False
        logging.debug({'is_exempt': is_exempt})
        for inspection in inspections:
            inspection_map = inspection['Inspect']['Map']
            logging.debug({'inspection_map': inspection_map})
            inspection_value = inspection['Inspect']['Value']
            logging.debug({'inspection_value': inspection_value})
            event_value = Investigate.get_value(
                event_distribution_config, inspection_map)
            logging.debug({'event_value': event_value})
            if event_value != inspection_value:
                inspection_map.append(event_value)
                violation = reduce(
                    lambda x, y: {y: x}, reversed(inspection_map))
                logging.debug({'violation': violation})
                violations.append(violation)
                update_map = inspection['Update']['Map']
                logging.debug({'update_map': update_map})
                update_value = inspection['Update']['Value']
                logging.debug({'update_value': update_value})
                Investigate.add_key_value(
                    event_distribution_config, update_map, update_value)
        if not violations:
            event_distribution_config = {}
        logging.debug(
            {'event_distribution_config': event_distribution_config})
        return is_exempt, violations, event_distribution_config

    def __is_exempt(self, exception_tags: list, requestor_tags: list):
        is_exempt = [x for x in exception_tags if x in requestor_tags]
        logging.debug({'is_exempt': is_exempt})
        return is_exempt

    '''
        gets tags for a cloudfront resource
        args: arn
        return: list
    '''

    def __tags(self) -> list:
        arn = list(Investigate.value_finder(self.event, 'aRN'))[0]
        response = self.call('list_tags_for_resource', {'Resource': arn})
        logging.debug({'response': response})
        tags = response['Tags']['Items']
        logging.debug({'tags': tags})
        return tags

    def __distribution_kwargs(self, event_distribution_config):
        self.iterable_ops(event_distribution_config, capitalize=True)
        id = self.event['detail']['responseElements']['distribution']['id']
        logging.debug({'id': id})
        response = self.call('get_distribution_config', {'Id': id})
        e_tag = response.get('ETag')
        kwargs = {
            'Id': id,
            'IfMatch': e_tag
        }
        logging.debug({'kwargs': kwargs})
        kwargs.update(event_distribution_config)
        logging.debug({'kwargs': kwargs})
        return kwargs

    def distribution(self):
        remediation_type = None
        is_exempt, violations, event_distribution_config = \
            self.__distribution_violations()
        remediate = self.account()['Remediate']
        if is_exempt:
            remediation_type = 'Exempt'
        if not remediate:
            remediation_type = 'Notification'
        if violations and not is_exempt and remediate:
            distribution_kwargs = self.__distribution_kwargs(
                event_distribution_config)
            response = self.call('update_distribution', distribution_kwargs)
            logging.debug({'response': response})
            remediation_type = 'update'
        logging.debug({'remediation_type': remediation_type})
        return remediation_type, violations, self.resource_type

    '''
        executes remediation based on event name
        args: None
        returns, None, delete or Update
    '''

    def remediate(self):
        # defines method to call
        remediations = {
            'UpdateDistributionWithTags': self.distribution,
            'UpdateDistribution': self.distribution,
            'CreateDistributionWithTags': self.distribution,
            'CreateDistribution': self.distribution
        }
        return remediations[self.event_name()]()
