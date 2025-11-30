"""Lightweight in-memory metrics collector for the Bug Triage AI Agent."""

from __future__ import annotations

import time
from threading import Lock
from typing import Any, Dict


class MetricsCollector:
    """Aggregates request/health metrics for observability endpoints."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._service_start_ts = time.time()
        self.reset()

    def reset(self) -> None:
        """Reset all counters (mainly used in tests)."""
        with self._lock:
            self.total_requests = 0
            self.successful_requests = 0
            self.failed_requests = 0
            self.validation_failures = 0
            self.total_bugs = 0
            self.total_duration = 0.0
            self.max_duration = 0.0
            self.warning_events = 0
            self.last_request_ts: float | None = None
            self.health_checks = 0
            self.healthy_health_checks = 0
            self.last_health_status: str = "unknown"
            self.last_health_check_ts: float | None = None

    def record_request(
        self,
        duration_seconds: float,
        bug_count: int,
        status: str,
        warnings_count: int = 0,
    ) -> None:
        """Record metrics for a single /execute invocation."""
        with self._lock:
            self.total_requests += 1
            self.total_bugs += bug_count
            self.total_duration += max(duration_seconds, 0.0)
            self.max_duration = max(self.max_duration, duration_seconds)
            self.warning_events += warnings_count
            self.last_request_ts = time.time()

            if status == "completed":
                self.successful_requests += 1
            elif status == "failed_validation":
                self.validation_failures += 1
                self.failed_requests += 1
            else:
                self.failed_requests += 1

    def record_health_check(self, status: str) -> None:
        """Record health check invocations and status."""
        with self._lock:
            self.health_checks += 1
            if status == "healthy":
                self.healthy_health_checks += 1
            self.last_health_status = status
            self.last_health_check_ts = time.time()

    def uptime_seconds(self) -> float:
        """Return service uptime in seconds."""
        return time.time() - self._service_start_ts

    def snapshot(self) -> Dict[str, Any]:
        """Return a snapshot of current metrics."""
        with self._lock:
            avg_latency = (
                (self.total_duration / self.total_requests) if self.total_requests else 0.0
            )
            success_rate = (
                self.successful_requests / self.total_requests if self.total_requests else 0.0
            )
            health_success_rate = (
                self.healthy_health_checks / self.health_checks if self.health_checks else 0.0
            )

            return {
                "totals": {
                    "requests": self.total_requests,
                    "bugs_processed": self.total_bugs,
                    "successful": self.successful_requests,
                    "failed": self.failed_requests,
                    "validation_failures": self.validation_failures,
                    "warning_events": self.warning_events,
                },
                "latency_ms": {
                    "average": round(avg_latency * 1000, 2),
                    "max": round(self.max_duration * 1000, 2),
                },
                "rates": {
                    "success_rate": round(success_rate, 3),
                },
                "health_checks": {
                    "invocations": self.health_checks,
                    "healthy_rate": round(health_success_rate, 3),
                    "last_status": self.last_health_status,
                    "last_checked_at": self._format_ts(self.last_health_check_ts),
                },
                "last_request_at": self._format_ts(self.last_request_ts),
                "uptime_seconds": round(self.uptime_seconds(), 2),
            }

    @staticmethod
    def _format_ts(ts: float | None) -> str | None:
        if ts is None:
            return None
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


metrics_collector = MetricsCollector()


