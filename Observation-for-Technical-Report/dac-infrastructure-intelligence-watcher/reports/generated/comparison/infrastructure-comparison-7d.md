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
| Observation index range | 72 -> 76 |
| First checked at UTC | 2026-06-27T17:16:45.438386+00:00 |
| Latest checked at UTC | 2026-06-28T09:30:32.330521+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 3 |
| Availability score | 0.82 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 6 |
| Observation index range | 77 -> 82 |
| First checked at UTC | 2026-06-28T12:51:16.533873+00:00 |
| Latest checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 3 |
| Availability score | 0.775 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 2, HEALTHY: 3 | DEGRADED: 3, HEALTHY: 3 | 6663.8 ms | 10044.83 ms | WORSENED |
| explorer_web | HEALTHY: 5 | HEALTHY: 6 | 671.4 ms | 680.0 ms | WORSENED |
| primary_explorer_api | HEALTHY: 5 | HEALTHY: 6 | 496.4 ms | 442.5 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 5 | SLOW: 6 | 27901.0 ms | 21332.0 ms |
| explorer_web | MODERATE: 5 | MODERATE: 6 | 737.0 ms | 801.0 ms |
| primary_explorer_api | FAST: 1, MODERATE: 4 | FAST: 4, MODERATE: 2 | 580.0 ms | 507.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.82 to 0.775: WORSENED.
- Official Public RPC average response changed from 6663.8 ms to 10044.83 ms: WORSENED.
- Explorer Web average response changed from 671.4 ms to 680.0 ms: WORSENED.
- Primary Explorer API average response changed from 496.4 ms to 442.5 ms: IMPROVED.
- The later observation window shows weaker overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 72 | 2026-06-27T17:16:45.438386+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 73 | 2026-06-27T19:57:07.933682+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 74 | 2026-06-27T20:59:11.427839+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 75 | 2026-06-28T06:01:40.043636+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 76 | 2026-06-28T09:30:32.330521+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 77 | 2026-06-28T12:51:16.533873+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 78 | 2026-06-28T14:43:06.952490+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 79 | 2026-06-29T09:24:55.311755+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 80 | 2026-06-29T13:49:24.711303+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 81 | 2026-06-30T08:44:47.357691+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 82 | 2026-06-30T13:28:33.493377+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

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
