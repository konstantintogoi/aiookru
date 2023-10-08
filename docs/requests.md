# Requests

`aiookru` executes http requests with `httpx.AsyncClient`.

## Request Format

`httpx.AsyncClient` makes **GET** requests according to
[Request Format](https://apiok.ru/dev/methods/).
For example:

```shell
GET https://api.ok.ru/fb.do?method=friends.get
```

## Response Format

```python
{
    "response": ...
}
```

or

```python
{
    "error": {
        "error_code": 1,
        "error_msg": "Unknown error occurred",
        "request_params": { ... }
    }
}
```
