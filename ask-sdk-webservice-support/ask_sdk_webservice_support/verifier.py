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
from __future__ import division
import os
import base64
import typing
import six
import warnings

from dateutil import tz
from datetime import datetime
from abc import ABCMeta, abstractmethod
from ask_sdk_runtime.exceptions import AskSdkException
from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen
from cryptography.x509 import (
    load_pem_x509_certificate, ExtensionOID, DNSName, 
    SubjectAlternativeName)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.exceptions import InvalidSignature
from contextlib import closing
from asn1crypto import pem
from certvalidator import CertificateValidator
from certvalidator.errors import PathValidationError

from .verifier_constants import (
    SIGNATURE_CERT_CHAIN_URL_HEADER, SIGNATURE_HEADER,
    CERT_CHAIN_URL_PROTOCOL, CERT_CHAIN_URL_HOSTNAME,
    CERT_CHAIN_URL_PORT, CERT_CHAIN_URL_STARTPATH,
    CERT_CHAIN_DOMAIN, CHARACTER_ENCODING,
    MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS,
    MAX_SKILL_EVENT_TOLERANCE_IN_MILLIS, ALEXA_SKILL_EVENT_LIST)

if typing.TYPE_CHECKING:
    from typing import Dict, Any, Optional
    from ask_sdk_model import RequestEnvelope
    from cryptography.x509 import Certificate
    from cryptography.hazmat.backends.interfaces import X509Backend
    from cryptography.hazmat.primitives.asymmetric.padding import (
        AsymmetricPadding)
    from cryptography.hazmat.primitives.hashes import HashAlgorithm
    from cryptography.hazmat.backends.openssl import rsa


class VerificationException(AskSdkException):
    """Class for exceptions raised during Request verification."""
    pass


class AbstractVerifier(object):
    """Abstract verifier class for implementing custom verifiers.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify(
            self, headers, serialized_request_env, deserialized_request_env):
        # type: (Dict[str, Any], str, RequestEnvelope) -> None
        """Abstract verify method that verifies and validates inputs.

        Custom verifiers should implement this method, to validate the
        headers and body of the input POST request. The method returns
        a :py:class:`VerificationException` if the validation fails, or
        succeeds silently.

        :param headers: headers of the input POST request
        :type headers: Dict[str, Any]
        :param serialized_request_env: raw request envelope in the
            input POST request
        :type serialized_request_env: str
        :param deserialized_request_env: deserialized request envelope
            instance of the input POST request
        :type deserialized_request_env:
            :py:class:`ask_sdk_model.request_envelope.RequestEnvelope`
        :raises: :py:class:`VerificationException` if verification fails
        """
        raise NotImplementedError


class RequestVerifier(AbstractVerifier):
    """Verifier that performs request signature verification.

    This is a concrete implementation of :py:class:`AbstractVerifier`
    class, handling the request signature verification of the input
    request. This verifier uses the Cryptography module x509 functions
    to validate the signature chain in the input request. The
    verification follows the mechanism explained here :
    https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request

    The constructor takes the header key names for retrieving Signature
    Certificate Chain and Signature. They are defaulted to the header
    names present in the
    :py:mod:`ask_sdk_webservice_support.verifier_constants`.
    Additionally, one can also provide the Padding and the Hash
    Algorithm function that is used to verify the input body.

    The verify method retrieves the Signature Certificate Chain URL,
    validates the URL, retrieves the chain from the URL, validates the
    signing certificate, extract the public key, base64 decode the
    Signature and verifies if the hash value of the request body matches
    with the decrypted signature.
    """
    def __init__(
            self,
            signature_cert_chain_url_key=SIGNATURE_CERT_CHAIN_URL_HEADER,
            signature_key=SIGNATURE_HEADER,
            padding=PKCS1v15(), hash_algorithm=SHA1()):
        # type: (str, str, AsymmetricPadding, HashAlgorithm) -> None
        """Verifier that performs request signature verification.

        This is a concrete implementation of
        :py:class:`AbstractVerifier` class, handling the request
        signature verification of the input request. This verifier uses
        the Cryptography module x509 functions to validate the
        signature chain in the input request. The verification follows
        the mechanism explained here :
        https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request

        The constructor takes the header key names for retrieving
        Signature Certificate Chain and Signature. They are defaulted
        to the header names present in the
        :py:mod:`ask_sdk_webservice_support.conf`. Additionally, one
        can also provide the Padding and the Hash Algorithm functions
        that is used to verify the input body. These are defaulted as
        :py:class:`cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15`
        and :py:class:`cryptography.hazmat.primitives.hashes.SHA1`
        instances respectively.

        A certificate cache is initialized, to store certificate chains
        for faster retrieval and validation in subsequent input
        dispatch.

        :param signature_cert_chain_url_key: Header key to be used, to
            retrieve Signature Certificate Chain URL from headers
        :type signature_cert_chain_url_key: str
        :param signature_key: Header key to be used, to
            retrieve Signature from headers
        :type signature_key: str
        :param padding: Asymmetric padding algorithm instance to be
            used to verify the hash value of the request body with the
            decrypted signature. Defaulted to `PKCS1v15`
        :type padding:
            cryptography.hazmat.primitives.asymmetric.padding.AsymmetricPadding
        :param hash_algorithm: Hash algorithm instance to be used
            to verify the hash value of the request body with the
            decrypted signature. Defaulted to `SHA1`
        :type hash_algorithm:
            cryptography.hazmat.primitives.hashes.HashAlgorithm
        """
        self._signature_cert_chain_url_key = signature_cert_chain_url_key
        self._signature_key = signature_key
        self._padding = padding
        self._hash_algorithm = hash_algorithm
        self._cert_cache = {}  # type: Dict[str, bytes]

    def verify(
            self, headers, serialized_request_env, deserialized_request_env):
        # type: (Dict[str, Any], str, RequestEnvelope) -> None
        """Verify if the input request signature and the body matches.

        The verify method retrieves the Signature Certificate Chain URL,
        validates the URL, retrieves the chain from the URL, validates
        the signing certificate, extract the public key, base64 decode
        the Signature and verifies if the hash value of the request body
        matches with the decrypted signature.

        :param headers: headers of the input POST request
        :type headers: Dict[str, Any]
        :param serialized_request_env: raw request envelope in the
            input POST request
        :type serialized_request_env: str
        :param deserialized_request_env: deserialized request envelope
            instance of the input POST request
        :type deserialized_request_env:
            :py:class:`ask_sdk_model.request_envelope.RequestEnvelope`
        :raises: :py:class:`VerificationException` if headers doesn't
            exist or verification fails
        """
        cert_url = None
        signature = None
        for header_key, header_value in six.iteritems(headers):
            if header_key.lower() == self._signature_cert_chain_url_key.lower():
                cert_url = header_value
            elif header_key.lower() == self._signature_key.lower():
                signature = header_value

        if cert_url is None or signature is None:
            raise VerificationException(
                "Missing Signature/Certificate for the skill request")

        cert_chain = self._retrieve_and_validate_certificate_chain(cert_url)

        self._valid_request_body(
            cert_chain, signature, serialized_request_env)

    def _retrieve_and_validate_certificate_chain(
            self, cert_url, x509_backend=default_backend()):
        # type: (str, X509Backend) -> Certificate
        """Retrieve and validate certificate chain.

        This method validates if the URL is valid, loads and
        validates the certificate chain, loads and validates the
        end certificate, before returning it.

        The end certificate is read, using the
        :py:func:`cryptography.x509.load_pem_x509_certificate` method.
        The x509 backend is set as default to the
        :py:class:`cryptography.hazmat.backends.default_backend`
        instance.

        :param cert_url: URL for retrieving certificate chain
        :type cert_url: str
        :param x509_backend: Backend to be used, for loading pem x509
            certificate
        :type x509_backend:
            cryptography.hazmat.backends.interfaces.X509Backend
        :return The certificate chain loaded from the URL
        :rtype cryptography.x509.Certificate
        :raises: :py:class:`VerificationException` if the URL is invalid,
            if the loaded certificate chain is invalid
        """
        self._validate_certificate_url(cert_url)

        cert_chain = self._load_cert_chain(cert_url)
        self._validate_cert_chain(cert_chain)

        end_cert = load_pem_x509_certificate(
                data=cert_chain, backend=x509_backend)
        self._validate_end_certificate(x509_cert=end_cert)
        return end_cert

    def _validate_certificate_url(self, cert_url):
        # type: (str) -> None
        """Validate the URL containing the certificate chain.

        This method validates if the URL provided adheres to the format
        mentioned here :
        https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#cert-verify-signature-certificate-url

        :param cert_url: URL for retrieving certificate chain
        :type cert_url: str
        :raises: :py:class:`VerificationException` if the URL is invalid
        """
        parsed_url = urlparse(cert_url)

        protocol = parsed_url.scheme
        if protocol.lower() != CERT_CHAIN_URL_PROTOCOL.lower():
            raise VerificationException(
                "Signature Certificate URL has invalid protocol: {}. "
                "Expecting {}".format(protocol, CERT_CHAIN_URL_PROTOCOL))

        hostname = parsed_url.hostname
        if (hostname is None or
                hostname.lower() != CERT_CHAIN_URL_HOSTNAME.lower()):
            raise VerificationException(
                "Signature Certificate URL has invalid hostname: {}. "
                "Expecting {}".format(hostname, CERT_CHAIN_URL_HOSTNAME))

        normalized_path = os.path.normpath(parsed_url.path)
        if not normalized_path.startswith(CERT_CHAIN_URL_STARTPATH):
            raise VerificationException(
                "Signature Certificate URL has invalid path: {}. "
                "Expecting the path to start with {}".format(
                    normalized_path, CERT_CHAIN_URL_STARTPATH))

        port = parsed_url.port
        if port is not None and port != CERT_CHAIN_URL_PORT:
            raise VerificationException(
                "Signature Certificate URL has invalid port: {}. "
                "Expecting {}".format(str(port), str(CERT_CHAIN_URL_PORT)))

    def _load_cert_chain(self, cert_url):
        # type: (str) -> bytes
        """Loads the certificate chain from the URL.

        This method loads the certificate chain from the certificate
        cache. If there is a cache miss, the certificate chain is
        loaded from the certificate URL.
        A :py:class:`VerificationException` is raised if the
        certificate chain cannot be loaded.

        :param cert_url: URL for retrieving certificate chain
        :type cert_url: str
        :return: Certificate chain loaded from cache or URL
        :rtype bytes
        :raises: :py:class:`VerificationException` if unable to load the
            certificate chain
        """
        try:
            if cert_url in self._cert_cache:
                return self._cert_cache[cert_url]
            else:
                if six.PY2:
                    with closing(urlopen(cert_url)) as cert_response:
                        cert_data = cert_response.read()  # type: bytes
                else:
                    with urlopen(cert_url) as cert_response:
                        cert_data = cert_response.read()  # type: bytes
                self._cert_cache[cert_url] = cert_data
                return cert_data
        except ValueError as e:
            raise VerificationException(
                "Unable to load certificate from URL", e)

    def _validate_cert_chain(self, cert_chain):
        # type: (bytes) -> None
        """Validate the certificate chain.

        This method checks if the passed in certificate chain is valid.
        A :py:class:`VerificationException` is raised if the certificate
        chain is not valid.

        The end certificate is read, using the
        :py:func:`cryptography.x509.load_pem_x509_certificate` method.
        The x509 backend is set as default to the
        :py:class:`cryptography.hazmat.backends.default_backend`
        instance.

        :param cert_chain: Certificate chain to be validated
        :type cert_chain: bytes
        :return: None
        :raises: :py:class:`VerificationException` if certificate chain is
            not valid
        """
        try:
            end_cert = None
            intermediate_certs = []
            for type_name, headers, der_bytes in pem.unarmor(
                    cert_chain, multiple=True):
                if end_cert is None:
                    end_cert = der_bytes
                else:
                    intermediate_certs.append(der_bytes)

            validator = CertificateValidator(end_cert, intermediate_certs)
            validator.validate_usage(key_usage={'digital_signature'})
        except PathValidationError as e:
            raise VerificationException("Certificate chain is not valid", e)

    def _validate_end_certificate(self, x509_cert):
        # type: (Certificate) -> None
        """Validate the end certificate.

        This method checks if the passed in certificate is valid,
        by doing the following checks :
        - The end certificate is not expired
        - The end certificate contains Alexa domain in it's SAN extensions

        A :py:class:`VerificationException` is raised if the certificate
        is not valid.

        :param x509_cert: Certificate to be validated
        :type x509_cert: cryptography.x509.Certificate
        :return: None
        :raises: :py:class:`VerificationException` if certificate is
            not valid
        """
        now = datetime.utcnow()
        if not (x509_cert.not_valid_before <= now <=
                x509_cert.not_valid_after):
            raise VerificationException("Signing Certificate expired")

        ext = x509_cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        ext_value = typing.cast(SubjectAlternativeName, ext.value)
        if CERT_CHAIN_DOMAIN not in ext_value.get_values_for_type(
                DNSName):
            raise VerificationException(
                "{} domain missing in Signature Certificate Chain".format(
                    CERT_CHAIN_DOMAIN))

    def _valid_request_body(
            self, cert_chain, signature, serialized_request_env):
        # type: (Certificate, str, str) -> None
        """Validate the request body hash with signature.

        This method checks if the hash value of the request body
        matches with the hash value of the signature, decrypted using
        certificate chain. A
        :py:class:`VerificationException` is raised if there is a
        mismatch.

        :param cert_chain: Certificate chain to be validated
        :type cert_chain: cryptography.x509.Certificate
        :param signature: Encrypted signature of the request
        :type: str
        :param serialized_request_env: Raw request body
        :type: str
        :raises: :py:class:`VerificationException` if certificate is
            not valid
        """
        decoded_signature = base64.b64decode(signature)
        public_key = cert_chain.public_key()  # type: rsa._RSAPublicKey
        request_env_bytes = serialized_request_env.encode(CHARACTER_ENCODING)

        try:
            public_key.verify(
                decoded_signature, request_env_bytes,
                self._padding, self._hash_algorithm)
        except InvalidSignature as e:
            raise VerificationException("Request body is not valid", e)


class TimestampVerifier(AbstractVerifier):
    """Verifier that performs request timestamp verification.

    This is a concrete implementation of :py:class:`AbstractVerifier`
    class, handling the request timestamp verification of the input
    request. The verification follows the mechanism explained here :
    https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#timestamp

    The constructor takes the tolerance value in milliseconds, that is
    the maximum tolerance limit the input request can have, with the
    current timestamp.

    The verify method retrieves the request timestamp and check if it
    falls in the limit set by the tolerance.

    """
    def __init__(
            self, tolerance_in_millis=MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS):
        # type: (float) -> None
        """Verifier that performs request timestamp verification.

        This is a concrete implementation of
        :py:class:`AbstractVerifier` class, handling the request
        timestamp verification of the input request. The verification
        follows the mechanism explained here:
        https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#timestamp

        The constructor takes the tolerance value in milliseconds,
        that is the maximum tolerance limit the input request can have,
        with the current timestamp. A :py:class:`VerificationException`
        is raised if the passed in tolerance value is negative or is
        more than the accepted tolerance limit, which is set in
        :py:mod:`ask_sdk_webservice_support.verifier_constant`.

        :param tolerance_in_millis: Tolerance value in milliseconds,
            to be used during verification
        :type tolerance_in_millis: float
        :raises: :py:class:`VerificationException` if tolerance value is
            invalid
        """
        if tolerance_in_millis > MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS:
            warnings.warn(
                "Provided tolerance value {} exceeds the maximum allowed "
                "value {}. Maximum value will be used instead".format(
                    tolerance_in_millis, MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS))
            tolerance_in_millis = MAX_NORMAL_REQUEST_TOLERANCE_IN_MILLIS

        if tolerance_in_millis < 0:
            raise VerificationException(
                "Negative tolerance values not supported")

        self._tolerance_in_millis = tolerance_in_millis

    def verify(
            self, headers, serialized_request_env, deserialized_request_env):
        # type: (Dict[str, Any], str, RequestEnvelope) -> None
        """Verify if the input request timestamp is in tolerated limits.

        The verify method retrieves the request timestamp and check if
        it falls in the limit set by the tolerance, by checking with
        the current timestamp in UTC.

        :param headers: headers of the input POST request
        :type headers: Dict[str, Any]
        :param serialized_request_env: raw request envelope in the
            input POST request
        :type serialized_request_env: str
        :param deserialized_request_env: deserialized request envelope
            instance of the input POST request
        :type deserialized_request_env:
            :py:class:`ask_sdk_model.request_envelope.RequestEnvelope`
        :raises: :py:class:`VerificationException` if difference between
            local timestamp and input request timestamp is more than
            specific tolerance limit
        """
        local_now = datetime.now(tz.tzutc())
        if (deserialized_request_env.request is None or 
        deserialized_request_env.request.timestamp is None):
            raise VerificationException("Timestamp verification failed")
        else:
            request_timestamp = deserialized_request_env.request.timestamp
            timestamp_diff = abs((local_now - request_timestamp).total_seconds())
            if timestamp_diff > (self._tolerance_in_millis / 1000):
                # For skill events, need to check if timestamp difference in
                # max skill event timestamp tolerance limit
                request_type = deserialized_request_env.request.object_type
                if (request_type in ALEXA_SKILL_EVENT_LIST and
                        timestamp_diff <= (MAX_SKILL_EVENT_TOLERANCE_IN_MILLIS / 1000)):
                    return

                raise VerificationException("Timestamp verification failed")
