# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 12 |
| Observation index range | 11 -> 22 |
| First checked at UTC | 2026-06-04T16:59:50.793517+00:00 |
| Latest checked at UTC | 2026-06-08T06:47:13.271825+00:00 |
| Overall status counts | DEGRADED: 5, HEALTHY: 6, PARTIAL_OUTAGE: 1 |
| Availability score | 0.7458 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 12 |
| Observation index range | 23 -> 34 |
| First checked at UTC | 2026-06-09T01:30:52.519172+00:00 |
| Latest checked at UTC | 2026-06-11T00:13:29.727818+00:00 |
| Overall status counts | DEGRADED: 6, HEALTHY: 6 |
| Availability score | 0.775 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 5, HEALTHY: 6, UNHEALTHY: 1 | DEGRADED: 6, HEALTHY: 6 | 2609.0 ms | 3018.33 ms | WORSENED |
| explorer_web | HEALTHY: 12 | HEALTHY: 12 | 600.08 ms | 572.0 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 12 | HEALTHY: 12 | 466.0 ms | 398.25 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | MODERATE: 3, SLOW: 9 | SLOW: 12 | 15388.0 ms | 15336.0 ms |
| explorer_web | FAST: 3, MODERATE: 9 | FAST: 5, MODERATE: 7 | 721.0 ms | 841.0 ms |
| primary_explorer_api | FAST: 8, MODERATE: 4 | FAST: 10, MODERATE: 2 | 620.0 ms | 544.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.7458 to 0.775: IMPROVED.
- Official Public RPC average response changed from 2609.0 ms to 3018.33 ms: WORSENED.
- Explorer Web average response changed from 600.08 ms to 572.0 ms: IMPROVED.
- Primary Explorer API average response changed from 466.0 ms to 398.25 ms: IMPROVED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 11 | 2026-06-04T16:59:50.793517+00:00 | PARTIAL_OUTAGE | UNHEALTHY | MODERATE | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 12 | 2026-06-04T17:34:38.689983+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
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

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
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
