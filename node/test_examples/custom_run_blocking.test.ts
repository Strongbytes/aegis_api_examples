import { describe, expect, it } from "vitest";
import data from "../../data/custom_run_data.json" with { type: "json" };
import type { CustomRunRequest, RunResponse } from "../aegis_types.ts";
import { API_RUNS_CUSTOM_URL, DEFAULT_RUN_TIMEOUT } from "../constants.ts";
import { expectRunPassed } from "../utils/assertions.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";

const client = createAegisClient(DEFAULT_RUN_TIMEOUT);

describe("Custom Run - Blocking", () => {
    it("Should successfully run custom blocking evaluation and validate results", async () => {
        const payload: CustomRunRequest = data;

        const { status, data: run } = await client.post<RunResponse>(API_RUNS_CUSTOM_URL, payload);
        expect(status).toBe(201);

        logRun(run);
        expectRunPassed(run);
    });
});
