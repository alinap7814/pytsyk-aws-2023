from remediator.src.iam import Iam
from remediator.src.cloudfront import Cloudfront
from remediator.src.reporter import Reporter
from remediator.src.s3 import S3
from remediator.src.accounts import Accounts


import logging
from os import environ
from os import environ

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

# sets logging format.
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

'''
    lambda handler, executes classes in response to events.
    args: event, context 
    returns: None
'''


def handler(event, context):
    logging.info({'event': event})
    # gets application name from env vars
    app_name: str = environ['APP_NAME']
    # checks if records key exist
    # if record keys exists then even is from event bridge other is from API cloud
    # trail
    records = event.get('Records')
    if records:
        # calls to operate on AWS accounts
        Accounts(event).operations()
        return
    event_source = event.get('source')
    logging.debug({'event_source': event_source})
    # gets the class to call by splitting event source(aws.iam, ...), getting last item and
    # converting to title case
    class_to_call = event_source.split('.')[-1].title()
    logging.info({'class_to_call': class_to_call})
    # set the remediation class
    remediation = eval(class_to_call)(event)
    # calls remediate method
    remediation_type, violations, resource_type = remediation.remediate()
    logging.debug({
        'remediation_type': remediation_type,
        'violations': violations,
        'resource_type': resource_type
    })
    if violations:
        Reporter(event, remediation_type, violations, resource_type).report()
