# -*- coding: utf-8 -*-
#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.
#
import boto3
import json
import typing
from boto3.session import ResourceNotExistsError
from botocore.exceptions import ClientError
from os.path import join
from ask_sdk_core.attributes_manager import AbstractPersistenceAdapter
from ask_sdk_core.exceptions import PersistenceException

from .object_keygen import user_id_keygen

if typing.TYPE_CHECKING:
    from typing import Callable, Dict
    from ask_sdk_model import RequestEnvelope
    from boto3.resources.base import ServiceResource


class S3Adapter(AbstractPersistenceAdapter):
    """Persistence Adapter implementation using AmazonS3.

    Amazon S3 based persistence adapter implementation. This
    internally uses the AWS Python SDK (`boto3`) to process
    the s3 operations.

    :param bucket_name: S3 bucket name to be used.
    :type bucket_name: str
    :param path_prefix: S3 path prefix
    :type path_prefix: str
    :param s3_client: S3 Client to be used. Defaulted to the s3 client generated from boto3.
    :type s3_client: boto3.client
    :param object_keygen: Callable function that takes a request envelope and
        provides a unique key value.
        Defaulted to user id keygen function.
    :type object_keygen: Callable[[ask_sdk_model.request_envelope.RequestEnvelope], str]
    """
    DEFAULT_PATH_PREFIX = ''
    S3_CLIENT_NAME = 's3'
    S3_OBJECT_BODY_NAME = 'Body'

    def __init__(self, bucket_name, path_prefix=None, s3_client=None, object_keygen=user_id_keygen):
        self.bucket_name = bucket_name
        if not path_prefix:
            self.path_prefix = self.DEFAULT_PATH_PREFIX
        else:
            self.path_prefix = path_prefix
        self.s3_client = s3_client
        if not s3_client:
            self.s3_client = boto3.client(self.S3_CLIENT_NAME)
        else:
            self.s3_client = s3_client
        self.object_keygen = object_keygen

    def get_attributes(self, request_envelope):
        # type: (RequestEnvelope) -> Dict[str, object]
        """Retrieves the attributes from s3 bucket.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
        :return: attributes in the s3 bucket
        :rtype: Dict[str, object]
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        obj_id = self.__get_object_id(request_envelope)
        try:
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj_id)
        except ResourceNotExistsError:
            raise PersistenceException("Failed to get attributes from s3 bucket {}."
                                       "Resource does not exist".format(self.bucket_name))
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return {}
            raise PersistenceException("Failed to get attributes from s3 bucket. "
                                       "Exception of type {} occurred: {}".format(type(ex).__name__, str(ex)))
        try:
            body = obj.get(self.S3_OBJECT_BODY_NAME)
            if not body:
                return {}
            attributes = json.loads(body.read())
            return attributes
        except Exception as e:
            raise PersistenceException("Failed to get attributes from s3 bucket. "
                                       "Exception of type {} occurred: {}".format(type(e).__name__, str(e)))

    def save_attributes(self, request_envelope, attributes):
        # type: (RequestEnvelope, Dict[str, object]) -> None
        """Saves attributes to the s3 bucket.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
        :param attributes: attributes to store in s3
        :type attributes: Dict[str, object]
        :rtype: None
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        obj_id = self.__get_object_id(request_envelope)
        json_data = json.dumps(attributes)
        try:
            self.s3_client.put_object(Body=json_data, Bucket=self.bucket_name, Key=obj_id)
        except ResourceNotExistsError:
            raise PersistenceException("Failed to save attributes to s3 bucket {}."
                                       "Resource does not exist".format(self.bucket_name))
        except Exception as e:
            raise PersistenceException("Failed to save attributes to s3 bucket. "
                                       "Exception of type {} occurred: {}".format(type(e).__name__, str(e)))

    def delete_attributes(self, request_envelope):
        # type: (RequestEnvelope) -> None
        """Deletes attributes from s3 bucket.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
        :rtype: None
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        obj_id = self.__get_object_id(request_envelope)
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=obj_id)
        except ResourceNotExistsError:
            raise PersistenceException("Failed to delete attributes from s3 bucket {}."
                                       "Resource does not exist".format(self.bucket_name))
        except Exception as e:
            raise PersistenceException("Failed to delete attributes from s3 bucket. "
                                       "Exception of type {} occurred: {}".format(type(e).__name__, str(e)))

    def __get_object_id(self, request_envelope):
        """ Joins the path prefix and the object_id.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
        :rtype: str
        """
        return join(self.path_prefix, self.object_keygen(request_envelope))
