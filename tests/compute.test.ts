import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { Compute } from '../lib/compute';


test('Lambda', () => {
    const app = new cdk.App()
    const stack = new cdk.Stack()
    const remediationTable = new cdk.aws_dynamodb.Table(stack, 'remediationTable', {
        partitionKey: { name: 'id', type: cdk.aws_dynamodb.AttributeType.STRING },
    });
    const policyTable = new cdk.aws_dynamodb.Table(stack, 'policyTable', {
        partitionKey: { name: 'id', type: cdk.aws_dynamodb.AttributeType.STRING },
    });
    const accountsTable = new cdk.aws_dynamodb.Table(stack, 'accountsTable', {
        partitionKey: { name: 'id', type: cdk.aws_dynamodb.AttributeType.STRING },
        stream: cdk.aws_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
    });
    const policiesBucket = new cdk.aws_s3.Bucket(stack, 'policiesBucket')
    const executionTemplateBucket = new cdk.aws_s3.Bucket(stack, 'executionTemplateBucket')
    // const lambda = new Compute(stack, 'test', 'app').lambda(
    //     remediationTable,
    //     policyTable,
    //     accountsTable,
    //     'test.com',
    //     policiesBucket,
    //     executionTemplateBucket
    // );
    //     // THEN
    const template = Template.fromStack(stack);
    // template.resourceCountIs('AWS::Lambda::Function', 1)
});
