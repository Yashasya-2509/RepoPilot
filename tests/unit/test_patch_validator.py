from backend.patches.validator import validate_unified_diff


def test_valid_diff_is_accepted_for_review():
    diff = (
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-return 0\n"
        "+return 1\n"
    )
    result = validate_unified_diff(diff)
    assert result["valid"] is True
    assert result["files"] == ["app.py"]


def test_parent_path_is_rejected():
    diff = (
        "--- a/../secret.txt\n"
        "+++ b/../secret.txt\n"
        "@@ -1,1 +1,1 @@\n"
        "-x\n"
        "+y\n"
    )
    result = validate_unified_diff(diff)
    assert result["valid"] is False
    assert any("Unsafe patch path" in error for error in result["errors"])
