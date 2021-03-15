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
import os
import unittest
import warnings
from datetime import datetime, timedelta

import six
from ask_sdk_model import IntentRequest, RequestEnvelope
from ask_sdk_model.events.skillevents import SkillEnabledRequest
from ask_sdk_webservice_support.verifier import (RequestVerifier,
                                                 TimestampVerifier,
                                                 VerificationException)
from ask_sdk_webservice_support.verifier_constants import (
    CERT_CHAIN_DOMAIN, CHARACTER_ENCODING,
    MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS,
    MAX_SKILL_EVENT_TOLERANCE_IN_MILLIS, SIGNATURE_CERT_CHAIN_URL_HEADER,
    SIGNATURE_HEADER)
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.x509 import Certificate, load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from dateutil.tz import tzlocal, tzutc
from freezegun import freeze_time
from six.moves.urllib.parse import ParseResult

try:
    import mock
except ImportError:
    from unittest import mock


class TestRequestVerifier(unittest.TestCase):
    PREPOPULATED_CERT_URL = "https://s3.amazonaws.com/echo.api/echo-api-cert-8.pem"
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

    def create_self_signed_certificate(self):
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
                x509.SubjectAlternativeName(
                    [x509.DNSName(u"{}".format(CERT_CHAIN_DOMAIN))]),
            critical=False).sign(
            private_key=self.private_key,
            algorithm=SHA1(),
            backend=default_backend()
        )  # type: Certificate

        self.request_verifier._cert_cache[
            self.PREPOPULATED_CERT_URL] = self.mock_certificate

    def load_valid_certificate(self):
        with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'echo-api-cert-7.pem'), 'rb') as cert_response:
            self.cert_bytes = cert_response.read()

        self.mock_certificate = load_pem_x509_certificate(
            data=self.cert_bytes, backend=default_backend())

        self.request_verifier._cert_cache[
            self.PREPOPULATED_CERT_URL] = self.cert_bytes

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

    def test_load_cert_chain_load_and_cache_cert(self):
        self.assertIsNone(
            self.request_verifier._cert_cache.get(
                self.PREPOPULATED_CERT_URL, None),
            "Invalid Certificate cached in Request Verifier Certificate "
            "Cache")
        with mock.patch(
                "ask_sdk_webservice_support.verifier.urlopen", autospec=True
        ) as mock_url_open:
            if six.PY2:
                # Because of the way mocks work with context manager in py2.7
                mock_url_open.return_value.read.return_value = "test"
            else:
                mock_url_open.return_value.__enter__.return_value.read.return_value = "test"
            self.request_verifier._load_cert_chain(self.PREPOPULATED_CERT_URL)

            self.assertEqual(
                self.request_verifier._cert_cache.get(self.PREPOPULATED_CERT_URL),
                "test",
                "Request Verifier loaded invalid certificate in certificate cache"
            )

    @freeze_time('2001-01-01')
    def test_validate_cert_chain_invalid_path(self):
        self.load_valid_certificate()
        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_cert_chain(cert_chain=self.cert_bytes)

        self.assertIn("Certificate chain is not valid", str(exc.exception))

    @freeze_time('2020-01-01')
    def test_validate_cert_chain_valid_path(self):
        self.load_valid_certificate()
        try:
            self.request_verifier._validate_cert_chain(cert_chain=self.cert_bytes)
        except:
            # Should never reach here
            self.fail("Request verifier couldn't validate a valid certificate chain")

    def test_validate_end_cert_expired_before_cert_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow() + timedelta(days=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_end_certificate(test_certificate)

        self.assertIn("Signing Certificate expired", str(exc.exception))

    def test_validate_end_cert_expired_after_cert_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow()
        test_certificate.not_valid_after = datetime.now() - timedelta(days=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_end_certificate(test_certificate)

        self.assertIn("Signing Certificate expired", str(exc.exception))

    def test_validate_end_cert_domain_missing_throw_exception(self):
        test_certificate = mock.MagicMock(spec=x509.Certificate)
        test_certificate.not_valid_before = datetime.utcnow() - timedelta(
            minutes=1)
        test_certificate.not_valid_after = datetime.utcnow() + timedelta(
            minutes=1)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._validate_end_certificate(test_certificate)

        self.assertIn(
            "domain missing in Signature Certificate Chain",
            str(exc.exception))

    def test_validate_end_cert_valid_cert(self):
        self.create_self_signed_certificate()
        try:
            self.request_verifier._validate_end_certificate(self.mock_certificate)
        except:
            # Should never reach here
            self.fail(
                "Request Verifier certificate validation failed for a "
                "valid certificate chain")

    def test_validate_request_body_for_valid_request(self):
        test_content = "This is some test content"
        self.create_self_signed_certificate()
        signature = self.sign_data(data=test_content)

        try:
            self.request_verifier._valid_request_body(
                cert_chain=self.mock_certificate,
                signature=base64.b64encode(signature),
                serialized_request_env=test_content)
        except:
            # Should never reach here
            self.fail(
                "Request verifier validate request body failed for a valid "
                "signed request")

    def test_validate_request_body_for_invalid_request(self):
        test_content = "This is some test content"
        self.create_self_signed_certificate()

        different_private_key = self.generate_private_key()
        signature = self.sign_data(
            data=test_content, private_key=different_private_key)

        with self.assertRaises(VerificationException) as exc:
            self.request_verifier._valid_request_body(
                cert_chain=self.mock_certificate,
                signature=base64.b64encode(signature),
                serialized_request_env=test_content)

        self.assertIn("Request body is not valid", str(exc.exception))

    def test_request_verification_for_valid_request(self):
        with mock.patch.object(
                RequestVerifier, '_retrieve_and_validate_certificate_chain'):
            with mock.patch.object(
                    RequestVerifier, '_valid_request_body'):
                self.headers[
                    SIGNATURE_CERT_CHAIN_URL_HEADER] = self.PREPOPULATED_CERT_URL
                self.headers[SIGNATURE_HEADER] = self.generate_private_key()
                try:
                    RequestVerifier().verify(
                        headers=self.headers,
                        serialized_request_env="test",
                        deserialized_request_env=RequestEnvelope())
                except:
                    # Should never reach here
                    self.fail("Request verifier couldn't verify a valid signed request")

    def test_request_verification_for_invalid_request(self):
        with mock.patch.object(
                RequestVerifier, '_retrieve_and_validate_certificate_chain'):
            with mock.patch.object(
                    RequestVerifier, '_valid_request_body',
                    side_effect=VerificationException(
                        'Request body is not valid')):
                self.headers[
                    SIGNATURE_CERT_CHAIN_URL_HEADER] = self.PREPOPULATED_CERT_URL
                self.headers[SIGNATURE_HEADER] = self.generate_private_key()

                with self.assertRaises(VerificationException) as exc:
                    RequestVerifier().verify(
                        headers=self.headers,
                        serialized_request_env="test",
                        deserialized_request_env=RequestEnvelope())

                self.assertIn("Request body is not valid", str(exc.exception))

class TestTimestampVerifier(unittest.TestCase):
    def setUp(self):
        self.timestamp_verifier = None

    def test_tolerance_value_more_than_max_throw_warning(self):
        test_tolerance_millis = MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS + 1
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.timestamp_verifier = TimestampVerifier(
                tolerance_in_millis=test_tolerance_millis)

            self.assertTrue(
                len(w) == 1, "Timestamp verifier fails throwing warning when "
                             "tolerance values exceeds maximum supported "
                             "tolerance value")
            self.assertIn(
                "Provided tolerance value {} exceeds the maximum allowed value".format(
                    test_tolerance_millis),
                str(w[0].message),
                "Timestamp verifier throws unexpected warning when tolerance "
                "value exceeds maximum supported tolerance value")
            self.assertEqual(
                self.timestamp_verifier._tolerance_in_millis,
                MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS,
                "Timestamp verifier initialized incorrect tolerance value "
                "when provided tolerance value exceeds maximum supported "
                "tolerance value")

    def test_tolerance_value_negative_throw_exception(self):
        test_tolerance_millis = -1
        with self.assertRaises(VerificationException) as exc:
            self.timestamp_verifier = TimestampVerifier(
                tolerance_in_millis=test_tolerance_millis)

        self.assertIn(
            "Negative tolerance values not supported", str(exc.exception))

    def test_tolerance_value_within_range_valid(self):
        test_tolerance_millis = MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS + 1
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
        valid_tolerance = int(MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS / 2 / 1000)
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

    @freeze_time('2020-01-01 01:00:00')
    def test_timestamp_verification_with_valid_timestamp_skill_event(self):
        test_request_envelope = RequestEnvelope(
            request=SkillEnabledRequest(
                timestamp=datetime(
                    year=2020, month=1, day=1, hour=0, minute=0, second=0,
                    tzinfo=tzutc())))
        self.timestamp_verifier = TimestampVerifier()
        try:
            self.timestamp_verifier.verify(
                headers={},
                serialized_request_env="",
                deserialized_request_env=test_request_envelope)
        except:
            # Should never reach here
            raise self.fail(
                "Timestamp verification failed for a valid skill event input request")

    @freeze_time('2020-01-01 01:01:00')
    def test_timestamp_verification_with_expired_timestamp_skill_event(self):
        test_request_envelope = RequestEnvelope(
            request=SkillEnabledRequest(
                timestamp=datetime(
                    year=2020, month=1, day=1, hour=0, minute=0, second=0,
                    tzinfo=tzutc())))
        self.timestamp_verifier = TimestampVerifier()
        with self.assertRaises(VerificationException) as exc:
            self.timestamp_verifier.verify(
                headers={},
                serialized_request_env="",
                deserialized_request_env=test_request_envelope)

        self.assertIn("Timestamp verification failed", str(exc.exception))
