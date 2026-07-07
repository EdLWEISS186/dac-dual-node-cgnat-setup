# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 1 |
| Observation index range | 83 -> 83 |
| First checked at UTC | 2026-07-06T16:44:58.068005+00:00 |
| Latest checked at UTC | 2026-07-06T16:44:58.068005+00:00 |
| Overall status counts | DEGRADED: 1 |
| Availability score | 0.55 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 1 |
| Observation index range | 84 -> 84 |
| First checked at UTC | 2026-07-06T18:32:00.687312+00:00 |
| Latest checked at UTC | 2026-07-06T18:32:00.687312+00:00 |
| Overall status counts | HEALTHY: 1 |
| Availability score | 1.0 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 1 | HEALTHY: 1 | 15569.0 ms | 7120.0 ms | IMPROVED |
| explorer_web | HEALTHY: 1 | HEALTHY: 1 | 684.0 ms | 468.0 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 1 | HEALTHY: 1 | 596.0 ms | 406.0 ms | IMPROVED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 1 | SLOW: 1 | 17038.0 ms | 13713.0 ms |
| explorer_web | MODERATE: 1 | FAST: 1 | 684.0 ms | 468.0 ms |
| primary_explorer_api | MODERATE: 1 | FAST: 1 | 604.0 ms | 419.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.55 to 1.0: IMPROVED.
- Official Public RPC average response changed from 15569.0 ms to 7120.0 ms: IMPROVED.
- Explorer Web average response changed from 684.0 ms to 468.0 ms: IMPROVED.
- Primary Explorer API average response changed from 596.0 ms to 406.0 ms: IMPROVED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 83 | 2026-07-06T16:44:58.068005+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 84 | 2026-07-06T18:32:00.687312+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | FAST | HEALTHY | FAST |

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
