# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 7 |
| Observation index range | 51 -> 57 |
| First checked at UTC | 2026-06-19T16:20:47.830658+00:00 |
| Latest checked at UTC | 2026-06-23T08:46:04.761597+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 4, PARTIAL_OUTAGE: 1 |
| Availability score | 0.7571 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 8 |
| Observation index range | 58 -> 65 |
| First checked at UTC | 2026-06-24T16:00:28.478127+00:00 |
| Latest checked at UTC | 2026-06-26T11:20:30.135425+00:00 |
| Overall status counts | DEGRADED: 4, HEALTHY: 2, PARTIAL_OUTAGE: 2 |
| Availability score | 0.575 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 2, HEALTHY: 4, UNHEALTHY: 1 | DEGRADED: 4, HEALTHY: 2, UNHEALTHY: 2 | 7527.86 ms | 15354.0 ms | WORSENED |
| explorer_web | HEALTHY: 7 | HEALTHY: 8 | 683.29 ms | 564.5 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 7 | HEALTHY: 8 | 540.57 ms | 434.88 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | MODERATE: 1, SLOW: 6 | SLOW: 8 | 23841.0 ms | 27011.0 ms |
| explorer_web | FAST: 2, MODERATE: 5 | FAST: 3, MODERATE: 5 | 1016.0 ms | 651.0 ms |
| primary_explorer_api | FAST: 2, MODERATE: 5 | FAST: 5, MODERATE: 3 | 942.0 ms | 511.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.7571 to 0.575: WORSENED.
- Official Public RPC average response changed from 7527.86 ms to 15354.0 ms: WORSENED.
- Explorer Web average response changed from 683.29 ms to 564.5 ms: IMPROVED.
- Primary Explorer API average response changed from 540.57 ms to 434.88 ms: IMPROVED.
- The later observation window shows weaker overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 51 | 2026-06-19T16:20:47.830658+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |
| 52 | 2026-06-21T07:05:49.768754+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 53 | 2026-06-21T10:45:15.026750+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 54 | 2026-06-22T16:01:14.927486+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 55 | 2026-06-22T21:50:02.920913+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 56 | 2026-06-23T05:34:47.341574+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 57 | 2026-06-23T08:46:04.761597+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 58 | 2026-06-24T16:00:28.478127+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 59 | 2026-06-24T18:06:14.278129+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 60 | 2026-06-25T07:53:39.662511+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 61 | 2026-06-25T10:36:00.952733+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 62 | 2026-06-25T15:44:39.846328+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 63 | 2026-06-25T19:29:25.516852+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 64 | 2026-06-26T08:18:53.347052+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 65 | 2026-06-26T11:20:30.135425+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |

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
