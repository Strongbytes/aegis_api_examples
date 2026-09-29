import sys
from typing import Any

import requests

from constants import API_KEY, DEFAULT_REQUEST_TIMEOUT


class _AegisSession(requests.Session):
    def __init__(self, timeout: float) -> None:
        super().__init__()
        self.headers["Authorization"] = f"Bearer {API_KEY}"
        self.timeout = timeout

    # requests has no session-wide timeout and doesn't raise on HTTP errors, so both are applied per request.
    def request(self, method: str | bytes, url: str | bytes, *args: Any, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)

        try:
            response = super().request(method, url, *args, **kwargs)
            response.raise_for_status()
        except requests.RequestException as error:
            if error.response is not None:
                print("Aegis API error:", error.response.status_code, error.response.text, file=sys.stderr)
            else:
                print("Aegis API error:", error, file=sys.stderr)

            raise

        return response


def create_aegis_client(timeout: float = DEFAULT_REQUEST_TIMEOUT) -> requests.Session:
    return _AegisSession(timeout)
