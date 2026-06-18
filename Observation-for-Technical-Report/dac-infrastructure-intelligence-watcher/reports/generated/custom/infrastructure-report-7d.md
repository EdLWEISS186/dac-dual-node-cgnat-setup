# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **7d**

Report layer version: **v1.8.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 10 |
| First snapshot | 2026-06-13T10-43-09-685105+00-00-health.json |
| Latest snapshot | 2026-06-15T20-07-32-425470+00-00-health.json |
| First checked at UTC | 2026-06-13T10:43:09.685105+00:00 |
| Latest checked at UTC | 2026-06-15T20:07:32.425470+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 5, PARTIAL_OUTAGE: 2 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 3, HEALTHY: 5, UNHEALTHY: 2 |
| explorer_web | HEALTHY: 10 |
| primary_explorer_api | HEALTHY: 10 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 1428.6 ms | 4632.0 ms | FAST: 2, MODERATE: 3, SLOW: 5 |
| explorer_web | 719.0 ms | 1246.0 ms | FAST: 1, MODERATE: 9 |
| primary_explorer_api | 537.1 ms | 1157.0 ms | FAST: 4, MODERATE: 6 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 35 | 2026-06-13T10:43:09.685105+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 36 | 2026-06-13T12:15:24.292365+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |
| 37 | 2026-06-13T17:43:45.241764+00:00 | PARTIAL_OUTAGE | UNHEALTHY | FAST | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 38 | 2026-06-13T18:57:21.166839+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 39 | 2026-06-14T02:47:39.011114+00:00 | PARTIAL_OUTAGE | UNHEALTHY | FAST | HEALTHY | MODERATE | HEALTHY | FAST |
| 40 | 2026-06-14T07:17:43.721261+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 41 | 2026-06-14T15:06:02.854660+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 42 | 2026-06-14T17:46:11.842614+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 43 | 2026-06-15T16:32:07.477470+00:00 | DEGRADED | DEGRADED | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 44 | 2026-06-15T20:07:32.425470+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |

## 5. Status & Response-Class Glossary

| Status / Class | Meaning |
|---|---|
| HEALTHY | The endpoint or overall infrastructure state is reachable and behaving as expected. |
| DEGRADED | The endpoint is reachable, but one or more checks or response-time indicators show reduced quality. |
| PARTIAL_OUTAGE | At least one monitored endpoint is unavailable or failing while other endpoints remain reachable. |
| UNHEALTHY | The endpoint failed required checks or did not provide usable responses. |
| FAST | The observed response-time class is fast for this watcher context. |
| MODERATE | The observed response-time class is acceptable but not fast. |
| SLOW | The observed response-time class is slow and may indicate degraded user experience. |
| UNKNOWN | The watcher could not classify the response-time state, often because older snapshots did not include this field. |
| N/A | Not available or not applicable for the selected observation, endpoint, or historical snapshot. |

## 6. Interpretation Guide

- Availability status describes whether a service is reachable and usable.
- Response class describes response-time behavior, not availability.
- Older snapshots may show UNKNOWN or null response class because response-time classification was added after the initial watcher release.
- This custom range report is independent observation material and not an official DAC service status page.

---

Prepared by **JERUZZALEM — DAC Infra Tester**.
