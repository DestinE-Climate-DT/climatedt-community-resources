import time
from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException


def _request_with_retry(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 30,
    retries: int = 3,
    stream: bool = False,
) -> Response:
    """Run an HTTP request with simple exponential backoff for transient errors."""
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
                timeout=timeout,
                stream=stream,
            )
        except RequestException as exc:
            last_error = exc
            if attempt < retries - 1:
                backoff = 0.5 * (2**attempt)
                time.sleep(backoff)
                continue
            break

        if response.status_code in (429, 500, 502, 503, 504):
            if attempt < retries - 1:
                backoff = 0.5 * (2**attempt)
                time.sleep(backoff)
                continue
            last_error = RequestException(
                f"{response.status_code} Server Error for url: {url}"
            )
            break

        response.raise_for_status()
        return response

    raise RuntimeError(
        f"Request failed after {retries} attempts: {method.upper()} {url}. "
        f"Last error: {last_error}"
    )


def request_json(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 30,
    retries: int = 3,
) -> dict[str, Any]:
    """Request a JSON endpoint and parse the response body."""
    response = _request_with_retry(
        method=method,
        url=url,
        headers=headers,
        json_body=json_body,
        timeout=timeout,
        retries=retries,
    )
    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response from {url}: {exc}") from exc
