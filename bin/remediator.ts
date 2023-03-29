#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { Stack } from '../lib/stack';
import { IntegrationTestStack } from '../integration_test/stack';
import { getEnvironment } from '../lib/environment';

const app = new cdk.App();

const stackEnv = { account: '563014625035', region: 'us-east-1' };
const appName: string = 'remediator'
const domainName: string = 'operations.aabglaunchpad.com'
const environment: string = 'prod' // getEnvironment();
const remediatorStackName = (environment !== 'prod') ? `${appName}-${environment}` : appName
const remediatorTestStackName = `${appName}-integration-${environment}`
const remediatorStack = new Stack(app, remediatorStackName, environment, appName, domainName, {
  stackName: remediatorStackName,
  env: stackEnv
});
const integrationTestStack = new IntegrationTestStack(app, remediatorTestStackName, {
  stackName: remediatorTestStackName,
  env: stackEnv
})