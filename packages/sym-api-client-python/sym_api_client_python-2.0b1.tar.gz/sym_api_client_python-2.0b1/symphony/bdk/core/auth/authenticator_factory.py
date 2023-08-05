"""Module for instantiating various authenticator objects.
"""
from symphony.bdk.core.auth.bot_authenticator import BotAuthenticator, BotAuthenticatorRsa
from symphony.bdk.core.auth.exception import AuthInitializationError
from symphony.bdk.core.auth.ext_app_authenticator import ExtensionAppAuthenticator, ExtensionAppAuthenticatorRsa
from symphony.bdk.core.auth.obo_authenticator import OboAuthenticator, OboAuthenticatorRsa
from symphony.bdk.core.client.api_client_factory import ApiClientFactory
from symphony.bdk.core.config.model.bdk_config import BdkConfig
from symphony.bdk.gen.login_api.authentication_api import AuthenticationApi
from symphony.bdk.gen.pod_api.pod_api import PodApi


class AuthenticatorFactory:
    """Authenticator Factory class

    Provides new instances for the main authenticators:
        - :class:`symphony.bdk.core.auth.bot_authenticator.BotAuthenticator`: to authenticate the main Bot service
          account
        - :class:`symphony.bdk.core.auth.obo_authenticator.OboAuthenticator`: to perform on-behalf-of authentication
        - :class:`symphony.bdk.core.auth.ext_app_authenticator.ExtensionAppAuthenticator`: to perform extension
          application authentication
    """

    def __init__(self, config: BdkConfig, api_client_factory: ApiClientFactory):
        """

        :param config: the bot configuration
        :param api_client_factory: the :class:`symphony.bdk.core.client.api_client_factory.ApiClientFactory` instance to
          create the BotAuthenticator from.
        """
        self._config = config
        self._api_client_factory = api_client_factory

    def get_bot_authenticator(self) -> BotAuthenticator:
        """Creates a new instance of a Bot Authenticator service.

        :return: a new :class:`symphony.bdk.core.auth.bot_authenticator.BotAuthenticator` instance.
        """
        if self._config.bot.is_rsa_configuration_valid():
            return BotAuthenticatorRsa(
                bot_config=self._config.bot,
                login_api_client=self._api_client_factory.get_login_client(),
                relay_api_client=self._api_client_factory.get_relay_client()
            )
        raise AuthInitializationError("RSA authentication should be configured. Only one field among private key "
                                      "path or content should be configured for bot authentication.")

    def get_obo_authenticator(self) -> OboAuthenticator:
        """Creates a new instance of a Obo Authenticator service.

        :return: a new :class:`symphony.bdk.core.auth.obo_authenticator.OboAuthenticator` instance.
        """
        if self._config.app.is_rsa_configuration_valid():
            return OboAuthenticatorRsa(
                app_config=self._config.app,
                login_api_client=self._api_client_factory.get_login_client()
            )
        raise AuthInitializationError("Application under 'app' field should be configured with a private key path or "
                                      "content in order to use OBO authentication.")

    def get_extension_app_authenticator(self) -> ExtensionAppAuthenticator:
        """Creates a new instance of an extension app authenticator service.

        :return: a new :class:`symphony.bdk.core.auth.ext_app_authenticator.ExtensionAppAuthenticator` instance.
        """
        if self._config.app.is_rsa_configuration_valid():
            return ExtensionAppAuthenticatorRsa(
                AuthenticationApi(self._api_client_factory.get_login_client()),
                PodApi(self._api_client_factory.get_pod_client()),
                self._config.app.app_id,
                self._config.app.private_key
            )
        raise AuthInitializationError("Application under 'app' field should be configured with a private key path or "
                                      "content in order to authenticate extension app.")
