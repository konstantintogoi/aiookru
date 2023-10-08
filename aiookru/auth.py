"""ok.ru API authorization."""
import logging
from typing import Any, Dict, Tuple

from httpx import AsyncClient

log = logging.getLogger(__name__)


class Grant:
    """Authorization Grant."""

    __slots__ = ('_client_id', '_auth_client')

    def __init__(self, client_id: str) -> None:
        """Set app info."""
        self._client_id = client_id
        self._auth_client = AsyncClient(
            default_encoding='application/json;charset=utf-8',
            follow_redirects=True,
        )

    async def __aenter__(self) -> 'Grant':
        """Enter."""
        await self.authorize()
        if not self._auth_client.is_closed:
            await self._auth_client.aclose()
        return self

    async def __aexit__(self, *args: Tuple[Any, Any, Any]) -> None:
        """Exit."""
        if not self._auth_client.is_closed:
            await self._auth_client.aclose()

    async def authorize(self) -> 'Grant':
        """Authorizate."""
        return self


class CodeGrant(Grant):
    """Session with authorization with OAuth 2.0 (Authorization Code Grant).

    The Authorization Code grant is used by confidential and public
    clients to exchange an authorization code for an access token.

    .. _OAuth 2.0 Authorization Code Grant
        https://oauth.net/2/grant-types/authorization-code/

    .. _Серверная OAuth авторизация
        https://apiok.ru/ext/oauth/server

    """

    __slots__ = (
        '_code',
        '_redirect_uri',
        '_application_secret_key',
        'access_token',
        'refresh_token',
        'expires_in',
    )

    def __init__(
            self,
            client_id: str,
            application_secret_key: str,
            redirect_uri: str,
            code: str,
        ) -> None:
        """Set credentials."""
        super().__init__(client_id=client_id)
        self._application_secret_key = application_secret_key
        self._redirect_uri = redirect_uri
        self._code = code

    async def authorize(self) -> 'CodeGrant':
        """Authorize with OAuth 2.0 (Authorization Code).

        Returns:
            CodeGrant

        """
        resp = await self._auth_client.post(
            'https://api.ok.ru/oauth/token.do',
            data={
                'code': self._code,
                'client_id': self._client_id,
                'client_secret': self._application_secret_key,
                'redirect_uri': self._redirect_uri,
                'grant_type': 'authorization_code',
            },
        )

        resp.raise_for_status()

        try:
            respjson: Dict[str, Any] = resp.json()
        except Exception:
            content = resp.read().decode()
            log.error(f'GET {resp.url} {resp.status_code}: {content}')
            raise

        try:
            self.access_token = respjson['access_token']
            self.refresh_token = respjson['refresh_token']
            self.expires_in = respjson['expires_in']
        except KeyError as e:
            raise KeyError(*e.args, respjson) from e

        return self


class RefreshGrant(Grant):
    """Session with authorization with OAuth 2.0 (Refresh Token).

    The Refresh Token grant type is used by clients to exchange
    a refresh token for an access token when the access token has expired.

    .. _OAuth 2.0 Refresh Token
        https://oauth.net/2/grant-types/refresh-token/

    .. _Использование refresh_token
        https://apiok.ru/ext/oauth/server

    """

    __slots__ = (
        '_application_secret_key',
        '_refresh_token',
        'token_type',
        'expires_in',
        'access_token',
    )

    def __init__(
            self,
            client_id: str,
            application_secret_key: str,
            refresh_token: str,
        ) -> None:
        """Set credentials."""
        super().__init__(client_id=client_id)
        self._application_secret_key = application_secret_key
        self._refresh_token = refresh_token

    async def authorize(self) -> 'RefreshGrant':
        """Authorize with OAuth 2.0 (Refresh Token)."""
        resp = await self._auth_client.post(
            'https://api.ok.ru/oauth/token.do',
            data={
                'client_id': self._client_id,
                'client_secret': self._application_secret_key,
                'refresh_token': self._refresh_token,
                'grant_type': 'refresh_token',
            },
        )

        resp.raise_for_status()

        try:
            respjson: Dict[str, Any] = resp.json()
        except Exception:
            content = resp.read().decode()
            log.error(f'GET {resp.url} {resp.status_code}: {content}')
            raise

        try:
            self.access_token = respjson['access_token']
            self.token_type = respjson['token_type']
            self.expires_in = respjson['expires_in']
        except KeyError as e:
            raise KeyError(*e.args, respjson) from e

        return self
