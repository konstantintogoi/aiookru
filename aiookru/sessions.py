"""Sessions."""
import logging
from enum import Enum
from hashlib import md5
from typing import Any, Dict, Generator, Tuple

from httpx import AsyncClient, Response

log = logging.getLogger(__name__)


class SignatureCircuit(Enum):
    """Signature circuit."""

    UNDEFINED = 0
    CLIENT_SERVER = 1
    SERVER_SERVER = 2


class Session:
    """A wrapper for `httpx.AsyncClient`.

    Attributes:
        client (AsyncClient): async client with default base url and encoding

    """

    __slots__ = ('client', 'raise_for_status')

    def __init__(
        self,
        raise_for_status: bool = True,
        base_url: str = 'https://api.ok.ru/fb.do',
        default_encoding: str = 'application/json;charset=utf-8',
    ) -> None:
        """Set base url and encoding."""
        self.raise_for_status = raise_for_status
        self.client = AsyncClient(
            default_encoding=default_encoding,
            follow_redirects=True,
            base_url=base_url,
        )


class PublicSession(Session):
    """Session for public API methods of OK API."""

    async def __aenter__(self) -> 'PublicSession':
        """Enter."""
        return self

    async def __aexit__(self, *args: Tuple[Any, Any, Any]) -> None:
        """Exit."""
        await self.close()

    def __await__(self) -> Generator[Any, None, 'PublicSession']:
        """Make `PublicSession` awaitable."""
        yield self

    async def close(self) -> None:
        """Close."""
        if self.client.is_closed is False:
            await self.client.aclose()

    async def request(
        self,
        path: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Request public data.

        Args:
            path (str): path
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        Raises:
            HTTPStatusError: if one occured

        """
        try:
            resp: Response = await self.client.get(path, params=params)
        except Exception:
            log.error(f'GET {path} request failed')
            raise
        else:
            log.info(f'GET {resp.url} {resp.status_code}')

        if self.raise_for_status:
            resp.raise_for_status()

        try:
            return resp.json()
        except Exception:
            content = resp.read().decode()
            log.error(f'GET {resp.url} {resp.status_code}: {content}')
            raise


class TokenSession(PublicSession):
    """Session for executing authorized requests."""

    ERROR = 'Invalid signature circuit. See https://apiok.ru/dev/methods/.'

    __slots__ = (
        'app_id',
        'app_key',
        'app_secret_key',
        'access_token',
        'session_secret_key',
        'format',
    )

    def __init__(
            self,
            app_id: str,
            app_key: str,
            app_secret_key: str,
            access_token: str,
            session_secret_key: str,
            format='json',  # noqa: A002
            raise_for_status: bool = True,
        ):
        """Set credentials."""
        super().__init__(raise_for_status)
        self.app_id = app_id
        self.app_key = app_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token
        self.session_secret_key = session_secret_key
        self.format = format

    async def __aenter__(self) -> 'TokenSession':
        """Enter."""
        return await self.authorize()

    def __await__(self) -> Generator[Any, None, 'TokenSession']:
        """Make `TokenSession` awaitable."""
        return self.authorize().__await__()

    @property
    def session_key(self) -> str:
        """Access token."""
        return self.access_token

    @session_key.setter
    def session_key(self, session_key: str) -> None:
        """Set access token."""
        self.access_token = session_key

    @property
    def required_params(self) -> Dict[str, str]:
        """Required parameters."""
        return {'application_key': self.app_key, 'format': self.format}

    @property
    def sig_circuit(self) -> SignatureCircuit:
        """Signature circuit."""
        if self.app_secret_key and self.access_token and self.app_key:
            return SignatureCircuit.SERVER_SERVER
        elif self.session_secret_key and self.access_token and self.app_key:
            return SignatureCircuit.CLIENT_SERVER
        else:
            return SignatureCircuit.UNDEFINED

    @property
    def secret_key(self) -> str:
        """Secret key according to signature circuit."""
        if self.sig_circuit is SignatureCircuit.CLIENT_SERVER:
            return self.session_secret_key
        elif self.sig_circuit is SignatureCircuit.SERVER_SERVER:
            plain = self.access_token + self.app_secret_key
            return md5(plain.encode('utf-8')).hexdigest().lower()
        else:
            return ''

    async def authorize(self) -> 'TokenSession':
        """Authorize."""
        return self

    def params2str(self, params: Dict[str, Any]) -> str:
        """Join query parametrs and secret key."""
        query = ''.join(k + '=' + str(params[k]) for k in sorted(params))
        return query + self.secret_key

    def sign_params(self, params: Dict[str, Any]) -> str:
        """Sign query parameters."""
        query = self.params2str(params)
        return md5(query.encode('utf-8')).hexdigest()

    async def request(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:  # noqa
        """Send a request.

        Args:
            path (str): path
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        """
        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)
        signature = self.sign_params(params)
        params.update({'sig': signature, 'access_token': self.access_token})
        return await super().request(path, params)


class ClientSession(TokenSession):
    """`TokenSession` with client-server signature circuit."""

    ERROR = 'Empty "session_secret_key" and/or "access_token"'

    def __init__(
            self,
            app_id: str,
            app_key: str,
            access_token: str,
            session_secret_key: str,
            format='json',  # noqa: A002
        ):
        """Set credentials."""
        super().__init__(
            app_id=app_id,
            app_key=app_key,
            app_secret_key='',
            access_token=access_token,
            session_secret_key=session_secret_key,
            format=format,
        )


class ServerSession(TokenSession):
    """`TokenSession` with server-server signature circuit."""

    ERROR = 'Empty "app_secret_key" and/or "access_token"'

    def __init__(
            self,
            app_id: str,
            app_key: str,
            app_secret_key: str,
            access_token: str,
            format: str = 'json',  # noqa: A002
        ):
        """Set credentials."""
        super().__init__(
            app_id=app_id,
            app_key=app_key,
            app_secret_key=app_secret_key,
            access_token=access_token,
            session_secret_key='',
            format=format,
        )


class CodeSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Authorization Code Grant).

    The Authorization Code grant is used by confidential and public
    clients to exchange an authorization code for an access token.

    .. _OAuth 2.0 Authorization Code Grant
        https://oauth.net/2/grant-types/authorization-code/

    .. _Серверная OAuth авторизация
        https://apiok.ru/ext/oauth/server

    """

    __slots__ = (
        'code', 'redirect_uri', 'refresh_token', 'token_type', 'expires_in',
    )

    def __init__(
            self,
            app_id: str,
            app_key: str,
            app_secret_key: str,
            code: str,
            redirect_uri: str,
            format='json',  # noqa: A002
            raise_for_status: bool = True,
        ) -> None:
        """Set credentials."""
        super().__init__(
            app_id=app_id,
            app_key=app_key,
            app_secret_key=app_secret_key,
            access_token='',
            session_secret_key='',
            format=format,
            raise_for_status=raise_for_status,
        )
        self.code = code
        self.redirect_uri = redirect_uri

    @property
    def params(self) -> Dict[str, str]:
        """Authorization request's parameters."""
        return {
            'code': self.code,
            'client_id': self.app_id,
            'client_secret': self.secret_key,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }

    async def authorize(self) -> 'CodeSession':
        """Authorize with OAuth 2.0 (Authorization Code).

        Returns:
            CodeSession

        """
        async with AsyncClient(follow_redirects=True, default_encoding='application/json;charset=utf-8') as cli:  # noqa
            resp = await cli.post('https:/api.ok.ru/oauth/token.do', data=self.params)  # noqa

            if self.raise_for_status:
                resp.raise_for_status()

            try:
                respjson: Dict[str, Any] = resp.json()
            except Exception:
                content = resp.read().decode()
                log.error(f'GET {resp.url} {resp.status_code}: {content}')
                raise

            self.access_token = respjson.get('access_token', '')
            self.token_type = respjson.get('token_type', '')
            self.refresh_token = respjson.get('refresh_token', '')
            self.expires_in = respjson.get('expires_in', '')

        return self


class PasswordSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Password Grant).

    The Password grant type is a way to exchange a user's credentials
    for an access token.

    .. _OAuth 2.0 Password Grant
        https://oauth.net/2/grant-types/password/

    """

    __slots__ = ('login', 'passwd')

    def __init__(
            self,
            app_id: str,
            app_key: str,
            app_secret_key: str,
            login: str,
            passwd: str,
            format: str = 'json',  # noqa: A002
            raise_for_status: bool = True,
        ) -> None:
        """Set credentials."""
        super().__init__(
            app_id=app_id,
            app_key=app_key,
            app_secret_key=app_secret_key,
            access_token='',
            session_secret_key='',
            format=format,
            raise_for_status=raise_for_status,
        )
        self.login = login
        self.passwd = passwd

    @property
    def params(self) -> Dict[str, Any]:
        """Authorization request's parameters."""
        return {
            'method': 'auth.login',
            'application_key': self.app_key,
            'user_name': self.login,
            'password': self.passwd,
            'verification_supported': 1,
            'verification_supported_v': 1,
            'format': 'json',
        }

    async def authorize(self) -> 'PasswordSession':
        """Authorize with OAuth 2.0 (Password Grant).

        Returns:
            PasswordSession

        """
        content = await super().request('', self.params)

        self.access_token = content.get('session_key', '')
        self.session_secret_key = content.get('session_secret_key', '')

        return self


class RefreshSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Refresh Token).

    The Refresh Token grant type is used by clients to exchange
    a refresh token for an access token when the access token has expired.

    .. _OAuth 2.0 Refresh Token
        https://oauth.net/2/grant-types/refresh-token/

    .. _Использование refresh_token
        https://apiok.ru/ext/oauth/server

    """

    __slots__ = ('refresh_token', 'token_type', 'expires_in')

    def __init__(
            self,
            app_id,
            app_key,
            app_secret_key,
            refresh_token,
            format='json',  # noqa: A002
            raise_for_status: bool = True,
        ) -> None:
        """Set credentials."""
        super().__init__(
            app_id=app_id,
            app_key=app_key,
            app_secret_key=app_secret_key,
            access_token='',
            session_secret_key='',
            format=format,
            raise_for_status=raise_for_status,
        )
        self.refresh_token = refresh_token
        self.token_type = ''
        self.expires_in = 0

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'refresh_token': self.refresh_token,
            'client_id': self.app_id,
            'client_secret': self.secret_key,
            'grant_type': 'refresh_token',
        }

    async def authorize(self):
        """Authorize with OAuth 2.0 (Refresh Token)."""
        async with AsyncClient(follow_redirects=True, default_encoding='application/json;charset=utf-8') as cli:  # noqa
            resp = await cli.post('https://api.ok.ru/oauth/token.do', data=self.params)  # noqa

            if self.raise_for_status:
                resp.raise_for_status()

            try:
                respjson: Dict[str, Any] = resp.json()
            except Exception:
                content = resp.read().decode()
                log.error(f'GET {resp.url} {resp.status_code}: {content}')
                raise

            self.access_token = respjson.get('access_token', '')
            self.token_type = respjson.get('token_type', '')
            self.expires_in = respjson.get('expires_in', '')

        return self
