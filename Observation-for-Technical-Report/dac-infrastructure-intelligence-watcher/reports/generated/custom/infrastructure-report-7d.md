# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **7d**

Report layer version: **v1.8.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 3 |
| First snapshot | 2026-06-29T13-49-24-711303+00-00-health.json |
| Latest snapshot | 2026-06-30T13-28-33-493377+00-00-health.json |
| First checked at UTC | 2026-06-29T13:49:24.711303+00:00 |
| Latest checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
| Overall status counts | DEGRADED: 1, HEALTHY: 2 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 1, HEALTHY: 2 |
| explorer_web | HEALTHY: 3 |
| primary_explorer_api | HEALTHY: 3 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 9222.0 ms | 18180.0 ms | SLOW: 3 |
| explorer_web | 679.33 ms | 723.0 ms | MODERATE: 3 |
| primary_explorer_api | 447.67 ms | 507.0 ms | FAST: 2, MODERATE: 1 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 80 | 2026-06-29T13:49:24.711303+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 81 | 2026-06-30T08:44:47.357691+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 82 | 2026-06-30T13:28:33.493377+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

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
