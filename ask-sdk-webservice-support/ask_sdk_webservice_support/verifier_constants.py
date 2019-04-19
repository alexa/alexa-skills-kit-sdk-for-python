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

#: Header key to be used, to retrieve request header that contains the
#: URL for the certificate chain needed to verify the request signature.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request>`__.
SIGNATURE_CERT_CHAIN_URL_HEADER = "SignatureCertChainUrl"

#: Header key to be used, to retrieve request header that contains the
#: request signature.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request>`__.
SIGNATURE_HEADER = "Signature"

#: Case insensitive protocol to be checked on signature certificate url.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#cert-verify-signature-certificate-url>`__.
CERT_CHAIN_URL_PROTOCOL = "https"

#: Case insensitive hostname to be checked on signature certificate url.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#cert-verify-signature-certificate-url>`__.
CERT_CHAIN_URL_HOSTNAME = "s3.amazonaws.com"

#: Path presence to be checked on signature certificate url.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#cert-verify-signature-certificate-url>`__.
CERT_CHAIN_URL_STARTPATH = "/echo.api/"

#: Port to be checked on signature certificate url.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#cert-verify-signature-certificate-url>`__.
CERT_CHAIN_URL_PORT = 443

#: Domain presence check in Subject Alternative Names (SANs) of
#: signing certificate.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request>`__.
CERT_CHAIN_DOMAIN = "echo-api.amazon.com"

#: Character encoding used in the request.
CHARACTER_ENCODING = "utf-8"

#: Default allowable tolerance in request timestamp.
#: For more info, check `link <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#timestamp>`__.
DEFAULT_TIMESTAMP_TOLERANCE_IN_MILLIS = 30000

#: Maximum allowable tolerance in request timestamp.
#: For more info, check `link <https://developer.amazon.com/docs/smapi/skill-events-in-alexa-skills.html#delivery-of-events-to-the-skill>`__.
MAX_TIMESTAMP_TOLERANCE_IN_MILLIS = 3600000
