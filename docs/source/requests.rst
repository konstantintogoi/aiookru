Requests
========

:code:`aiookru` executes http requests with :code:`httpx.AsyncClient`.

Request Format
--------------

:code:`httpx.AsyncClient` makes **GET** requests according to
`Request Format <https://apiok.ru/dev/methods/>`_.
For example:

.. code-block:: shell

    GET https://api.ok.ru/fb.do?method=friends.get


Response Format
---------------

.. code-block:: shell

    {
        "response": ...
    }

or

.. code-block:: shell

    {
        "error": {
            "error_code": 1,
            "error_msg": "Unknown error occurred",
            "request_params": { ... }
        }
    }
