import typing
from abc import ABCMeta, abstractmethod

from ask_sdk_model_runtime import (DefaultApiClient, DefaultSerializer,
                                   ApiConfiguration,
                                   AuthenticationConfiguration)
from ask_smapi_model.services.skill_management import (
    SkillManagementServiceClient)

if typing.TYPE_CHECKING:
    from ask_sdk_model_runtime import ApiClient, Serializer

DEFAULT_API_ENDPOINT = "https://api.amazonalexa.com"

from .smapi_builder import SmapiClientBuilder

class StandardSmapiClientBuilder(SmapiClientBuilder):
    """Standard SmapiClient Builder class used to generate
    :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
    object with default Serializer and ApiClient implementations.
    :param client_id: The ClientId value from LWA profiles.
    :type client_id: str
    :param client_secret: The ClientSecret value from LWA profiles.
    :type client_secret: str
    :param refresh_token: Client refresh_token required to get access token
        for API calls.
    :type refresh_token: str
    """

    def __init__(self, client_id, client_secret, refresh_token):
        # type: (str, str, str) -> None
        """Smapi Builder class used to generate
        :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        object with default Serializer and ApiClient implementations.

        :param client_id: The ClientId value from LWA profiles.
        :type client_id: str
        :param client_secret: The ClientSecret value from LWA profiles.
        :type client_secret: str
        :param refresh_token: Client refresh_token required to get access token
        for API calls.
        """
        super(StandardSmapiClientBuilder, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def client(self):
        # type: () -> SkillManagementServiceClient
        """Creates the smapi client object using AuthenticationConfiguration
        and ApiConfiguration registered values.

        :return: A smapi object that can be used for making SMAPI method
            invocations.
        :rtype: :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        """
        if self.api_endpoint is None:
            self.api_endpoint = DEFAULT_API_ENDPOINT

        api_configuration = ApiConfiguration(serializer=DefaultSerializer(),
                                             api_client=DefaultApiClient(),
                                             api_endpoint=self.api_endpoint)

        authentication_configuration = AuthenticationConfiguration(
            client_id=self.client_id, client_secret=self.client_secret,
            refresh_token=self.refresh_token)

        return SkillManagementServiceClient(
            api_configuration=api_configuration,
            authentication_configuration=authentication_configuration)