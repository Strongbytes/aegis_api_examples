import { setTimeout as sleep } from "node:timers/promises";
import type { AxiosInstance } from "axios";
import type { RunResponse } from "../aegis_types.ts";
import { API_RUNS_PATH, DEFAULT_REFETCH_INTERVAL, DEFAULT_RUN_TIMEOUT } from "../constants.ts";

export async function waitForRunToFinish(
    client: AxiosInstance,
    runId: RunResponse["id"],
): Promise<RunResponse> {
    const deadline = Date.now() + DEFAULT_RUN_TIMEOUT;

    while (Date.now() < deadline) {
        await sleep(DEFAULT_REFETCH_INTERVAL);

        const { data: run } = await client.get<RunResponse>(`${API_RUNS_PATH}/${runId}`);

        if (run.finished_at !== null) {
            return run;
        }
    }

    throw new Error(`Run ${runId} did not finish within ${DEFAULT_RUN_TIMEOUT / 1000}s.`);
}
