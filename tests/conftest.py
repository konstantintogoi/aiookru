"""Conftest."""
import json
from asyncio import AbstractEventLoop, get_event_loop_policy
from typing import Generator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Event loop."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def error_server(httpserver):
    """Return error server."""
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': 'application/json;charset=utf-8'},
        'content': json.dumps({
            'error_code': -1,
            'error_msg': 'error msg',
            'error_data': 'error data',
        }),
    })
    return httpserver


@pytest.fixture
async def data_server(httpserver):
    """Return data server."""
    httpserver.serve_content(**{
        'code': 200,
        'headers': {'Content-Type': 'application/json;charset=utf-8'},
        'content': json.dumps({'key': 'value'}),
    })
    return httpserver
