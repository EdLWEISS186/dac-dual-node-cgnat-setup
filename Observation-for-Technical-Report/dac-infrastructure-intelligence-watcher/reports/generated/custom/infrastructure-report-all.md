# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **all**

Report layer version: **v1.4.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 14 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-04T19-47-12-825324+00-00-health.json |
| First checked at UTC | 2026-06-04T09:54:55.772035+00:00 |
| Latest checked at UTC | 2026-06-04T19:47:12.825324+00:00 |
| Overall status counts | DEGRADED: 4, HEALTHY: 5, PARTIAL_OUTAGE: 5 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 4, HEALTHY: 5, UNHEALTHY: 5 |
| explorer_web | HEALTHY: 14 |
| primary_explorer_api | HEALTHY: 14 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 2096.75 ms | 5347.0 ms | MODERATE: 2, SLOW: 2, UNKNOWN: 10 |
| explorer_web | 1149.71 ms | 2299.0 ms | MODERATE: 4, UNKNOWN: 10 |
| primary_explorer_api | 523.5 ms | 620.0 ms | FAST: 1, MODERATE: 3, UNKNOWN: 10 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 1 | 2026-06-04T09:54:55.772035+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 2 | 2026-06-04T09:59:08.192048+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 3 | 2026-06-04T09:59:48.937274+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 4 | 2026-06-04T10:00:10.486388+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 5 | 2026-06-04T10:02:58.023788+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 6 | 2026-06-04T11:35:39.447567+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 7 | 2026-06-04T11:36:10.013189+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 8 | 2026-06-04T11:38:16.082796+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 9 | 2026-06-04T11:38:26.409385+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 10 | 2026-06-04T11:50:50.288397+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 11 | 2026-06-04T16:59:50.793517+00:00 | PARTIAL_OUTAGE | UNHEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 12 | 2026-06-04T17:34:38.689983+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 13 | 2026-06-04T17:39:38.929050+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 14 | 2026-06-04T19:47:12.825324+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |

## 5. Interpretation Guide

- Availability status describes whether a service is reachable and usable.
- Response class describes response-time behavior, not availability.
- Older snapshots may show `N/A` response class because response-time classification was added after the initial watcher release.
- This custom range report is independent observation material and not an official DAC service status page.

---

Prepared by **JERUZZALEM — DAC Infra Tester**.
