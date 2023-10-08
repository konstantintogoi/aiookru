# Session

The session makes **GET** requests when you call instances of `APIMethod`
class that are returned as attributes of an `API` instance.

## Request

By default, the session
(`CodeSession`, `PasswordSession`, `RefreshSession`)
tries to infer which signature generation circuit to use:

- if `application_secret_key` is not empty string - server-server signature generation circuit is used
- else if `session_secret_key` is not empty string - client-server signature generation circuit is used
- else exception is raised

You can explicitly set a signature generation circuit for signing requests
by passing to `API` one of the sessions below.

### Client-Server signature generation circuit

Let's consider the following example of API request with client-server signature:

```python
from aiookru import TokenSession, API

session = TokenSession(
    client_id=123456,
    application_key='ABCDEFGHIGKLMNOPK',
    application_secret_key='',
    access_token='-s-2GUXOAvQYI7-RfxsZtV1wezsdtVPv92xfuaSQ8.SAIV1O2ywYra2-3ywes5St2yvcuZSr9UUWN2TtbWtWKVTuAy8',
    session_secret_key='ae5362b5b588cc7294c2414d71b74d5d',
)
api = API(session)

events = await api.events.get()
```

It is equivalent to **GET** request:

```shell
https://api.ok.ru/fb.do
    ?application_key=ABCDEFGHIGKLMNOPK
    &format=json
    &method=events.get
    &sig=03a41413523ea8092507949d6e711963
    &access_token=-s-2GUXOAvQYI7-RfxsZtV1wezsdtVPv92xfuaSQ8.SAIV1O2ywYra2-3ywes5St2yvcuZSr9UUWN2TtbWtWKVTuAy8
```

The following steps were taken:

1. `session_secret_key` used as secret key
2. sorted request parameters and secret key were concatenated: `application_key=ABCDEFGHIGKLMNOPKformat=jsonmethod=events.getae5362b5b588cc7294c2414d71b74d5d`
3. signature `03a41413523ea8092507949d6e711963` calculated as MD5 of the previous string
4. signature appended to **GET** request parameters
5. `access_token` appended to **GET** request parameters

#### ClientSession

For making requests with `session_secret_key` and `access_token`.

```python
from aiookru import ClientSession, API

session = ClientSession(client_id, application_key, access_token, session_secret_key)
api = API(session)
...
```

### Server-Server signature generation circuit

Let's consider the following example of API request with server-server signature:

```python
from aiookru import TokenSession, API

session = TokenSession(
    client_id=123456,
    application_key='ABCDEFGHIGKLMNOPK',
    application_secret_key='ABC123DEF456GHI789JKL123',
    access_token='-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7',
    session_secret_key='',
)
api = API(session)

events = await api.events.get()
```

It is equivalent to **GET** request:

```shell
https://api.ok.ru/fb.do
    ?application_key=ABCDEFGHIGKLMNOPK
    &format=json
    &method=events.get
    &sig=232c8eb921951c4dba9b72606f9ddb4c
    &access_token=-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7
```

The following steps were taken:

1. `b1a2b89707a94624c43afae67d59274c` used as secret key, it was calculated as MD5(`access_token` + `application_secret_key`)
2. sorted request parameters and secret key were concatenated: `application_key=ABCDEFGHIGKLMNOPKformat=jsonmethod=events.getb1a2b89707a94624c43afae67d59274c`
3. signature `232c8eb921951c4dba9b72606f9ddb4c` calculated as MD5 of the previous string
4. signature appended to **GET** request parameters
5. `access_token` appended to **GET** request parameters

#### ServerSession

For making requests with `application_secret_key` and `access_token`.

```python
from aiookru import ServerSession, API

session = ServerSession(client_id, application_key, application_secret_key, access_token)
api = API(session)
...
```

#### CodeSession

Server session with authorization with [Authorization Code](https://oauth.net/2/grant-types/authorization-code/).

```python
from aiookru import CodeSession, API

async with CodeSession(client_id, application_key, application_secret_key, code, redirect_uri) as session:
    api = API(session)
    ...
```

#### PasswordSession

Server session with authorization with [logn and password](https://oauth.net/2/grant-types/password/)`.

```python
from aiookru import PasswordSession, API

async with PasswordSession(client_id, application_key, application_secret_key, refresh_token) as session:
    api = API(session)
    ...
```

#### RefreshSession

Server session with authorization with [Refresh Token](https://oauth.net/2/grant-types/refresh-token/).

```python
from aiookru import RefreshSession, API

async with RefreshSession(client_id, application_key, application_secret_key, refresh_token) as session:
    api = API(session)
    ...
```
