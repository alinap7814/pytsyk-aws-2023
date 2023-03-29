

# import logging
# from os import environ
# from unittest.mock import patch, call
# import unittest
# from rest_handler.__main__ import handler
# accounts_get_event = {
#     'resource': '/accounts',
#     'path': '/accounts',
#     'httpMethod': 'GET',
#     'headers': {
#         'Accept-Encoding': 'identity',
#         'Authorization': 'test-auth',
#         'Host': 'api-remediator-cdk.operations.aabglaunchpad.com',
#         'X-Amzn-Trace-Id': 'Root=1-637799be-002e8d2825a9913b6f8c3fbf',
#         'X-Forwarded-For': '67.205.203.115',
#         'X-Forwarded-Port': '443',
#         'X-Forwarded-Proto': 'https'
#     },
#     'multiValueHeaders': {
#         'Accept-Encoding': ['identity'],
#         'Authorization': ['test-auth'],
#         'Host': ['api-remediator-cdk.operations.aabglaunchpad.com'],
#         'X-Amzn-Trace-Id': ['Root=1-637799be-002e8d2825a9913b6f8c3fbf'],
#         'X-Forwarded-For': ['67.205.203.115'],
#         'X-Forwarded-Port': ['443'],
#         'X-Forwarded-Proto': ['https']
#     },
#     'queryStringParameters': None,
#     'multiValueQueryStringParameters': None,
#     'pathParameters': None,
#     'stageVariables': None,
#     'requestContext': {
#         'resourceId': 'lophpb',
#         'authorizer': {
#             'claims': {
#                 'origin_jti': '27441226-012d-48c6-980d-6f278cce311a',
#                 'sub': '53bc314d-a416-471a-a299-f6e85e6a892d',
#                 'aud': '1irnegu16e6f24opdfiasgjjq7',
#                 'event_id': 'ec3ef6ee-163b-4d83-a1dd-7603f33c108b',
#                 'token_use': 'id',
#                 'auth_time': '1668782526',
#                 'iss': 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_lKlPLWVrr',
#                 'cognito:username': 'remediatorUser',
#                 'exp': 'Fri Nov 18 15:42:06 UTC 2022',
#                 'iat': 'Fri Nov 18 14:42:06 UTC 2022',
#                 'jti': 'c91ff097-b6e7-4255-9ebd-9769e0f8f592'
#             }
#         },
#         'resourcePath': '/accounts',
#         'httpMethod': 'GET',
#         'extendedRequestId': 'bzT1xEamIAMFfSQ=',
#         'requestTime': '18/Nov/2022:14:42:06 +0000',
#         'path': '/accounts',
#         'accountId': '563014625035',
#         'protocol': 'HTTP/1.1',
#         'stage': 'cdk',
#         'domainPrefix': 'api-remediator-cdk',
#         'requestTimeEpoch': 1668782526310,
#         'requestId': '8c04ec38-b3eb-43c5-9f7a-a9acd0e77422',
#         'identity': {
#             'cognitoIdentityPoolId': None,
#             'accountId': None,
#             'cognitoIdentityId': None,
#             'caller': None,
#             'sourceIp': '67.205.203.115',
#             'principalOrgId': None,
#             'accessKey': None,
#             'cognitoAuthenticationType': None,
#             'cognitoAuthenticationProvider': None,
#             'userArn': None,
#             'userAgent': None,
#             'user': None
#         },
#         'domainName': 'api-remediator-cdk.operations.aabglaunchpad.com',
#         'apiId': 'geh7jb5e99'
#     },
#     'body': None,
#     'isBase64Encoded': False
# }


# @patch.dict(
#     environ,
#     {
#         'APP_NAME': 'remediator',
#         'ACCOUNTS_TABLE_NAME': 'remediator-cdk-accountsTable01CD9783-1PP5T9WKDPUJ3'
#     }
# )
# class TestMain(unittest.TestCase):

#     @patch('rest_handler.__main__.Accounts')
#     def test_handler_accounts_get(
#         self,
#         mocked_accounts
#     ):
#         handler(accounts_get_event, None)
#         mocked_accounts.assert_called()


# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
