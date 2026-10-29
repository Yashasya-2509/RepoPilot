import os
from collections import Counter
from pathlib import Path

from backend.config import Settings

IGNORED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".next", "coverage", "vendor",
}
SENSITIVE_NAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_ed25519", "credentials.json", "secrets.json",
}
LANGUAGES = {
    ".py": "Python", ".java": "Java", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust",
    ".cpp": "C++", ".cc": "C++", ".c": "C", ".h": "C/C++ Header",
    ".cs": "C#", ".php": "PHP", ".rb": "Ruby", ".swift": "Swift",
    ".kt": "Kotlin", ".kts": "Kotlin", ".sql": "SQL", ".sh": "Shell",
    ".html": "HTML", ".css": "CSS", ".md": "Markdown", ".json": "JSON",
    ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
}


def is_sensitive_name(name: str) -> bool:
    lower = name.lower()
    return (
        lower in SENSITIVE_NAMES
        or lower.startswith(".env.")
        or lower.endswith((".pem", ".p12", ".pfx", ".key"))
        or "secret" in lower
    )


def inspect_repository(root: Path, settings: Settings) -> dict:
    """Inventory files as data. Never imports or executes repository content."""
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Repository path must be a directory.")

    files: list[dict] = []
    skipped = Counter()
    languages = Counter()

    for current_dir, dirs, filenames in os.walk(root, followlinks=False):
        current = Path(current_dir)
        kept_dirs = []
        for name in dirs:
            directory = current / name
            if name in IGNORED_DIRS:
                skipped["ignored_directory"] += 1
            elif directory.is_symlink():
                skipped["symlink_directory"] += 1
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs

        for filename in filenames:
            path = current / filename
            if is_sensitive_name(filename):
                skipped["sensitive_name"] += 1
                continue
            if path.is_symlink():
                skipped["symlink"] += 1
                continue
            try:
                if not path.is_file():
                    skipped["not_regular_file"] += 1
                    continue
                size = path.stat().st_size
                if size > settings.max_file_bytes:
                    skipped["too_large"] += 1
                    continue
                with path.open("rb") as stream:
                    prefix = stream.read(8192)
                if b"\x00" in prefix:
                    skipped["binary"] += 1
                    continue
                language = LANGUAGES.get(path.suffix.lower(), "Other")
                relative = path.relative_to(root).as_posix()
                files.append({"path": relative, "size_bytes": size, "language": language})
                languages[language] += 1
                if len(files) >= settings.max_files:
                    skipped["file_limit_reached"] += 1
                    dirs[:] = []
                    break
            except OSError:
                skipped["unreadable"] += 1

    files.sort(key=lambda item: item["path"])
    return {
        "repository": root.name,
        "file_count": len(files),
        "languages": dict(sorted(languages.items())),
        "files": files,
        "skipped": dict(sorted(skipped.items())),
    }


def safe_read_text(root: Path, relative_path: str, settings: Settings) -> str:
    """Read a bounded, non-sensitive regular file under the repository root."""
    root = root.resolve(strict=True)
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Path must be a safe repository-relative path.")

    candidate = root.joinpath(relative)
    # Check every existing path component for symlinks.
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("Symlinks are not readable by the repository service.")

    resolved = candidate.resolve(strict=True)
    if root not in resolved.parents:
        raise ValueError("Path escapes repository root.")
    if not resolved.is_file() or is_sensitive_name(resolved.name):
        raise ValueError("File is not eligible for reading.")
    if resolved.stat().st_size > settings.max_file_bytes:
        raise ValueError("File exceeds configured size limit.")

    data = resolved.read_bytes()
    if b"\x00" in data[:8192]:
        raise ValueError("Binary files are not eligible for reading.")
    return data.decode("utf-8", errors="replace")
