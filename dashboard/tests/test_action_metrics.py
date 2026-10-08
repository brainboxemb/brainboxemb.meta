import datetime as dt
import importlib.util
import pathlib
import sys
import unittest
import time
from threading import Lock
from unittest import mock

MODULE = pathlib.Path(__file__).parents[1] / "src" / "collect_action_metrics.py"
spec = importlib.util.spec_from_file_location("action_metrics", MODULE)
action_metrics = importlib.util.module_from_spec(spec)
assert spec.loader
sys.modules[spec.name] = action_metrics
spec.loader.exec_module(action_metrics)


class ActionMetricsTests(unittest.TestCase):

    def test_parallel_collection_and_bounded_concurrency(self):
        config = {"dashboard": {"owner": "brainboxemb"},
                  "groups": [{"repositories": ["one", "two", "three", "four", "five"]}]}
        lock = Lock()
        active = 0
        peak = 0
        def fetch(owner, repo, token, cutoff, stats=None):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(active, peak)
            time.sleep(0.02)
            with lock:
                active -= 1
            stats.update({"pages": 1, "runs": 1})
            return [{"status": "completed", "conclusion": "success", "workflow_id": 1,
                     "name": "Build", "run_started_at": "2026-10-07T10:00:00Z",
                     "updated_at": "2026-10-07T10:00:01Z"}]
        with mock.patch.object(action_metrics, "fetch_recent_runs", side_effect=fetch):
            snapshot, errors = action_metrics.build_snapshot(config, None)
        self.assertEqual(errors, [])
        self.assertEqual(snapshot["summary"]["runs"], 5)
        self.assertEqual(sum(w["runs"] for w in snapshot["workflows"]), 5)
        self.assertGreater(peak, 1)
        self.assertLessEqual(peak, 4)

    def test_collection_failure_does_not_publish_partial_snapshot(self):
        config = {"dashboard": {"owner": "brainboxemb"},
                  "groups": [{"repositories": ["ok", "broken"]}]}
        def fetch(owner, repo, token, cutoff, stats=None):
            if repo == "broken":
                raise RuntimeError("API error")
            return []
        with mock.patch.object(action_metrics, "fetch_recent_runs", side_effect=fetch):
            snapshot, errors = action_metrics.build_snapshot(config, None)
        self.assertIsNone(snapshot)
        self.assertIn("broken", errors[0])

    def test_pagination_counts_pages_and_runs(self):
        cutoff = dt.datetime(2026, 9, 8, tzinfo=dt.timezone.utc)
        batch = [{"created_at": "2026-10-08T00:00:00Z"}] * 100
        with mock.patch.object(action_metrics, "request_json_with_retry", side_effect=[
            {"workflow_runs": batch},
            {"workflow_runs": [{"created_at": "2026-09-07T00:00:00Z"}]}
        ]) as req:
            stats = {}
            runs = action_metrics.fetch_recent_runs("brainboxemb", "repo", None, cutoff, stats)
        self.assertEqual(len(runs), 100)
        self.assertEqual(stats, {"pages": 2, "runs": 100})
        self.assertEqual(req.call_count, 2)

    def test_summarize_runs(self):
        runs = [
            {
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-09-10T10:00:00Z",
                "run_started_at": "2026-09-10T10:02:00Z",
                "updated_at": "2026-09-10T10:12:00Z",
            },
            {
                "status": "completed",
                "conclusion": "failure",
                "created_at": "2026-09-10T11:00:00Z",
                "run_started_at": "2026-09-10T11:01:00Z",
                "updated_at": "2026-09-10T11:06:00Z",
            },
        ]

        metrics = action_metrics.summarize_runs(runs)
        self.assertEqual(metrics["runs"], 2)
        self.assertEqual(metrics["success"], 1)
        self.assertEqual(metrics["failed"], 1)
        self.assertEqual(metrics["cancelled"], 0)
        self.assertEqual(metrics["success_rate"], 50.0)
        self.assertEqual(metrics["runtime_seconds"], 900)
        self.assertEqual(metrics["avg_runtime_seconds"], 450.0)
        self.assertEqual(metrics["avg_queue_seconds"], 90.0)

    def test_snapshot_state_ignores_collection_timestamp(self):
        base = {
            "generated_at": "2026-09-09T12:00:00Z",
            "period_start": "2026-08-10",
            "period_end": "2026-09-09",
            "window_days": 30,
            "summary": {"runs": 1},
            "repositories": [{"name": "repo", "runs": 1}],
            "workflows": [{"name": "Build", "runs": 1}],
        }
        newer = dict(base)
        newer["generated_at"] = "2026-09-10T12:00:00Z"
        newer["period_start"] = "2026-08-11"
        newer["period_end"] = "2026-09-10"
        self.assertEqual(
            action_metrics.snapshot_state(base),
            action_metrics.snapshot_state(newer),
        )

    def test_configured_repositories_are_deduplicated(self):
        config = {
            "dashboard": {"owner": "brainboxemb"},
            "groups": [
                {"repositories": ["one", "two"]},
                {"repositories": ["one"]},
            ],
        }
        repositories = action_metrics.configured_repositories(config)
        self.assertEqual(
            [(item["owner"], item["name"]) for item in repositories],
            [("brainboxemb", "one"), ("brainboxemb", "two")],
        )


if __name__ == "__main__":
    unittest.main()
