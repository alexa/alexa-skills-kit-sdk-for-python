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
import datetime
import decimal

from six import PY3
from mock import patch

from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.exceptions import SerializationException

from . import data

if PY3:
    from unittest import mock
    unicode_type = str
    long_type = int
else:
    import mock
    unicode_type = unicode
    long_type = long


class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.test_serializer = DefaultSerializer()

    def test_none_obj_serialization(self):
        test_obj = None
        assert self.test_serializer.serialize(test_obj) is None, \
            "Default Serializer serialized None object incorrectly"

    def test_primitive_obj_serialization(self):
        test_obj = "test"
        assert self.test_serializer.serialize(test_obj) == test_obj, \
            "Default Serializer serialized str object incorrectly"

        test_obj = 123
        assert self.test_serializer.serialize(test_obj) == test_obj, \
            "Default Serializer serialized int object incorrectly"

        test_obj = u"test"
        assert self.test_serializer.serialize(test_obj) == test_obj, \
            "Default Serializer serialized unicode object incorrectly"

        test_obj = b"test"
        assert self.test_serializer.serialize(test_obj) == test_obj, \
            "Default Serializer serialized bytes object incorrectly"

        test_obj = False
        assert self.test_serializer.serialize(test_obj) == test_obj, \
            "Default Serializer serialized bool object incorrectly"

    def test_list_obj_serialization(self):
        test_obj_inst = data.ModelTestObject2(int_var=123)
        test_list_obj = ["test", 123, test_obj_inst]

        expected_list = ["test", 123, {"var4Int": 123}]
        assert self.test_serializer.serialize(test_list_obj) == expected_list, \
            "Default Serializer serialized list object incorrectly"

    def test_tuple_obj_serialization(self):
        test_obj_inst = data.ModelTestObject2(int_var=123)
        test_tuple_obj = ("test", 123, test_obj_inst)

        expected_tuple = ("test", 123, {"var4Int": 123})
        assert self.test_serializer.serialize(test_tuple_obj) == expected_tuple, \
            "Default Serializer serialized tuple object incorrectly"

    def test_datetime_obj_serialization(self):
        test_obj = datetime.datetime(2018, 1, 1, 10, 20, 30)
        expected_datetime = "2018-01-01T10:20:30"
        assert self.test_serializer.serialize(test_obj) == expected_datetime, \
            "Default Serializer serialized datetime object incorrectly"

    def test_date_obj_serialization(self):
        test_obj = datetime.date(2018, 1, 1)
        expected_date = "2018-01-01"
        assert self.test_serializer.serialize(test_obj) == expected_date, \
            "Default Serializer serialized datetime object incorrectly"

    def test_dict_obj_serialization(self):
        test_obj_inst = data.ModelTestObject2(int_var=123)
        test_dict_obj = {
            "test_str": "test",
            "test_int": 123,
            "test_obj": test_obj_inst
        }

        expected_dict = {
            "test_str": "test",
            "test_obj": {
                "var4Int": 123
            },
            "test_int": 123,
        }
        assert self.test_serializer.serialize(test_dict_obj) == expected_dict, \
            "Default Serializer serialized dict object incorrectly"

    def test_model_obj_serialization(self):
        test_model_obj_2 = data.ModelTestObject2(int_var=123)
        test_model_obj_1 = data.ModelTestObject1(
            str_var="test", datetime_var=datetime.datetime(
                2018, 1, 1, 10, 20, 30), obj_var=test_model_obj_2)

        expected_serialized_obj = {
            "var1": "test",
            "var2Time": "2018-01-01T10:20:30",
            "var3Object": {
                "var4Int": 123
            }
        }
        assert self.test_serializer.serialize(test_model_obj_1) == expected_serialized_obj, \
            "Default Serializer serialized model object incorrectly"

    def test_enum_obj_serialization(self):
        test_model_obj_2 = data.ModelTestObject2(int_var=123)
        test_enum_obj = data.ModelEnumObject("ENUM_VAL_1")
        test_model_obj_1 = data.ModelTestObject1(
            str_var="test", datetime_var=datetime.datetime(
                2018, 1, 1, 10, 20, 30), obj_var=test_model_obj_2,
            enum_var=test_enum_obj)

        expected_serialized_obj = {
            "var1": "test",
            "var2Time": "2018-01-01T10:20:30",
            "var6Enum": "ENUM_VAL_1",
            "var3Object": {
                "var4Int": 123
            }
        }
        assert self.test_serializer.serialize(test_model_obj_1) == expected_serialized_obj, \
            "Default Serializer serialized enum object incorrectly"

    def test_decimal_obj_without_decimals_serialization(self):
        test_decimal_obj = decimal.Decimal(10)
        expected_obj = 10
        actual_obj = self.test_serializer.serialize(test_decimal_obj)

        assert actual_obj == expected_obj, (
            "Default Serializer serialized decimal object containing no "
            "decimals incorrectly")
        assert type(actual_obj) == int, (
            "Default Serializer serialized decimal object containing no "
            "decimals to incorrect type")

    def test_decimal_obj_with_decimals_serialization(self):
        test_decimal_obj = decimal.Decimal(10.5)
        expected_obj = 10.5
        actual_obj = self.test_serializer.serialize(test_decimal_obj)

        assert actual_obj == expected_obj, (
            "Default Serializer serialized decimal object containing "
            "decimals incorrectly")
        assert type(actual_obj) == float, (
            "Default Serializer serialized decimal object containing "
            "decimals to incorrect type")


class TestDeserialization(unittest.TestCase):
    def setUp(self):
        self.test_serializer = DefaultSerializer()

    def test_none_obj_deserialization(self):
        test_payload = None
        test_obj_type = str
        assert self.test_serializer.deserialize(
            test_payload, test_obj_type) is None, \
            "Default Serializer deserialized None object incorrectly"

    def test_str_obj_deserialization(self):
        test_payload = "test"
        test_obj_type = str
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, \
                "Default Serializer deserialized string object incorrectly"

    def test_unicode_obj_deserialization(self):
        test_payload = u"√"
        test_obj_type = unicode_type
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == u"\u221a", \
                "Default Serializer deserialized unicode string object incorrectly"

    def test_int_obj_deserialization(self):
        test_payload = 123
        test_obj_type = int
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, \
                "Default Serializer deserialized int object incorrectly"

    def test_long_obj_deserialization(self):
        test_payload = 123
        test_obj_type = long_type
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == long_type(test_payload), \
                "Default Serializer deserialized long object incorrectly"

    def test_primitive_obj_deserialization_raising_unicode_exception(self):
        test_serializer = DefaultSerializer()
        mocked_primitive_type = mock.Mock(
            side_effect=UnicodeEncodeError('hitchhiker', u"", 42, 43, 'the universe and everything else'))

        test_serializer.PRIMITIVE_TYPES = [mocked_primitive_type]

        test_payload = u"√"
        test_obj_type = mocked_primitive_type
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert test_serializer.deserialize(
                test_payload, test_obj_type) == u"\u221a", \
                "Default Serializer deserialized primitive type which raises UnicodeEncodeError incorrectly"

    def test_primitive_obj_deserialization_raising_type_error(self):
        test_serializer = DefaultSerializer()
        mocked_primitive_type = mock.Mock(side_effect=TypeError())

        test_serializer.PRIMITIVE_TYPES = [mocked_primitive_type]

        test_payload = "test"
        test_obj_type = mocked_primitive_type
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, \
                "Default Serializer deserialized primitive type which raises TypeError incorrectly"

    def test_primitive_obj_deserialization_raising_value_error(self):
        test_payload = "test"
        test_obj_type = int

        with self.assertRaises(SerializationException) as exc:
            with patch("json.loads") as mock_json_loader:
                mock_json_loader.return_value = test_payload
                self.test_serializer.deserialize(test_payload, test_obj_type)

        assert "Failed to parse test into 'int' object" in str(exc.exception), \
            "Default Serializer didn't throw SerializationException when invalid primitive type is deserialized"

    def test_datetime_obj_serialization(self):
        # payload in iso8601 format
        test_payload = "2018-01-01T10:20:30"
        test_obj_type = datetime.datetime

        expected_obj = datetime.datetime(2018, 1, 1, 10, 20, 30)
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(test_payload, test_obj_type) == expected_obj, \
                "Default Serializer deserialized datetime object incorrectly"

    def test_date_obj_serialization(self):
        # payload in iso8601 format
        test_payload = "2018-01-01"
        test_obj_type = datetime.date

        expected_obj = datetime.date(2018, 1, 1)
        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(test_payload, test_obj_type) == expected_obj, \
                "Default Serializer deserialized date object incorrectly"

    def test_datetime_obj_deserialization_raising_value_error(self):
        test_payload = "abc-wx-yzT25:80:90"
        test_obj_type = datetime.datetime

        with self.assertRaises(SerializationException) as exc:
            with patch("json.loads") as mock_json_loader:
                mock_json_loader.return_value = test_payload
                self.test_serializer.deserialize(test_payload, test_obj_type)

        assert "Failed to parse abc-wx-yzT25:80:90 into 'datetime' object" in str(exc.exception), \
            "Default Serializer didn't throw SerializationException when invalid datetime type is deserialized"

    def test_datetime_obj_deserialization_raising_import_error(self):
        test_payload = "abc-wx-yzT25:80:90"
        test_obj_type = datetime.datetime

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            with mock.patch('dateutil.parser.parse') as parse_class:
                parse_class.side_effect = ImportError
                assert self.test_serializer.deserialize(
                    test_payload, test_obj_type) == test_payload, \
                    "Default Serializer didn't return datetime correctly for import errors"
                parse_class.assert_called_once_with(test_payload)

    def test_obj_type_deserialization(self):
        test_payload = "test"
        test_obj_type = object

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, \
                "Default Serializer deserialization of object returned other than the object itself"

    def test_native_type_mapping_deserialization(self):
        test_payload = "test"
        test_obj_type = "str"

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, (
                "Default Serializer deserialization of object with object_type of string class under native mapping "
                "not deserialized correctly")

    def test_polymorphic_list_obj_deserialization(self):
        test_payload = ["test", 123, "2018-01-01T10:20:30"]
        test_obj_type = "list[str, long, datetime]"

        deserialized_datetime_obj = datetime.datetime(2018, 1, 1, 10, 20, 30)
        expected_obj = ["test", 123, deserialized_datetime_obj]

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized list containing poly type object incorrectly")

    def test_similar_list_obj_deserialization(self):
        test_payload = ["test", "test1", "2018-01-01T10:20:30"]
        test_obj_type = "list[str]"
        expected_obj = ["test", "test1", "2018-01-01T10:20:30"]

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized list object containing similar type objects incorrectly")

    def test_dict_obj_deserialization(self):
        test_payload = {
            "test_key": ["test_val_1", "test_val_2"],
            "test_date_str": ["2018-01-01T10:20:30"]
        }
        test_obj_type = "dict(str, list[str])"

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, (
                "Default Serializer deserialized dict object incorrectly")

    def test_model_obj_deserialization(self):
        test_payload = {
            "var1": "test",
            "var2Time": "2018-01-01T10:20:30",
            "var3Object": {
                "var4Int": 123
            },
            "var6Enum": "ENUM_VAL_1"
        }
        test_obj_type = data.ModelTestObject1
        expected_datetime_obj = datetime.datetime(2018, 1, 1, 10, 20, 30)
        expected_sub_obj = data.ModelTestObject2(int_var=123)
        expected_enum_obj = data.ModelEnumObject("ENUM_VAL_1")
        expected_obj = data.ModelTestObject1(
            str_var="test", datetime_var=expected_datetime_obj, obj_var=expected_sub_obj, enum_var=expected_enum_obj)

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized model object incorrectly")

    def test_model_obj_with_additional_params_in_payload_deserialization(self):
        test_payload = {
            "var4Int": 123,
            "add_param_1": "Test"
        }
        test_obj_type = data.ModelTestObject2
        expected_obj = data.ModelTestObject2(int_var=123)
        expected_obj.add_param_1 = "Test"

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized model object incorrectly when payload has additional parameters")

    def test_invalid_model_obj_deserialization(self):
        test_payload = {
            "var_1": "some value"
        }
        test_obj_type = data.InvalidModelObject

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == test_payload, (
                "Default Serializer didn't provide payload back when an invalid model object type "
                "(without attribute map and swagger type dict) is passed")

    def test_invalid_model_obj_type_deserialization(self):
        test_payload = {
            "var_1": "some value"
        }
        test_obj_type = "InvalidModelObject"

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            with self.assertRaises(SerializationException) as exc:
                self.test_serializer.deserialize(test_payload, test_obj_type)

            assert "Unable to resolve class {} from installed modules".format(test_obj_type) in str(exc.exception), (
                "Default Serializer didn't throw SerializationException when deserialization is called with invalid "
                "object type")

    def test_invalid_json_deserialization(self):
        test_payload = {
            "var_1": "some value"
        }
        test_obj_type = "str"

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.side_effect = Exception
            with self.assertRaises(SerializationException) as exc:
                self.test_serializer.deserialize(test_payload, test_obj_type)

        assert "Couldn't parse response body" in str(exc.exception), \
            "Default Serializer didn't throw SerializationException when invalid json is deserialized"

    def test_parent_model_obj_with_discriminator_deserialization(self):
        test_payload = {
            "ChildType": 'ChildType1',
            "var1": "Some string",
            "var3Object": {
                "var4Int": 123
            },
            "testVar": "test string"
        }
        test_obj_type = data.ModelAbstractParentObject
        expected_sub_obj = data.ModelTestObject2(int_var=123)
        expected_obj = data.ModelChildObject1(
            str_var="Some string", obj_var=expected_sub_obj, test_var="test string")

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized model object incorrectly when object type is parent class "
                "with discriminator")

    def test_child_discriminator_model_obj_deserialization(self):
        test_payload = {
            "ChildType": 'ChildType2',
            "var1": "Some string",
            "var3Object": {
                "var4Int": 123
            },
            "testIntVar": 456
        }
        test_obj_type = data.ModelChildObject2
        expected_sub_obj = data.ModelTestObject2(int_var=123)
        expected_obj = data.ModelChildObject2(
            str_var="Some string", obj_var=expected_sub_obj, test_int_var=456)

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            assert self.test_serializer.deserialize(
                test_payload, test_obj_type) == expected_obj, (
                "Default Serializer deserialized model object incorrectly when object type is parent class "
                "with discriminator")

    def test_parent_model_obj_with_invalid_discriminator_deserialization(self):
        test_payload = {
            "ChildType": 'InvalidType',
            "var1": "Some string",
            "var3Object": {
                "var4Int": 123
            },
            "testVar": "test string"
        }
        test_obj_type = data.ModelAbstractParentObject

        with patch("json.loads") as mock_json_loader:
            mock_json_loader.return_value = test_payload
            with self.assertRaises(SerializationException) as exc:
                self.test_serializer.deserialize(test_payload, test_obj_type)

            assert "Couldn't resolve object by discriminator type" in str(exc.exception), (
                "Default Serializer didn't throw SerializationException when deserialization is called with invalid "
                "discriminator type in payload and parent model")
