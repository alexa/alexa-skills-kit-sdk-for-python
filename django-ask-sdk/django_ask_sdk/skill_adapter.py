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
import logging

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    JsonResponse, HttpResponseBadRequest, HttpResponseServerError)

from ask_sdk_webservice_support.webservice_handler import (
    WebserviceSkillHandler)
from ask_sdk_webservice_support.verifier import (
    VerificationException, RequestVerifier)
from ask_sdk_webservice_support import verifier_constants
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_core.skill import CustomSkill

if typing.TYPE_CHECKING:
    from typing import List
    from django.http import HttpRequest, HttpResponse
    from ask_sdk_webservice_support.verifier import AbstractVerifier

#: ``Signature Certificate Chain URL`` header key in Django HTTP Headers.
#: This is different from the `header key <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request>`__
#: provided by Alexa, because of Django's HTTP
#: `Meta headers <https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.HttpRequest.META>`__.
SIGNATURE_CERT_CHAIN_URL_KEY = "HTTP_SIGNATURECERTCHAINURL"

#: ``Signature`` header key in Django HTTP Headers. This is different from
#: the `header key <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html#checking-the-signature-of-the-request>`__
#: provided by Alexa, because of Django's HTTP
#: `Meta headers <https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.HttpRequest.META>`__.
SIGNATURE_KEY = "HTTP_SIGNATURE"

logger = logging.getLogger("django.ask-sdk")


class SkillAdapter(View):
    """Provides a base interface to register skill and dispatch the request.

    The class constructor takes a
    :py:class:`ask_sdk_core.skill.CustomSkill` instance, an optional
    verify_request boolean, an optional verify_timestamp boolean and
    an optional list of
    :py:class:`ask_sdk_webservice_support.verifier.AbstractVerifier`
    instances.

    The :meth:`post` function is the only available method on the view,
    that intakes the input POST request from Alexa, verifies the request
    and dispatch it to the skill.

    By default, the
    :py:class:`ask_sdk_webservice_support.verifier.RequestVerifier` and
    :py:class:`ask_sdk_webservice_support.verifier.TimestampVerifier`
    instances are added to the skill verifier list. To disable this, set
    the ``verify_request`` and ``verify_timestamp`` input arguments to
    ``False`` respectively.

    For example, if you developed a skill using an instance
    of :py:class:`ask_sdk_core.skill_builder.SkillBuilder` or it's
    subclasses, then to register it as an endpoint in your django
    app ``example``, you can add the following in ``example.urls.py``:

    .. code-block:: python

        import skill
        from django_ask_sdk.skill_response import SkillAdapter

        view = SkillAdapter.as_view(skill=skill.sb.create())

        urlpatterns = [
            path("/myskill", view, name='index')
        ]
    """
    # Creating class attributes, since Django View `as_view` method
    # sets these from __init__ only if they exist on the class.
    skill = None
    verify_signature = None
    verify_timestamp = None
    verifiers = None

    def __init__(
            self, skill, verify_signature=True, verify_timestamp=True,
            verifiers=None):
        # type: (CustomSkill, bool, bool, List[AbstractVerifier]) -> None
        """Instantiate the view and set the verifiers on the handler.

        :param skill: A :py:class:`ask_sdk_core.skill.CustomSkill`
            instance. If you are using the skill builder from ask-sdk,
            then you can use the ``create`` method under it, to create a
            skill instance
        :type skill: ask_sdk_core.skill.CustomSkill
        :param verify_signature: Enable request signature verification
        :type verify_signature: bool
        :param verify_timestamp: Enable request timestamp verification
        :type verify_timestamp: bool
        :param verifiers: An optional list of verifiers, that needs to
            be applied on the input request, before invoking the
            request handlers. For more information, look at
            `hosting the skill as webservice <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>`_
        :type verifiers:
            list[ask_sdk_webservice_support.verifier.AbstractVerifier]
        :raises: :py:class:`TypeError` if
            the provided skill instance is not a
            :py:class:`ask_sdk_core.skill.CustomSkill` instance
        """
        self._skill = skill

        if not isinstance(skill, CustomSkill):
            raise TypeError(
                "Invalid skill instance provided. Expected a custom "
                "skill instance.")

        if verifiers is None:
            verifiers = []

        self._verifiers = verifiers

        if verify_signature:
            request_verifier = RequestVerifier(
                signature_cert_chain_url_key=SIGNATURE_CERT_CHAIN_URL_KEY,
                signature_key=SIGNATURE_KEY)
            self._verifiers.append(request_verifier)

        self._webservice_handler = WebserviceSkillHandler(
            skill=self._skill, verify_signature=False,
            verify_timestamp=verify_timestamp,
            verifiers=self._verifiers
        )
        self._webservice_handler._add_custom_user_agent("django-ask-sdk")

        super(SkillAdapter, self).__init__()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # type: (HttpRequest, object, object) -> HttpResponse
        """Inspect the HTTP method and delegate to the view method.

        This is the default implementation of the
        :py:class:`django.views.View` method, which will inspect the
        HTTP method in the input request and delegate it to the
        corresponding method in the view. The only allowed method on
        this view is ``post``.

        :param request: The input request sent to the view
        :type request: django.http.HttpRequest
        :return: The response from the view
        :rtype: django.http.HttpResponse
        :raises: :py:class:`django.http.HttpResponseNotAllowed` if the
            method is invoked for other than HTTP POST request.
            :py:class:`django.http.HttpResponseBadRequest` if the
            request verification fails.
            :py:class:`django.http.HttpResponseServerError` for any
            internal exception.
        """
        return super(SkillAdapter, self).dispatch(request)

    def post(self, request, *args, **kwargs):
        # type: (HttpRequest, object, object) -> HttpResponse
        """The method that handles HTTP POST request on the view.

        This method is called when the view receives a HTTP POST
        request, which is generally the request sent from Alexa during
        skill invocation. The request is verified through the
        registered list of verifiers, before invoking the request
        handlers. The method returns a
        :py:class:`django.http.JsonResponse` in case of successful
        skill invocation.

        :param request: The input request sent by Alexa to the skill
        :type request: django.http.HttpRequest
        :return: The response from the skill to Alexa
        :rtype: django.http.JsonResponse
        :raises: :py:class:`django.http.HttpResponseBadRequest` if the
            request verification fails.
            :py:class:`django.http.HttpResponseServerError` for any
            internal exception.
        """
        try:
            content = request.body.decode(
                verifier_constants.CHARACTER_ENCODING)
            response = self._webservice_handler.verify_request_and_dispatch(
                http_request_headers=request.META, http_request_body=content)

            return JsonResponse(
                data=response, safe=False)
        except VerificationException:
            logger.exception(msg="Request verification failed")
            return HttpResponseBadRequest(
                content="Incoming request failed verification")
        except AskSdkException:
            logger.exception(msg="Skill dispatch exception")
            return HttpResponseServerError(
                content="Exception occurred during skill dispatch")
