import asyncio
import io
import ssl
from pathlib import Path
from typing import Optional, Tuple, Union

import certifi
from aiohttp import ClientSession, FormData, TCPConnector
from aiohttp.typedefs import StrOrURL

from .utils import json


class BaseClient:
    def __init__(self):
        self._session: Optional[ClientSession] = None

    def _get_session(self):
        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(
            connector=connector,
            json_serialize=json.dumps,
        )
        return self._session

    async def _make_request(
        self, method: str, url: StrOrURL, **kwargs
    ) -> Tuple[int, dict]:
        session = self._get_session()
        result = await session.request(method, url, **kwargs)
        return result.status, await result.json(loads=json.loads)

    def _prepare_form(self, file: Union[str, Path, io.IOBase]):
        form = FormData()
        form.add_field("file", self._prepare_file(file))
        return form

    @staticmethod
    def _prepare_file(file: Union[str, Path, io.IOBase]):
        if isinstance(file, str):
            return open(file, "rb")

        if isinstance(file, io.IOBase):
            return file

        if isinstance(file, Path):
            return file.open("rb")

        raise TypeError("Not supported file type.")

    async def close(self):
        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()
        await asyncio.sleep(0.25)
