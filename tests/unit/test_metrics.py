from backend.evaluation.metrics import summarize_runs


def test_metrics_are_calculated_from_actual_runs():
    result = summarize_runs([
        {"success": True, "duration_seconds": 2.0, "cost": 0.02},
        {"success": False, "duration_seconds": 4.0, "cost": 0.04},
    ])
    assert result["task_count"] == 2
    assert result["success_rate"] == 0.5
    assert result["median_duration_seconds"] == 3.0
    assert result["mean_cost"] == 0.03


def test_empty_metrics_do_not_invent_values():
    result = summarize_runs([])
    assert result["task_count"] == 0
    assert result["success_rate"] is None
