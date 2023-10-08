[![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/konstantintogoi/aiookru/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/pypi/v/aiookru.svg)](https://pypi.python.org/pypi/aiookru)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/aiookru.svg)](https://pypi.python.org/pypi/aiookru)
[![Read the Docs](https://readthedocs.org/projects/aiookru/badge/?version=latest)](https://aiookru.readthedocs.io/en/latest)
[![GitHub Pages](https://github.com/konstantintogoi/aiookru/actions/workflows/pages/pages-build-deployment/badge.svg)](https://konstantintogoi.github.io/aiookru)

# aiookru

aiookru is a python [ok.ru API](https://apiok.ru/) wrapper.
The main features are:

* authorization ([Authorization Code](https://oauth.net/2/grant-types/authorization-code/), [Refresh Token](https://oauth.net/2/grant-types/refresh-token/))
* [REST API](https://apiok.ru/en/dev/methods/rest) methods


## Usage

To use [ok.ru API](https://apiok.ru/) you need a registered app and an `access_token`

```python
import aiookru

client_id = '12345678'
application_key = 'ABCDEFGHIJKLMNOPQ'
application_secret_key = '0A1B2C3D4E5F6G7H8I9K10L11M12N13O14P15Q'
redirect_uri = 'http://apiok.ru/oauth_callback'

code = ''  # get code from login form

async with aiookru.CodeGrant(client_id, application_secret_key, redirect_uri, code) as grant:
    access_token = grant.access_token
    refresh_token = grant.refresh_token

async with aiookru.API(access_token, application_key, application_secret_key=application_secret_key) as okru:
    events = await okru.events.get()

async with aiookru.RefreshGrant(client_id, application_secret_key, refresh_token) as grant:
    access_token = grant.access_token
```

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
