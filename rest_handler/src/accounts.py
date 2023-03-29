from boto3 import resource
from os import environ

'''
    object to interface with data base
    args = event, EventBridge event
'''



class Accounts:
    def __init__(self):
        self.table: object = resource('dynamodb').Table(
            environ['ACCOUNTS_TABLE_NAME'])
    '''
        gets all items from database
    '''

    def get(self) -> list:
        # scans dynamoDb table
        table_scan: object = self.table.scan()
        accounts: list = table_scan['Items']
        return accounts
