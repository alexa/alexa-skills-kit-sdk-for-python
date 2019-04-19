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

from dateutil import tz
from datetime import datetime
from abc import ABCMeta, abstractmethod
from ask_sdk_runtime.exceptions import AskSdkException
from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen
from cryptography.x509 import (
    load_pem_x509_certificate, ExtensionOID, DNSName)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.exceptions import InvalidSignature

from .verifier_constants import (
    SIGNATURE_CERT_CHAIN_URL_HEADER, SIGNATURE_HEADER,
    CERT_CHAIN_URL_PROTOCOL, CERT_CHAIN_URL_HOSTNAME,
    CERT_CHAIN_URL_PORT, CERT_CHAIN_URL_STARTPATH,
    CERT_CHAIN_DOMAIN, CHARACTER_ENCODING,
    MAX_TIMESTAMP_TOLERANCE_IN_MILLIS,
    DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS)

if typing.TYPE_CHECKING:
    from typing import Dict, Any
    from ask_sdk_model import RequestEnvelope
    from cryptography.x509 import Certificate
    from cryptography.hazmat.backends.interfaces import X509Backend
    from cryptography.hazmat.primitives.asymmetric.padding import (
        AsymmetricPadding)
    from cryptography.hazmat.primitives.hashes import HashAlgorithm


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
        self._cert_cache = {}

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
        cert_url = headers.get(self._signature_cert_chain_url_key)
        signature = headers.get(self._signature_key)

        if cert_url is None or signature is None:
            raise VerificationException(
                "Missing Signature/Certificate for the skill request")

        cert_chain = self._retrieve_and_validate_certificate_chain(cert_url)

        self._valid_request_body(
            cert_chain, signature, serialized_request_env)

    def _retrieve_and_validate_certificate_chain(self, cert_url):
        # type: (str) -> Certificate
        """Retrieve and validate certificate chain.

        This method validates if the URL is valid and loads and
        validates the certificate chain, before returning it.

        :param cert_url: URL for retrieving certificate chain
        :type cert_url: str
        :return The certificate chain loaded from the URL
        :rtype cryptography.x509.Certificate
        :raises: :py:class:`VerificationException` if the URL is invalid,
            if the loaded certificate chain is invalid
        """
        self._validate_certificate_url(cert_url)

        cert_chain = self._load_cert_chain(cert_url)
        self._validate_cert_chain(cert_chain)
        return cert_chain

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

    def _load_cert_chain(self, cert_url, x509_backend=default_backend()):
        # type: (str, X509Backend) -> Certificate
        """Loads the certificate chain from the URL.

        This method loads the certificate chain from the certificate
        cache. If there is a cache miss, the certificate chain is
        loaded from the certificate URL using the
        :py:func:`cryptography.x509.load_pem_x509_certificate` method.
        The x509 backend is set as default to the
        :py:class:`cryptography.hazmat.backends.default_backend`
        instance. A :py:class:`VerificationException` is raised if the
        certificate cannot be loaded.

        :param cert_url: URL for retrieving certificate chain
        :type cert_url: str
        :param x509_backend: Backend to be used, for loading pem x509
            certificate
        :type x509_backend:
            cryptography.hazmat.backends.interfaces.X509Backend
        :return: Certificate chain loaded from cache or URL
        :rtype cryptography.x509.Certificate
        :raises: :py:class:`VerificationException` if unable to load the
            certificate
        """
        try:
            if cert_url in self._cert_cache:
                return self._cert_cache.get(cert_url)
            else:
                with urlopen(cert_url) as cert_response:
                    cert_data = cert_response.read()
                    x509_certificate = load_pem_x509_certificate(
                        cert_data, x509_backend)
                    self._cert_cache[cert_url] = x509_certificate
                    return x509_certificate
        except ValueError as e:
            raise VerificationException(
                "Unable to load certificate from URL", e)

    def _validate_cert_chain(self, cert_chain):
        # type: (Certificate) -> None
        """Validate the certificate chain.

        This method checks if the passed in certificate chain is valid,
        i.e it is not expired and the Alexa domain is present in the
        SAN extensions of the certificate chain. A
        :py:class:`VerificationException` is raised if the certificate
        chain is not valid.

        :param cert_chain: Certificate chain to be validated
        :type cert_chain: cryptography.x509.Certificate
        :return: None
        :raises: :py:class:`VerificationException` if certificated is
            not valid
        """
        now = datetime.utcnow()
        if not (cert_chain.not_valid_before <= now <=
                cert_chain.not_valid_after):
            raise VerificationException("Signing Certificate expired")

        ext = cert_chain.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        if CERT_CHAIN_DOMAIN not in ext.value.get_values_for_type(
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
        public_key = cert_chain.public_key()
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
            self, tolerance_in_millis=DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS):
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
        if tolerance_in_millis > MAX_TIMESTAMP_TOLERANCE_IN_MILLIS:
            raise VerificationException(
                "Provided tolerance value {} exceeds the maximum allowed "
                "value {}".format(
                    tolerance_in_millis, MAX_TIMESTAMP_TOLERANCE_IN_MILLIS))

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
        request_timestamp = deserialized_request_env.request.timestamp
        if (abs((local_now - request_timestamp).seconds) >
                (self._tolerance_in_millis / 1000)):
            raise VerificationException("Timestamp verification failed")
