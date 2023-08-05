import os

disabled = os.getenv("DISABLE_UJSON")
if not disabled:
    try:
        import ujson as json
    except ImportError:
        import json  # type: ignore
else:
    import json  # type: ignore


def loads(data) -> dict:
    return json.loads(data)


def dumps(data) -> str:
    return json.dumps(data, ensure_ascii=False)
