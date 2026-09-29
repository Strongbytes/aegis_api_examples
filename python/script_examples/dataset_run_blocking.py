import json
import sys

from aegis_types import DatasetRunRequest, RunResponse
from constants import API_RUNS_DATASET_PATH, DEFAULT_RUN_TIMEOUT, ROOT_DIR
from utils.client import create_aegis_client
from utils.reporting import log_run
from utils.run_report_download import download_run_report


def main() -> None:
    try:
        with create_aegis_client(DEFAULT_RUN_TIMEOUT) as client:
            data: DatasetRunRequest = json.loads(
                (ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8")
            )
            payload: DatasetRunRequest = {**data, "is_blocking": True}

            run: RunResponse = client.post(API_RUNS_DATASET_PATH, json=payload).json()
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
