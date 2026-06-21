# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 6 |
| Observation index range | 41 -> 46 |
| First checked at UTC | 2026-06-14T15:06:02.854660+00:00 |
| Latest checked at UTC | 2026-06-18T14:34:01.163762+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 2, PARTIAL_OUTAGE: 1 |
| Availability score | 0.6417 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 7 |
| Observation index range | 47 -> 53 |
| First checked at UTC | 2026-06-18T17:47:21.319826+00:00 |
| Latest checked at UTC | 2026-06-21T10:45:15.026750+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 4 |
| Availability score | 0.8071 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 3, HEALTHY: 2, UNHEALTHY: 1 | DEGRADED: 3, HEALTHY: 4 | 5719.33 ms | 3449.57 ms | IMPROVED |
| explorer_web | HEALTHY: 6 | HEALTHY: 7 | 695.33 ms | 605.0 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 6 | HEALTHY: 7 | 488.5 ms | 471.57 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | MODERATE: 2, SLOW: 4 | FAST: 1, MODERATE: 2, SLOW: 4 | 20946.0 ms | 17553.0 ms |
| explorer_web | FAST: 2, MODERATE: 4 | FAST: 2, MODERATE: 5 | 1246.0 ms | 1016.0 ms |
| primary_explorer_api | FAST: 2, MODERATE: 4 | FAST: 4, MODERATE: 3 | 703.0 ms | 811.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.6417 to 0.8071: IMPROVED.
- Official Public RPC average response changed from 5719.33 ms to 3449.57 ms: IMPROVED.
- Explorer Web average response changed from 695.33 ms to 605.0 ms: IMPROVED.
- Primary Explorer API average response changed from 488.5 ms to 471.57 ms: IMPROVED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 41 | 2026-06-14T15:06:02.854660+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 42 | 2026-06-14T17:46:11.842614+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 43 | 2026-06-15T16:32:07.477470+00:00 | DEGRADED | DEGRADED | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 44 | 2026-06-15T20:07:32.425470+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |
| 45 | 2026-06-18T11:35:52.595819+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 46 | 2026-06-18T14:34:01.163762+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 47 | 2026-06-18T17:47:21.319826+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 48 | 2026-06-19T00:07:49.114576+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 49 | 2026-06-19T05:22:45.224068+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |
| 50 | 2026-06-19T13:33:33.772138+00:00 | DEGRADED | DEGRADED | FAST | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 51 | 2026-06-19T16:20:47.830658+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |
| 52 | 2026-06-21T07:05:49.768754+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 53 | 2026-06-21T10:45:15.026750+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

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
