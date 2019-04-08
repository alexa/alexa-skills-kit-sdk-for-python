# -*- coding: utf-8 -*-
#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights
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
import typing
from boto3.session import ResourceNotExistsError
from ask_sdk_core.attributes_manager import AbstractPersistenceAdapter
from ask_sdk_core.exceptions import PersistenceException

from .partition_keygen import user_id_partition_keygen

if typing.TYPE_CHECKING:
    from typing import Callable, Dict
    from ask_sdk_model import RequestEnvelope
    from boto3.resources.base import ServiceResource


class DynamoDbAdapter(AbstractPersistenceAdapter):
    """Persistence Adapter implementation using Amazon DynamoDb.

    Amazon DynamoDb based persistence adapter implementation. This
    internally uses the AWS Python SDK (`boto3`) to process the
    dynamodb operations. The adapter tries to create the table if
    ``create_table`` is set, during initialization.

    :param table_name: Name of the table to be created or used
    :type table_name: str
    :param partition_key_name: Partition key name to be used.
        Defaulted to 'id'
    :type partition_key_name: str
    :param attribute_name: Attribute name for storing and
        retrieving attributes from dynamodb.
        Defaulted to 'attributes'
    :type attribute_name: str
    :param create_table: Should the adapter try to create the table
        if it doesn't exist. Defaulted to False
    :type create_table: bool
    :param partition_keygen: Callable function that takes a
        request envelope and provides a unique partition key value.
        Defaulted to user id keygen function
    :type partition_keygen: Callable[[RequestEnvelope], str]
    :param dynamodb_resource: Resource to be used, to perform
        dynamo operations. Defaulted to resource generated from
        boto3
    :type dynamodb_resource: boto3.resources.base.ServiceResource
    """

    def __init__(
            self, table_name, partition_key_name="id",
            attribute_name="attributes", create_table=False,
            partition_keygen=user_id_partition_keygen,
            dynamodb_resource=boto3.resource("dynamodb")):
        # type: (str, str, str, bool, Callable[[RequestEnvelope], str], ServiceResource) -> None
        """Persistence Adapter implementation using Amazon DynamoDb.

        Amazon DynamoDb based persistence adapter implementation. This
        internally uses the AWS Python SDK (`boto3`) to process the
        dynamodb operations. The adapter tries to create the table if
        `create_table` is set, during initialization.

        :param table_name: Name of the table to be created or used
        :type table_name: str
        :param partition_key_name: Partition key name to be used.
            Defaulted to 'id'
        :type partition_key_name: str
        :param attribute_name: Attribute name for storing and
            retrieving attributes from dynamodb.
            Defaulted to 'attributes'
        :type attribute_name: str
        :param create_table: Should the adapter try to create the table
            if it doesn't exist. Defaulted to False
        :type create_table: bool
        :param partition_keygen: Callable function that takes a
            request envelope and provides a unique partition key value.
            Defaulted to user id keygen function
        :type partition_keygen: Callable[[RequestEnvelope], str]
        :param dynamodb_resource: Resource to be used, to perform
            dynamo operations. Defaulted to resource generated from
            boto3
        :type dynamodb_resource: boto3.resources.base.ServiceResource
        """
        self.table_name = table_name
        self.partition_key_name = partition_key_name
        self.attribute_name = attribute_name
        self.create_table = create_table
        self.partition_keygen = partition_keygen
        self.dynamodb = dynamodb_resource
        self.__create_table_if_not_exists()

    def get_attributes(self, request_envelope):
        # type: (RequestEnvelope) -> Dict[str, object]
        """Get attributes from table in Dynamodb resource.

        Retrieves the attributes from Dynamodb table. If the table
        doesn't exist, returns an empty dict if the
        ``create_table`` variable is set as True, else it raises
        PersistenceException. Raises PersistenceException if `get_item`
        fails on the table.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.RequestEnvelope
        :return: Attributes stored under the partition keygen mapping
            in the table
        :rtype: Dict[str, object]
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            partition_key_val = self.partition_keygen(request_envelope)
            response = table.get_item(
                Key={self.partition_key_name: partition_key_val},
                ConsistentRead=True)
            if "Item" in response:
                return response["Item"][self.attribute_name]
            else:
                return {}
        except ResourceNotExistsError:
            raise PersistenceException(
                "DynamoDb table {} doesn't exist or in the process of "
                "being created. Failed to get attributes from "
                "DynamoDb table.".format(self.table_name))
        except Exception as e:
            raise PersistenceException(
                "Failed to retrieve attributes from DynamoDb table. "
                "Exception of type {} occurred: {}".format(
                    type(e).__name__, str(e)))

    def save_attributes(self, request_envelope, attributes):
        # type: (RequestEnvelope, Dict[str, object]) -> None
        """Saves attributes to table in Dynamodb resource.

        Saves the attributes into Dynamodb table. Raises
        PersistenceException if table doesn't exist or ``put_item`` fails
        on the table.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.RequestEnvelope
        :param attributes: Attributes stored under the partition keygen
            mapping in the table
        :type attributes: Dict[str, object]
        :rtype: None
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            partition_key_val = self.partition_keygen(request_envelope)
            table.put_item(
                Item={self.partition_key_name: partition_key_val,
                      self.attribute_name: attributes})
        except ResourceNotExistsError:
            raise PersistenceException(
                "DynamoDb table {} doesn't exist. Failed to save attributes "
                "to DynamoDb table.".format(
                    self.table_name))
        except Exception as e:
            raise PersistenceException(
                "Failed to save attributes to DynamoDb table. Exception of "
                "type {} occurred: {}".format(
                    type(e).__name__, str(e)))

    def delete_attributes(self, request_envelope):
        # type: (RequestEnvelope) -> None
        """Deletes attributes from table in Dynamodb resource.

        Deletes the attributes from Dynamodb table. Raises
        PersistenceException if table doesn't exist or ``delete_item`` fails
        on the table.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.RequestEnvelope
        :rtype: None
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            partition_key_val = self.partition_keygen(request_envelope)
            table.delete_item(
                Key={self.partition_key_name: partition_key_val})
        except ResourceNotExistsError:
            raise PersistenceException(
                "DynamoDb table {} doesn't exist. Failed to delete attributes "
                "from DynamoDb table.".format(
                    self.table_name))
        except Exception as e:
            raise PersistenceException(
                "Failed to delete attributes in DynamoDb table. Exception of "
                "type {} occurred: {}".format(
                    type(e).__name__, str(e)))

    def __create_table_if_not_exists(self):
        # type: () -> None
        """Creates table in Dynamodb resource if it doesn't exist and
        create_table is set as True.

        :rtype: None
        :raises: PersistenceException: When `create_table` fails on
            dynamodb resource.
        """
        if self.create_table:
            try:
                self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': self.partition_key_name,
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': self.partition_key_name,
                            'AttributeType': 'S'
                        }

                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
            except Exception as e:
                if e.__class__.__name__ != "ResourceInUseException":
                    raise PersistenceException(
                        "Create table if not exists request "
                        "failed: Exception of type {} "
                        "occurred: {}".format(
                            type(e).__name__, str(e)))
