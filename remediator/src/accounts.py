
from os import environ
from re import A
from boto3 import client
from json import dumps
import logging
from remediator.src.investigator import Investigate
from copy import deepcopy
from time import sleep
from botocore.exceptions import ClientError
from boto3 import resource


class Accounts:
    def __init__(self, event):
        self.event = event
        self.administrator_role_arn = environ['ADMINISTRATION_ROLE_ARN']
        self.administrator_account_id = environ['ADMINISTRATION_ACCOUNT_ID']
        self.app_name = environ['APP_NAME']
        self.environment = environ['ENVIRONMENT']

    @staticmethod
    def create_cloudformation_parameters(parameters):
        logging.info('start')
        logging.debug({'parameters': parameters})
        cloudformation_parameters = []
        for parameter_key, parameter_value in parameters.items():
            cloudformation_parameter = {
                'ParameterKey': parameter_key
            }
            if parameter_value:
                cloudformation_parameter.update(
                    {'ParameterValue': str(parameter_value)})
            else:
                cloudformation_parameter.update({'UsePreviousValue': True})
            cloudformation_parameters.append(cloudformation_parameter)
        logging.debug({'cloudformation_parameters': cloudformation_parameters})
        return cloudformation_parameters

    def get_stack_set_name(self, account_name):
        if self.environment == 'prod':
            return f'{self.app_name}-{account_name}'
        else:
            return f'{self.app_name}-{account_name}-{self.environment}'

    def stack_set_operation(
        self,
        account_name,
        operation,
        rule_state=None,
        execution_role=None,
        contact=None,
        get_template=None
    ):
        operation_id = None
        parameters = {
            'administrationAccountId': self.administrator_account_id,
            'environment': self.environment,
            'ruleState': rule_state,
            'appName': self.app_name,
        }
        logging.info(f'start {operation} on {account_name}')
        cloudformation_parameters = \
            self.create_cloudformation_parameters(parameters)
        template_bucket_name = environ['EXECUTION_TEMPLATE_BUCKET_NAME']
        stack_set_name = self.get_stack_set_name(account_name)
        if operation == 'delete':
            stack_set_kwargs = {'StackSetName': stack_set_name}
        else:
            stack_set_kwargs = {
                'StackSetName': stack_set_name,
                'Parameters': cloudformation_parameters,
                'AdministrationRoleARN': self.administrator_role_arn,
                'ExecutionRoleName': execution_role,
                'Capabilities': ['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
                'Tags': [
                    {
                        'Key': 'AdmnistrationAccount',
                        'Value': self.administrator_account_id
                    },
                    {
                        'Key': 'Contact', 'Value': contact
                    }
                ]
            }
            if get_template:
                template_body = \
                    Investigate.reader(template_bucket_name, 'template.yml')
                stack_set_kwargs.update({'TemplateBody': template_body})
            else:
                stack_set_kwargs.update({'UsePreviousTemplate': True})
        try:
            response = getattr(client('cloudformation'),
                               f'{operation}_stack_set')(**stack_set_kwargs)
            operation_id = response.get('OperationId')
        except ClientError as client_error:
            client_error_response = client_error.response
            logging.warning(client_error_response)
            operation_id = None
        logging.info(f'complete {operation} on {account_name}')
        return {stack_set_name: operation_id}

    def stack_instance_operation(
        self,
        account_name,
        account_number,
        account_regions,
        operation
    ):
        logging.info(f'start {account_name} {operation}')
        stack_set_name = self.get_stack_set_name(account_name)
        stack_instance_kwargs = {
            'StackSetName': stack_set_name,
            'Accounts': [str(account_number)],
            'Regions': account_regions,
            'OperationPreferences': {
                'RegionConcurrencyType': 'PARALLEL',
                'MaxConcurrentPercentage': 100,
                'FailureTolerancePercentage': 25
            }
        }
        if operation == 'delete':
            stack_instance_kwargs['RetainStacks'] = False
        try:
            response = \
                getattr(client('cloudformation'),
                        f'{operation}_stack_instances')(**stack_instance_kwargs)
            operation_id = response['OperationId']
            logging.debug(response)
            logging.info(f'complete {account_name} {operation}')
            return {stack_set_name: operation_id}
        except ClientError as client_error:
            client_error_response = client_error.response
            logging.warning(client_error_response)
            code = client_error_response['Error']['Code']
            message = client_error_response['Error']['Message']
            if code == 'OperationInProgressException':
                logging.debug(client_error_response)
                operation_id_pending = message.split(':')[-1].strip()
                operation_in_progress = [
                    {stack_set_name: operation_id_pending}]
                self.stack_set_operations_waiter(operation_in_progress)
                return self.stack_instance_operation(
                    account_name, account_number, account_regions, operation)

    def stack_instances_operation(self, index):
        logging.info(f'start')
        operations_in_progress = []
        record = self.event['Records'][index]
        event_name = record['eventName']
        new_image = Investigate.iterable_ops(
            record['dynamodb'].get('NewImage', {}), dynamo_deserialize=True)
        logging.debug({'new_image': new_image})
        old_image = Investigate.iterable_ops(
            record['dynamodb'].get('OldImage', {}), dynamo_deserialize=True)
        logging.debug({'old_image': old_image})
        if event_name == 'INSERT':
            administration_managed = new_image.get('AdministrationManaged')
            if administration_managed:
                account_name = new_image.get('Name')
                rule_state = new_image.get('RuleState')
                contact = new_image.get('Contact', 'None')
                account_regions = new_image.get('Regions', [])
                account_number = new_image.get('AccountNumber')
                execution_role = new_image.get('ExecutionRoleName')
                self.stack_set_operation(
                    account_name=account_name,
                    operation='create',
                    rule_state=rule_state,
                    execution_role=execution_role,
                    contact=contact,
                    get_template=True
                )
                operation = self.stack_instance_operation(
                    account_name=account_name,
                    account_number=account_number,
                    account_regions=account_regions,
                    operation='create')
                operations_in_progress.append(operation)
                logging.info({'operation': operation})
        elif event_name == 'MODIFY':
            administration_managed = new_image.get('AdministrationManaged')
            if administration_managed:
                updates = \
                    [
                        key for key in new_image.keys() & old_image
                        if new_image[key] != old_image.get(key)
                    ]
                logging.debug({'updates': updates})
                account_number = new_image.get('AccountNumber')
                account_name = new_image.get('Name')
                execution_role = new_image.get('ExecutionRoleName')
                contact = new_image.get('Contact')
                rule_state = new_image.get('RuleState')
                update_stack_set = any(
                    key_update == 'RuleState' or key_update == 'Contact' for key_update in updates)
                update_regions = any(update == 'Regions' for update in updates)
                logging.debug({'update_stack_set': update_stack_set})
                logging.debug({'update_regions': update_regions})
                if update_stack_set:
                    logging.info('updating stack set')
                    operation = self.stack_set_operation(
                        account_name, 'update', rule_state, execution_role, contact)
                    operations_in_progress.append(operation)
                    logging.info({'operation': operation})
            if update_regions:
                updated_regions = new_image.get('Regions', [])
                oudated_regions = old_image.get('Regions', [])
                regions_to_delete = list(
                    set(oudated_regions) - set(updated_regions))
                regions_to_add = list(
                    set(updated_regions) - set(oudated_regions))
                if regions_to_delete:
                    operation = self.stack_instance_operation(
                        account_name, account_number, regions_to_delete, 'delete')
                    operations_in_progress.append(operation)
                    logging.info({'operation': operation})
                if regions_to_add:
                    operation = self.stack_instance_operation(
                        account_name, account_number, regions_to_add, 'create')
                    operations_in_progress.append(operation)
                    logging.info({'operation': operation})
        elif event_name == 'REMOVE':
            administration_managed = old_image.get('AdministrationManaged')
            if administration_managed:
                regions_to_delete = old_image.get('Regions', [])
                account_number = old_image.get('AccountNumber')
                account_name = old_image.get('Name')
                operation = self.stack_instance_operation(
                    account_name, account_number, regions_to_delete, 'delete')
                operations_in_progress.append(operation)
                logging.info({'operation': operation})
        logging.info('complete')
        return operations_in_progress

    def stack_set_operations_waiter(self, in_progress, attempt=1):
        logging.info(f'start {attempt}')
        logging.debug({'in_progress': in_progress})
        pending_statuses = ['RUNNING', 'STOPPING', 'QUEUED']
        in_progress_copy = deepcopy(in_progress)
        logging.debug({'in_progress_copy': in_progress_copy})
        for in_progress in in_progress:
            if not in_progress:
                in_progress_copy.remove(in_progress)
                continue
            logging.debug({'in_progress': in_progress})
            for stack_set_name, operation_id in in_progress.items():
                if not operation_id:
                    in_progress_copy.remove(in_progress)
                    continue
                kwargs = {
                    'StackSetName': stack_set_name,
                    'OperationId': operation_id
                }
                stack_set_operation = \
                    client('cloudformation').describe_stack_set_operation(
                        **kwargs)['StackSetOperation']
                operation_status = stack_set_operation['Status']
                logging.info(stack_set_operation)
                if operation_status == 'FAILED':
                    logging.error(stack_set_operation)
                    in_progress_copy.remove(in_progress)
                    # TODO notify of failure
                    continue
                elif operation_status == 'SUCCEEDED':
                    in_progress_copy.remove(in_progress)
                    continue
                elif operation_status in pending_statuses:
                    continue
            logging.debug({'in_progress_copy': in_progress_copy})
            logging.info(f'complete {attempt}')
        if in_progress_copy:
            sleep(20)
            attempt += 1
            logging.debug({'attempt': attempt})
            self.stack_set_operations_waiter(in_progress_copy, attempt)

    def update_stack_set_template(self):
        logging.info('start')
        operations_in_progress = []
        table: object = resource('dynamodb').Table(
            environ['ACCOUNTS_TABLE'])
        accounts = table.scan().get('Items')
        logging.debug({'accounts': accounts})
        if accounts:
            for account in accounts:
                operation = self.stack_set_operation(
                    account_name=account['Name'],
                    operation='update',
                    rule_state=account['RuleState'],
                    execution_role=account['ExecutionRoleName'],
                    contact=account['Contact'],
                    get_template=True
                )
                operations_in_progress.append(operation)
        logging.debug({'operations_in_progress': operations_in_progress})
        logging.info('complete')
        return operations_in_progress

    def operations(self):
        logging.info('start')
        operations_in_progress = []
        records = self.event['Records']
        update_accounts_stack_sets_template = [
            record for record in records if record['eventSource'] == 'aws:s3'
        ]
        if update_accounts_stack_sets_template:
            operations = self.update_stack_set_template()
            operations_in_progress.extend(operations)
        for index, record in enumerate(records):
            if record['eventSource'] != 'aws:dynamodb':
                continue
            logging.debug({'index': index})
            operations = self.stack_instances_operation(index)
            operations_in_progress.extend(operations)
        logging.debug({'operations_in_progress': operations_in_progress})
        if operations_in_progress:
            self.stack_set_operations_waiter(operations_in_progress)
        delete_stack_sets = [
            record for record in records if record['eventName'] == 'REMOVE'
        ]
        for delete_stack_set in delete_stack_sets:
            account = Investigate.iterable_ops(
                delete_stack_set['dynamodb'].get('OldImage'), dynamo_deserialize=True)
            account_name = account['Name']
            if not account['AdministrationManaged']:
                continue
            self.stack_set_operation(account_name, 'delete')
        logging.info('complete')
