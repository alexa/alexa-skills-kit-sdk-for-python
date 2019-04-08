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

from ask_sdk_model.request_envelope import RequestEnvelope
from ask_sdk_model.session import Session
from ask_sdk_core.attributes_manager import (
    AttributesManager, AttributesManagerException)
from .data.mock_persistence_adapter import MockPersistenceAdapter


class TestAttributesManager(unittest.TestCase):
    def test_attributes_manager_with_no_request_envelope(self):
        with self.assertRaises(AttributesManagerException) as exc:
            self.attributes_manager = AttributesManager(
                request_envelope=None)

        assert "RequestEnvelope cannot be none!" in str(exc.exception), (
            "AttributesManager should raise error when requestEnvelope is "
            "none")

    def test_get_initial_request_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        assert attributes_manager.request_attributes == {}, (
            "AttributesManager fails to set the initial request attributes "
            "to be {}")

    def test_get_session_attributes_from_in_session_request_envelope(self):
        session = Session(
            new=None, session_id=None, user=None,
            attributes={"mockKey": "mockValue"}, application=None)
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        assert attributes_manager.session_attributes == {
            "mockKey": "mockValue"}, (
            "AttributesManager fails to get session attributes from in "
            "session request envelope")

    def test_get_default_session_attributes_from_new_session_request_envelope(self):
        session = Session(
            new=True, session_id=None, user=None,
            attributes=None, application=None)
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        assert attributes_manager.session_attributes == {}, (
            "AttributesManager fails to get default session attributes from "
            "new session request envelope")

    def test_get_session_attributes_from_out_of_session_request_envelope(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        attributes_manager._request_envelope.session = None
        with self.assertRaises(AttributesManagerException) as exc:
            test_session_attributes = attributes_manager.session_attributes

        assert "Cannot get SessionAttributes from out of session request!" in str(exc.exception), (
            "AttributesManager should raise error when trying to get session "
            "attributes from out of session envelope")

    def test_get_persistent_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        assert attributes_manager.persistent_attributes == {
            "key_1": "v1", "key_2": "v2"}, (
            "AttributesManager fails to get persistent attributes from "
            "persistent adapter")

    def test_get_persistent_attributes_without_persistence_adapter(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        with self.assertRaises(AttributesManagerException) as exc:
            test_persistent_attributes = attributes_manager.persistent_attributes

        assert "Cannot get PersistentAttributes without Persistence adapter" in str(exc.exception), (
            "AttributesManager should raise error when trying to get "
            "persistent attributes without persistence adapter")

    def test_set_request_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)
        attributes_manager.request_attributes = {"key": "value"}

        assert attributes_manager.request_attributes == {"key": "value"}, (
            "AttributesManager fails to set the request attributes")

    def test_set_session_attributes(self):
        session = Session(
            new=None, session_id=None, user=None,
            attributes={"mockKey": "mockValue"}, application=None)
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        attributes_manager.session_attributes = {
            "mockKey": "updatedMockValue"}

        assert attributes_manager.session_attributes == {
            "mockKey": "updatedMockValue"}, (
            "AttributesManager fails to set the session attributes")

    def test_set_session_attributes_to_out_of_session_request_envelope(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        attributes_manager._request_envelope.session = None
        with self.assertRaises(AttributesManagerException) as exc:
            attributes_manager.session_attributes = {"key": "value"}

        assert "Cannot set SessionAttributes to out of session request!" in str(exc.exception), (
            "AttributesManager should raise error when trying to set session "
            "attributes to out of session request")

    def test_set_persistent_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.persistent_attributes = {"key": "value"}

        assert attributes_manager.persistent_attributes == {
            "key": "value"}, (
            "AttributesManager fails to set the persistent attributes")

    def test_set_persistent_attributes_without_persistence_adapter(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        with self.assertRaises(AttributesManagerException) as exc:
            attributes_manager.persistent_attributes = {"key": "value"}

        assert "Cannot set PersistentAttributes without persistence adapter!" in str(exc.exception), (
            "AttributesManager should raise error when trying to set "
            "persistent attributes without persistence adapter")

    def test_save_persistent_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.persistent_attributes = {"key": "value"}

        attributes_manager.save_persistent_attributes()

        assert attributes_manager._persistence_adapter.attributes == {
            "key": "value"}, (
            "AttributesManager fails to save persistent attributes via "
            "persistence adapter")

    def test_save_persistent_attributes_without_persistence_adapter(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope)

        with self.assertRaises(AttributesManagerException) as exc:
            attributes_manager.save_persistent_attributes()

        assert "Cannot save PersistentAttributes without persistence adapter!" in str(exc.exception), (
            "AttributesManager should raise error when trying to save "
            "persistent attributes without persistence adapter"
        )

    def test_save_persistent_attributes_without_changing_persistent_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.save_persistent_attributes()

        assert attributes_manager._persistence_adapter.attributes == {
            "key_1": "v1", "key_2": "v2"}, (
            "AttributesManager should do nothing if persistent attributes "
            "has not been changed")

    def test_get_persistent_attributes_with_calling_get_persistent_attributes_multiple_times(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.persistent_attributes
        attributes_manager.persistent_attributes
        attributes_manager.persistent_attributes
        attributes_manager.persistent_attributes

        assert attributes_manager._persistence_adapter.get_count == 1, (
            "AttributesManager should make only 1 get_attributes call "
            "during multiple get_persistent_attributes calls")

    def test_delete_persistent_attributes(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.persistent_attributes = {"key": "value"}
        attributes_manager.delete_persistent_attributes()

        assert attributes_manager._persistence_adapter.attributes == {}, (
            "AttributesManager fails to delete persistent attributes via "
            "persistence adapter")

    def test_delete_persistent_attributes_with_calling_delete_persistent_attributes_multiple_times(self):
        session = Session()
        request_envelope = RequestEnvelope(
            version=None, session=session, context=None, request=None)
        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=MockPersistenceAdapter())

        attributes_manager.persistent_attributes = {"key": "value"}

        attributes_manager.delete_persistent_attributes()
        attributes_manager.delete_persistent_attributes()
        attributes_manager.delete_persistent_attributes()
        attributes_manager.delete_persistent_attributes()

        assert attributes_manager._persistence_adapter.del_count == 1, (
            "AttributesManager should make only 1 delete_attributes call "
            "during multiple delete_persistent_attributes calls")