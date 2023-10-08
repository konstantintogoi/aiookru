[![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/KonstantinTogoi/aiookru/blob/master/LICENSE)
[![Last Release](https://img.shields.io/pypi/v/aiookru.svg)](https://pypi.python.org/pypi/aiookru)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/aiookru.svg)](https://pypi.python.org/pypi/aiookru)

# aiookru

aiookru is a python [ok.ru API](https://apiok.ru/) wrapper.
The main features are:

* authorization ([Authorization Code](https://oauth.net/2/grant-types/authorization-code/), [Password Grant](https://oauth.net/2/grant-types/password/), [Refresh Token](https://oauth.net/2/grant-types/refresh-token/))
* [REST API](https://apiok.ru/en/dev/methods/rest) methods


## Usage

To use [ok.ru API](https://apiok.ru/) you need a registered app and [ok.ru](https://ok.ru) account.
For more details, see [aiookru Documentation](https://konstantintogoi.github.io/aiookru).

### Client application

Use `ClientSession` when REST API is needed in:

- client component of the client-server application
- standalone mobile/desktop application

i.e. when you embed your app's info (application key) in publicly available code.

```python
from aiookru import ClientSession, API

session = ClientSession(client_id, application_key, access_token, session_secret_key)
api = API(session)

events = await api.events.get()
friends = await api.friends.get()
```

Pass `session_secret_key` and `access_token`
that were received after authorization.
For more details, see [authorization instruction](https://konstantintogoi.github.io/aiookru/authorization).

### Server application

Use `ServerSession` when REST API is needed in:

- server component of the client-server application
- requests from your servers

```python
from aiookru import ServerSession, API

session = ServerSession(client_id, application_key, application_secret_key, access_token)
api = API(session)

events = await api.events.get()
friends = await api.friends.get()
```

Pass `application_secret_key` and `access_token` that was received after authorization.
For more details, see [authorization instruction](https://konstantintogoi.github.io/aiookru/authorization).

## Installation

```shell
pip install aiookru
```

## Supported Python Versions

Python 3.7, 3.8, 3.9 are supported.

License
-------

**aiookru** is released under the BSD 2-Clause License.
