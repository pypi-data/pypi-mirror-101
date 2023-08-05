import importlib
import os
from configparser import (ConfigParser, NoOptionError, NoSectionError,
                          ParsingError)
from os import path

import boto3

from notificationhub_sdk.base import ImproperlyConfigured
from notificationhub_sdk.common import MessageType

TOKEN_PATH = "/var/run/secrets/eks.amazonaws.com/serviceaccount/token"

class SQSProducer:
    """
    Used for pushing the messages to SQS
    """
    setting_keys = (
        ('access_key_id', 'NOTIFICATION_HUB_SQS_ACCESS_KEY_ID'),
        ('secret_access_key', 'NOTIFICATION_HUB_SQS_SECRET_ACCESS_KEY'),
        ('region', 'NOTIFICATION_HUB_SQS_REGION'),
        ('queue_name', 'NOTIFICATION_HUB_SQS_QUEUE_NAME'),  # transactional queue name
        ('marketing_queue_name', 'NOTIFICATION_HUB_MARKETING_SQS_QUEUE_NAME'), # marketing queue name
        ('otp_queue_name', 'NOTIFICATION_HUB_OTP_SQS_QUEUE_NAME'), # otp queue name
        ('eks_role_arn', 'EKS_ROLE_ARN'),  # for EKS role-based access; to push msgs to SQS
    )

    def __init__(self, **kwargs):
        # Retrieve Settings
        self.access_key_id = self._get_setting(*self.setting_keys[0], **kwargs)
        self.secret_access_key = self._get_setting(*self.setting_keys[1], **kwargs)
        self.region = self._get_setting(*self.setting_keys[2], **kwargs)
        self.queue_name = self._get_setting(*self.setting_keys[3], **kwargs)
        self.marketing_queue_name = self._get_setting(*self.setting_keys[4], **kwargs)
        self.otp_queue_name = self._get_setting(*self.setting_keys[5], **kwargs)
        self.eks_role_arn = self._get_setting(*self.setting_keys[6], **kwargs)

        # check whether at least one queue is set or not
        if (self.queue_name is None or self.queue_name == "") and \
            (self.marketing_queue_name is None or self.marketing_queue_name == "") and \
                (self.otp_queue_name is None or self.otp_queue_name == ""):
            raise ImproperlyConfigured('At least one queue should be set.')

        self._session = None
        self._queue = None
        self.init_sqs_session(kwargs.get('endpoint_url'))


    def _get_setting(self, kw_name, env_name, **kwargs):
        """
        To read the setting from django settings or env
        :param kw_name: setting value to be retrived
        :param env_name: kw
        :return: Setting Value retrieved from the django setting or env
        """
        value = ""
        if kwargs.get(kw_name):
            return kwargs[kw_name]
        value = self.__get_from_django_settings(env_name)
        # If not found in Django settings, retrieve from environment variables
        if not value:
            value = os.getenv(env_name)

        return value

    @staticmethod
    def __get_from_django_settings(name):
        """
        If the Django project is initiated, then retrieves the settings
        from Django settings
        :param name: Setting Name
        :return: Setting Value
        """
        try:
            module = importlib.import_module('django.conf')
            settings = getattr(module, 'settings')
            return getattr(settings, name, None)
        except ImportError:
            return None

    def init_sqs_session(self, endpoint_url=None):
        """
        creates aws session based on different criteria
        - Access key and secret key given in the settings
        - EC2: based on the assumption that the role is given to the EC2 instance
        - EKS-role based access: eks_role_arn is taken into consideration
        - Local settings: read from the local ~/.aws/credentials path
        """
        if endpoint_url:
            client_kwargs['endpoint_url'] = endpoint_url

        session_created = False
        
        # Access key and secret key given in the settings
        if self.access_key_id and self.secret_access_key:
            client_kwargs = {
                'service_name': "sqs",
                'aws_access_key_id': self.access_key_id,
                'aws_secret_access_key': self.secret_access_key,
                'region_name': self.region
            }
            self._session = boto3.resource(**client_kwargs)
            if self._session is not None:
                session_created = True

        # EC2: based on the assumption that the role is given to the EC2 instance
        if self._session is None and not session_created:
            client_kwargs = {
                'service_name': "sqs",
                'region_name': self.region
            }
            self._session = boto3.resource(**client_kwargs)
            if self._session is not None:
                session_created = True

        # eks role-based access
        if self.eks_role_arn and self.eks_role_arn != "":
            # check whether the given information has the account number or not
            aws_client = boto3.client('sts')
            if aws_client == None or aws_client == "":
                raise ImproperlyConfigured('Issue while connecting to SQS region `{}`'.format(self.region))

            try:
                if not path.exists(TOKEN_PATH):
                    raise ImproperlyConfigured('Token not present in pod. Check token at `{}`'.format(TOKEN_PATH))
                with open(TOKEN_PATH, 'r') as file:
                    access_details = file.read()
                response = aws_client.assume_role_with_web_identity(
                    RoleArn=self.eks_role_arn,
                    RoleSessionName='string',
                    WebIdentityToken=access_details,
                )
                if not response:
                    raise ImproperlyConfigured('Issue with token in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self.eks_role_arn))
                session_created = True
            except ImportError:
                raise ImproperlyConfigured('Token not present in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self.eks_role_arn))
        
        # local development
        if self._session is None and not session_created:
            self._session = boto3.resource("sqs")
            if self._session is not None:
                session_created = True

        # check whether session is created after all possible options
        if not session_created:
            raise ImproperlyConfigured('AWS session is not created due to improper setting provided in region `{}`'.format(self.region))

    def send_message(self, message_body: str, message_type: MessageType) -> str:
        """
        Sends a message to Amazon SQS
        :param message_body: The message to be pushed to queue
        :param message_type: The type of message to be processed. This is used to identify the queue
        :returns The MessageId returned by AWS
        :raises ConnectionError if failure in sending occurs
        """
        queue_name = self.queue_name
        if message_type == MessageType.MARKETING:
            queue_name = self.marketing_queue_name
        elif message_type == MessageType.TRANSACTIONAL:
            queue_name = self.queue_name
        elif message_type == MessageType.OTP:
            queue_name = self.otp_queue_name

        self._queue = self._session.get_queue_by_name(QueueName=queue_name)
        res = self._queue.send_message(QueueUrl=self._queue.url, MessageBody=str(message_body))
        status_code = res.get('ResponseMetadata').get('HTTPStatusCode')
        if status_code / 100 != 2:
            raise ConnectionError('Failed to send message to Hub Queue')
        return res['MessageId']
