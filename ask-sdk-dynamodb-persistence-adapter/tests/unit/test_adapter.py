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
import unittest

from boto3.exceptions import ResourceNotExistsError
from ask_sdk_model import RequestEnvelope
from ask_sdk_core.exceptions import PersistenceException
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

try:
    import mock
except ImportError:
    from unittest import mock


class ResourceInUseException(Exception):
    pass


class TestDynamoDbAdapter(unittest.TestCase):
    def setUp(self):
        self.dynamodb_resource = mock.Mock()
        self.partition_keygen = mock.Mock()
        self.request_envelope = RequestEnvelope()
        self.expected_key_schema = [{'AttributeName': 'id', 'KeyType': 'HASH'}]
        self.expected_attribute_definitions = [
            {'AttributeName': 'id', 'AttributeType': 'S'}]
        self.expected_provision_throughput = {
            'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        self.attributes = {"test_key": "test_val"}

    def test_get_attributes_from_existing_table(self):
        mock_table = mock.Mock()
        mock_table.get_item.return_value = {
            "Item": {"attributes": self.attributes}}
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        assert test_dynamodb_adapter.get_attributes(
            request_envelope=self.request_envelope) == self.attributes, (
            "Get attributes from dynamodb table retrieves wrong values")
        self.dynamodb_resource.Table.assert_called_once_with("test_table"), (
            "Existing table name passed incorrectly to dynamodb get "
            "table call")
        self.partition_keygen.assert_called_once_with(self.request_envelope), (
            "Partition Keygen provided incorrect input parameters during get "
            "attributes call")
        mock_table.get_item.assert_called_once_with(
            Key={"id": "test_partition_key"}, ConsistentRead=True), (
            "Partition keygen provided incorrect key for get attributes call")

    def test_get_attributes_from_existing_table_custom_key_name_attribute_name(self):
        mock_table = mock.Mock()
        mock_table.get_item.return_value = {
            "Item": {"custom_attr": self.attributes}}
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource,
            partition_key_name="custom_key", attribute_name="custom_attr")

        assert test_dynamodb_adapter.get_attributes(
            request_envelope=self.request_envelope) == self.attributes, (
            "Get attributes from dynamodb table retrieves wrong values when "
            "custom partition key name and "
            "custom attribute name passed")
        self.dynamodb_resource.Table.assert_called_once_with("test_table"), (
            "Existing table name passed incorrectly to dynamodb get table "
            "call")
        self.partition_keygen.assert_called_once_with(self.request_envelope), (
            "Partition Keygen provided incorrect input parameters during get "
            "item call")
        mock_table.get_item.assert_called_once_with(
            Key={"custom_key": "test_partition_key"}, ConsistentRead=True), (
            "Partition keygen provided incorrect key for get attributes call")

    def test_get_attributes_from_existing_table_get_item_fails(self):
        mock_table = mock.Mock()
        mock_table.get_item.side_effect = Exception("test exception")
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.get_attributes(
                request_envelope=self.request_envelope)

        assert "Failed to retrieve attributes from DynamoDb table" in str(
            exc.exception), (
            "Get attributes didn't raise Persistence Exception when get item "
            "failed on dynamodb resource")
        mock_table.get_item.assert_called_once_with(
            Key={"id": "test_partition_key"}, ConsistentRead=True), (
            "Partition keygen provided incorrect key for get attributes call")

    def test_get_attributes_from_existing_table_get_item_returns_no_item(self):
        mock_table = mock.Mock()
        mock_table.get_item.return_value = {"attributes": self.attributes}
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        assert test_dynamodb_adapter.get_attributes(
            request_envelope=self.request_envelope) == {}, (
            "Get attributes returns incorrect response when no item is "
            "present in dynamodb table for provided key")

    def test_get_attributes_fails_with_no_existing_table_create_table_default_false(self):
        self.dynamodb_resource.Table.side_effect = ResourceNotExistsError(
            "test", "test", "test")
        self.dynamodb_resource.create_table.return_value = "test"
        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.get_attributes(
                request_envelope=self.request_envelope)

        assert "DynamoDb table test_table doesn't exist" in str(
            exc.exception), (
            "Get attributes didn't raise Persistence Exception when no "
            "existing table and create table set as false")
        self.dynamodb_resource.create_table.assert_not_called(), (
            "Create table called on dynamodb resource when create_table "
            "flag is set as False")

    def test_save_attributes_to_existing_table(self):
        mock_table = mock.Mock()
        mock_table.put_item.return_value = True
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        try:
            test_dynamodb_adapter.save_attributes(
                request_envelope=self.request_envelope, attributes=self.attributes)
        except:
            # Should not reach here
            raise Exception("Save attributes failed on existing table")

        self.dynamodb_resource.Table.assert_called_once_with("test_table"), (
            "Existing table name passed incorrectly to dynamodb get table "
            "call")
        self.partition_keygen.assert_called_once_with(
            self.request_envelope), (
            "Partition Keygen provided incorrect input parameters during "
            "save attributes call")
        mock_table.put_item.assert_called_once_with(
            Item={"id": "test_partition_key", "attributes":
                self.attributes}), (
            "Partition keygen provided incorrect partition key in item for "
            "save attributes call")

    def test_save_attributes_to_existing_table_custom_key_name_attribute_name(self):
        mock_table = mock.Mock()
        mock_table.put_item.return_value = True
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource,
            partition_key_name="custom_key", attribute_name="custom_attr")

        try:
            test_dynamodb_adapter.save_attributes(
                request_envelope=self.request_envelope,
                attributes=self.attributes)
        except:
            # Should not reach here
            raise Exception(
                "Save attributes failed on existing table when custom "
                "partition key name and custom attribute "
                "name passed")

        self.dynamodb_resource.Table.assert_called_once_with("test_table"), (
            "Existing table name passed incorrectly to dynamodb get table call")
        self.partition_keygen.assert_called_once_with(
            self.request_envelope), (
            "Partition Keygen provided incorrect input parameters during "
            "save attributes call")
        mock_table.put_item.assert_called_once_with(
            Item={"custom_key": "test_partition_key", "custom_attr":
                self.attributes}), (
            "Partition keygen provided incorrect partition key in item for "
            "save attributes call")

    def test_save_attributes_to_existing_table_put_item_fails(self):
        mock_table = mock.Mock()
        mock_table.put_item.side_effect = ValueError("test exception")
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.save_attributes(
                request_envelope=self.request_envelope,
                attributes=self.attributes)

        assert ("Failed to save attributes to DynamoDb table. "
                "Exception of type ValueError occurred: test "
                "exception") in str(exc.exception), (
            "Save attributes didn't raise Persistence Exception when put item "
            "failed on dynamodb resource")
        mock_table.put_item.assert_called_once_with(
            Item={"id": "test_partition_key", "attributes":
                self.attributes}), (
            "DynamoDb Put item called with incorrect parameters")

    def test_save_attributes_fails_with_no_existing_table(self):
        self.dynamodb_resource.Table.side_effect = ResourceNotExistsError(
            "test", "test", "test")
        self.dynamodb_resource.create_table.return_value = "test"
        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.save_attributes(
                request_envelope=self.request_envelope, attributes=self.attributes)

        assert "DynamoDb table test_table doesn't exist" in str(
            exc.exception), (
            "Save attributes didn't raise Persistence Exception when no "
            "existing table and create table set as false")
        self.dynamodb_resource.create_table.assert_not_called(), (
            "Create table called on dynamodb resource when create_table flag "
            "is set as False")

    def test_existence_check_not_done_if_flag_not_set(self):
        self.dynamodb_resource.Table.side_effect = Exception(
            "Invalid call to get table")
        self.dynamodb_resource.create_table.side_effect = Exception(
            "Invalid call to create table")

        DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource,
            create_table=False)

        self.dynamodb_resource.create_table.assert_not_called(), (
            "Create table called when create_table flag is not set, during "
            "Adapter initialization")

    def test_create_table_doesnt_raise_exception_if_flag_set_existing_table(self):
        self.dynamodb_resource.create_table.side_effect = \
            ResourceInUseException("Invalid call to create table")

        DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource,
            create_table=True)

        self.dynamodb_resource.create_table.assert_called_once(), (
            "Create table called when create_table flag is set "
            "during Adapter initialization and resource already exists")

    def test_catch_get_table_exception_if_flag_set(self):
        self.dynamodb_resource.create_table.side_effect = ValueError(
            "Invalid call to create table")

        with self.assertRaises(PersistenceException) as exc:
            DynamoDbAdapter(
                table_name="test_table",
                partition_keygen=self.partition_keygen,
                dynamodb_resource=self.dynamodb_resource, create_table=True)

        assert (
            "Create table if not exists request failed: Exception of type "
            "ValueError occurred: "
            "Invalid call to create table") in str(exc.exception), (
            "create table if not exists didn't raise exception when "
            "create_table flag is set and create table "
            "resource raises exception")

    def test_delete_attributes_to_existing_table(self):
        mock_table = mock.Mock()
        mock_table.delete_item.return_value = True
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        try:
            test_dynamodb_adapter.delete_attributes(
                request_envelope=self.request_envelope)
        except:
            # Should not reach here
            raise Exception("Delete attributes failed on existing table")

        self.dynamodb_resource.Table.assert_called_once_with("test_table"), (
            "Existing table name passed incorrectly to dynamodb get table "
            "call")
        self.partition_keygen.assert_called_once_with(
            self.request_envelope), (
            "Partition Keygen provided incorrect input parameters during "
            "delete attributes call")
        mock_table.delete_item.assert_called_once_with(
            Key={"id": "test_partition_key"}), (
            "Partition keygen provided incorrect partition key in item for "
            "delete attributes call")

    def test_delete_attributes_to_existing_table_delete_item_fails(self):
        mock_table = mock.Mock()
        mock_table.delete_item.side_effect = ValueError("test exception")
        self.dynamodb_resource.Table.return_value = mock_table
        self.partition_keygen.return_value = "test_partition_key"

        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.delete_attributes(
                request_envelope=self.request_envelope)

        assert ("test exception") in str(exc.exception), (
            "Delete attributes didn't raise Persistence Exception when delete item "
            "failed on dynamodb resource")
        mock_table.delete_item.assert_called_once_with(
            Key={"id": "test_partition_key"}), (
            "DynamoDb Delete item called with incorrect parameters")

    def test_delete_attributes_fails_with_no_existing_table(self):
        self.dynamodb_resource.Table.side_effect = ResourceNotExistsError(
            "test", "test", "test")
        self.dynamodb_resource.create_table.return_value = "test"
        test_dynamodb_adapter = DynamoDbAdapter(
            table_name="test_table", partition_keygen=self.partition_keygen,
            dynamodb_resource=self.dynamodb_resource)

        with self.assertRaises(PersistenceException) as exc:
            test_dynamodb_adapter.delete_attributes(
                request_envelope=self.request_envelope)

        assert "DynamoDb table test_table doesn't exist" in str(
            exc.exception), (
            "Delete attributes didn't raise Persistence Exception when no "
            "existing table and create table set as false")
        self.dynamodb_resource.create_table.assert_not_called(), (
            "Create table called on dynamodb resource when create_table flag "
            "is set as False")

    def tearDown(self):
        self.dynamodb_resource = None
        self.partition_keygen = None
        self.request_envelope = None
        self.expected_key_schema = None
        self.expected_attribute_definitions = None
        self.expected_provision_throughput = None
        self.attributes = None
