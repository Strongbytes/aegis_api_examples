import { existsSync } from "node:fs";
import path from "node:path";

const ENV_FILE = path.resolve(import.meta.dirname, "../.env");

// CI usually sets these variables directly without a .env file, and loadEnvFile throws when it's missing.
if (existsSync(ENV_FILE)) {
    process.loadEnvFile(ENV_FILE);
}

function requireEnv(name: string): string {
    const value = process.env[name]?.trim();
    if (!value) {
        throw new Error(`${name} is not set. Add it to the root .env file or the environment.`);
    }
    return value;
}

function requireHttpUrl(name: string): string {
    const value = requireEnv(name);
    if (!URL.canParse(value) || !["http:", "https:"].includes(new URL(value).protocol)) {
        throw new Error(`${name} must be an http(s) URL, for example https://your-aegis-host.`);
    }
    return value;
}

function positiveNumberEnv(name: string, fallback: number): number {
    const raw = process.env[name]?.trim();
    if (!raw) {
        return fallback;
    }

    const value = Number(raw);
    if (!Number.isFinite(value) || value <= 0) {
        throw new Error(`${name} must be a positive number, got "${raw}".`);
    }
    return value;
}

export const API_BASE_URL = requireHttpUrl("AEGIS_API_URL");
export const API_KEY = requireEnv("AEGIS_API_KEY");

export const API_RUNS_PATH = "/runs";
export const API_RUNS_CUSTOM_PATH = "/runs/custom";
export const API_RUNS_DATASET_PATH = "/runs/dataset";

export const DEFAULT_REFETCH_INTERVAL =
    positiveNumberEnv("AEGIS_REFETCH_INTERVAL_SECONDS", 10) * 1000;

export const DEFAULT_REQUEST_TIMEOUT = 60 * 1000;
export const DEFAULT_RUN_TIMEOUT = 5 * 60 * 1000;
