import re
from datetime import datetime, timezone
from pathlib import Path

import httpx

from constants import API_RUNS_PATH

RUN_REPORTS_DIR = Path(__file__).resolve().parent.parent / "run_reports"

EXTENSIONS_BY_CONTENT_TYPE = {
    "application/json": ".json",
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "text/csv": ".csv",
    "text/html": ".html",
    "text/plain": ".txt",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
}


def extension_from_headers(headers: httpx.Headers) -> str:
    disposition = headers.get("content-disposition", "")
    match = re.search(r"""filename\*?=(?:UTF-8'')?"?([^";]+)"?""", disposition, re.IGNORECASE)
    if match:
        return Path(match.group(1)).suffix

    content_type = headers.get("content-type", "").split(";")[0].strip()
    return EXTENSIONS_BY_CONTENT_TYPE.get(content_type, "")


def download_run_report(client: httpx.Client, run_id: int) -> Path:
    response = client.get(f"{API_RUNS_PATH}/{run_id}/download")

    timestamp = re.sub(
        r"[:.]",
        "-",
        datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    )
    extension = extension_from_headers(response.headers)
    file_path = RUN_REPORTS_DIR / f"run_{run_id}_{timestamp}{extension}"

    RUN_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(response.content)

    return file_path
