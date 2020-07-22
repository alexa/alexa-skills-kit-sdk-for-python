# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#

import typing
from ask_sdk_model.slot_value import SlotValue


if typing.TYPE_CHECKING:
    from typing import Dict, Optional


class InvalidSlotValue(SlotValue):
    deserialized_types = {
        'object_type': 'str',
        'value': 'str'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'value': 'value'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, value=None):
        # type: (Optional[str]) -> None
        """Slot value containing a list of other slot value objects.

        :param values: An array containing the values captured for this slot.
        :type values: (optional) list[ask_sdk_model.slot_value.SlotValue]
        """
        self.__discriminator_value = "Invalid"  # type: str

        self.object_type = self.__discriminator_value
        super(InvalidSlotValue, self).__init__(object_type=self.__discriminator_value)
        self.value = value
