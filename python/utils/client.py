import sys

import httpx

from constants import API_BASE_URL, API_KEY, DEFAULT_REQUEST_TIMEOUT


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_error:
        # Response hooks run before the body is read, so it has to be read explicitly.
        response.read()
        print("Aegis API error:", response.status_code, response.text, file=sys.stderr)

    response.raise_for_status()


def create_aegis_client(timeout: float = DEFAULT_REQUEST_TIMEOUT) -> httpx.Client:
    return httpx.Client(
        base_url=API_BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=timeout,
        event_hooks={"response": [_raise_for_status]},
    )
