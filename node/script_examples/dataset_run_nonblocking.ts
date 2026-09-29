import data from "../../data/dataset_run_data.json" with { type: "json" };
import type { DatasetRunRequest, RunResponse } from "../aegis_types.ts";
import { API_RUNS_DATASET_PATH } from "../constants.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";
import { waitForRunToFinish } from "../utils/polling.ts";
import { downloadRunReport } from "../utils/run_report_download.ts";

async function main(): Promise<void> {
    try {
        const client = createAegisClient();

        const payload: DatasetRunRequest = { ...data, is_blocking: false };

        const { data: startedRun } = await client.post<RunResponse>(API_RUNS_DATASET_PATH, payload);

        const run = await waitForRunToFinish(client, startedRun.id);
        logRun(run);

        const reportPath = await downloadRunReport(client, run.id);
        console.log("Run report saved to:", reportPath);
    } catch (error) {
        // Log only the message: an Axios error object carries the request headers, which include the API key.
        console.error("Something went wrong:", error instanceof Error ? error.message : error);
        process.exitCode = 1;
    }
}

await main();
