Session
=======

The session makes **GET** requests when you call instances of :code:`APIMethod`
class that are returned as attributes of an :code:`API` instance.

Request
-------

By default, the session
(:code:`CodeSession`, :code:`PasswordSession`, :code:`RefreshSession`)
tries to infer which signature generation circuit to use:

- if :code:`app_secret_key` is not empty string - server-server signature generation circuit is used
- else if :code:`session_secret_key` is not empty string - client-server signature generation circuit is used
- else exception is raised

You can explicitly set a signature generation circuit for signing requests
by passing to :code:`API` one of the sessions below.

Client-Server signature generation circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider the following example of API request with client-server signature:

.. code-block:: python

    from aiookru import TokenSession, API

    session = TokenSession(
        app_id=123456,
        app_key='ABCDEFGHIGKLMNOPK',
        app_secret_key='',
        access_token='-s-2GUXOAvQYI7-RfxsZtV1wezsdtVPv92xfuaSQ8.SAIV1O2ywYra2-3ywes5St2yvcuZSr9UUWN2TtbWtWKVTuAy8',
        session_secret_key='ae5362b5b588cc7294c2414d71b74d5d',
    )
    api = API(session)

    events = await api.events.get()

It is equivalent to **GET** request:

.. code-block:: shell

    https://api.ok.ru/fb.do
        ?application_key=ABCDEFGHIGKLMNOPK
        &format=json
        &method=events.get
        &sig=03a41413523ea8092507949d6e711963
        &access_token=-s-2GUXOAvQYI7-RfxsZtV1wezsdtVPv92xfuaSQ8.SAIV1O2ywYra2-3ywes5St2yvcuZSr9UUWN2TtbWtWKVTuAy8

The following steps were taken:

1. :code:`session_secret_key` used as secret key
2. sorted request parameters and secret key were concatenated: :code:`application_key=ABCDEFGHIGKLMNOPKformat=jsonmethod=events.getae5362b5b588cc7294c2414d71b74d5d`
3. signature :code:`03a41413523ea8092507949d6e711963` calculated as MD5 of the previous string
4. signature appended to **GET** request parameters
5. :code:`access_token` appended to **GET** request parameters

ClientSession
^^^^^^^^^^^^^

For making requests with :code:`session_secret_key` and :code:`access_token`.

.. code-block:: python

    from aiookru import ClientSession, API

    session = ClientSession(app_id, app_key, access_token, session_secret_key)
    api = API(session)
    ...

Server-Server signature generation circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider the following example of API request with server-server signature:

.. code-block:: python

    from aiookru import TokenSession, API

    session = TokenSession(
        app_id=123456,
        app_key='ABCDEFGHIGKLMNOPK',
        app_secret_key='ABC123DEF456GHI789JKL123',
        access_token='-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7',
        session_secret_key='',
    )
    api = API(session)

    events = await api.events.get()

It is equivalent to **GET** request:

.. code-block:: shell

    https://api.ok.ru/fb.do
        ?application_key=ABCDEFGHIGKLMNOPK
        &format=json
        &method=events.get
        &sig=232c8eb921951c4dba9b72606f9ddb4c
        &access_token=-s-84W-s3egarWUsbkq-IWTucuedzTKT8VUXIA.s4Xx8IW7

The following steps were taken:

1. :code:`b1a2b89707a94624c43afae67d59274c` used as secret key, it was calculated as MD5(:code:`access_token` + :code:`app_secret_key`)
2. sorted request parameters and secret key were concatenated: :code:`application_key=ABCDEFGHIGKLMNOPKformat=jsonmethod=events.getb1a2b89707a94624c43afae67d59274c`
3. signature :code:`232c8eb921951c4dba9b72606f9ddb4c` calculated as MD5 of the previous string
4. signature appended to **GET** request parameters
5. :code:`access_token` appended to **GET** request parameters

ServerSession
^^^^^^^^^^^^^

For making requests with :code:`app_secret_key` and :code:`access_token`.

.. code-block:: python

    from aiookru import ServerSession, API

    session = ServerSession(app_id, app_key, app_secret_key, access_token)
    api = API(session)
    ...

CodeSession
^^^^^^^^^^^^^^^^^

Server session with authorization with
`Authorization Code <https://oauth.net/2/grant-types/authorization-code/>`_.

.. code-block:: python

    from aiookru import CodeSession, API

    async with CodeSession(app_id, app_key, app_secret_key, code, redirect_uri) as session:
        api = API(session)
        ...

PasswordSession
^^^^^^^^^^^^^^^^^^^^

Server session with authorization with
`logn and password <https://oauth.net/2/grant-types/password/>`_`.

.. code-block:: python

    from aiookru import PasswordSession, API

    async with PasswordSession(app_id, app_key, app_secret_key, refresh_token) as session:
        api = API(session)
        ...

RefreshSession
^^^^^^^^^^^^^^^^^^^^

Server session with authorization with
`Refresh Token <https://oauth.net/2/grant-types/refresh-token/>`_.

.. code-block:: python

    from aiookru import RefreshSession, API

    async with RefreshSession(app_id, app_key, app_secret_key, refresh_token) as session:
        api = API(session)
        ...
