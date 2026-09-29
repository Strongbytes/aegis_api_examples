import { describe, expect, it } from "vitest";

import { API_RUNS_CUSTOM_URL } from "../constants.ts";
import type { CustomRunRequest, RunResponse } from "../aegis_types.ts";
import { createAegisClient } from "../utils/client.ts";
import { waitForRunToFinish } from "../utils/polling.ts";
import { logRun } from "../utils/logging.ts";
import { expectRunPassed } from "../utils/assertions.ts";
import data from "../../data/custom_run_data.json" with { type: "json" };

const client = createAegisClient();

describe("Custom Run - Non-Blocking", () => {
    it("Should successfully run custom non-blocking evaluation and validate results", async () => {
        const payload: CustomRunRequest = { ...data, is_blocking: false };

        const { status, data: startedRun } = await client.post<RunResponse>(
            API_RUNS_CUSTOM_URL,
            payload,
        );
        expect(status).toBe(201);
        expect(startedRun.finished_at).toBeNull();

        const run = await waitForRunToFinish(client, startedRun.id);

        logRun(run);
        expectRunPassed(run);
    });
});
