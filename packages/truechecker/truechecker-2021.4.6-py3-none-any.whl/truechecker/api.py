import io
from pathlib import Path
from typing import Optional, Union

from .base import BaseClient
from .const import HTTPMethods
from .exceptions import (
    AlreadyRunning,
    BadRequest,
    Unauthorized,
)
from .models import CheckJob, Profile

API_HOST = "https://checker.trueweb.app/api"


class TrueChecker(BaseClient):
    API_VERSION = "1.1.0"

    def __init__(self, token: str, api_host: Optional[str] = None):
        super().__init__()
        self.__token = token
        self._api_host = api_host or API_HOST

    async def check_profile(
        self,
        file: Union[str, Path, io.IOBase],
        delay: Optional[float] = None,
    ) -> CheckJob:
        """ Bot check request. """
        method = HTTPMethods.PUT
        url = f"{self._api_host}/profile/{self.__token}"

        # prepare params
        params = {}
        if delay is not None:
            params["delay"] = delay
        form = self._prepare_form(file)

        status, data = await self._make_request(method, url, params=params, data=form)
        if status != 200:
            if status == 401:
                raise Unauthorized(data["message"])
            if status == 409:
                raise AlreadyRunning(data["message"])
            raise BadRequest(data["message"])
        return CheckJob(**data)

    async def get_profile(self, username: str) -> Profile:
        """ Returns checked bot profile on success. """
        method = HTTPMethods.GET
        url = f"{self._api_host}/profile/{username}"
        status, profile_data = await self._make_request(method, url)
        return Profile(**profile_data)

    async def get_job_status(self, job_id: str) -> CheckJob:
        """ Returns current job status. """
        method = HTTPMethods.GET
        url = f"{self._api_host}/job/{job_id}"
        status, job_data = await self._make_request(method, url)
        return CheckJob(**job_data)

    async def cancel_job(self, job_id: str) -> CheckJob:
        """ Cancel running Job. """
        method = HTTPMethods.DELETE
        url = f"{self._api_host}/job/{job_id}"
        status, job_data = await self._make_request(method, url)
        return CheckJob(**job_data)
