import path from "node:path";
import dotenv from "dotenv";

dotenv.config({
    path: path.resolve(import.meta.dirname, "../.env"),
    quiet: true,
});

export const API_BASE_URL = process.env.AEGIS_API_URL ?? "";
export const API_KEY = process.env.AEGIS_API_KEY ?? "";

export const API_RUNS_URL = `${API_BASE_URL}/runs`;
export const API_RUNS_CUSTOM_URL = `${API_BASE_URL}/runs/custom`;
export const API_RUNS_DATASET_URL = `${API_BASE_URL}/runs/dataset`;

export const DEFAULT_REFETCH_INTERVAL =
    Number(process.env.AEGIS_REFETCH_INTERVAL_SECONDS || 10) * 1000;

export const DEFAULT_RUN_TIMEOUT = 5 * 60 * 1000;
