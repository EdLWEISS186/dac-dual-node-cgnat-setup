# DAC Enode Intelligence Watcher — Custom Last 7 Days Report

Generated at UTC: `2026-07-09T23:19:19.309294+00:00`

Report range: **Last 7 Days**

Project: **DAC Enode Intelligence Watcher**

This custom report is generated from local watcher JSON outputs.

Important note: this report is observation-based. It does not make official DAC ownership claims and should not be treated as a definitive decentralization measurement.

## 1. Report Scope

| Field | Value |
| --- | --- |
| Range | Last 7 Days |
| Observation count | 7 |
| First observed source time | Jul 1, 2026 (12:00 CEST) |
| Last observed source time | Jul 8, 2026 (11:00 CEST) |
| Latest watcher checked_at_utc | 2026-07-08T09:54:50.646653+00:00 |
| Latest source generated time | Wed Jul  8 11:00:01 AM CEST 2026 |

## 2. Enode Movement Summary

| Metric | Value |
| --- | --- |
| Minimum enode count | 12 |
| Maximum enode count | 15 |
| Average enode count | 13.43 |
| Total added observations | 4 |
| Total removed observations | 3 |
| Target ports observed | 28657 |

## 3. Observation Source Coverage

| Phase | Observations |
| --- | --- |
| automated_watcher | 7 |

## 4. Anomaly Summary

| Field | Value |
| --- | --- |
| Selected anomaly signals | 0 |
| Global anomaly summary | 12 anomaly signals were detected across 143 observations. The highest observed anomaly severity is CRITICAL. |
| Global highest severity | CRITICAL |
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
| Overall concentration label | MODERATE |
| Headline | Observed infrastructure shows moderate concentration under the current heuristic model. |
| Key observation | Top live ASN is AS51167 with 15 unique IPs (36.59%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (43.9%). |
| Interpretation | Top live ASN controls at least 35% of observed unique IPs. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Label |
| --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 36.59 | MODERATE |
| Live Country | DE | 18 | 43.9 | MODERATE |
| DAC Infrastructure Signal | Retained Infrastructure Signal | 14 | 34.15 | LOW |

## 6. Observation Timeline

| # | Phase | Status | Source Time | Current | Added | Removed | Unchanged | Port |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 137 | automated_watcher | changed | Jul 1, 2026 (12:00 CEST) | 13 | 1 | 0 | 12 | 28657 |
| 138 | automated_watcher | changed | Jul 1, 2026 (22:00 CEST) | 14 | 1 | 0 | 13 | 28657 |
| 139 | automated_watcher | changed | Jul 2, 2026 (13:00 CEST) | 15 | 1 | 0 | 14 | 28657 |
| 140 | automated_watcher | changed | Jul 3, 2026 (19:00 CEST) | 14 | 0 | 1 | 14 | 28657 |
| 141 | automated_watcher | changed | Jul 4, 2026 (07:00 CEST) | 13 | 0 | 1 | 13 | 28657 |
| 142 | automated_watcher | changed | Jul 4, 2026 (18:00 CEST) | 12 | 0 | 1 | 12 | 28657 |
| 143 | automated_watcher | changed | Jul 8, 2026 (11:00 CEST) | 13 | 1 | 0 | 12 | 28657 |

## 7. Report-Use Notes

- Use the 7D report for short-range rotation and recent watcher movement.
- Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.
- Use the All Time report for full testnet observation history preserved by this watcher.
- For publication-quality interpretation, compare this Markdown output with dashboard charts, raw JSON outputs, and selected snapshots.
