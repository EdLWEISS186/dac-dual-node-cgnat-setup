# DAC Enode Intelligence Watcher — Custom Last 30 Days Report

Generated at UTC: `2026-06-03T08:46:29.689903+00:00`

Report range: **Last 30 Days**

Project: **DAC Enode Intelligence Watcher**

This custom report is generated from local watcher JSON outputs.

Important note: this report is observation-based. It does not make official DAC ownership claims and should not be treated as a definitive decentralization measurement.

## 1. Report Scope

| Field | Value |
| --- | --- |
| Range | Last 30 Days |
| Observation count | 21 |
| First observed source time | May 15, 2026 (00:00 CEST) |
| Last observed source time | Jun 2, 2026 (22:00 CEST) |
| Latest watcher checked_at_utc | 2026-06-02T21:19:37.546922+00:00 |
| Latest source generated time | Tue Jun  2 10:00:02 PM CEST 2026 |

## 2. Enode Movement Summary

| Metric | Value |
| --- | --- |
| Minimum enode count | 7 |
| Maximum enode count | 15 |
| Average enode count | 12.1 |
| Total added observations | 58 |
| Total removed observations | 29 |
| Target ports observed | 28657 |

## 3. Observation Source Coverage

| Phase | Observations |
| --- | --- |
| automated_watcher | 7 |
| manual_backfill | 14 |

## 4. Anomaly Summary

| Field | Value |
| --- | --- |
| Selected anomaly signals | 5 |
| Global anomaly summary | 5 anomaly signals were detected across 21 observations. The highest observed anomaly severity is HIGH. |
| Global highest severity | HIGH |
| Recommended action | Use these anomaly events as candidates for deeper manual review and future technical reporting. |

| Severity | Signals in selected range |
| --- | --- |
| HIGH | 5 |

| Anomaly Type | Signals in selected range |
| --- | --- |
| AGGRESSIVE_ROTATION | 3 |
| LARGE_ENODE_COUNT_DROP | 1 |
| HIGH_REMOVAL_EVENT | 1 |

## 5. Provider / ASN Concentration Context

| Field | Value |
| --- | --- |
| Overall concentration label | ELEVATED |
| Headline | Observed infrastructure shows elevated concentration under the current heuristic model. |
| Key observation | Top live ASN is AS51167 with 15 unique IPs (51.72%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (62.07%). |
| Interpretation | Top live ASN controls at least 50% of observed unique IPs. Observed IPs show notable concentration in one live ASN country code. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Label |
| --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 51.72 | ELEVATED |
| Live Country | DE | 18 | 62.07 | ELEVATED |
| DAC Infrastructure Signal | Unknown / No Signal | 10 | 34.48 | LOW |

## 6. Observation Timeline

| # | Phase | Status | Source Time | Current | Added | Removed | Unchanged | Port |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | manual_backfill | manual_initial | May 15, 2026 (00:00 CEST) | 11 | 11 | 0 | 0 | 28657 |
| 2 | manual_backfill | manual_changed | May 16, 2026 (20:00 CEST) | 14 | 4 | 1 | 10 | 28657 |
| 3 | manual_backfill | manual_changed | May 17, 2026 (16:00 CEST) | 13 | 1 | 2 | 12 | 28657 |
| 4 | manual_backfill | manual_changed | May 18, 2026 (08:00 CEST) | 13 | 1 | 1 | 12 | 28657 |
| 5 | manual_backfill | manual_changed | May 19, 2026 (16:00 CEST) | 7 | 1 | 7 | 6 | 28657 |
| 6 | manual_backfill | manual_changed | May 20, 2026 (20:00 CEST) | 12 | 5 | 0 | 7 | 28657 |
| 7 | manual_backfill | manual_changed | May 22, 2026 (00:00 CEST) | 12 | 1 | 1 | 11 | 28657 |
| 8 | manual_backfill | manual_changed | May 23, 2026 (12:00 CEST) | 12 | 4 | 4 | 8 | 28657 |
| 9 | manual_backfill | manual_changed | May 24, 2026 (04:00 CEST) | 9 | 0 | 3 | 9 | 28657 |
| 10 | manual_backfill | manual_changed | May 25, 2026 (04:00 CEST) | 12 | 3 | 0 | 9 | 28657 |
| 11 | manual_backfill | manual_changed | May 28, 2026 (08:00 CEST) | 14 | 5 | 3 | 9 | 28657 |
| 12 | manual_backfill | manual_unchanged | May 29, 2026 (04:00 CEST) | 14 | 0 | 0 | 14 | 28657 |
| 13 | manual_backfill | manual_changed | May 30, 2026 (12:00 CEST) | 14 | 1 | 1 | 13 | 28657 |
| 14 | manual_backfill | manual_changed | May 31, 2026 (12:00 CEST) | 15 | 2 | 1 | 13 | 28657 |
| 15 | automated_watcher | initial | Jun 1, 2026 (04:00 CEST) | 12 | 12 | 0 | 0 | 28657 |
| 16 | automated_watcher | changed | Jun 1, 2026 (08:00 CEST) | 13 | 1 | 0 | 12 | 28657 |
| 17 | automated_watcher | changed | Jun 1, 2026 (12:00 CEST) | 9 | 0 | 4 | 9 | 28657 |
| 18 | automated_watcher | changed | Jun 1, 2026 (22:00 CEST) | 10 | 1 | 0 | 9 | 28657 |
| 19 | automated_watcher | changed | Jun 2, 2026 (06:00 CEST) | 12 | 2 | 0 | 10 | 28657 |
| 20 | automated_watcher | changed | Jun 2, 2026 (12:00 CEST) | 12 | 1 | 1 | 11 | 28657 |
| 21 | automated_watcher | changed | Jun 2, 2026 (22:00 CEST) | 14 | 2 | 0 | 12 | 28657 |

## 7. Report-Use Notes

- Use the 7D report for short-range rotation and recent watcher movement.
- Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.
- Use the All Time report for full testnet observation history preserved by this watcher.
- For publication-quality interpretation, compare this Markdown output with dashboard charts, raw JSON outputs, and selected snapshots.
