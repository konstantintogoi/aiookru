# Authorization

The preferred way to authorize is an `async with` statement.

## Authorization Code Grant

```python
import aiookru

client_id = '12345678'
application_secret_key = '0A1B2C3D4E5F6G7H8I9K10L11M12N13O14P15Q'
redirect_uri = 'http://apiok.ru/oauth_callback'
code = ''  # get code from login form

async with aiookru.CodeGrant(client_id, application_secret_key, redirect_uri, code) as grant:
    access_token = grant.access_token
    refresh_token = grant.refresh_token
```

After authorization the `grant` will have the following attributes:

* `access_token`,
* `refresh_token`,
* `expires_in`.

About OAuth 2.0 Authorization Code Grant: https://oauth.net/2/grant-types/authorization-code/

For more details, see https://apiok.ru/ext/oauth/server

## Refresh Grant

```python
import aiookru

client_id = '12345678'
application_secret_key = '0A1B2C3D4E5F6G7H8I9K10L11M12N13O14P15Q'
refresh_token = 'refresh token'

async with aiookru.RefreshGrant(client_id, application_secret_key, refresh_token) as grant:
    access_token = grant.access_token
```

After authorization the `grant` will have the following attributes:

* `access_token`,
* `token_type`,
* `expires_in`.

About OAuth 2.0 Refresh Token: https://oauth.net/2/grant-types/refresh-token/

For more details, see https://apiok.ru/ext/oauth/server
