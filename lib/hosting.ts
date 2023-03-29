import * as cdk from 'aws-cdk-lib';
import { readFileSync } from 'fs'
import { Construct } from 'constructs';


export class Hosting {
    scope: Construct;
    environment: string;
    appName: string;
    constructor(scope: Construct, appName: string, environment: string) {
        this.scope = scope,
            this.appName = appName,
            this.environment = environment
    }
    app(restApi: cdk.aws_apigateway.LambdaRestApi, userPool: cdk.aws_cognito.UserPool, userPoolClient: cdk.aws_cognito.UserPoolClient) {
        const buildSpec = readFileSync('amplify-build-specs.yml', "utf8");
        // const document: any = load(accountsContent);
        const amplifyName = (this.environment !== 'prod') ? `${this.appName}-amplify-${this.environment}` : `${this.appName}-amplify`
        const cfnApp = new cdk.aws_amplify.CfnApp(this.scope, `amplifyApp`, {
            name: amplifyName,
            customRules: [
                {
                    "source": "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf)$)([^.]+$)/>",
                    "target": "/index.html",
                    "status": "200",
                    "condition": "",
                }
            ],
            buildSpec: buildSpec,
            environmentVariables: [
                {
                    name: 'API_ENDPOINT',
                    value: `https://${restApi.restApiId}.execute-api.${cdk.Stack.of(this.scope).region}.amazonaws.com/${restApi.deploymentStage.stageName}`
                },
                {
                    name: 'USER_POOL_ID',
                    value: userPool.userPoolId
                },
                {
                    name: 'USER_POOL_CLIENT_ID',
                    value: userPoolClient.userPoolClientId
                },
                {
                    name: 'REGION',
                    value: cdk.Stack.of(this.scope).region
                }
            ]
        });
        new cdk.CfnOutput(this.scope, 'amplifyAppId', {
            value: cfnApp.attrAppId,
        })
    }
}


