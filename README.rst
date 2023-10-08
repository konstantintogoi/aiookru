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

To use `ok.ru API <https://apiok.ru/>`_ you need a registered app and an :code:`access_token`.

.. code-block:: python

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
