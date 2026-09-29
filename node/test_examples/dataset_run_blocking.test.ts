import { describe, expect, it } from "vitest";
import data from "../../data/dataset_run_data.json" with { type: "json" };
import type { DatasetRunRequest, RunResponse } from "../aegis_types.ts";
import { API_RUNS_DATASET_PATH, DEFAULT_RUN_TIMEOUT } from "../constants.ts";
import { expectRunPassed } from "../utils/assertions.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";

const client = createAegisClient(DEFAULT_RUN_TIMEOUT);

describe("Dataset Run - Blocking", () => {
    it("Should successfully run dataset blocking evaluation and validate results", async () => {
        const payload: DatasetRunRequest = { ...data, is_blocking: true };

        const { status, data: run } = await client.post<RunResponse>(
            API_RUNS_DATASET_PATH,
            payload,
        );
        expect(status).toBe(201);

        logRun(run);
        expectRunPassed(run);
    });
});
