# -*- coding: utf-8 -*-
#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights
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

if typing.TYPE_CHECKING:
    from typing import List, Tuple


def get_header_value(header_list, key):
    # type: (List[Tuple[str, str]], str) -> List[str]
    """Filter the header_list with provided key value.

    This method is used to parse through the header list obtained from the
    SMAPI response header object and retrieve list of specific tuple objects
    with keys like Location, RequestId etc if present.

    :param header_list: The list of response headers returned from Alexa
        SKill Management API calls.
    :type: List[Tuple[str, str]]
    :param key: The field value which needs to be retrieved.
    :type: str
    :return: Returns the list field values if present, since there maybe
        multiple tuples with same key values.
    :rtype: List[Union[None,str]]
    """
    header_value = []  # type: List
    if not header_list or key is None:
        return header_value
    return list(map(lambda x: x[1], filter(lambda x: x[0] == key, header_list)))
