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
| Observation index range | 81 -> 81 |
| First checked at UTC | 2026-06-30T08:44:47.357691+00:00 |
| Latest checked at UTC | 2026-06-30T08:44:47.357691+00:00 |
| Overall status counts | DEGRADED: 1 |
| Availability score | 0.55 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 2 |
| Observation index range | 82 -> 83 |
| First checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
| Latest checked at UTC | 2026-07-06T16:44:58.068005+00:00 |
| Overall status counts | DEGRADED: 1, HEALTHY: 1 |
| Availability score | 0.775 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 1 | DEGRADED: 1, HEALTHY: 1 | 15369.0 ms | 10302.5 ms | IMPROVED |
| explorer_web | HEALTHY: 1 | HEALTHY: 2 | 686.0 ms | 656.5 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 1 | HEALTHY: 2 | 382.0 ms | 530.0 ms | WORSENED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 1 | SLOW: 2 | 18180.0 ms | 17038.0 ms |
| explorer_web | MODERATE: 1 | MODERATE: 2 | 686.0 ms | 684.0 ms |
| primary_explorer_api | FAST: 1 | FAST: 1, MODERATE: 1 | 419.0 ms | 604.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.55 to 0.775: IMPROVED.
- Official Public RPC average response changed from 15369.0 ms to 10302.5 ms: IMPROVED.
- Explorer Web average response changed from 686.0 ms to 656.5 ms: IMPROVED.
- Primary Explorer API average response changed from 382.0 ms to 530.0 ms: WORSENED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 81 | 2026-06-30T08:44:47.357691+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 82 | 2026-06-30T13:28:33.493377+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |
| 83 | 2026-07-06T16:44:58.068005+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |

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
