from os import getenv
import boto3
import boto3.session
from botocore.exceptions import ClientError
import logging


class Session:


    def __init__(self,
                 region_name: str,
                 oidc_account: str = None,
                 oidc_role: str = None,
                 target_account: str = None,
                 ci_roles: list = None
                 ):
        self.web_role_arn = f"arn:aws:iam::{oidc_account}:role/{oidc_role}"
        self.ci_role_arns = ci_roles
        self.target_account = target_account
        self.ci_roles = ci_roles
        self.region_name = region_name

    def __session_kwargs(self, credentials):
        credentials = credentials['Credentials']
        access_key_id = credentials['AccessKeyId']
        secret_access_key = credentials['SecretAccessKey']
        session_token = credentials['SessionToken']
        return {
            'aws_access_key_id': access_key_id,
            'aws_secret_access_key': secret_access_key,
            'aws_session_token': session_token,
            'region_name': self.region_name
        }

    def web(self):
        logging.info('getting web credentials')
        ci_project_id = getenv('CI_PROJECT_ID')
        ci_pipeline_id = getenv('CI_PIPELINE_ID')
        web_idenity_token = getenv('CI_JOB_JWT_V2')
        sts = boto3.client('sts')
        try:
            credentials = sts.assume_role_with_web_identity(
                RoleArn=self.web_role_arn,
                RoleSessionName=f"gitlab-{ci_project_id}-{ci_pipeline_id}",
                WebIdentityToken=web_idenity_token
            )
            session_kwargs = self.__session_kwargs(credentials)
            session = boto3.session.Session(**session_kwargs)
            return session
        except ClientError as client_error:
            logging.error(client_error.response)
            exit()

    def get(self):
        logging.info('getting ci roles credentials')
        if not self.ci_roles:
            return boto3.session.Session()
        session = self.web()
        sts = session.client('sts')
        gitlab_user_email = getenv('GITLAB_USER_EMAIL')
        logging.info({'gitlab_user_email': gitlab_user_email})
        for ci_role in self.ci_roles:
            try:
                credentials = sts.assume_role(
                    RoleArn=f"arn:aws:iam::{self.target_account}:role/{ci_role}",
                    RoleSessionName=gitlab_user_email,
                )
                session_kwargs = self.__session_kwargs(credentials)
                session = boto3.session.Session(**session_kwargs)
                return session
            except ClientError as client_error:
                logging.error(client_error.response)
                exit()
