import unittest
from unittest.mock import patch
from rest_handler.src.accounts import Accounts
from os import environ



@patch.dict(
    environ,
    {
        'APP_NAME': 'remediator',
        'ACCOUNTS_TABLE_NAME': 'remediator-cdk-accountsTable01CD9783-1PP5T9WKDPUJ3'
    }
)
class TestAccounts(unittest.TestCase):
    @patch('rest_handler.src.accounts.resource')
    def test_get(
        self,
        mocked_resource
    ):
        items = {
            'Items': [
                {
                    'AccountNumber': '000000000000',
                    'RuleState': 'ENABLED',
                    'Regions': ['us-east-1'],
                    'ExecutionRoleName': 'LaunchPadOperationsStackSetExecutionRole',
                    'AdministrationManaged': True,
                    'Remediate': True,
                    'Name': 'singapore',
                    'Contact': 'AABG_LaunchPad_Security_Team@accenture.com'
                }
            ]
        }
        mocked_resource('dynamodb').Table().scan.return_value = items
        accounts = Accounts().get()
        self.assertListEqual(accounts, items['Items'])


if __name__ == '__main__':
    unittest.main(warnings=False)
