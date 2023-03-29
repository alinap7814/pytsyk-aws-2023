import logging
from rest_handler.src.accounts import Accounts
import json


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


def handler(event, context):
    status_code = 200
    logging.debug({'event': event})
    # gets string from event = "/value", removes first char and title cases
    class_to_call = eval(event['resource'][1:].title())(event)
    logging.info({'class_to_call': class_to_call})
    # gets the method to call from class and makes it lower case
    method_to_call = event['httpMethod'].lower()
    logging.info({'method_to_call': method_to_call})
    # gets body from call
    body = getattr(class_to_call, method_to_call)()
    logging.debug({'body': body})
    response = {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        }
    }
    return response
