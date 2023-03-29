import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { remediatorDynamoDbTables } from './tables'
import { remediatorS3Buckets } from './buckets';

interface Resources {
    [key: string]: any
}


export class Storage {
    scope: Construct
    env: string
    appName: string
    constructor(scope: Construct, env: string, appName: string) {
        this.scope = scope,
            this.env = env
    }
    dynamoDbTables() {
        let tables: Resources = {}
        remediatorDynamoDbTables.forEach(element => {
            let elementLogicalId = element.LogicalId
            let elementPartitionKey = element.PartitionKey
            let elementSortKey = element.SortKey
            let elementStream = element.Stream
            if (elementSortKey === undefined) {
                let elementSortKey = cdk.Aws.NO_VALUE
            }
            if (elementStream === undefined) {
                let Stream = cdk.Aws.NO_VALUE
            }
            let table = new cdk.aws_dynamodb.Table(this.scope, elementLogicalId, {
                partitionKey: elementPartitionKey,
                sortKey: elementSortKey,
                stream: elementStream
            })
            let cfnTable = table.node.defaultChild as cdk.aws_dynamodb.CfnTable
            cfnTable.overrideLogicalId(elementLogicalId)
            if (this.env !== 'prod') {
                table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY)
            }
            tables[`${elementLogicalId}`] = table
            new cdk.CfnOutput(this.scope, `${elementLogicalId}Name`, {
                value: table.tableName,
            })
        })
        return tables
    }
    s3Buckets() {
        const buckets: Resources = {}
        remediatorS3Buckets.forEach(element => {
            let elementLogicalId = element.LogicalId
            let bucket = new cdk.aws_s3.Bucket(this.scope, elementLogicalId, {
                encryption: cdk.aws_s3.BucketEncryption.S3_MANAGED
            })
            let cfnBcket = bucket.node.defaultChild as cdk.aws_s3.CfnBucket
            cfnBcket.overrideLogicalId(elementLogicalId)
            let bucketArn = bucket.bucketArn
            if (this.env !== 'prod') {
                bucket.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY)
            }
            bucket.addToResourcePolicy(
                new cdk.aws_iam.PolicyStatement({
                    effect: cdk.aws_iam.Effect.DENY,
                    actions: ['s3:*'],
                    principals: [new cdk.aws_iam.StarPrincipal()],
                    resources: [
                        bucketArn,
                        `${bucketArn}/*`
                    ],
                    conditions: {
                        "Bool": { "aws:SecureTransport": false }
                    }
                })
            )
            buckets[`${elementLogicalId}`] = bucket
            new cdk.CfnOutput(this.scope, `${elementLogicalId}Name`, {
                value: bucket.bucketName,
            })
        })
        return buckets
    }
}
