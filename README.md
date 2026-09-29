# Aegis API Examples

Examples of calling the Aegis API from Node and Python, written as tests you can drop into a CI/CD pipeline. Each test starts an evaluation run, waits for it to finish, and fails if the run or any of its evaluations didn't succeed or scored below its threshold. A pipeline step that runs them will fail the build when quality drops.

The examples live in `test_examples/` under both `node/` and `python/`, and both languages cover the same cases:

- **Custom runs** (`custom_run_*`) send the full evaluation in the request: metrics, thresholds, and the data to evaluate. The payload is in `data/custom_run_data.json`.
- **Dataset runs** (`dataset_run_*`) point to a dataset that already exists in Aegis by its ID. The payload is in `data/dataset_run_data.json`.

Each case has a blocking and a non-blocking version. The blocking test waits for the API to return the finished run in a single request. The non-blocking test starts the run, then polls `/runs/{id}` until it finishes, which suits long runs that could outlast a request timeout.

Both languages read the same payload files in `data/`, so edit those to run the examples against your own metrics, datasets, and thresholds.

## Setup

Copy the env template and fill in your values:

```bash
cp .env.template .env
```

```
AEGIS_API_URL=https://your-aegis-host
AEGIS_API_KEY=your-api-key
AEGIS_REFETCH_INTERVAL_SECONDS=10
```

Both the Node and Python examples read this root `.env` file. `AEGIS_REFETCH_INTERVAL_SECONDS` is how often the non-blocking examples poll for results (defaults to 10).

## Node

Requires [Node.js](https://nodejs.org/) 22.12+ and [pnpm](https://pnpm.io/installation).

```bash
cd node
pnpm install
```

Tests live in `test_examples/` as `*.test.ts` files and run through Vitest rather than with `node` directly. Standalone scripts go in `script_examples/`.

Run all tests:

```bash
pnpm test
```

Run a single file:

```bash
pnpm vitest run test_examples/custom_run_blocking.test.ts
pnpm vitest run test_examples/custom_run_nonblocking.test.ts
```

Vitest strips types without checking them. To type-check:

```bash
pnpm typecheck
```

## Python

Requires [Python](https://www.python.org/downloads/) 3.10+.

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tests live in `test_examples/` as `test_*.py` files. Standalone scripts go in `script_examples/`; run them from the `python` folder as modules so they can import `constants`:

```bash
python -m script_examples.your_script
```

Run all tests. They run in parallel, one worker per CPU:

```bash
pytest
```

Run a single file:

```bash
pytest test_examples/test_custom_run_nonblocking.py
```
