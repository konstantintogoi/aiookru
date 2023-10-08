"""ok.ru API."""
from hashlib import md5
from typing import Any, Dict, Generator, Tuple

from .session import TokenSession


class API:
    """ok.ru API.

    Attributes:
        session (TokenSession): session.

    """

    __slots__ = ('session', )

    def __init__(
        self,
        access_token: str,
        application_key: str,
        session_secret_key: str = '',
        application_secret_key: str = '',
    ):
        """Set session."""
        if session_secret_key:
            secret_key = session_secret_key
        elif application_secret_key:
            plain_secret = access_token + application_secret_key
            secret_key = md5(plain_secret.encode('utf-8')).hexdigest().lower()
        else:
            secret_key = ''
        self.session = TokenSession(
            application_key=application_key,
            access_token=access_token,
            secret_key=secret_key,
        )

    def __await__(self) -> Generator['API', None, None]:
        """Await self."""
        yield self

    async def __aenter__(self) -> 'API':
        """Enter."""
        return self

    async def __aexit__(self, *args: Tuple[Any, Any, Any]) -> None:
        """Exit."""
        if not self.session.client.is_closed:
            await self.session.client.aclose()

    def __getattr__(self, name: str):
        """Return an API method."""
        return APIMethod(self, name)

    async def __call__(self, name: str, **params: Dict[str, Any]) -> 'APIMethod':  # noqa
        """Call an API method by its name.

        Args:
            name (str): full method's name
            params (Dict[str, Any]): query parameters

        Return:
            APIMethod

        """
        return await getattr(self, name)(**params)


class APIMethod:
    """ok.ru REST API method."""

    __slots__ = ('_api', '_name')

    def __init__(self, api: API, name: str):
        """Set method name."""
        self._api = api
        self._name = name

    def __getattr__(self, name):
        """Chain methods.

        Args:
            name (str): method name

        """
        return APIMethod(self._api, f'{self._name}.{name}')

    async def __call__(self, **params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a request.

        Args:
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        """
        params['method'] = self._name
        return await self._api.session.request(params=params)
