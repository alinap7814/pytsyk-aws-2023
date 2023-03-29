import { aws_dynamodb as dynamoDb } from 'aws-cdk-lib';
const remediatorDynamoDbTables: any[] = [
    {
        LogicalId: 'remediationTable',
        PartitionKey: { name: 'RemediationId', type: dynamoDb.AttributeType.STRING },
        SortKey: { name: 'RemediationType', type: dynamoDb.AttributeType.STRING }
    },
    {
        LogicalId: 'policiesTable',
        PartitionKey: { name: 'ResourceType', type: dynamoDb.AttributeType.STRING },
        SortKey: { name: 'EventSource', type: dynamoDb.AttributeType.STRING }


    },
    {
        LogicalId: 'accountsTable',
        PartitionKey: { name: 'AccountNumber', type: dynamoDb.AttributeType.STRING },
        Stream: dynamoDb.StreamViewType.NEW_AND_OLD_IMAGES
    },
    {
        LogicalId: 'usersTable',
        PartitionKey: { name: 'UserName', type: dynamoDb.AttributeType.STRING }
    }
]

export { remediatorDynamoDbTables }