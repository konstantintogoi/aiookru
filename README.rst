.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://github.com/konstantintogoi/aiookru/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/aiookru.svg
    :target: https://pypi.python.org/pypi/aiookru

.. image:: https://img.shields.io/pypi/pyversions/aiookru.svg
    :target: https://pypi.python.org/pypi/aiookru

.. image:: https://readthedocs.org/projects/aiookru/badge/?version=latest
    :target: https://aiookru.readthedocs.io/en/latest

.. image:: https://github.com/konstantintogoi/aiookru/actions/workflows/pages/pages-build-deployment/badge.svg
    :target: https://konstantintogoi.github.io/aiookru

.. index-start-marker1

aiookru
=======

async python `ok.ru API <https://apiok.ru/>`_ wrapper
for `REST API <https://apiok.ru/en/dev/methods/rest>`_ methods.

Usage
-----

To use `ok.ru API <https://apiok.ru/>`_ you need a registered app and `ok.ru <https://ok.ru>`_ account.

Client application
~~~~~~~~~~~~~~~~~~

Use :code:`ClientSession` for:

- client component of the client-server application
- standalone mobile/desktop application

i.e. when you embed your app's info (application key) in publicly available code.

.. code-block:: python

    import aiookru

    session = ClientSession(client_id, application_key, access_token, session_secret_key)
    api = API(session)

    friends = await api.friends.get()
    events = await api.events.get()

Pass :code:`session_secret_key` and :code:`access_token`
that were received after authorization.
For more details, see `authorization instruction <https://konstantintogoi.github.io/aiookru/authorization>`_.

Server application
~~~~~~~~~~~~~~~~~~

Use :code:`ServerSession` for:

- server component of the client-server application
- requests from your servers

.. code-block:: python

    import aiookru

    session = ServerSession(client_id, application_key, application_secret_key, access_token)
    api = API(session)

    friends = await api.friends.get()
    events = await api.events.get()


Pass :code:`application_secret_key` and :code:`access_token` that was received after authorization.
For more details, see `authorization instruction <https://konstantintogoi.github.io/aiookru/authorization>`_.

Installation
------------

.. code-block:: shell

    $ pip install aiookru


Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.7, 3.8, 3.9 are supported.

License
-------

**aiookru** is released under the BSD 2-Clause License.
