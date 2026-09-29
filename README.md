# Aegis API Examples

Examples of calling the Aegis API from Node and Python, written as tests you can drop into a CI/CD pipeline. Each test starts an evaluation run, waits for it to finish, and fails if the run or any of its evaluations didn't succeed or scored below its threshold. A pipeline step that runs them will fail the build when quality drops.

The examples live in `test_examples/` under both `node/` and `python/`, and both languages cover the same cases:

- **Custom runs** (`custom_run_*`) send the full evaluation in the request: metrics, thresholds, and the data to evaluate. The payload is in `data/custom_run_data.json`.
- **Dataset runs** (`dataset_run_*`) point to a dataset that already exists in Aegis by its ID. The payload is in `data/dataset_run_data.json`.

Each case has a blocking and a non-blocking version. The blocking test waits for the API to return the finished run in a single request. The non-blocking test starts the run, then polls `/runs/{id}` until it finishes, which suits long runs that could outlast a request timeout.

Both languages read the same payload files in `data/`, so edit those to run the examples against your own metrics, datasets, and thresholds.

Each language also has the same four cases as standalone scripts in `script_examples/`. A script starts the run, prints the results without checking them, and downloads the run report from `/runs/{id}/download` into a `run_reports/` folder next to it (`node/run_reports/` or `python/run_reports/`). Each report is saved as `run_{id}_{timestamp}` so earlier reports are never overwritten. The `run_reports/` folders are git-ignored.

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

Requires [Node.js](https://nodejs.org/) 22.18+ and [pnpm](https://pnpm.io/installation).

```bash
cd node
pnpm install
```

Tests live in `test_examples/` as `*.test.ts` files and run through Vitest rather than with `node` directly.

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

Scripts in `script_examples/` run with `node` directly, which strips the types itself:

```bash
node script_examples/custom_run_blocking.ts
node script_examples/custom_run_nonblocking.ts
node script_examples/dataset_run_blocking.ts
node script_examples/dataset_run_nonblocking.ts
```

Lint, format, and sort imports with [Biome](https://biomejs.dev/), configured in `biome.json`:

```bash
pnpm fix
```

To check without changing any files, as a CI job would, use `pnpm check` instead.

## Python

Requires [Python](https://www.python.org/downloads/) 3.10+.

Create a virtual environment inside the `python` folder and activate it:

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
```

Then install the project in editable mode, together with the `dev` dependency group:

```bash
pip install --upgrade pip
pip install -e . --group dev
```

This installs the dependencies listed in `pyproject.toml` and registers the shared modules (`constants`, `aegis_types`, and `utils`) with the virtual environment, so the tests and scripts can import them from any folder. "Editable" means the install points at your source files instead of copying them, so your changes take effect without reinstalling. Run it again only if you change `pyproject.toml`, for example to add a dependency.

Dependency groups need pip 25.1+, hence the upgrade. The `dev` group contains the test tools plus the linter, formatter, and type checker. A CI job that only runs the tests can install the smaller `test` group instead with `pip install -e . --group test`.

Activate the virtual environment (`source .venv/bin/activate`) in each new terminal before running anything below.

Tests live in `test_examples/` as `test_*.py` files.

Run all tests. They run in parallel, one worker per CPU:

```bash
pytest
```

Run a single file:

```bash
pytest test_examples/test_custom_run_nonblocking.py
```

Run a script from `script_examples/`:

```bash
python script_examples/custom_run_blocking.py
python script_examples/custom_run_nonblocking.py
python script_examples/dataset_run_blocking.py
python script_examples/dataset_run_nonblocking.py
```

Lint, format, and type-check with [Ruff](https://docs.astral.sh/ruff/) and [mypy](https://mypy.readthedocs.io/), both configured in `pyproject.toml`:

```bash
ruff check --fix .
ruff format .
mypy
```

To check without changing any files, as a CI job would, use `ruff check .` and `ruff format --check .` instead.
