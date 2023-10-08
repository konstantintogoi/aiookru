"""Sessions."""
import logging
from hashlib import md5
from typing import Any, Dict

from httpx import AsyncClient, Response

log = logging.getLogger(__name__)


class Session:
    """A wrapper for `httpx.AsyncClient`.

    Attributes:
        client (AsyncClient): async client with default base url and encoding

    """

    __slots__ = ('client',)

    def __init__(self) -> None:
        """Set base url and encoding."""
        self.client = AsyncClient(
            default_encoding='application/json;charset=utf-8',
            base_url='https://api.ok.ru',
            follow_redirects=True,
        )


class PublicSession(Session):
    """Session for public API methods of OK API."""

    async def request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Request public data.

        Args:
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        Raises:
            HTTPStatusError: if one occured

        """
        try:
            resp: Response = await self.client.get('fb.do', params=params)
        except Exception:
            log.error(f'GET {params["method"]} request failed')
            raise
        else:
            log.info(f'GET {resp.url} {resp.status_code}')

        resp.raise_for_status()

        try:
            return resp.json()
        except Exception:
            content = resp.read().decode()
            log.error(f'GET {resp.url} {resp.status_code}: {content}')
            raise


class TokenSession(PublicSession):
    """Session for executing authorized requests."""

    __slots__ = ('_application_key', '_access_token', '_secret_key')

    def __init__(
        self,
        access_token: str,
        application_key: str,
        secret_key: str,
    ):
        """Set credentials."""
        super().__init__()
        self._application_key = application_key
        self._access_token = access_token
        self._secret_key = secret_key

    async def request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request.

        Args:
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        """
        params['format'] = 'json'
        params['application_key'] = self._application_key
        params = {k: params[k] for k in params if params[k]}
        params['sig'] = self.sign_params(params)
        params['access_token'] = self._access_token
        return await super().request(params)

    def sign_params(self, params: Dict[str, Any]) -> str:
        """Sign query parameters."""
        query = self.params2str(params)
        return md5(query.encode('utf-8')).hexdigest()

    def params2str(self, params: Dict[str, Any]) -> str:
        """Join query parametrs and secret key."""
        query = ''.join(k + '=' + str(params[k]) for k in sorted(params))
        return query + self._secret_key
