# RepoPilot benchmark

Store benchmark tasks as JSONL. Each task should identify a fixed fixture repository commit, bug report, expected behavior, and test command metadata. Do not store secrets or private customer code.

Suggested fields:
- `task_id`
- `repository_fixture`
- `bug_report`
- `expected_files`
- `fix_test`
- `regression_tests`
- `difficulty`
- `notes`

Report task count, exact metric definitions, model/provider, configuration, and failures. Never report a performance improvement without a reproducible baseline and saved run results.
