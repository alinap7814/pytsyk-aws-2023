from remediator.src.connector import Connector
from remediator.src.investigator import Investigate

from json import loads
import logging
from operator import itemgetter


'''
    object to interact with iam service
    Inheratance:
        - Connector, to interact with AWS
        - Investigate, sets of methods to get information from several sources
    - args:
        - event, aws cloudwatch event

'''


class Iam(Investigate, Connector):

    def __init__(self, event):
        self.event = event
        self.service = 'iam'
        self.abstraction = 'client'
        self.resource_type = 'policy'

    def __policy_remediations(self) -> tuple:
        # set event name as Policy for policy lookup in table
        logging.debug({'event': self.event})
        remediations: dict = self.remediations()
        logging.debug({'remediations': remediations})
        inspections: list = remediations['Inspections']
        logging.debug({'inspections': inspections})
        exceptions: dict = remediations['Exceptions']
        logging.debug({'exceptions': exceptions})
        return inspections, exceptions

    def __policy_violations(self):
        resource_wildcard = None
        action_wildcard = None
        logging.info('scaning policy')
        request_parameters = self.request_parameters()
        logging.debug({'request_parameters': request_parameters})
        policy_document = loads(request_parameters['policyDocument'])
        logging.debug({'policy_document': policy_document})
        inspections, exceptions = self.__policy_remediations()
        policy_violations = []
        for inspection in inspections:
            for inspection_name, inspection in inspection.items():
                logging.debug({'inspection_name': inspection_name})
                logging.debug({'execution': inspection})
                policy_document_statements = policy_document['Statement']
                logging.debug(
                    {'policy_document_statements': policy_document_statements})
                for policy_document_statement in policy_document_statements:
                    resource = policy_document_statement['Resource']
                    logging.debug({'resource': resource})
                    is_list_resource = isinstance(resource, list)
                    logging.debug({'is_list_resource': is_list_resource})
                    if is_list_resource:
                        if any(x == inspection for x in resource):
                            resource_wildcard = True
                    else:
                        if resource == inspection:
                            resource_wildcard = True
                    logging.debug({'resource_wildcard': resource_wildcard})
                    if not resource_wildcard:
                        continue
                    action = policy_document_statement['Action']
                    logging.debug({'action': action})
                    is_list_action = isinstance(action, list)
                    logging.debug({'is_list_action': is_list_action})
                    if is_list_action:
                        for action_item in action:
                            logging.debug({'action_item': action_item})
                            _, event_action = \
                                action_item.split(':')
                            logging.debug({'event_action': event_action})
                            if event_action == inspection:
                                action_wildcard = True
                    else:
                        _, event_action = action.split(':')
                        logging.debug({'event_action': event_action})
                        if event_action == inspection:
                            action_wildcard = True
                    logging.debug({'action_wildcard': action_wildcard})
                    is_in_violation = True \
                        if action_wildcard and resource_wildcard else False
                    logging.debug({'is_in_violation': is_in_violation})
                    if is_in_violation:
                        policy_violations.append(policy_document_statement)
        return policy_violations, exceptions

    def __is_exempt(self, exception_tags: list, requestor_tags: list):
        is_exempt = [x for x in exception_tags if x in requestor_tags]
        logging.debug({'is_exempt': is_exempt})
        return is_exempt

    def __role_tags(self):
        role_name = self.request_parameters()['roleName']
        response = self.call('list_role_tags', {'RoleName': role_name})
        tags = response.get('Tags')
        logging.debug({'tags': tags})
        return tags

    def iam_policy(self):
        event_name = self.event_name()
        request_parameters = self.request_parameters()
        remediation_type = None
        policy_violations, exceptions = self.__policy_violations()
        logging.debug({'policy_violations': policy_violations})
        logging.debug({'exceptions': exceptions})
        for exception in exceptions:
            exception_tags = exception.get('Tags', [])
        logging.debug({'exceptions_tags': exception_tags})
        if event_name == 'PutRolePolicy':
            requestor_tags = self.__role_tags()
        elif event_name == 'CreatePolicy':
            requestor_tags = request_parameters.get('tags', [])
        elif event_name == 'CreatePolicyVersion':
            requestor_tags = self.__policy_tags()
        is_exempt = self.__is_exempt(exception_tags, requestor_tags)
        remediate = self.account().get('Remediate')
        if is_exempt:
            remediation_type = 'exempt'
        if not remediate:
            remediation_type = 'Notification'
            is_exempt = True
        elif policy_violations and not is_exempt:
            role_name = request_parameters.get('roleName')
            logging.debug({'role_name': role_name})
            policy_name = request_parameters.get('policyName')
            logging.debug({'policy_name': policy_name})
            if event_name == 'PutRolePolicy':
                self.call(
                    'delete_role_policy',
                    {'RoleName': role_name, 'PolicyName': policy_name}
                )
            elif event_name == 'CreatePolicy':
                event_details = self.event['detail']
                response_elements = event_details['responseElements']
                policy = response_elements.get('policy')
                policy_arn = policy.get('arn')
                self.call(
                    'delete_policy',
                    {'PolicyArn': policy_arn}
                )
            elif event_name == 'CreatePolicyVersion':
                policy_arn = self.request_parameters()['policyArn']
                policy_versions = \
                    self.call(
                        'list_policy_versions', {'PolicyArn': policy_arn}
                    )['Versions']
                policy_versions_sorted = \
                    sorted(policy_versions, key=itemgetter(
                        'CreateDate'), reverse=True)
                version_to_set = policy_versions_sorted[1]['VersionId']
                logging.debug({'version_to_set': version_to_set})
                version_to_delete = policy_versions_sorted[0]['VersionId']
                self.call(
                    'set_default_policy_version',
                    {'PolicyArn': policy_arn, 'VersionId': version_to_set}
                )
                self.call(
                    'delete_policy_version',
                    {'PolicyArn': policy_arn, 'VersionId': version_to_delete}
                )
            remediation_type = 'delete'
        return remediation_type, policy_violations, self.resource_type

    def __policy_tags(self):
        policy_arn = self.request_parameters()['policyArn']
        response = self.call('list_policy_tags', {'PolicyArn': policy_arn})
        tags = response.get('Tags')
        return tags

    def remediate(self):
        remediations = self.iam_policy()
        return remediations
