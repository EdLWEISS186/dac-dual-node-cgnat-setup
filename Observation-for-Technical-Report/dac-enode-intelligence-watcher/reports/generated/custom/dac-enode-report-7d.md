# DAC Enode Intelligence Watcher — Custom Last 7 Days Report

Generated at UTC: `2026-06-06T18:48:10.386698+00:00`

Report range: **Last 7 Days**

Project: **DAC Enode Intelligence Watcher**

This custom report is generated from local watcher JSON outputs.

Important note: this report is observation-based. It does not make official DAC ownership claims and should not be treated as a definitive decentralization measurement.

## 1. Report Scope

| Field | Value |
| --- | --- |
| Range | Last 7 Days |
| Observation count | 20 |
| First observed source time | May 31, 2026 (12:00 CEST) |
| Last observed source time | Jun 6, 2026 (20:00 CEST) |
| Latest watcher checked_at_utc | 2026-06-06T18:48:07.928531+00:00 |
| Latest source generated time | Sat Jun  6 08:00:01 PM CEST 2026 |

## 2. Enode Movement Summary

| Metric | Value |
| --- | --- |
| Minimum enode count | 8 |
| Maximum enode count | 15 |
| Average enode count | 11.7 |
| Total added observations | 30 |
| Total removed observations | 14 |
| Target ports observed | 28657 |

## 3. Observation Source Coverage

| Phase | Observations |
| --- | --- |
| automated_watcher | 19 |
| manual_backfill | 1 |

## 4. Anomaly Summary

| Field | Value |
| --- | --- |
| Selected anomaly signals | 0 |
| Global anomaly summary | 5 anomaly signals were detected across 33 observations. The highest observed anomaly severity is HIGH. |
| Global highest severity | HIGH |
| Recommended action | Use these anomaly events as candidates for deeper manual review and future technical reporting. |

| Severity | Signals in selected range |
| --- | --- |
| N/A | 0 |

| Anomaly Type | Signals in selected range |
| --- | --- |
| N/A | 0 |

## 5. Provider / ASN Concentration Context

| Field | Value |
| --- | --- |
| Overall concentration label | ELEVATED |
| Headline | Observed infrastructure shows elevated concentration under the current heuristic model. |
| Key observation | Top live ASN is AS51167 with 15 unique IPs (50.0%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (60.0%). |
| Interpretation | Top live ASN controls at least 50% of observed unique IPs. Observed IPs show notable concentration in one live ASN country code. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Label |
| --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 50.0 | ELEVATED |
| Live Country | DE | 18 | 60.0 | ELEVATED |
| DAC Infrastructure Signal | Unknown / No Signal | 9 | 30.0 | LOW |

## 6. Observation Timeline

| # | Phase | Status | Source Time | Current | Added | Removed | Unchanged | Port |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 14 | manual_backfill | manual_changed | May 31, 2026 (12:00 CEST) | 15 | 2 | 1 | 13 | 28657 |
| 15 | automated_watcher | initial | Jun 1, 2026 (04:00 CEST) | 12 | 12 | 0 | 0 | 28657 |
| 16 | automated_watcher | changed | Jun 1, 2026 (08:00 CEST) | 13 | 1 | 0 | 12 | 28657 |
| 17 | automated_watcher | changed | Jun 1, 2026 (12:00 CEST) | 9 | 0 | 4 | 9 | 28657 |
| 18 | automated_watcher | changed | Jun 1, 2026 (22:00 CEST) | 10 | 1 | 0 | 9 | 28657 |
| 19 | automated_watcher | changed | Jun 2, 2026 (06:00 CEST) | 12 | 2 | 0 | 10 | 28657 |
| 20 | automated_watcher | changed | Jun 2, 2026 (12:00 CEST) | 12 | 1 | 1 | 11 | 28657 |
| 21 | automated_watcher | changed | Jun 2, 2026 (22:00 CEST) | 14 | 2 | 0 | 12 | 28657 |
| 22 | automated_watcher | changed | Jun 3, 2026 (12:00 CEST) | 10 | 0 | 4 | 10 | 28657 |
| 23 | automated_watcher | changed | Jun 3, 2026 (14:00 CEST) | 8 | 0 | 2 | 8 | 28657 |
| 24 | automated_watcher | changed | Jun 3, 2026 (22:00 CEST) | 10 | 2 | 0 | 8 | 28657 |
| 25 | automated_watcher | changed | Jun 4, 2026 (00:00 CEST) | 11 | 1 | 0 | 10 | 28657 |
| 26 | automated_watcher | changed | Jun 4, 2026 (02:00 CEST) | 12 | 1 | 0 | 11 | 28657 |
| 27 | automated_watcher | changed | Jun 4, 2026 (12:00 CEST) | 11 | 0 | 1 | 11 | 28657 |
| 28 | automated_watcher | changed | Jun 4, 2026 (18:00 CEST) | 10 | 0 | 1 | 10 | 28657 |
| 29 | automated_watcher | changed | Jun 6, 2026 (08:00 CEST) | 11 | 1 | 0 | 10 | 28657 |
| 30 | automated_watcher | changed | Jun 6, 2026 (10:00 CEST) | 12 | 1 | 0 | 11 | 28657 |
| 31 | automated_watcher | changed | Jun 6, 2026 (14:00 CEST) | 13 | 1 | 0 | 12 | 28657 |
| 32 | automated_watcher | changed | Jun 6, 2026 (16:00 CEST) | 14 | 1 | 0 | 13 | 28657 |
| 33 | automated_watcher | changed | Jun 6, 2026 (20:00 CEST) | 15 | 1 | 0 | 14 | 28657 |

## 7. Report-Use Notes

- Use the 7D report for short-range rotation and recent watcher movement.
- Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.
- Use the All Time report for full testnet observation history preserved by this watcher.
- For publication-quality interpretation, compare this Markdown output with dashboard charts, raw JSON outputs, and selected snapshots.
