# Authorization

The preferred way to authorize is an :code:`async with` statement.
After authorization the session will have the following attributes:

* :code:`access_token`,
* :code:`session_secret_key` if Password Grant used
* :code:`token_type` if Code Grant / Refresh Token Grant used
* :code:`refresh_token` if Code Grant used
* :code:`expires_in` if Code Grant / Refresh Token Grant used

## Authorization Code Grant

```python
from aiookru import CodeSession, API

client_id = 123456
application_key = 'abcde'
application_secret_key = 'xyz'

async with CodeSession(client_id, application_key, application_secret_key, code, redirect_uri) as session:
    api = API(session)
    ...
```

About OAuth 2.0 Authorization Code Grant: https://oauth.net/2/grant-types/authorization-code/

For more details, see https://apiok.ru/ext/oauth/server

## Password Grant

```python
from aiookru import PasswordSession, API

client_id = 123456
application_key = 'abcde'
application_secret_key = ''

async with PasswordSession(client_id, application_key, application_secret_key, login, passwd) as session:
    api = API(session)
    ...
```

About OAuth 2.0 Password Grant: https://oauth.net/2/grant-types/password/

## Refresh Token

```python
from aiookru import RefreshSession, API

client_id = 123456
application_key = 'abcde'
application_secret_key = 'xyz'

async with RefreshSession(client_id, application_key, application_secret_key, refresh_token) as session:
    api = API(session)
    ...
```

About OAuth 2.0 Refresh Token: https://oauth.net/2/grant-types/refresh-token/

For more details, see https://apiok.ru/ext/oauth/server
