# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **all**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 12 |
| Observation index range | 1 -> 12 |
| First checked at UTC | 2026-06-04T09:54:55.772035+00:00 |
| Latest checked at UTC | 2026-06-04T17:34:38.689983+00:00 |
| Overall status counts | DEGRADED: 3, HEALTHY: 4, PARTIAL_OUTAGE: 5 |
| Availability score | 0.5542 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 12 |
| Observation index range | 13 -> 24 |
| First checked at UTC | 2026-06-04T17:39:38.929050+00:00 |
| Latest checked at UTC | 2026-06-09T05:51:55.728730+00:00 |
| Overall status counts | DEGRADED: 6, HEALTHY: 6 |
| Availability score | 0.775 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 3, HEALTHY: 4, UNHEALTHY: 5 | DEGRADED: 6, HEALTHY: 6 | 2018.0 ms | 2772.25 ms | WORSENED |
| explorer_web | HEALTHY: 12 | HEALTHY: 12 | 1230.67 ms | 616.25 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 12 | HEALTHY: 12 | 549.0 ms | 447.0 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | MODERATE: 1, SLOW: 1, UNKNOWN: 10 | MODERATE: 2, SLOW: 10 | 5347.0 ms | 15388.0 ms |
| explorer_web | MODERATE: 2, UNKNOWN: 10 | FAST: 3, MODERATE: 9 | 2299.0 ms | 841.0 ms |
| primary_explorer_api | MODERATE: 2, UNKNOWN: 10 | FAST: 9, MODERATE: 3 | 620.0 ms | 539.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.5542 to 0.775: IMPROVED.
- Official Public RPC average response changed from 2018.0 ms to 2772.25 ms: WORSENED.
- Explorer Web average response changed from 1230.67 ms to 616.25 ms: IMPROVED.
- Primary Explorer API average response changed from 549.0 ms to 447.0 ms: IMPROVED.
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
| 8 | 2026-06-04T11:38:16.082796+00:00 | PARTIAL_OUTAGE | UNHEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 9 | 2026-06-04T11:38:26.409385+00:00 | DEGRADED | DEGRADED | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 10 | 2026-06-04T11:50:50.288397+00:00 | HEALTHY | HEALTHY | N/A | HEALTHY | N/A | HEALTHY | N/A |
| 11 | 2026-06-04T16:59:50.793517+00:00 | PARTIAL_OUTAGE | UNHEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 12 | 2026-06-04T17:34:38.689983+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 13 | 2026-06-04T17:39:38.929050+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 14 | 2026-06-04T19:47:12.825324+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 15 | 2026-06-06T12:16:24.339927+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 16 | 2026-06-06T15:41:44.603473+00:00 | HEALTHY | HEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | FAST |
| 17 | 2026-06-07T08:29:35.513958+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 18 | 2026-06-07T10:41:05.109781+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 19 | 2026-06-07T12:12:00.907268+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 20 | 2026-06-07T17:06:43.581492+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 21 | 2026-06-08T01:59:16.847351+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 22 | 2026-06-08T06:47:13.271825+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |
| 23 | 2026-06-09T01:30:52.519172+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 24 | 2026-06-09T05:51:55.728730+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

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
