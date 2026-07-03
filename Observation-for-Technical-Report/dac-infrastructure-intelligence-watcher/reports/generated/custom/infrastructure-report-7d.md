# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **7d**

Report layer version: **v1.8.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 16 |
| First snapshot | 2026-06-26T22-06-06-469588+00-00-health.json |
| Latest snapshot | 2026-06-30T13-28-33-493377+00-00-health.json |
| First checked at UTC | 2026-06-26T22:06:06.469588+00:00 |
| Latest checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
| Overall status counts | DEGRADED: 8, HEALTHY: 8 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 8, HEALTHY: 8 |
| explorer_web | HEALTHY: 16 |
| primary_explorer_api | HEALTHY: 16 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 8781.06 ms | 27901.0 ms | SLOW: 16 |
| explorer_web | 653.5 ms | 801.0 ms | MODERATE: 16 |
| primary_explorer_api | 466.19 ms | 612.0 ms | FAST: 7, MODERATE: 9 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 67 | 2026-06-26T22:06:06.469588+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 68 | 2026-06-26T23:22:07.890400+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 69 | 2026-06-27T13:14:03.249844+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 70 | 2026-06-27T14:55:49.430298+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 71 | 2026-06-27T16:00:02.127479+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 72 | 2026-06-27T17:16:45.438386+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 73 | 2026-06-27T19:57:07.933682+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 74 | 2026-06-27T20:59:11.427839+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 75 | 2026-06-28T06:01:40.043636+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 76 | 2026-06-28T09:30:32.330521+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 77 | 2026-06-28T12:51:16.533873+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 78 | 2026-06-28T14:43:06.952490+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 79 | 2026-06-29T09:24:55.311755+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
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
