# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 5 |
| Observation index range | 45 -> 49 |
| First checked at UTC | 2026-06-18T11:35:52.595819+00:00 |
| Latest checked at UTC | 2026-06-19T05:22:45.224068+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 2, PARTIAL_OUTAGE: 1 |
| Availability score | 0.66 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 6 |
| Observation index range | 50 -> 55 |
| First checked at UTC | 2026-06-19T13:33:33.772138+00:00 |
| Latest checked at UTC | 2026-06-22T21:50:02.920913+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 3, PARTIAL_OUTAGE: 1 |
| Availability score | 0.7167 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 2, HEALTHY: 2, UNHEALTHY: 1 | DEGRADED: 2, HEALTHY: 3, UNHEALTHY: 1 | 8142.2 ms | 6194.33 ms | IMPROVED |
| explorer_web | HEALTHY: 5 | HEALTHY: 6 | 549.4 ms | 653.83 ms | WORSENED |
| primary_explorer_api | HEALTHY: 5 | HEALTHY: 6 | 421.4 ms | 539.83 ms | WORSENED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | MODERATE: 1, SLOW: 4 | FAST: 1, MODERATE: 1, SLOW: 4 | 20946.0 ms | 23841.0 ms |
| explorer_web | FAST: 2, MODERATE: 3 | FAST: 1, MODERATE: 5 | 647.0 ms | 1016.0 ms |
| primary_explorer_api | FAST: 4, MODERATE: 1 | FAST: 1, MODERATE: 5 | 506.0 ms | 811.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.66 to 0.7167: IMPROVED.
- Official Public RPC average response changed from 8142.2 ms to 6194.33 ms: IMPROVED.
- Explorer Web average response changed from 549.4 ms to 653.83 ms: WORSENED.
- Primary Explorer API average response changed from 421.4 ms to 539.83 ms: WORSENED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 45 | 2026-06-18T11:35:52.595819+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 46 | 2026-06-18T14:34:01.163762+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 47 | 2026-06-18T17:47:21.319826+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 48 | 2026-06-19T00:07:49.114576+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 49 | 2026-06-19T05:22:45.224068+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 50 | 2026-06-19T13:33:33.772138+00:00 | DEGRADED | DEGRADED | FAST | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 51 | 2026-06-19T16:20:47.830658+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |
| 52 | 2026-06-21T07:05:49.768754+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 53 | 2026-06-21T10:45:15.026750+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 54 | 2026-06-22T16:01:14.927486+00:00 | PARTIAL_OUTAGE | UNHEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 55 | 2026-06-22T21:50:02.920913+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

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
