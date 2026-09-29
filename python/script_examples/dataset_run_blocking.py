import json
import sys

from constants import API_RUNS_DATASET_URL, DEFAULT_RUN_TIMEOUT, ROOT_DIR
from aegis_types import DatasetRunRequest, RunResponse
from utils.client import create_aegis_client
from utils.logging import log_run
from utils.run_report_download import download_run_report


def main() -> None:
    try:
        with create_aegis_client(DEFAULT_RUN_TIMEOUT) as client:
            payload: DatasetRunRequest = json.loads((ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8"))

            run: RunResponse = client.post(API_RUNS_DATASET_URL, json=payload).json()
            log_run(run)

            report_path = download_run_report(client, run["id"])
            print("Run report saved to:", report_path)
    except Exception as error:
        # Log only the message: a requests exception carries the request, whose headers include the API key.
        print("Something went wrong:", error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
