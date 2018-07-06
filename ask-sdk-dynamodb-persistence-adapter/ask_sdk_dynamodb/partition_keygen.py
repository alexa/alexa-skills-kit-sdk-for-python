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
import typing

from ask_sdk_core.exceptions import PersistenceException

if typing.TYPE_CHECKING:
    from ask_sdk_model import RequestEnvelope


def user_id_partition_keygen(request_envelope):
    # type: (RequestEnvelope) -> str
    """Retrieve user id from request envelope, to use as partition key.

    :param request_envelope: Request Envelope passed during skill
        invocation
    :type request_envelope: ask_sdk_model.RequestEnvelope
    :return: User Id retrieved from request envelope
    :rtype: str
    :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
    """
    try:
        user_id = request_envelope.context.system.user.user_id
        return user_id
    except AttributeError:
        raise PersistenceException("Couldn't retrieve user id from request "
                                   "envelope, for partition key use")


def device_id_partition_keygen(request_envelope):
    # type: (RequestEnvelope) -> str
    """Retrieve device id from request envelope, to use as partition key.

    :param request_envelope: Request Envelope passed during skill
        invocation
    :type request_envelope: ask_sdk_model.RequestEnvelope
    :return: Device Id retrieved from request envelope
    :rtype: str
    :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
    """
    try:
        device_id = request_envelope.context.system.device.device_id
        return device_id
    except AttributeError:
        raise PersistenceException("Couldn't retrieve device id from "
                                   "request envelope, for partition key use")
