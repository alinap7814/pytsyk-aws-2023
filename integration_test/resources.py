import logging
import json
from time import sleep
import logging
from botocore.exceptions import ClientError
from boto3 import client, resource

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s | %(lineno)s - '
    '%(message)s', level=logging.INFO)

# suppress loggers of chatty packages
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.action').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.factory').setLevel(logging.CRITICAL)


class Resources:

    def __init__(
            self,
            environment,
    ):
        self.environment = environment
        self.stack_name: str = f"remediator-integration-{self.environment}"
        self.administration_stack_name = f"remediator-{self.environment}"
        self.iam_client = client('iam')
        self.s3_client = client('s3')
        self.cloudformation_client = client('cloudformation')
        self.cloudfront_client = client('cloudfront')
        self.dynamodb_resource = resource('dynamodb')

    def tests(self):
        results = []
        tests = {
            'nonCompliantRole': self.role_check_with_non_compliant_policy,
            'nonCompliantExemptRole': self.role_check_with_non_compliant_policy_exempt,
            'nonCompliantManagedPolicy': self.check_managed_policy_non_compliant,
            'compliantManagedPolicy': self.check_managed_policy_compliant,
            'compliantDist': self.check_distribution_non_compliant,
            'nonCompliantExemptDist': self.check_distribution_non_compliant_exempt,
            'nonCompliantBucket': self.check_bucket_ssl_policy_non_compliant,
            'nonCompliantExemptBucket': self.check_bucket_ssl_policy_non_compliant_exempt
        }
        stack_resources = self.cloudformation_client.list_stack_resources(
            StackName=self.stack_name,
        )['StackResourceSummaries']
        for stack_resource in stack_resources:
            logical_resource_id = stack_resource['LogicalResourceId'][:-8]
            resource_name = stack_resource['PhysicalResourceId']
            test = tests.get(logical_resource_id)
            if test:
                result = test(resource_name)
                results.append({logical_resource_id: result})
        print(results)

    def role_check_with_non_compliant_policy(self, role_name):
        policy_names = self.iam_client.list_role_policies(
            RoleName=role_name)['PolicyNames']
        return False if 'non-compliant' in policy_names else True

    def role_check_with_non_compliant_policy_exempt(self, role_name):
        checks = ['compliant', 'non-compliant']
        policy_names = self.iam_client.list_role_policies(
            RoleName=role_name)['PolicyNames']
        for check in checks:
            if check not in policy_names:
                return False
        return True

    def check_managed_policy_non_compliant(self, policy_arn):
        try:
            response = self.iam_client.get_policy(PolicyArn=policy_arn)
        except ClientError as client_error:
            client_error_response = client_error.response
            code = client_error_response['Error']['Code']
            if code == 'NoSuchEntity':
                return True
        return False

    def check_managed_policy_non_compliant_exempt(self, policy_arn):
        try:
            response = self.iam_client.get_policy(PolicyArn=policy_arn)
        except ClientError as client_error:
            client_error_response = client_error.response
            code = client_error_response['Error']['Code']
            if code == 'NoSuchEntity':
                return False
        return True

    def check_managed_policy_compliant(self, policy_arn):
        try:
            response = self.iam_client.get_policy(PolicyArn=policy_arn)
        except ClientError as client_error:
            client_error_response = client_error.response
            code = client_error_response['Error']['Code']
            if code == 'NoSuchEntity':
                return False
        return True

    def check_bucket_ssl_policy_non_compliant(self, bucket_name):
        statement_to_check = [
            {
                'Effect': 'Deny',
                'Principal': '*',
                'Action': 's3:*',
                'Resource': [
                    f'arn:aws:s3:::{bucket_name}',
                    f'arn:aws:s3:::{bucket_name}/*'
                ],
                'Condition': {
                    'Bool': {
                        'aws:SecureTransport': 'false'
                    }
                }
            }
        ]
        try:
            logging.info('getting policy')
            bucket_policy = self.s3_client.get_bucket_policy(
                Bucket=bucket_name).get('Policy')
            logging.info('checking policy')
            bucket_policy = json.loads(bucket_policy)
            logging.debug({'bucket_policy': bucket_policy})
            statement = bucket_policy.get('Statement')
            logging.debug({'statement': statement})
            logging.debug({'statement_to_check': statement_to_check})
            if statement == statement_to_check:
                return True
            return False
        except ClientError as client_error:
            client_error_response = client_error.response
            code = client_error_response['Error']['Code']
            if code == 'NoSuchBucketPolicy':
                return False

    def check_bucket_ssl_policy_non_compliant_exempt(self, bucket_name):
        try:
            policy = self.s3_client.get_bucket_policy(Bucket=bucket_name)
        except ClientError as client_error:
            client_error_response = client_error.response
            code = client_error_response['Error']['Code']
            if code == 'NoSuchBucketPolicy':
                return True
        return False

    def check_distribution_non_compliant(self, distribution_id):
        distribution = self.cloudfront_client.get_distribution(Id=distribution_id)[
            'Distribution']
        behavior = distribution['DistributionConfig']['DefaultCacheBehavior']
        trusted_signers = behavior['TrustedSigners']['Enabled']
        return trusted_signers

    def check_distribution_non_compliant_exempt(self, distribution_id):
        distribution = self.cloudfront_client.get_distribution(Id=distribution_id)[
            'Distribution']
        behavior = distribution['DistributionConfig']['DefaultCacheBehavior']
        trusted_signers = behavior['TrustedSigners']['Enabled']
        if not trusted_signers:
            return True
        return trusted_signers

    def update_remediate(self, remediate=True):
        logging.info(f'updating account to remeiate={remediate}')
        test_stack_name = self.stack_name
        self.stack_name = self.administration_stack_name
        table_name = 'remediator-cdk-accountsTable01CD9783-DYG6QU3QBDU9'
        table = self.dynamodb_resource.Table(table_name)
        table.update_item(
            Key={'AccountNumber': '563014625035'},
            UpdateExpression="set Remediate = :r",
            ExpressionAttributeValues={
                ':r': remediate,
            }
        )
        self.stack_name = test_stack_name


Resources('cdk').update_remediate(False)
