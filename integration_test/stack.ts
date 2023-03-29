
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class IntegrationTestStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
        const logicalIds: string[] = ['nonCompliant', 'nonCompliantExempt', 'compliant']
        const testServicePrincipal = new cdk.aws_iam.ServicePrincipal('lambda.amazonaws.com')
        const compliantStatement = new cdk.aws_iam.PolicyStatement({
            actions: ['logs:PutLogEvents'],
            resources: ['*']
        })
        const nonCompliantStatement = new cdk.aws_iam.PolicyStatement({
            actions: ['logs:*'],
            resources: ['*']
        })
        const cloudFrontOriginAccessIdentity = new cdk.aws_cloudfront.CfnCloudFrontOriginAccessIdentity(this, 'cloudFrontOriginAccessIdentity', {
            cloudFrontOriginAccessIdentityConfig: {
                comment: 'integrationTest'
            }
        })
        const cloudFrontOriginAccessIdentityId = cdk.Fn.ref('cloudFrontOriginAccessIdentity')
        logicalIds.forEach(logicalId => {
            let role = new cdk.aws_iam.Role(this, `${logicalId}Role`, {
                assumedBy: testServicePrincipal,
            })
            let bucket = new cdk.aws_s3.Bucket(this, `${logicalId}Bucket`, {
                encryption: cdk.aws_s3.BucketEncryption.S3_MANAGED
            })
            bucket.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY)
            let managedPolicy = new cdk.aws_iam.ManagedPolicy(this, `${logicalId}ManagedPolicy`)
            let distribution = new cdk.aws_cloudfront.CfnDistribution(this, `${logicalId}Distribution`, {
                distributionConfig: {
                    enabled: false,
                    defaultCacheBehavior: {
                        targetOriginId: 'only-origin',
                        viewerProtocolPolicy: 'redirect-to-https',
                        forwardedValues: {
                            queryString: false
                        }
                    },
                    origins: [
                        {
                            id: 'only-origin',
                            domainName: bucket.bucketDomainName,
                            s3OriginConfig: {
                                originAccessIdentity: cdk.Fn.sub("origin-access-identity/cloudfront/${cloudFrontOriginAccessIdentity}"),
                            }
                        }
                    ],

                }
            })
            if (logicalId === 'compliant') {
                distribution.addOverride('Properties.DistributionConfig.DefaultCacheBehavior.TrustedSigners', ['self'])
                bucket.addToResourcePolicy(
                    new cdk.aws_iam.PolicyStatement({
                        effect: cdk.aws_iam.Effect.DENY,
                        actions: ['s3:*'],
                        principals: [new cdk.aws_iam.StarPrincipal()],
                        resources: [
                            bucket.bucketArn,
                            bucket.arnForObjects('*')
                        ],
                        conditions: {
                            "Bool": { "aws:SecureTransport": false }
                        }
                    })
                )
                managedPolicy.addStatements(compliantStatement)
                role.attachInlinePolicy(new cdk.aws_iam.Policy(this, `${logicalId}Policy`, {
                    statements: [new cdk.aws_iam.PolicyStatement({
                        actions: ['s3:*'],
                        resources: [
                            bucket.bucketArn,
                            bucket.arnForObjects('*')
                        ]
                    })]
                }))
            } else if (logicalId === 'nonCompliant') {
                managedPolicy.addStatements(nonCompliantStatement)
                role.attachInlinePolicy(new cdk.aws_iam.Policy(this, `${logicalId}Policy`, {
                    statements: [nonCompliantStatement]
                }))
            } else if (logicalId === 'nonCompliantExempt') {
                managedPolicy.addStatements(nonCompliantStatement)
                role.attachInlinePolicy(new cdk.aws_iam.Policy(this, `${logicalId}Policy`, {
                    statements: [nonCompliantStatement]
                }))
                let resourcesToTagExempt = [role, bucket, distribution]
                resourcesToTagExempt.forEach(resourceToTagExempt => {
                    if (resourceToTagExempt === bucket) {
                        cdk.Tags.of(resourceToTagExempt).add('Accessibility', 'Public')
                        cdk.Tags.of(resourceToTagExempt).add('S3PolicyUpdateException', 'True')
                    }
                    if (resourceToTagExempt === distribution) {
                        resourceToTagExempt.addOverride('Properties.Tags', [{ 'Key': 'Exempt', 'Value': 'True' }])
                    }
                    else {
                        cdk.Tags.of(resourceToTagExempt).add('Exempt', 'True')
                    }
                })
            }
        })
    }
}
