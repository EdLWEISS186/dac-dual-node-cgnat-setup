# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **7d**

Report layer version: **v1.8.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 21 |
| First snapshot | 2026-06-21T07-05-49-768754+00-00-health.json |
| Latest snapshot | 2026-06-27T17-16-45-438386+00-00-health.json |
| First checked at UTC | 2026-06-21T07:05:49.768754+00:00 |
| Latest checked at UTC | 2026-06-27T17:16:45.438386+00:00 |
| Overall status counts | DEGRADED: 9, HEALTHY: 9, PARTIAL_OUTAGE: 3 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 9, HEALTHY: 9, UNHEALTHY: 3 |
| explorer_web | HEALTHY: 21 |
| primary_explorer_api | HEALTHY: 21 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 11436.76 ms | 27011.0 ms | SLOW: 21 |
| explorer_web | 620.52 ms | 1016.0 ms | FAST: 4, MODERATE: 17 |
| primary_explorer_api | 475.86 ms | 942.0 ms | FAST: 10, MODERATE: 11 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 52 | 2026-06-21T07:05:49.768754+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 53 | 2026-06-21T10:45:15.026750+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 54 | 2026-06-22T16:01:14.927486+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 55 | 2026-06-22T21:50:02.920913+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 56 | 2026-06-23T05:34:47.341574+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 57 | 2026-06-23T08:46:04.761597+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 58 | 2026-06-24T16:00:28.478127+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 59 | 2026-06-24T18:06:14.278129+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 60 | 2026-06-25T07:53:39.662511+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 61 | 2026-06-25T10:36:00.952733+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 62 | 2026-06-25T15:44:39.846328+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 63 | 2026-06-25T19:29:25.516852+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 64 | 2026-06-26T08:18:53.347052+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 65 | 2026-06-26T11:20:30.135425+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 66 | 2026-06-26T20:55:49.405430+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 67 | 2026-06-26T22:06:06.469588+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 68 | 2026-06-26T23:22:07.890400+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 69 | 2026-06-27T13:14:03.249844+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 70 | 2026-06-27T14:55:49.430298+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 71 | 2026-06-27T16:00:02.127479+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 72 | 2026-06-27T17:16:45.438386+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

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
