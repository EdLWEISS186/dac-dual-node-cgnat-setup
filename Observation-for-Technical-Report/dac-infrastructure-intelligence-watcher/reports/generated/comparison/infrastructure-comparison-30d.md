# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **30d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 7 |
| Observation index range | 1 -> 7 |
| First checked at UTC | 2026-06-04T09:54:55.772035+00:00 |
| Latest checked at UTC | 2026-06-04T11:36:10.013189+00:00 |
| Overall status counts | DEGRADED: 2, HEALTHY: 2, PARTIAL_OUTAGE: 3 |
| Availability score | 0.5286 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 8 |
| Observation index range | 8 -> 15 |
| First checked at UTC | 2026-06-04T11:38:16.082796+00:00 |
| Latest checked at UTC | 2026-06-06T12:16:24.339927+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 3, PARTIAL_OUTAGE: 2 |
| Availability score | 0.6313 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 2, HEALTHY: 2, UNHEALTHY: 3 | DEGRADED: 3, HEALTHY: 3, UNHEALTHY: 2 | N/A ms | 1975.6 ms | N/A |
| explorer_web | HEALTHY: 7 | HEALTHY: 8 | 1491.43 ms | 790.12 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 7 | HEALTHY: 8 | N/A ms | 518.2 ms | N/A |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | UNKNOWN: 7 | MODERATE: 2, SLOW: 3, UNKNOWN: 3 | N/A ms | 5347.0 ms |
| explorer_web | UNKNOWN: 7 | MODERATE: 5, UNKNOWN: 3 | 2299.0 ms | 1012.0 ms |
| primary_explorer_api | UNKNOWN: 7 | FAST: 2, MODERATE: 3, UNKNOWN: 3 | N/A ms | 620.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.5286 to 0.6313: IMPROVED.
- Official Public RPC average response changed from N/A ms to 1975.6 ms: N/A.
- Explorer Web average response changed from 1491.43 ms to 790.12 ms: IMPROVED.
- Primary Explorer API average response changed from N/A ms to 518.2 ms: N/A.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 1 | 2026-06-04T09:54:55.772035+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 2 | 2026-06-04T09:59:08.192048+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 3 | 2026-06-04T09:59:48.937274+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 4 | 2026-06-04T10:00:10.486388+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 5 | 2026-06-04T10:02:58.023788+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 6 | 2026-06-04T11:35:39.447567+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 7 | 2026-06-04T11:36:10.013189+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 8 | 2026-06-04T11:38:16.082796+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 9 | 2026-06-04T11:38:26.409385+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 10 | 2026-06-04T11:50:50.288397+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 11 | 2026-06-04T16:59:50.793517+00:00 | PARTIAL_OUTAGE | UNHEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 12 | 2026-06-04T17:34:38.689983+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 13 | 2026-06-04T17:39:38.929050+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 14 | 2026-06-04T19:47:12.825324+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 15 | 2026-06-06T12:16:24.339927+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

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
