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
import base64
import unittest

from datetime import datetime, timedelta
from dateutil.tz import tzutc, tzlocal
from six.moves.urllib.parse import ParseResult
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from ask_sdk_model import RequestEnvelope, IntentRequest
from ask_sdk_webservice_support.verifier import (
    RequestVerifier, TimestampVerifier, VerificationException)
from ask_sdk_webservice_support.verifier_constants import (
    SIGNATURE_CERT_CHAIN_URL_HEADER, SIGNATURE_HEADER,
    CERT_CHAIN_DOMAIN, CHARACTER_ENCODING, MAX_TIMESTAMP_TOLERANCE_IN_MILLIS,
    DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS)

try:
    import mock
except ImportError:
    from unittest import mock


class TestRequestVerifier(unittest.TestCase):
    PREPOPULATED_CERT_URL = "https://s3.amazonaws.com/echo.api/doesnotexist"
    VALID_URL = "https://s3.amazonaws.com/echo.api/cert"
    VALID_URL_WITH_PORT = "https://s3.amazonaws.com:443/echo.api/cert"
    VALID_URL_WITH_PATH_TRAVERSAL = (
        "https://s3.amazonaws.com/echo.api/../echo.api/cert")
    INVALID_URL_WITH_INVALID_HOST_NAME = "https://very.bad/echo.api/cert"
    INVALID_URL_WITH_INVALID_PORT = (
        "https://s3.amazonaws.com:563/echo.api/cert")
    INVALID_URL_WITH_INVALID_PATH = "https://s3.amazonaws.com/cert"
    INVALID_URL_WITH_INVALID_PATH_TRAVERSAL = (
        "https://s3.amazonaws.com/echo.api/../cert")
    INVALID_URL_WITH_INVALID_UPPER_CASE_PATH = (
        "https://s3.amazonaws.com/ECHO.API/cert")
    MALFORMED_URL = "badUrl"

    def setUp(self):
        self.headers = {
            SIGNATURE_CERT_CHAIN_URL_HEADER: "TestUrl",
            SIGNATURE_HEADER: "Test Signature"
        }
        self.request_verifier = RequestVerifier()

    @staticmethod
    def generate_private_key():
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def create_certificate(self):
        self.private_key = self.generate_private_key()

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"WA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Seattle"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Amazon Alexa"),
            x509.NameAttribute(
                NameOID.COMMON_NAME, u"{}".format(self.PREPOPULATED_CERT_URL)),
            ])

        self.mock_certificate = x509.CertificateBuilder().subject_name(
            name=subject).issuer_name(
            name=issuer).public_key(
            key=self.private_key.public_key()).serial_number(
            number=x509.random_serial_number()).not_valid_before(
            time=datetime.utcnow() - timedelta(minutes=1)).not_valid_after(
            time=datetime.utcnow() + timedelta(minutes=1)).add_extension(
            extension=x509.SubjectAlternativeName(
                [x509.DNSName(u"{}".format(CERT_CHAIN_DOMAIN))]),
            critical=False).sign(
            private_key=self.private_key,
            algorithm=SHA1(),
            backend=default_backend()
        )

        self.request_verifier._cert_cache[
            self.PREPOPULATED_CERT_URL] = self.mock_certificate

    def sign_data(
            self, data, private_key=None,
            padding=PKCS1v15(), hash_algorithm=SHA1()):
        if private_key is None:
            private_key = self.private_key

        return private_key.sign(
            data=data.encode(CHARACTER_ENCODING),
            padding=padding,
            algorithm=hash_algorithm
        )

    def test_no_cert_url_header_throw_exception(self):
        self.headers.pop(SIGNATURE_CERT_CHAIN_URL_HEADER)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier.verify(self.headers, None, None)

        self.assertIn(
            "Missing Signature/Certificate for the skill request",
            str(exc.exception))

    def test_no_signature_header_throw_exception(self):
        self.headers.pop(SIGNATURE_HEADER)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier.verify(self.headers, None, None)

        self.assertIn(
            "Missing Signature/Certificate for the skill request",
            str(exc.exception))

    def test_validate_cert_url_scheme_mismatch_throw_exception(self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.MALFORMED_URL)

        self.assertIn(
            "Signature Certificate URL has invalid protocol",
            str(exc.exception))

    def test_validate_cert_url_hostname_mismatch_throw_exception(self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.INVALID_URL_WITH_INVALID_HOST_NAME)

        self.assertIn(
            "Signature Certificate URL has invalid hostname",
            str(exc.exception))

    def test_validate_cert_url_start_path_mismatch_throw_exception(self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.INVALID_URL_WITH_INVALID_PATH)

        self.assertIn(
            "Signature Certificate URL has invalid path", str(exc.exception))

    def test_validate_cert_url_normalized_start_path_mismatch_throw_exception(
            self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.INVALID_URL_WITH_INVALID_PATH_TRAVERSAL)

        self.assertIn(
            "Signature Certificate URL has invalid path", str(exc.exception))

    def test_validate_cert_url_start_path_case_mismatch_throw_exception(self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.INVALID_URL_WITH_INVALID_UPPER_CASE_PATH)

        self.assertIn(
            "Signature Certificate URL has invalid path", str(exc.exception))

    def test_validate_cert_url_port_mismatch_throw_exception(self):
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_certificate_url(
                self.INVALID_URL_WITH_INVALID_PORT)

        self.assertIn(
            "Signature Certificate URL has invalid port", str(exc.exception))

    def test_validate_cert_url_for_valid_url(self):
        try:
            self.request_verifier._validate_certificate_url(self.VALID_URL)
        except:
            # Should never reach here
            self.fail(
                "Request Verifier couldn't validate a valid certificate URL")

    def test_validate_cert_url_for_valid_url_with_port(self):
        try:
            self.request_verifier._validate_certificate_url(
                self.VALID_URL_WITH_PORT)
        except:
            # Should never reach here
            self.fail(
                "Request Verifier couldn't validate a valid certificate "
                "URL with valid port")

    def test_validate_cert_url_for_valid_url_with_path_traversal(self):
        try:
            self.request_verifier._validate_certificate_url(
                self.VALID_URL_WITH_PATH_TRAVERSAL)
        except:
            # Should never reach here
            self.fail(
                "Request Verifier couldn't validate a valid certificate "
                "URL with path traversal")

    def test_load_cert_chain_invalid_cert_url_throw_exception(self):
        mocked_parsed_url = mock.MagicMock(spec=ParseResult)
        with mock.patch(
                "ask_sdk_webservice_support.verifier.urlparse",
                return_value=mocked_parsed_url):

            with self.assertRaises(VerificationException) as exc:
                self.request_verifier._load_cert_chain(self.MALFORMED_URL)

        self.assertIn(
            "Unable to load certificate from URL", str(exc.exception))

    def test_load_cert_chain_invalid_cert_throw_exception(self):
        with mock.patch(
                "ask_sdk_webservice_support.verifier.urlopen"
        ) as mock_url_open:
            with mock.patch(
                    "ask_sdk_webservice_support.verifier."
                    "load_pem_x509_certificate", side_effect=ValueError):
                mock_url_open.read.return_value = "test"

                with self.assertRaises(VerificationException) as exc:
                    self.request_verifier._load_cert_chain(self.MALFORMED_URL)

        self.assertIn(
            "Unable to load certificate from URL", str(exc.exception))

    def test_load_cert_chain_load_and_cache_cert(self):
        self.assertIsNone(
            self.request_verifier._cert_cache.get(
                self.PREPOPULATED_CERT_URL, None),
            "Invalid Certificate cached in Request Verifier Certificate "
            "Cache")
        with mock.patch(
                "ask_sdk_webservice_support.verifier.urlopen"
        ) as mock_url_open:
            mock_url_open.read.return_value = "test"
            mock_x509_cert = "Test_Certificate"

            with mock.patch(
                    "ask_sdk_webservice_support."
                    "verifier.load_pem_x509_certificate",
                    return_value=mock_x509_cert
            ):
                self.request_verifier._load_cert_chain(
                    self.PREPOPULATED_CERT_URL)

                self.assertEqual(
                    self.request_verifier._cert_cache.get(
                        self.PREPOPULATED_CERT_URL), mock_x509_cert, (
                        "Request Verifier loaded invalid certificate in "
                        "certificate cache"))

    def test_validate_cert_chain_expired_before_cert_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow() + timedelta(days=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_cert_chain(test_certificate)

        self.assertIn("Signing Certificate expired", str(exc.exception))

    def test_validate_cert_chain_expired_after_cert_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow()
        test_certificate.not_valid_after = datetime.now() - timedelta(days=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_cert_chain(test_certificate)

        self.assertIn("Signing Certificate expired", str(exc.exception))

    def test_validate_cert_chain_domain_missing_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow() - timedelta(
            minutes=1)
        test_certificate.not_valid_after = datetime.utcnow() + timedelta(
            minutes=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_cert_chain(test_certificate)

        self.assertIn(
            "domain missing in Signature Certificate Chain",
            str(exc.exception))

    def test_validate_cert_chain_valid_cert(self):
        self.create_certificate()
        try:
            self.request_verifier._validate_cert_chain(self.mock_certificate)
        except:
            # Should never reach here
            self.fail(
                "Request Verifier certificate validation failed for a "
                "valid certificate chain")

    def test_request_verification_for_valid_request(self):
        test_content = "This is some test content"
        self.create_certificate()
        signature = self.sign_data(data=test_content)

        self.headers[
            SIGNATURE_CERT_CHAIN_URL_HEADER] = self.PREPOPULATED_CERT_URL
        self.headers[SIGNATURE_HEADER] = base64.b64encode(signature)

        try:
            self.request_verifier.verify(
                headers=self.headers,
                serialized_request_env=test_content,
                deserialized_request_env=RequestEnvelope())
        except:
            # Should never reach here
            self.fail(
                "Request verifier couldn't verify a valid signed request")

    def test_request_verification_for_invalid_request(self):
        test_content = "This is some test content"
        self.create_certificate()

        different_private_key = self.generate_private_key()
        signature = self.sign_data(
            data=test_content, private_key=different_private_key)

        self.headers[
            SIGNATURE_CERT_CHAIN_URL_HEADER] = self.PREPOPULATED_CERT_URL
        self.headers[SIGNATURE_HEADER] = base64.b64encode(signature)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier.verify(
                headers=self.headers,
                serialized_request_env=test_content,
                deserialized_request_env=RequestEnvelope())

        self.assertIn("Request body is not valid", str(exc.exception))


class TestTimestampVerifier(unittest.TestCase):
    def setUp(self):
        self.timestamp_verifier = None

    def test_tolerance_value_more_than_max_throw_exception(self):
        test_tolerance_millis = MAX_TIMESTAMP_TOLERANCE_IN_MILLIS + 1
        with self.assertRaises(VerificationException) as exc:
            self.timestamp_verifier = TimestampVerifier(
                tolerance_in_millis=test_tolerance_millis)

        self.assertIn(
            "Provided tolerance value {} exceeds the maximum allowed "
            "value".format(test_tolerance_millis), str(exc.exception))

    def test_tolerance_value_negative_throw_exception(self):
        test_tolerance_millis = -1
        with self.assertRaises(VerificationException) as exc:
            self.timestamp_verifier = TimestampVerifier(
                tolerance_in_millis=test_tolerance_millis)

        self.assertIn(
            "Negative tolerance values not supported", str(exc.exception))

    def test_tolerance_value_within_range_valid(self):
        test_tolerance_millis = DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS + 1
        try:
            self.timestamp_verifier = TimestampVerifier(
                tolerance_in_millis=test_tolerance_millis)
        except:
            # Should never reach here
            self.fail(
                "Timestamp verifier fails initialization with valid "
                "tolerance value")

    def test_timestamp_verification_with_expired_timestamp(self):
        test_request_envelope = RequestEnvelope(
            request=IntentRequest(
                timestamp=datetime(year=2019, month=1, day=1, tzinfo=tzutc())))
        self.timestamp_verifier = TimestampVerifier()
        with self.assertRaises(VerificationException) as exc:
            self.timestamp_verifier.verify(
                headers={},
                serialized_request_env="",
                deserialized_request_env=test_request_envelope)

        self.assertIn("Timestamp verification failed", str(exc.exception))

    def test_timestamp_verification_with_valid_future_server_timestamp(self):
        valid_tolerance = int(DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS / 2 / 1000)
        valid_future_datetime = datetime.now(tzutc()) + timedelta(seconds=valid_tolerance)
        test_request_envelope = RequestEnvelope(
            request=IntentRequest(
                timestamp=valid_future_datetime))
        self.timestamp_verifier = TimestampVerifier()
        try:
            self.timestamp_verifier.verify(
                headers={},
                serialized_request_env="",
                deserialized_request_env=test_request_envelope)
        except:
            # Should never reach here
            raise self.fail(
                "Timestamp verification failed for a valid input request")

    def test_timestamp_verification_with_valid_timestamp(self):
        test_request_envelope = RequestEnvelope(
            request=IntentRequest(
                timestamp=datetime.now(tz=tzlocal())))
        self.timestamp_verifier = TimestampVerifier()
        try:
            self.timestamp_verifier.verify(
                headers={},
                serialized_request_env="",
                deserialized_request_env=test_request_envelope)
        except:
            # Should never reach here
            raise self.fail(
                "Timestamp verification failed for a valid input request")
