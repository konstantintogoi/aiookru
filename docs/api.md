# REST API

Methods: https://apiok.ru/en/dev/methods/rest.

## Executing requests

`API` tries to infer which signature generation circuit to use:

- if `application_secret_key` is not empty string - server-server signature generation circuit is used
- if `session_secret_key` is not empty string - client-server signature generation circuit is used


### Server-Server signature generation circuit

```python
import aiookru

application_key = 'ABCDEFGHIGKLMNOPK'
application_secret_key = 'ABC123DEF456GHI789JKL123'
access_token = '-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7'

async with aiookru.API(access_token, application_key, application_secret_key=application_secret_key) as okru:
    events = await okru.events.get()
```

is equivalent to **GET** request:

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


### Client-Server signature generation circuit

```python
import aiookru

application_key = 'ABCDEFGHIGKLMNOPK'
access_token = '-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7'
session_secret_key = 'ae5362b5b588cc7294c2414d71b74d5d'

async with aiookru.API(access_token, application_key, session_secret_key=session_secret_key) as okru:
    events = await okru.events.get()
```

is equivalent to **GET** request:

```shell
GET https://api.ok.ru/fb.do
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
