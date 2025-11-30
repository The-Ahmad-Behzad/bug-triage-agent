"""Unit tests for the metrics collector."""

from src.utils.metrics import MetricsCollector


def test_metrics_collector_records_success_and_failure():
    collector = MetricsCollector()

    collector.record_request(duration_seconds=0.1, bug_count=2, status="completed", warnings_count=1)
    collector.record_request(duration_seconds=0.2, bug_count=1, status="failed_validation")
    collector.record_request(duration_seconds=0.05, bug_count=0, status="error")
    collector.record_health_check("healthy")
    collector.record_health_check("degraded")

    snapshot = collector.snapshot()

    assert snapshot["totals"]["requests"] == 3
    assert snapshot["totals"]["successful"] == 1
    assert snapshot["totals"]["failed"] == 2
    assert snapshot["totals"]["warning_events"] == 1
    assert snapshot["latency_ms"]["average"] > 0
    assert snapshot["rates"]["success_rate"] == round(1 / 3, 3)
    assert snapshot["health_checks"]["invocations"] == 2
    assert snapshot["health_checks"]["healthy_rate"] == round(1 / 2, 3)


def test_metrics_collector_reset():
    collector = MetricsCollector()
    collector.record_request(0.1, 1, "completed")
    collector.reset()
    snapshot = collector.snapshot()
    assert snapshot["totals"]["requests"] == 0
    assert snapshot["totals"]["bugs_processed"] == 0

