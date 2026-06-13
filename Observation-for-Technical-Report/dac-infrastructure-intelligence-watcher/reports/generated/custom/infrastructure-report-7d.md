# DAC Infrastructure Intelligence Watcher — Custom Range Report

Range: **7d**

Report layer version: **v1.8.0**

This report is generated from infrastructure health snapshots and is intended for range-based technical review.

---

## 1. Range Summary

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Snapshot count | 20 |
| First snapshot | 2026-06-07T08-29-35-513958+00-00-health.json |
| Latest snapshot | 2026-06-13T12-15-24-292365+00-00-health.json |
| First checked at UTC | 2026-06-07T08:29:35.513958+00:00 |
| Latest checked at UTC | 2026-06-13T12:15:24.292365+00:00 |
| Overall status counts | DEGRADED: 10, HEALTHY: 10 |

## 2. Endpoint Status Counts

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 10, HEALTHY: 10 |
| explorer_web | HEALTHY: 20 |
| primary_explorer_api | HEALTHY: 20 |

## 3. Response-Time Summary

| Endpoint | Average response | Max response | Response class counts |
|---|---:|---:|---|
| official_public_rpc | 3008.05 ms | 15388.0 ms | MODERATE: 1, SLOW: 19 |
| explorer_web | 569.45 ms | 841.0 ms | FAST: 8, MODERATE: 12 |
| primary_explorer_api | 414.3 ms | 544.0 ms | FAST: 17, MODERATE: 3 |

## 4. Snapshot Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 17 | 2026-06-07T08:29:35.513958+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 18 | 2026-06-07T10:41:05.109781+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 19 | 2026-06-07T12:12:00.907268+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 20 | 2026-06-07T17:06:43.581492+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 21 | 2026-06-08T01:59:16.847351+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 22 | 2026-06-08T06:47:13.271825+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 23 | 2026-06-09T01:30:52.519172+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 24 | 2026-06-09T05:51:55.728730+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 25 | 2026-06-09T12:21:12.097443+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 26 | 2026-06-09T15:36:15.483799+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 27 | 2026-06-09T17:35:46.336066+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 28 | 2026-06-09T21:23:45.229029+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 29 | 2026-06-10T12:00:49.579476+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 30 | 2026-06-10T16:06:33.205459+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 31 | 2026-06-10T18:40:39.968153+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 32 | 2026-06-10T21:13:30.728841+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 33 | 2026-06-10T22:57:26.492242+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 34 | 2026-06-11T00:13:29.727818+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 35 | 2026-06-13T10:43:09.685105+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 36 | 2026-06-13T12:15:24.292365+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |

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
