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
| Observation index range | 35 -> 39 |
| First checked at UTC | 2026-06-13T10:43:09.685105+00:00 |
| Latest checked at UTC | 2026-06-14T02:47:39.011114+00:00 |
| Overall status counts | DEGRADED: 1, HEALTHY: 2, PARTIAL_OUTAGE: 2 |
| Availability score | 0.59 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 5 |
| Observation index range | 40 -> 44 |
| First checked at UTC | 2026-06-14T07:17:43.721261+00:00 |
| Latest checked at UTC | 2026-06-15T20:07:32.425470+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 3 |
| Availability score | 0.82 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 1, HEALTHY: 2, UNHEALTHY: 2 | DEGRADED: 2, HEALTHY: 3 | 1249.6 ms | 1607.6 ms | WORSENED |
| explorer_web | HEALTHY: 5 | HEALTHY: 5 | 706.2 ms | 731.8 ms | WORSENED |
| primary_explorer_api | HEALTHY: 5 | HEALTHY: 5 | 566.4 ms | 507.8 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | FAST: 2, MODERATE: 1, SLOW: 2 | MODERATE: 2, SLOW: 3 | 3548.0 ms | 4632.0 ms |
| explorer_web | MODERATE: 5 | FAST: 1, MODERATE: 4 | 825.0 ms | 1246.0 ms |
| primary_explorer_api | FAST: 3, MODERATE: 2 | FAST: 1, MODERATE: 4 | 1157.0 ms | 703.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.59 to 0.82: IMPROVED.
- Official Public RPC average response changed from 1249.6 ms to 1607.6 ms: WORSENED.
- Explorer Web average response changed from 706.2 ms to 731.8 ms: WORSENED.
- Primary Explorer API average response changed from 566.4 ms to 507.8 ms: IMPROVED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 35 | 2026-06-13T10:43:09.685105+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 36 | 2026-06-13T12:15:24.292365+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |
| 37 | 2026-06-13T17:43:45.241764+00:00 | PARTIAL_OUTAGE | UNHEALTHY | FAST | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 38 | 2026-06-13T18:57:21.166839+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 39 | 2026-06-14T02:47:39.011114+00:00 | PARTIAL_OUTAGE | UNHEALTHY | FAST | HEALTHY | MODERATE | HEALTHY | FAST |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 40 | 2026-06-14T07:17:43.721261+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 41 | 2026-06-14T15:06:02.854660+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 42 | 2026-06-14T17:46:11.842614+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 43 | 2026-06-15T16:32:07.477470+00:00 | DEGRADED | DEGRADED | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 44 | 2026-06-15T20:07:32.425470+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | FAST | HEALTHY | FAST |

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
