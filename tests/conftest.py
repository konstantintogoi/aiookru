"""Conftest."""
import json
from asyncio import AbstractEventLoop, get_event_loop_policy
from typing import Any, Dict, Generator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Event loop."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def error() -> Dict[str, Any]:
    """Return an error."""
    return {'error_code': -1, 'error_msg': 'test error msg'}


@pytest.fixture
def data() -> Dict[str, Any]:
    """Return data."""
    return {'key': 'value'}


@pytest.yield_fixture
async def error_server(httpserver, error):
    """Return error server."""
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': 'application/json;charset=utf-8'},
        'content': json.dumps(error),
    })
    return httpserver


@pytest.yield_fixture
async def data_server(httpserver, data):
    """Return data server."""
    httpserver.serve_content(**{
        'code': 200,
        'headers': {'Content-Type': 'application/json;charset=utf-8'},
        'content': json.dumps(data),
    })
    return httpserver
