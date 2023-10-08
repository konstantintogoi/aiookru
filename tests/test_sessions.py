"""Sessions tests."""
import pytest
from httpx import HTTPStatusError

from aiookru.session import PublicSession, TokenSession


class TestPublicSession:
    """Tests of PublicSession class."""

    @pytest.mark.asyncio
    async def test_failed_request(self, error_server):
        """Test failed request."""
        session = PublicSession()
        session.client.base_url = error_server.url

        with pytest.raises(HTTPStatusError):
            await session.request({})

    @pytest.mark.asyncio
    async def test_regular_request(self, data_server):
        """Test regular request."""
        session = PublicSession()
        session.client.base_url = data_server.url

        assert await session.request({}) == {'key': 'value'}


class TestTokenSession:
    """Tests of TokenSession class."""

    @pytest.mark.asyncio
    async def test_params2str(self):
        """Test query string."""
        session = TokenSession(
            application_key='application_key',
            access_token='access_token',
            secret_key='secret_key',
        )

        params = {'"a"': 1, '"b"': 2, '"c"': 3}
        assert session.params2str(params) == '"a"=1"b"=2"c"=3secret_key'

    @pytest.mark.asyncio
    async def test_failed_request(self, error_server):
        """Test failed request."""
        session = TokenSession(
            application_key='application_key',
            access_token='access_token',
            secret_key='secret_key',
        )
        session.client.base_url = error_server.url

        with pytest.raises(HTTPStatusError):
            await session.request(params={'key': 'value'})

    @pytest.mark.asyncio
    async def test_regular_request(self, data_server):
        """Test regular request."""
        session = TokenSession(
            application_key='application_key',
            access_token='access_token',
            secret_key='secret_key',
        )
        session.client.base_url = data_server.url

        assert await session.request(params={'k': 'v'}) == {'key': 'value'}
