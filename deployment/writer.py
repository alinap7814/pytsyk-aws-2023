from threading import local
from boto3.session import Session
from reader import Reader
from os import listdir
import logging


class Writer:


    def __init__(
            self,
            environment,
            app_name
    ):
        self.environment = environment
        self.session = Session()
        self.app_name = app_name

    def get_stack_output_value(self, output_key):
        logging.info('start')
        cloudformation = self.session.client('cloudformation')
        stack_name = f'{self.app_name}' if self.environment == 'prod' \
            else f'{self.app_name}-{self.environment}'
        stack = cloudformation.describe_stacks(
            StackName=stack_name,
        )['Stacks'][0]
        outputs = stack['Outputs']
        for output in outputs:
            if output['OutputKey'] == output_key:
                return output['OutputValue']

    def file_names(self, directory):
        files = []
        file_names = listdir(directory)
        for file_name in file_names:
            files.append(file_name)
        return files

    def delete_accounts(self):
        table_name = self.get_stack_output_value('accountsTableName')
        logging.debug({'table_name': table_name})
        dynamodb = self.session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        accounts = table.scan()['Items']
        for account in accounts:
            table.delete_item(Key={'AccountNumber': account['AccountNumber']})

    def account_items(self):
        logging.info('start')
        table_name = self.get_stack_output_value('accountsTableName')
        logging.debug({'table_name': table_name})
        dynamodb = self.session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        local_items = Reader().yml('accounts.yml').get(self.environment, False)
        local_items = local_items if local_items else Reader().yml(
            'accounts.yml').get('dev', False)
        logging.debug({'local_items': local_items})
        table_items = table.scan().get('Items')
        logging.debug({'table_items': table_items})
        for table_item in table_items:
            logging.debug({'table_item': table_item})
            key_to_search = 'AccountNumber'
            account_number = table_item[key_to_search]
            if local_items:
                item_in_local = next((
                    True for item in local_items
                    if item[key_to_search] == account_number), False)
                logging.debug({'item_in_local': item_in_local})
            else:
                item_in_local = False
            if not item_in_local:
                key_to_delete = {key_to_search: account_number}
                logging.debug({'key_to_delete': key_to_delete})
                response = table.delete_item(Key=key_to_delete)
        if not local_items:
            return
        for local_item in local_items:
            logging.debug({'local_item': local_item})
            account_number = local_item['AccountNumber']
            account_name = local_item['Name']
            logging.debug({'account_number': account_number})
            table_items = [x for x in table_items
                           if x['AccountNumber'] == account_number]
            logging.debug({'table_items': table_items})
            if not table_items:
                response = table.put_item(Item=local_item)
                logging.debug({'put_response': response})
                continue
            table_item = table_items[0]
            to_update_attributes = [
                key for key in table_item.keys() & local_item
                if table_item[key] != local_item[key]
            ]
            logging.debug({'to_update_attributes': to_update_attributes})
            update_expressions = []
            expression_attribute_values = {}
            if to_update_attributes:
                for to_update_attribute in to_update_attributes:
                    t = local_item[to_update_attribute]
                    update_expression = f'{to_update_attribute} = :{to_update_attribute}'
                    update_expressions.append(update_expression)
                    expression_attribute_value = {f':{to_update_attribute}':
                                                  local_item[to_update_attribute]}
                    expression_attribute_values.update(
                        expression_attribute_value)
                update_expressions = f"SET {','.join(update_expressions)}"
                logging.debug({'update_expressions': update_expressions})
                logging.debug(
                    {'expression_attribute_values': expression_attribute_values})
                response = table.update_item(
                    Key={'AccountNumber': account_number},
                    UpdateExpression=update_expressions,
                    ExpressionAttributeValues=expression_attribute_values
                )
                logging.debug({'update_response': response})

    def policy_items(self):
        logging.info('start')
        table_name = self.get_stack_output_value('policiesTableName')
        logging.debug({'table_name': table_name})
        dynamodb = self.session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        remediation_policies_directory = 'remediations'
        local_items = []
        file_names = self.file_names(remediation_policies_directory)
        logging.debug({'file_names': file_names})
        for file_name in file_names:
            file_path = f"{remediation_policies_directory}/{file_name}"
            policy = Reader().yml(file_path)
            local_items.append(policy)
        logging.debug({'local_items': local_items})
        table_items = table.scan()['Items']
        for table_item in table_items:
            logging.debug({'table_item': table_item})
            if table_item not in local_items:
                account_number = table_item.get('AccountNumber')
                if account_number:
                    key = {'AccountNumber': account_number}
                else:
                    resource_type = table_item.get('ResourceType')
                    event_source = table_item.get('EventSource')
                    key = {'ResourceType': resource_type,
                           'EventSource': event_source}
                table.delete_item(Key=key)
        for local_item in local_items:
            table.put_item(Item=local_item)
        logging.info('end')

    def execution_template(self, delete=False):
        logging.info('start')
        template_key = 'template.yml'
        bucket_name = self.get_stack_output_value(
            'executionTemplateBucketName')
        s3 = self.session.resource('s3')
        if delete:
            bucket = s3.Bucket(bucket_name)
            bucket.delete_objects(Delete={'Objects': [{'Key': template_key}]})
            return
        s3.Object(bucket_name, template_key).upload_file(
            f"./execution_infra/{template_key}")

    def policies(self, delete=False):
        logging.info('start')
        policies_dir = 'acp_policies'
        bucket_name = self.get_stack_output_value('policiesBucketName')
        s3 = self.session.resource('s3')
        file_names = self.file_names(policies_dir)
        objects = []
        for file_name in file_names:
            if delete:
                objects.append({'Key': file_name})
            s3.Object(bucket_name, file_name).upload_file(
                f"./{policies_dir}/{file_name}")
        if objects:
            bucket = s3.Bucket(bucket_name)
            bucket.delete_objects(Delete={'Objects': objects})
        logging.info('end')
