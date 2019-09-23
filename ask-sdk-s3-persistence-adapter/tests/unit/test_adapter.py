import unittest

import json
import os
from boto3.exceptions import ResourceNotExistsError
from ask_sdk_model import RequestEnvelope
from ask_sdk_core.exceptions import PersistenceException
from ask_sdk_s3.adapter import S3Adapter

try:
    import mock
except ImportError:
    from unittest import mock

_MOCK_DATA = {"key1": "value1", "key2": "value2", "key3": "1.1"}


class TestS3Adapter(unittest.TestCase):
    def setUp(self):
        self.s3_client = mock.Mock()
        self.object_keygen = mock.Mock()
        self.request_envelope = RequestEnvelope()
        self.bucket_name = "test_bucket"
        self.bucket_key = "test_key"

    def test_get_attributes_from_existing_bucket(self):
        self.object_keygen.return_value = "test_object_key"
        mock_object = {"Body": MockData()}
        self.s3_client.get_object = mock.MagicMock(return_value=mock_object)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        result = test_s3_adapter.get_attributes(request_envelope=self.request_envelope)

        self.assertEquals(_MOCK_DATA, result)
        self.s3_client.get_object.assert_called()

    def test_get_attributes_from_existing_bucket_no_prefix(self):
        self.object_keygen.return_value = "test_object_key"
        mock_object = {"Body": MockData()}
        self.s3_client.get_object = mock.MagicMock(return_value=mock_object)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=None,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        result = test_s3_adapter.get_attributes(request_envelope=self.request_envelope)

        self.assertEquals(_MOCK_DATA, result)
        self.s3_client.get_object.assert_called()

    def test_get_attributes_from_existing_bucket_get_object_fails(self):
        self.object_keygen.return_value = "test_object_key"
        self.s3_client.get_object.read.side_effect = Exception("test exception")

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.get_attributes(request_envelope=self.request_envelope)

    def test_get_attributes_resource_not_exist_fails(self):
        self.object_keygen.return_value = "test_object_key"
        self.s3_client.get_object.side_effect = ResourceNotExistsError("resource does not exist",
                                                                       self.bucket_key, self.bucket_name)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.get_attributes(request_envelope=self.request_envelope)

    def test_get_attributes_from_existing_bucket_get_object_returns_no_item(self):
        self.object_keygen.return_value = "test_object_key"
        mock_object = {"Body": {}}
        self.s3_client.get_object = mock.MagicMock(return_value=mock_object)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        result = test_s3_adapter.get_attributes(request_envelope=self.request_envelope)
        self.assertEquals({}, result)

    def test_get_attributes_from_existing_bucket_get_object_null_returns_no_item(self):
        self.object_keygen.return_value = "test_object_key"
        mock_object = {"Body": None}
        self.s3_client.get_object = mock.MagicMock(return_value=mock_object)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        result = test_s3_adapter.get_attributes(request_envelope=self.request_envelope)
        self.assertEquals({}, result)

    def test_get_attributes_from_existing_bucket_get_object_invalid_json_fails(self):
        self.object_keygen.return_value = "test_object_key"
        mock_object = {"Body": MockMalformedData()}
        self.s3_client.get_object = mock.MagicMock(return_value=mock_object)

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.get_attributes(request_envelope=self.request_envelope)

    def test_save_attributes_to_existing_bucket(self):
        self.object_keygen.return_value = "test_object_key"
        json_data = json.dumps(_MOCK_DATA)
        generated_key = os.path.join("test_key", "test_object_key")

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        test_s3_adapter.save_attributes(request_envelope=self.request_envelope, attributes=_MOCK_DATA)

        self.object_keygen.assert_called_once_with(self.request_envelope)
        self.s3_client.put_object.assert_called_once_with(Body=json_data,
                                                          Bucket=self.bucket_name,
                                                          Key=generated_key)

    def test_save_attributes_to_existing_bucket_put_item_fails(self):
        self.object_keygen.return_value = "test_object_key"
        self.s3_client.put_object.side_effect = Exception("test exception")

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.save_attributes(request_envelope=self.request_envelope, attributes=_MOCK_DATA)

    def test_save_attributes_fails_with_no_existing_bucket(self):
        self.object_keygen.return_value = "test_object_key"

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        self.s3_client.put_object.side_effect = ResourceNotExistsError("resource does not exist",
                                                                       self.bucket_key, self.bucket_name)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.save_attributes(request_envelope=self.request_envelope, attributes=_MOCK_DATA)

    def test_delete_attributes_to_existing_bucket(self):
        self.object_keygen.return_value = "test_object_key"

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        test_s3_adapter.delete_attributes(request_envelope=self.request_envelope)

        self.object_keygen.assert_called_once_with(self.request_envelope)
        self.s3_client.delete_object.assert_called_once_with(
                                                          Bucket=self.bucket_name,
                                                          Key=os.path.join("test_key", "test_object_key"))

    def test_delete_attributes_to_existing_bucket_delete_object_fails(self):
        self.object_keygen.return_value = "test_object_key"
        self.s3_client.delete_object.side_effect = Exception("test exception")

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.delete_attributes(request_envelope=self.request_envelope)

    def test_delete_attributes_fails_with_no_existing_bucket(self):
        self.object_keygen.return_value = "test_object_key"

        test_s3_adapter = S3Adapter(bucket_name=self.bucket_name, path_prefix=self.bucket_key,
                                    s3_client=self.s3_client, object_keygen=self.object_keygen)
        self.s3_client.delete_object.side_effect = ResourceNotExistsError("resource does not exist",
                                                                          self.bucket_key, self.bucket_name)

        with self.assertRaises(PersistenceException) as exc:
            test_s3_adapter.delete_attributes(request_envelope=self.request_envelope)

    def tearDown(self):
        self.s3_client = None
        self.object_keygen = None
        self.request_envelope = None
        self.bucket_name = None
        self.bucket_key = None


class MockData:
    def read(self):
        return json.dumps(_MOCK_DATA)


class MockMalformedData:
    def read(self):
        return json.dumps({"malformed json\n"})