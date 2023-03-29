import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { join } from 'path'


export class Compute {
    scope: Construct;
    env: string;
    appName: string;
    constructor(scope: Construct, env: string, appName: string) {
        this.scope = scope,
            this.env = env,
            this.appName = appName
    }
    lambda(
        remediationTable: cdk.aws_dynamodb.Table,
        policiesTable: cdk.aws_dynamodb.Table,
        accountsTable: cdk.aws_dynamodb.Table,
        emailDomainSource: string,
        policiesBucket: cdk.aws_s3.Bucket,
        executionTemplateBucket: cdk.aws_s3.Bucket
    ) {
        const remediatorFunctionRole = new cdk.aws_iam.Role(this.scope, 'functionRole', {
            assumedBy: new cdk.aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        });
        const remediatorRole = (this.env !== 'prod') ? `${this.appName}-$Region-role-${this.env}` : `${this.appName}-$Region-role`
        const remidiatorFunctionName = (this.env !== 'prod') ? `${this.appName}-function-${this.env}` : `${this.appName}-function`
        const remediatorFunction = new cdk.aws_lambda.DockerImageFunction(this.scope, 'function', {
            functionName: remidiatorFunctionName,
            code: cdk.aws_lambda.DockerImageCode.fromImageAsset(join(__dirname, '../')),
            role: remediatorFunctionRole,
            timeout: cdk.Duration.minutes(10),
            environment: {
                REMEDIATION_TABLE: remediationTable.tableName,
                EMAIL_DOMAIN_SOURCE: emailDomainSource,
                POLICIES_BUCKET: policiesBucket.bucketName,
                POLICIES_TABLE: policiesTable.tableName,
                REMEDIATOR_EXECUTION_ROLE: remediatorRole,
                APP_NAME: this.appName,
                EMAIL_SENDER: this.appName,
                ACCOUNTS_TABLE: accountsTable.tableName,
                ADMINISTRATION_STACK_NAME: cdk.Stack.of(this.scope).stackName,
                ENVIRONMENT: this.env,
                ADMINISTRATION_ROLE_ARN: cdk.Fn.importValue('administrationRoleArn'),
                ADMINISTRATION_ACCOUNT_ID: cdk.Stack.of(this.scope).account,
                EXECUTION_TEMPLATE_BUCKET_NAME: executionTemplateBucket.bucketName
            }
        });
        const remediatorFunctionLogs = new cdk.aws_logs.LogGroup(this.scope, "functionLogGroup", {
            logGroupName: `/aws/lambda/${remidiatorFunctionName}`,
            removalPolicy: cdk.RemovalPolicy.DESTROY,
            retention: 5
        });
        const remediationRolePermissions = new cdk.aws_iam.Policy(this.scope, 'remediationPolicy', {
            statements: [new cdk.aws_iam.PolicyStatement({
                actions: [
                    'iam:DeleteRolePolicy',
                    'iam:DeletePolicy',
                    'iam:ListRoleTags',
                    'iam:ListPolicyTags',
                    'iam:ListPolicyVersion',
                    'iam:DeletePolicyVersion',
                    'iam:SetDefaultPolicyVersion',
                    'iam:DeletePolicyVersion',
                    's3:GetBucketPolicy',
                    's3:GetBucketTagging',
                    's3:PutBucketPolicy',
                    'cloudfront:ListTagForResource',
                    'cloudfront:GetDistributionConfig',
                    'cloudfront:UpdateDistribution',
                    'sts:AssumeRole'
                ],
                resources: ['*']
            })]
        })
        const remediatorOnboardAccountsPermission = new cdk.aws_iam.Policy(this.scope, 'remediatorOnboardAccountsPermission', {
            statements: [new cdk.aws_iam.PolicyStatement({
                actions: [
                    'cloudformation:*',
                    'iam:PassRole'
                ],
                resources: [
                    cdk.Fn.sub("arn:aws:cloudformation:${AWS::Region}:${AWS::AccountId}:stackset/".concat(this.appName).concat("-*")),
                    cdk.Fn.importValue('administrationRoleArn')
                ]
            })]
        })
        const remediatorEmailPermission = new cdk.aws_iam.Policy(this.scope, 'remediatorEmailPermission', {
            statements: [new cdk.aws_iam.PolicyStatement({
                actions: [
                    'ses:SendRawEmail'
                ],
                resources: [
                    cdk.Fn.sub("arn:aws:ses:${AWS::Region}:${AWS::AccountId}:identity/".concat(emailDomainSource)),
                    cdk.Fn.importValue('administrationRoleArn')
                ]
            })]
        })
        remediationTable.grantWriteData(remediatorFunctionRole)
        policiesTable.grantReadData(remediatorFunctionRole)
        accountsTable.grantReadWriteData(remediatorFunctionRole)
        accountsTable.grantStreamRead(remediatorFunctionRole)
        executionTemplateBucket.grantRead(remediatorFunctionRole)
        policiesBucket.grantRead(remediatorFunctionRole)
        remediatorFunctionLogs.grantWrite(remediatorFunctionRole)
        remediatorFunctionRole.attachInlinePolicy(remediationRolePermissions)
        remediatorFunctionRole.attachInlinePolicy(remediatorOnboardAccountsPermission)
        remediatorFunctionRole.attachInlinePolicy(remediatorEmailPermission)
        remediatorFunction.addEventSourceMapping('accountsTableEventMapping', {
            eventSourceArn: accountsTable.tableStreamArn,
            startingPosition: cdk.aws_lambda.StartingPosition.LATEST,
            retryAttempts: 1
        })
        executionTemplateBucket.addEventNotification(
            cdk.aws_s3.EventType.OBJECT_CREATED,
            new cdk.aws_s3_notifications.LambdaDestination(remediatorFunction)
        )
        let cfnFemediatorFunction = remediatorFunction.node.defaultChild as cdk.aws_lambda.CfnFunction
        let cfnFemediatorFunctionLogs = remediatorFunctionLogs.node.defaultChild as cdk.aws_logs.CfnLogGroup
        cfnFemediatorFunction.overrideLogicalId('function')
        cfnFemediatorFunctionLogs.overrideLogicalId('functionLogGroup')
        return remediatorFunction
    }
}
