from os import path

import boto3

from notificationhub_sdk.base import ImproperlyConfigured

TOKEN_PATH = "/var/run/secrets/eks.amazonaws.com/serviceaccount/token"
SQS_SERVICE_NAME = "sqs"

class SessionCreator:
    """
    Used to create AWS Session
    """
    
    def __init__(self,
                 region: str,
                 access_key: str,
                 secret_key: str, 
                 eks_role_arn: str):
        """
        Parameters:
            access_key: access key of aws account
            secret_key: secret key of aws account
            eks_role_arn: eks role which has access to SQS 
        """
        self._region = region
        self._acces_key = access_key
        self._secret_key = secret_key
        self._eks_role_arn = eks_role_arn
        
    def get_aws_session(self):
        """
        creates aws session based on different criteria
        - Access key and secret key given in the settings
        - EC2: based on the assumption that the role is given to the EC2 instance
        - EKS-role based access: eks_role_arn is taken into consideration
        - Local settings: read from the local ~/.aws/credentials path
        """
        session_created = False
        
        # Access key and secret key given in the settings
        if self._acces_key and self._secret_key:
            client_kwargs = {
                'service_name': SQS_SERVICE_NAME,
                'aws_access_key_id': self._acces_key,
                'aws_secret_access_key': self._secret_key,
                'region_name': self._region
            }
            session = boto3.resource(**client_kwargs)
            if session is not None:
                session_created = True
        else:
            # EC2: based on the assumption that the role is given to the EC2 instance
            client_kwargs = {
                'service_name': SQS_SERVICE_NAME,
                'region_name': self._region
            }
            session = boto3.resource(**client_kwargs)
            if session is not None:
                session_created = True

            # eks role-based access
            if self._eks_role_arn and self._eks_role_arn != "":
                # check whether the given information has the account number or not
                aws_client = boto3.client('sts')
                if aws_client == None or aws_client == "":
                    raise ImproperlyConfigured('Issue while connecting to SQS region `{}`'.format(self._region))

                try:
                    if not path.exists(TOKEN_PATH):
                        raise ImproperlyConfigured('Token not present in pod. Check token at `{}`'.format(TOKEN_PATH))
                    with open(TOKEN_PATH, 'r') as file:
                        access_details = file.read()
                    response = aws_client.assume_role_with_web_identity(
                        RoleArn=self._eks_role_arn,
                        RoleSessionName='string',
                        WebIdentityToken=access_details,
                    )
                    if not response:
                        raise ImproperlyConfigured('Issue with token in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self._eks_role_arn))
                    session_created = True
                except ImportError:
                    raise ImproperlyConfigured('Token not present in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self._eks_role_arn))
        
        # local development
        if session is None and not session_created:
            session = boto3.resource(SQS_SERVICE_NAME)
            if session is not None:
                session_created = True

        # check whether session is created after all possible options
        if session is None and not session_created:
            raise ImproperlyConfigured('AWS session is not created due to improper setting provided in region `{}`'.format(self._region))

        return session
