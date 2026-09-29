import { describe, expect, it } from "vitest";

import { API_RUNS_DATASET_URL, DEFAULT_RUN_TIMEOUT } from "../constants.ts";
import type { DatasetRunRequest, RunResponse } from "../aegis_types.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";
import { expectRunPassed } from "../utils/assertions.ts";
import data from "../../data/dataset_run_data.json" with { type: "json" };

const client = createAegisClient(DEFAULT_RUN_TIMEOUT);

describe("Dataset Run - Blocking", () => {
    it("Should successfully run dataset blocking evaluation and validate results", async () => {
        const payload: DatasetRunRequest = data;

        const { status, data: run } = await client.post<RunResponse>(
            API_RUNS_DATASET_URL,
            payload,
        );
        expect(status).toBe(201);

        logRun(run);
        expectRunPassed(run);
    });
});
