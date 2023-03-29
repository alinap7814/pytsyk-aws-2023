import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { eventSources } from './sources';


export class Events {
    scope: Construct;
    env: string;
    appName: string;
    constructor(scope: Construct, env: string, appName: string) {
        this.scope = scope,
            this.env = env,
            this.appName = appName
    }
    remediator(lambdaFunction: cdk.aws_lambda.Function) {
        const eventBusName = (this.env !== 'prod') ? `${this.appName}-event-bus-${this.env}` : `${this.appName}-event-bus`
        const policyStatementId = `${eventBusName}-statement`
        const remediatorEventBus = new cdk.aws_events.EventBus(this.scope, 'eventBus', {
            eventBusName: eventBusName
        })
        const remediatorEventBusPolicy = new cdk.aws_events.CfnEventBusPolicy(this.scope, 'eventBusPolicy', {
            statementId: policyStatementId,
            action: 'events:PutEvents',
            eventBusName: remediatorEventBus.eventBusName,
            principal: '*',
            condition: {
                key: "aws:PrincipalOrgID",
                value: "o-92tlgkezai",
                type: "StringEquals"
            }
        })
        let cfnRemediatorEventBus = remediatorEventBus.node.defaultChild as cdk.aws_events.CfnEventBus
        cfnRemediatorEventBus.overrideLogicalId('eventBus')
        const remediatorRule = new cdk.aws_events.Rule(this.scope, 'remediatorRule', {
            eventBus: remediatorEventBus,
            eventPattern: {
                source: eventSources,
                detail: {
                    userIdentity: {
                        sessionContext: {
                            sessionIssuer: {
                                userName: [{ "anything-but": { "prefix": this.appName } }]
                            }
                        }
                    }
                }
            }
        })
        remediatorRule.addTarget(new cdk.aws_events_targets.LambdaFunction(lambdaFunction))
    }
}
