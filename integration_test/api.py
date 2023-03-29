from boto3 import resource, client
import json
from botocore.exceptions import ClientError
import logging
import http.client

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


class Rest:
    def __init__(self, client_id):
        self.client_id = client_id

    def get_cognito_token(self):
        connection = http.client.HTTPSConnection(
            'cognito-idp.us-east-1.amazonaws.com')
        headers = {
            "Content-type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"
        }
        data = {
            "AuthParameters": {
                "USERNAME": "remediatorUser",
                "PASSWORD": "Miami305!"
            },
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": self.client_id
        }
        connection.request('POST', '/', json.dumps(data), headers)
        response = connection.getresponse()
        status_code = response.status
        if status_code == 200:
            decoded_response = response.read().decode()
            id_token = json.loads(decoded_response)[
                'AuthenticationResult']['IdToken']
            connection.close()
            return id_token
        else:
            logging.error(status_code)
            exit()

    def request(self, path):
        uri = f"api-remediator-cdk.operations.aabglaunchpad.com"
        authorization = self.get_cognito_token()
        connection = http.client.HTTPSConnection(uri)
        headers = {
            'Authorization': authorization
        }
        connection.request('GET', f"/{path}", headers=headers)
        response = connection.getresponse()
        logging.info(response.status)
        logging.info(response.read().decode())


Rest('5866ou2uitvbdgfrg3lj2dsmu').request('accounts')
