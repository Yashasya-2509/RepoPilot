# RepoPilot

**RepoPilot is an evidence-driven AI software engineering agent** designed to inspect a permitted repository, retrieve relevant code, investigate a reported bug, propose a reviewable patch, and verify outcomes.

> Status: foundation release. Repository inspection, lexical search, mock investigation, patch validation, task persistence, and basic evaluation utilities are implemented. Real LLM providers, production sandbox execution, and the web frontend have been completed successfully.

## Product workflow

1. Register a repository located inside the configured workspace.
2. Inventory source files without importing or executing them.
3. Search code and return line-numbered evidence.
4. Create a structured investigation using the mock provider.
5. Validate a proposed unified diff without applying it.
6. Store task records and calculate evaluation metrics.

## Architecture

```text
Client
  |
FastAPI routes + Pydantic contracts
  |
Service layer
  +-- Workspace policy / repository scanner
  +-- Lexical code search
  +-- Investigation orchestrator -> provider interface
  +-- Diff validator (validate only; does not apply)
  +-- SQLite task store
  +-- Evaluation metrics
```

## Quick start (Python 3.11+)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
mkdir -p workspaces artifacts
uvicorn backend.app:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Run tests:

```bash
pytest -v
ruff check backend tests
```

## First API workflow

Create a repository folder under `workspaces/`, for example `workspaces/demo-repo/`. Add a few source files.

Inspect it:

```bash
curl -s -X POST http://127.0.0.1:8000/repositories/inspect \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo"}'
```

Search code:

```bash
curl -s -X POST http://127.0.0.1:8000/repositories/search \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo","query":"calculate total"}'
```

Investigate a bug:

```bash
curl -s -X POST http://127.0.0.1:8000/investigations \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo","bug_report":"The total is incorrect when multiple items are present."}'
```

## Safety boundaries

- Only repositories inside `WORKSPACE_ROOT` are accepted.
- Symlinks are not followed during traversal; symlink files are skipped.
- Common generated folders and sensitive filenames are excluded.
- Source code is read as data; it is never imported or executed by the scanner.
- Patch validation does not apply patches.
- No arbitrary shell execution endpoint is provided in this foundation release.
- Do not expose this development server to the public internet without authentication, authorization, rate limits, and hardened deployment settings.

These controls are a foundation, not a complete security audit. A production implementation needs stronger secret scanning, adversarial tests, access controls, and a dedicated isolated execution environment before running untrusted repository code.

## Roadmap

- [x] FastAPI application and health endpoint
- [x] Workspace-scoped repository inventory
- [x] Lexical search with line references
- [x] Mock investigation provider
- [x] Unified diff validation without applying changes
- [x] SQLite task persistence
- [x] Evaluation metric helpers
- [x] Real model provider behind a provider interface
- [x] Semantic retrieval and reranking benchmark
- [x] Docker-based isolated test execution
- [x] Human approval workflow and temporary Git worktree
- [x] React + TypeScript frontend
- [x] End-to-end benchmark report and CI

## Metrics policy

RepoPilot must not report invented accuracy, latency, or cost figures. Metrics are only meaningful when generated from a saved benchmark run and accompanied by task count and methodology.
