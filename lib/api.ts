import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { join } from 'path';
import { apiResources } from './api-resources';


export class Rest {
  scope: Construct;
  environment: string;
  appName: string;
  constructor(scope: Construct, environment: string, appName: string) {
    this.scope = scope,
      this.appName = appName,
      this.environment = environment
  }
  api({ accountsTable, remediationTable, usersTable, domainName }: { accountsTable: cdk.aws_dynamodb.Table; remediationTable: cdk.aws_dynamodb.Table; usersTable: cdk.aws_dynamodb.Table; domainName: string; }): readonly [cdk.aws_apigateway.LambdaRestApi, cdk.aws_cognito.UserPool, cdk.aws_cognito.UserPoolClient] {
    const functionName = (this.environment !== 'prod') ? `${this.appName}-rest-handler-function-${this.environment}` : `${this.appName}-rest-handler-function`
    const stageName = (this.environment !== 'prod') ? this.environment : 'v1'
    const restApiLogGroupName = (this.environment !== 'prod') ? `${this.appName}-rest-api-logs-${this.environment}` : `${this.appName}-rest-api-logs`
    const recordName = (this.environment !== 'prod') ? `api-${this.appName}-${this.environment}` : `api-${this.appName}`
    const customDomainName = `${recordName}.${domainName}`
    const restHandler = new cdk.aws_lambda.DockerImageFunction(this.scope, "restHandler", {
      functionName: functionName,
      code: cdk.aws_lambda.DockerImageCode.fromImageAsset(join(__dirname, '../rest_handler')),
      environment: {
        ACCOUNTS_TABLE_NAME: accountsTable.tableName,
        REMEDIATION_TABLE_NAME: remediationTable.tableName,
        USER_TABLE_NAME: usersTable.tableName,
        APP_NAME: this.appName
      }
    });
    const restHandlerLogs = new cdk.aws_logs.LogGroup(this.scope, "restHandlerLogs", {
      logGroupName: `/aws/lambda/${functionName}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      retention: 5
    })

    const restApiLogGroup = new cdk.aws_logs.LogGroup(this.scope, "restApiLogs", {
      logGroupName: restApiLogGroupName,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      retention: 5
    });
    const zone = cdk.aws_route53.HostedZone.fromLookup(this.scope, "hostedZone", {
      domainName: domainName,
    });

    const certificate = new cdk.aws_certificatemanager.DnsValidatedCertificate(this.scope, 'crossRegionCertificate', {
      domainName: customDomainName,
      hostedZone: zone,
      cleanupRoute53Records: true
    });
    const restApi = new cdk.aws_apigateway.LambdaRestApi(this.scope, 'restApi', {
      restApiName: recordName,
      handler: restHandler,
      proxy: false,
      cloudWatchRole: true,
      defaultCorsPreflightOptions: {
        allowHeaders: ['*'],
        allowMethods: ['*'],
        allowOrigins: ['*']
      },
      deployOptions: {
        accessLogDestination: new cdk.aws_apigateway.LogGroupLogDestination(restApiLogGroup),
        accessLogFormat: cdk.aws_apigateway.AccessLogFormat.clf(),
        loggingLevel: cdk.aws_apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
        stageName: stageName
      },
      domainName: {
        domainName: customDomainName,
        certificate: certificate
      }
    })
    const aRecord = new cdk.aws_route53.ARecord(this.scope, "apiDns", {
      zone,
      recordName: recordName,
      target: cdk.aws_route53.RecordTarget.fromAlias(
        new cdk.aws_route53_targets.ApiGateway(restApi)
      ),
    });
    const userPool = new cdk.aws_cognito.UserPool(this.scope, 'userPool', {
      signInAliases: {
        username: true
      },
      autoVerify: { email: true, phone: true },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      customAttributes: {
        accounts: new cdk.aws_cognito.StringAttribute({ mutable: true })
      }
    });
    const userPoolClient = userPool.addClient('userPoolClient', {
      authFlows: {
        userPassword: true,
        userSrp: true,
      }
    });
    const devUser = (this.environment !== 'prod') ? new cdk.aws_cognito.CfnUserPoolUser(this.scope, 'devUser', {
      userPoolId: userPool.userPoolId,
      username: `${this.appName}User`
    }) : null

    const authorizer = new cdk.aws_apigateway.CfnAuthorizer(this.scope, 'authorizer', {
      name: `${recordName}-authorizer`,
      restApiId: restApi.restApiId,
      type: 'COGNITO_USER_POOLS',
      identitySource: 'method.request.header.Authorization',
      providerArns: [userPool.userPoolArn],
    });
    const lambdaIntegration = new cdk.aws_apigateway.LambdaIntegration(restHandler)
    apiResources.forEach(resouceElement => {
      let elementResource: string = resouceElement.Resource
      let elementMethods: string[] = resouceElement.Methods
      let apiResource = restApi.root.addResource(elementResource);
      elementMethods.forEach(elementMethod => {
        apiResource.addMethod(elementMethod, lambdaIntegration, {
          authorizationType: cdk.aws_apigateway.AuthorizationType.COGNITO,
          authorizer: {
            authorizerId: authorizer.ref
          }
        });
      });
    })
    restHandlerLogs.grantWrite(restHandler)
    accountsTable.grantReadWriteData(restHandler)
    remediationTable.grantReadWriteData(restHandler)
    usersTable.grantReadWriteData(restHandler)
    return [restApi, userPool, userPoolClient] as const
  }
}


