# DAC Enode Intelligence Watcher — Custom Last 7 Days Report

Generated at UTC: `2026-07-24T22:18:18.304183+00:00`

Report range: **Last 7 Days**

Project: **DAC Enode Intelligence Watcher**

This custom report is generated from local watcher JSON outputs.

Important note: this report is observation-based. It does not make official DAC ownership claims and should not be treated as a definitive decentralization measurement.

## 1. Report Scope

| Field | Value |
| --- | --- |
| Range | Last 7 Days |
| Observation count | 3 |
| First observed source time | Jul 20, 2026 (15:00 CEST) |
| Last observed source time | Jul 23, 2026 (13:00 CEST) |
| Latest watcher checked_at_utc | 2026-07-24T04:32:49.852183+00:00 |
| Latest source generated time | 2026-07-24 06:00 CEST |

## 2. Enode Movement Summary

| Metric | Value |
| --- | --- |
| Minimum enode count | 13 |
| Maximum enode count | 14 |
| Average enode count | 13.33 |
| Total added observations | 2 |
| Total removed observations | 1 |
| Target ports observed | 28657 |

## 3. Observation Source Coverage

| Phase | Observations |
| --- | --- |
| automated_watcher | 3 |

## 4. Anomaly Summary

| Field | Value |
| --- | --- |
| Selected anomaly signals | 0 |
| Global anomaly summary | 12 anomaly signals were detected across 151 observations. The highest observed anomaly severity is CRITICAL. |
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
| Key observation | Top live ASN is AS51167 with 15 unique IPs (35.71%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (42.86%). |
| Interpretation | Top live ASN controls at least 35% of observed unique IPs. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Label |
| --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 35.71 | MODERATE |
| Live Country | DE | 18 | 42.86 | MODERATE |
| DAC Infrastructure Signal | Retained Infrastructure Signal | 14 | 33.33 | LOW |

## 6. Observation Timeline

| # | Phase | Status | Source Time | Current | Added | Removed | Unchanged | Port |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 148 | automated_watcher | changed | Jul 20, 2026 (15:00 CEST) | 13 | 1 | 0 | 12 | 28657 |
| 149 | automated_watcher | changed | Jul 23, 2026 (03:00 CEST) | 14 | 1 | 0 | 13 | 28657 |
| 150 | automated_watcher | changed | Jul 23, 2026 (13:00 CEST) | 13 | 0 | 1 | 13 | 28657 |

## 7. Report-Use Notes

- Use the 7D report for short-range rotation and recent watcher movement.
- Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.
- Use the All Time report for full testnet observation history preserved by this watcher.
- For publication-quality interpretation, compare this Markdown output with dashboard charts, raw JSON outputs, and selected snapshots.
