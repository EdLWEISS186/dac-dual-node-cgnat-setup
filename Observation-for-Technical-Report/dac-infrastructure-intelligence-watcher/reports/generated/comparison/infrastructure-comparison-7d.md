# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 11 |
| Observation index range | 52 -> 62 |
| First checked at UTC | 2026-06-21T07:05:49.768754+00:00 |
| Latest checked at UTC | 2026-06-25T15:44:39.846328+00:00 |
| Overall status counts | DEGRADED: 5, HEALTHY: 4, PARTIAL_OUTAGE: 2 |
| Availability score | 0.65 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 12 |
| Observation index range | 63 -> 74 |
| First checked at UTC | 2026-06-25T19:29:25.516852+00:00 |
| Latest checked at UTC | 2026-06-27T20:59:11.427839+00:00 |
| Overall status counts | DEGRADED: 5, HEALTHY: 6, PARTIAL_OUTAGE: 1 |
| Availability score | 0.7458 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 5, HEALTHY: 4, UNHEALTHY: 2 | DEGRADED: 5, HEALTHY: 6, UNHEALTHY: 1 | 11647.36 ms | 11397.25 ms | IMPROVED |
| explorer_web | HEALTHY: 11 | HEALTHY: 12 | 645.55 ms | 607.42 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 11 | HEALTHY: 12 | 501.45 ms | 459.75 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 11 | SLOW: 12 | 25009.0 ms | 27901.0 ms |
| explorer_web | FAST: 3, MODERATE: 8 | FAST: 1, MODERATE: 11 | 1016.0 ms | 737.0 ms |
| primary_explorer_api | FAST: 5, MODERATE: 6 | FAST: 5, MODERATE: 7 | 942.0 ms | 612.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.65 to 0.7458: IMPROVED.
- Official Public RPC average response changed from 11647.36 ms to 11397.25 ms: IMPROVED.
- Explorer Web average response changed from 645.55 ms to 607.42 ms: IMPROVED.
- Primary Explorer API average response changed from 501.45 ms to 459.75 ms: IMPROVED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

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

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
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
| 73 | 2026-06-27T19:57:07.933682+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 74 | 2026-06-27T20:59:11.427839+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

## 6. Status & Response-Class Glossary

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

## 7. Interpretation Guide

- Window A represents the earlier observation segment.
- Window B represents the later observation segment.
- For availability score, higher is better.
- For response time, lower is better.
- Older snapshots may show N/A or UNKNOWN response classes because response-time classification was added after the initial watcher release.
- This comparison report is independent observation material and not an official DAC service status page.

---

Prepared by **JERUZZALEM — DAC Infra Tester**.
