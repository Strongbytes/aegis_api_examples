import json
import sys

from aegis_types import CustomRunRequest, RunResponse
from constants import API_RUNS_CUSTOM_URL, ROOT_DIR
from utils.client import create_aegis_client
from utils.polling import wait_for_run_to_finish
from utils.reporting import log_run
from utils.run_report_download import download_run_report


def main() -> None:
    try:
        with create_aegis_client() as client:
            data: CustomRunRequest = json.loads(
                (ROOT_DIR / "data/custom_run_data.json").read_text(encoding="utf-8")
            )
            payload: CustomRunRequest = {**data, "is_blocking": False}

            started_run: RunResponse = client.post(API_RUNS_CUSTOM_URL, json=payload).json()

            run = wait_for_run_to_finish(client, started_run["id"])
            log_run(run)

            report_path = download_run_report(client, run["id"])
            print("Run report saved to:", report_path)
    except Exception as error:
        # Log only the message: an httpx exception carries the request,
        # whose headers include the API key.
        print("Something went wrong:", error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
