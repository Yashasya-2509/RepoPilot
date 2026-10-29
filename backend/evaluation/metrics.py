from statistics import mean, median


def summarize_runs(runs: list[dict]) -> dict:
    """Summarize already-measured runs. Missing values are ignored, not fabricated."""
    if not runs:
        return {
            "task_count": 0,
            "success_rate": None,
            "median_duration_seconds": None,
            "mean_cost": None,
        }

    outcomes = [run["success"] for run in runs if isinstance(run.get("success"), bool)]
    durations = [
        float(run["duration_seconds"])
        for run in runs
        if isinstance(run.get("duration_seconds"), (int, float))
        and run["duration_seconds"] >= 0
    ]
    costs = [
        float(run["cost"])
        for run in runs
        if isinstance(run.get("cost"), (int, float)) and run["cost"] >= 0
    ]

    return {
        "task_count": len(runs),
        "success_rate": mean(outcomes) if outcomes else None,
        "median_duration_seconds": median(durations) if durations else None,
        "mean_cost": mean(costs) if costs else None,
    }
