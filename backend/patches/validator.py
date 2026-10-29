import re
from pathlib import PurePosixPath

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@")
MAX_PATCH_FILES = 20


def validate_unified_diff(diff: str) -> dict:
    """Validate basic unified-diff structure and paths. Does not apply the patch."""
    errors = []
    files = []
    saw_hunk = False
    current_file = None

    for line in diff.splitlines():
        if line.startswith(("--- ", "+++ ")):
            raw_path = line[4:].split("\t", 1)[0].strip()
            if raw_path == "/dev/null":
                continue
            if raw_path.startswith(("a/", "b/")):
                raw_path = raw_path[2:]
            path = PurePosixPath(raw_path)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                errors.append(f"Unsafe patch path: {raw_path}")
                continue
            if path.parts[0] == ".git" or any(part in {".env", "secrets.json"} for part in path.parts):
                errors.append(f"Protected path in patch: {raw_path}")
                continue
            if line.startswith("+++ "):
                current_file = raw_path
                if raw_path not in files:
                    files.append(raw_path)
        elif HUNK_RE.match(line):
            saw_hunk = True

    if not files:
        errors.append("No eligible changed file found in diff.")
    if not saw_hunk:
        errors.append("No unified-diff hunk header was found.")
    if len(files) > MAX_PATCH_FILES:
        errors.append(f"Patch exceeds the {MAX_PATCH_FILES}-file limit.")

    return {
        "valid": not errors,
        "files": files,
        "errors": errors,
        "note": "Validation only: this function does not apply or execute the patch.",
    }
