import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Storage } from './storage';
import { Events } from './events';
import { Compute } from './compute';
import { Rest } from './api'
import { Hosting } from './hosting'



export class Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, env: string, appName: string, domainName: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const events = new Events(this, env, appName)
    const storage = new Storage(this, env, appName)
    const compute = new Compute(this, env, appName)
    const rest = new Rest(this, env, appName)
    const hosting = new Hosting(this, env, appName)
    const storageTablesDynamoDbTables = storage.dynamoDbTables()
    const remediationTable = storageTablesDynamoDbTables['remediationTable']
    const policiesTable = storageTablesDynamoDbTables['policiesTable']
    const accountsTable = storageTablesDynamoDbTables['accountsTable']
    const usersTable = storageTablesDynamoDbTables['usersTable']
    const emailDomainSource = 'operations.aabglaunchpad.com'
    const storageS3Buckets = storage.s3Buckets()
    const executionTemplateBucket = storageS3Buckets['executionTemplateBucket']
    const policiesBucket = storageS3Buckets['policiesBucket']
    const remediatorFunction = compute.lambda(
      remediationTable,
      policiesTable,
      accountsTable,
      emailDomainSource,
      policiesBucket,
      executionTemplateBucket
    )
    events.remediator(remediatorFunction)
    const [restApi, userPool, userPoolClient] = rest.api({ accountsTable, remediationTable, usersTable, domainName })
    hosting.app(restApi, userPool, userPoolClient)
  }
}