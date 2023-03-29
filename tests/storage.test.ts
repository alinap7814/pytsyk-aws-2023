import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { Storage } from '../lib/storage';


test('Tables', () => {
    const app = new cdk.App()
    const stack = new cdk.Stack()
    const tables = new Storage(stack, 'test', 'app').dynamoDbTables();
    //     // THEN
    const template = Template.fromStack(stack);
    template.resourceCountIs('AWS::DynamoDB::Table', 3)
});

test('Buckets', () => {
    const app = new cdk.App()
    const stack = new cdk.Stack()
    const tables = new Storage(stack, 'test', 'app').s3Buckets();
    //     // THEN
    const template = Template.fromStack(stack);
    template.resourceCountIs('AWS::S3::Bucket', 2)
});