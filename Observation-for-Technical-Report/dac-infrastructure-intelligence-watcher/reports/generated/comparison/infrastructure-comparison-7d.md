# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 10 |
| Observation index range | 17 -> 26 |
| First checked at UTC | 2026-06-07T08:29:35.513958+00:00 |
| Latest checked at UTC | 2026-06-09T15:36:15.483799+00:00 |
| Overall status counts | DEGRADED: 5, HEALTHY: 5 |
| Availability score | 0.775 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 11 |
| Observation index range | 27 -> 37 |
| First checked at UTC | 2026-06-09T17:35:46.336066+00:00 |
| Latest checked at UTC | 2026-06-13T17:43:45.241764+00:00 |
| Overall status counts | DEGRADED: 5, HEALTHY: 5, PARTIAL_OUTAGE: 1 |
| Availability score | 0.7227 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 5, HEALTHY: 5 | DEGRADED: 5, HEALTHY: 5, UNHEALTHY: 1 | 3215.1 ms | 2575.82 ms | IMPROVED |
| explorer_web | HEALTHY: 10 | HEALTHY: 11 | 605.5 ms | 559.91 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 10 | HEALTHY: 11 | 432.8 ms | 407.55 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 10 | FAST: 1, MODERATE: 1, SLOW: 9 | 15388.0 ms | 15336.0 ms |
| explorer_web | FAST: 3, MODERATE: 7 | FAST: 5, MODERATE: 6 | 841.0 ms | 825.0 ms |
| primary_explorer_api | FAST: 7, MODERATE: 3 | FAST: 10, MODERATE: 1 | 544.0 ms | 623.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.775 to 0.7227: WORSENED.
- Official Public RPC average response changed from 3215.1 ms to 2575.82 ms: IMPROVED.
- Explorer Web average response changed from 605.5 ms to 559.91 ms: IMPROVED.
- Primary Explorer API average response changed from 432.8 ms to 407.55 ms: IMPROVED.
- The later observation window shows weaker overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

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

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
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
| 37 | 2026-06-13T17:43:45.241764+00:00 | PARTIAL_OUTAGE | UNHEALTHY | FAST | HEALTHY | MODERATE | HEALTHY | MODERATE |

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
