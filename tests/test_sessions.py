"""Sessions tests."""
import pytest
from httpx import HTTPStatusError

from aiookru.session import PublicSession, TokenSession


class TestPublicSession:
    """Tests of PublicSession class."""

    @pytest.mark.asyncio
    async def test_error_request(self, error_server, error):
        """Test error request."""
        async with PublicSession() as session:
            session.client.base_url = error_server.url

            session.raise_for_status = False
            response = await session.request('', {})
            assert response == error

    @pytest.mark.asyncio
    async def test_error_request_with_raising(self, error_server):
        """Test error request that raises an error."""
        async with PublicSession() as session:
            session.client.base_url = error_server.url

            session.raise_for_status = True
            with pytest.raises(HTTPStatusError):
                await session.request('', {})

    @pytest.mark.asyncio
    async def test_data_request(self, data_server, data):
        """Test regular request."""
        async with PublicSession() as session:
            session.client.base_url = data_server.url

            session.raise_for_status = False
            response = await session.request('', {})
            assert response == data

            session.raise_for_status = True
            response = await session.request('', {})
            assert response == data


class TestTokenSession:
    """Tests of TokenSession class."""

    @pytest.fixture
    def app(self):
        """Return app info."""
        return {'client_id': None, 'application_key': 123, 'application_secret_key': ''}

    @pytest.fixture
    def token(self):
        """Return token info."""
        return {'access_token': 'token', 'session_secret_key': ''}

    @pytest.mark.asyncio
    async def test_required_params(self, app, token):
        """Test required query parameters."""
        async with TokenSession(**app, **token) as session:
            assert 'application_key' in session.required_params
            assert 'format' in session.required_params

    @pytest.mark.asyncio
    async def test_params2str(self, app, token):
        """Test query string."""
        async with TokenSession(**app, **token) as session:
            params = {'"a"': 1, '"b"': 2, '"c"': 3}

            session.application_secret_key = ''
            session.session_secret_key = ''
            query = session.params2str(params)
            assert query == '"a"=1"b"=2"c"=3'

            session.application_secret_key = ''
            session.session_secret_key = 'session secret key'
            query = session.params2str(params)
            assert query == '"a"=1"b"=2"c"=3session secret key'

            session.session_secret_key = ''
            session.application_secret_key = 'app secret key'
            query = session.params2str(params)
            assert query == '"a"=1"b"=2"c"=3904c9e548e858829e2879d1603a7b0cc'

    @pytest.mark.asyncio
    async def test_error_request(self, app, token, error_server, error):
        """Test error request."""
        async with TokenSession(**app, **token) as session:
            session.client.base_url = error_server.url
            session.session_secret_key = 'session key'

            session.raise_for_status = False
            response = await session.request('', params={'key': 'value'})
            assert response == error

    @pytest.mark.asyncio
    async def test_error_request_with_raising(self, app, token, error_server):
        """Test error request that raises an error."""
        async with TokenSession(**app, **token) as session:
            session.client.base_url = error_server.url
            session.session_secret_key = 'session secret key'

            session.raise_for_status = True
            with pytest.raises(HTTPStatusError):
                _ = await session.request('', params={'key': 'value'})

    @pytest.mark.asyncio
    async def test_data_request(self, app, token, data_server, data):
        """Test regular request."""
        async with TokenSession(**app, **token) as session:
            session.client.base_url = data_server.url
            session.session_secret_key = 'session secret key'

            session.raise_for_status = False
            response = await session.request('', params={'key': 'value'})
            assert response == data

            session.raise_for_status = True
            response = await session.request('', params={'key': 'value'})
            assert response == data
