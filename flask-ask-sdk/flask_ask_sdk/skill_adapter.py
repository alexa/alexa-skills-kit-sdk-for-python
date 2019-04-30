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

from werkzeug import exceptions
from flask import current_app, request as flask_request, jsonify, Response
from ask_sdk_webservice_support.webservice_handler import (
    WebserviceSkillHandler)
from ask_sdk_webservice_support.verifier import (
    AbstractVerifier, VerificationException)
from ask_sdk_webservice_support import verifier_constants
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_core.skill import CustomSkill
from flask import Flask

if typing.TYPE_CHECKING:
    from typing import List

#: Extension name used for saving extension instance in app.extensions
EXTENSION_NAME = "ASK_SDK_SKILL_ADAPTER"

#: Configuration key used for setting request signature verification
VERIFY_SIGNATURE_APP_CONFIG = "ASK_SDK_VERIFY_SIGNATURE"

#: Configuration key used for setting request timestamp verification
VERIFY_TIMESTAMP_APP_CONFIG = "ASK_SDK_VERIFY_TIMESTAMP"


class SkillAdapter(object):
    """Provides a base interface to register skill and dispatch the request.

    The class constructor takes a
    :py:class:`ask_sdk_core.skill.CustomSkill` instance, the skill id,
    an optional list of
    :py:class:`ask_sdk_webservice_support.verifier.AbstractVerifier`
    instances and an optional flask application. One can also use the
    :meth:`init_app` method, to pass in a :py:class:`flask.Flask`
    application instance, to instantiate the config values and the
    webservice handler.

    The :meth:`dispatch_request` function can be used to map the input
    request to the skill invocation. The :meth:`register` function can
    also be used alternatively, to register the :meth:`dispatch_request`
    function to the provided route.

    By default, the
    :py:class:`ask_sdk_webservice_support.verifier.RequestVerifier` and
    :py:class:`ask_sdk_webservice_support.verifier.TimestampVerifier`
    instances are added to the skill verifier list. To disable this, set
    the :py:const:`VERIFY_SIGNATURE_APP_CONFIG` and
    :py:const:`VERIFY_TIMESTAMP_APP_CONFIG` app configuration values to
    ``False``.

    An instance of the extension is added to the application extensions
    mapping, under the key :py:const:`EXTENSION_NAME`. Since multiple
    skills can be configured on different routes in the same application,
    through multiple extension instances, each extension is added as a
    skill id mapping under the app extensions :py:const:`EXTENSION_NAME`
    dictionary.

    For example, to use this class with a skill created using ask-sdk-core:

    .. code-block:: python

        from flask import Flask
        from ask_sdk_core.skill_builder import SkillBuilder
        from flask_ask_sdk.skill_adapter import SkillAdapter

        app = Flask(__name__)
        skill_builder = SkillBuilder()
        # Register your intent handlers to skill_builder object

        skill_adapter = SkillAdapter(
            skill=skill_builder.create(), skill_id=<SKILL_ID>, app=app)

        @app.route("/"):
        def invoke_skill:
            return skill_adapter.dispatch_request()

    Alternatively, you can also use the ``register`` method:

    .. code-block:: python

        from flask import Flask
        from ask_sdk_core.skill_builder import SkillBuilder
        from flask_ask_sdk.skill_adapter import SkillAdapter

        app = Flask(__name__)
        skill_builder = SkillBuilder()
        # Register your intent handlers to skill_builder object

        skill_adapter = SkillAdapter(
            skill=skill_builder.create(), skill_id=<SKILL_ID>, app=app)

        skill_adapter.register(app=app, route="/")
    """

    def __init__(self, skill, skill_id, verifiers=None, app=None):
        # type: (CustomSkill, int, List[AbstractVerifier], Flask) -> None
        """Instantiate the extension and set the app config values.

        :param skill: A :py:class:`ask_sdk_core.skill.CustomSkill`
            instance. If you are using the skill builder from ask-sdk,
            then you can use the ``create`` method under it, to create a
            skill instance
        :type skill: ask_sdk_core.skill.CustomSkill
        :param skill_id: Skill ID for the skill instance. This is used
            to store the skill under the app extensions
        :type skill_id: int
        :param verifiers: An optional list of verifiers, that needs to
            be applied on the input request, before invoking the
            request handlers. For more information, look at
            `hosting the skill as webservice <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>`_
        :type verifiers:
            list[ask_sdk_webservice_support.verifier.AbstractVerifier]
        :param app: A :py:class:`flask.Flask` application instance
        :type app: flask.Flask
        :raises: :py:class:`TypeError` if
            the provided skill instance is not a
            :py:class:`ask_sdk_core.skill.CustomSkill` instance
        """
        self._skill_id = skill_id
        self._skill = skill
        self._webservice_handler = None

        if verifiers is None:
            verifiers = []

        self._verifiers = verifiers

        if not isinstance(skill, CustomSkill):
            raise TypeError(
                "Invalid skill instance provided. Expected a custom "
                "skill instance.")

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # type: (Flask) -> None
        """Register the extension on the given Flask application.

        Use this function only when no Flask application was provided
        in the ``app`` keyword argument to the constructor of this class.

        The function sets ``True`` defaults for
        :py:const:`VERIFY_SIGNATURE_APP_CONFIG` and
        :py:const:`VERIFY_TIMESTAMP_APP_CONFIG` configurations. It adds
        the skill id: self instance mapping to the application
        extensions, and creates a
        :py:class:`ask_sdk_webservice_support.webservice_handler.WebserviceHandler`
        instance, for request verification and dispatch.

        :param app: A :py:class:`flask.Flask` application instance
        :type app: flask.Flask
        :rtype: None
        """
        app.config.setdefault(VERIFY_SIGNATURE_APP_CONFIG, True)
        app.config.setdefault(VERIFY_TIMESTAMP_APP_CONFIG, True)

        if EXTENSION_NAME not in app.extensions:
            app.extensions[EXTENSION_NAME] = {}

        app.extensions[EXTENSION_NAME][self._skill_id] = self

        with app.app_context():
            self._create_webservice_handler(self._skill, self._verifiers)

    def _create_webservice_handler(self, skill, verifiers):
        # type: (CustomSkill, List[AbstractVerifier]) -> None
        """Create the handler for request verification and dispatch.

        :param skill: A :py:class:`ask_sdk_core.skill.CustomSkill`
            instance. If you are using the skill builder from ask-sdk,
            then you can use the ``create`` method under it, to create a
            skill instance
        :type skill: ask_sdk_core.skill.CustomSkill
        :param verifiers: A list of verifiers, that needs to
            be applied on the input request, before invoking the
            request handlers.
        :type verifiers:
            list[ask_sdk_webservice_support.verifier.AbstractVerifier]
        :rtype: None
        """
        if verifiers is None:
            verifiers = []

        self._webservice_handler = WebserviceSkillHandler(
            skill=skill,
            verify_signature=current_app.config.get(
                VERIFY_SIGNATURE_APP_CONFIG, True),
            verify_timestamp=current_app.config.get(
                VERIFY_TIMESTAMP_APP_CONFIG, True),
            verifiers=verifiers)

        self._webservice_handler._add_custom_user_agent("flask-ask-sdk")

    def dispatch_request(self):
        # type: () -> Response
        """Method that handles request verification and routing.

        This method can be used as a function to register on the URL
        rule. The request is verified through the registered list of
        verifiers, before invoking the request handlers. The method
        returns a JSON response for the Alexa service to respond to the
        request.

        :return: The skill response for the input request
        :rtype: flask.Response
        :raises: :py:class:`werkzeug.exceptions.MethodNotAllowed` if the
            method is invoked for other than HTTP POST request.
            :py:class:`werkzeug.exceptions.BadRequest` if the
            verification fails.
            :py:class:`werkzeug.exceptions.InternalServerError` for any
            internal exception.
        """
        if flask_request.method != "POST":
            raise exceptions.MethodNotAllowed()

        try:
            content = flask_request.data.decode(
                verifier_constants.CHARACTER_ENCODING)
            response = self._webservice_handler.verify_request_and_dispatch(
                http_request_headers=flask_request.headers,
                http_request_body=content)

            return jsonify(response)
        except VerificationException:
            current_app.logger.error(
                "Request verification failed", exc_info=True)
            raise exceptions.BadRequest(
                description="Incoming request failed verification")
        except AskSdkException:
            current_app.logger.error(
                "Skill dispatch exception", exc_info=True)
            raise exceptions.InternalServerError(
                description="Exception occurred during skill dispatch")

    def register(self, app, route, endpoint=None):
        # type: (Flask, str, str) -> None
        """Method to register the routing on the app at provided route.

        This is a utility method, that can be used for registering the
        ``dispatch_request`` on the provided :py:class:`flask.Flask`
        application at the provided URL ``route``.

        :param app: A :py:class:`flask.Flask` application instance
        :type app: flask.Flask
        :param route: The URL rule where the skill dispatch has to be
            registered
        :type route: str
        :param endpoint: The endpoint for the registered URL rule.
            This can be used to set multiple skill endpoints on same app.
        :type endpoint: str
        :rtype: None
        :raises: :py:class:`TypeError` if ``app`` or `route`` is not
            provided or is of an invalid type
        """
        if app is None or not isinstance(app, Flask):
            raise TypeError("Expected a valid Flask instance")

        if route is None or not isinstance(route, str):
            raise TypeError("Expected a valid URL rule string")

        app.add_url_rule(
            route, view_func=self.dispatch_request, methods=["POST"],
            endpoint=endpoint)
