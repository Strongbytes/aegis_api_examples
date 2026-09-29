import data from "../../data/custom_run_data.json" with { type: "json" };
import type { CustomRunRequest, RunResponse } from "../aegis_types.ts";
import { API_RUNS_CUSTOM_PATH, DEFAULT_RUN_TIMEOUT } from "../constants.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";
import { downloadRunReport } from "../utils/run_report_download.ts";

async function main(): Promise<void> {
    try {
        const client = createAegisClient(DEFAULT_RUN_TIMEOUT);

        const payload: CustomRunRequest = { ...data, is_blocking: true };

        const { data: run } = await client.post<RunResponse>(API_RUNS_CUSTOM_PATH, payload);
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
