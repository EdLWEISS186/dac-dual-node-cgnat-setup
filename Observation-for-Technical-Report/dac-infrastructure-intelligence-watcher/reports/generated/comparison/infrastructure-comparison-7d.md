# DAC Infrastructure Intelligence Watcher — Observation Window Comparison

Comparison scope: **7d**

Comparison layer version: **v1.8.1**

This report compares two infrastructure observation windows derived from tracked health snapshots.

---

## 1. Window Summary

### Window A

| Field | Value |
|---|---|
| Snapshot count | 2 |
| Observation index range | 78 -> 79 |
| First checked at UTC | 2026-06-28T14:43:06.952490+00:00 |
| Latest checked at UTC | 2026-06-29T09:24:55.311755+00:00 |
| Overall status counts | DEGRADED: 1, HEALTHY: 1 |
| Availability score | 0.775 |

### Window B

| Field | Value |
|---|---|
| Snapshot count | 3 |
| Observation index range | 80 -> 82 |
| First checked at UTC | 2026-06-29T13:49:24.711303+00:00 |
| Latest checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
| Overall status counts | DEGRADED: 1, HEALTHY: 2 |
| Availability score | 0.85 |

## 2. Endpoint Availability and Response Comparison

| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |
|---|---|---|---:|---:|---|
| official_public_rpc | DEGRADED: 1, HEALTHY: 1 | DEGRADED: 1, HEALTHY: 2 | 9855.0 ms | 9222.0 ms | IMPROVED |
| explorer_web | HEALTHY: 2 | HEALTHY: 3 | 755.5 ms | 679.33 ms | IMPROVED |
| primary_explorer_api | HEALTHY: 2 | HEALTHY: 3 | 439.5 ms | 447.67 ms | WORSENED |

## 3. Response Class Comparison

| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |
|---|---|---|---:|---:|
| official_public_rpc | SLOW: 2 | SLOW: 3 | 16979.0 ms | 18180.0 ms |
| explorer_web | MODERATE: 2 | MODERATE: 3 | 801.0 ms | 723.0 ms |
| primary_explorer_api | FAST: 1, MODERATE: 1 | FAST: 2, MODERATE: 1 | 502.0 ms | 507.0 ms |

## 4. Interpretation

- Overall availability score changed from 0.775 to 0.85: IMPROVED.
- Official Public RPC average response changed from 9855.0 ms to 9222.0 ms: IMPROVED.
- Explorer Web average response changed from 755.5 ms to 679.33 ms: IMPROVED.
- Primary Explorer API average response changed from 439.5 ms to 447.67 ms: WORSENED.
- The later observation window shows stronger overall infrastructure availability.

## 5. Window Timelines

### Window A Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
| 78 | 2026-06-28T14:43:06.952490+00:00 | HEALTHY | HEALTHY | SLOW | HEALTHY | MODERATE | HEALTHY | MODERATE |
| 79 | 2026-06-29T09:24:55.311755+00:00 | DEGRADED | DEGRADED | SLOW | HEALTHY | MODERATE | HEALTHY | FAST |

### Window B Timeline

| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |
|---:|---|---|---|---|---|---|---|---|
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
