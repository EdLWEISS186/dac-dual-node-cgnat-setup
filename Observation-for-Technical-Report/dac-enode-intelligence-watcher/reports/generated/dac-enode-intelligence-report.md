# DAC Enode Intelligence Watcher — Technical Observation Report

Generated at UTC: `2026-06-01T09:48:59.503819+00:00`

Project: **DAC Enode Intelligence Watcher**

Maintainer: **JERUZZALEM — DAC Infra Tester**

Related previous report:

- `5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation`

---

## 1. Executive Summary

Across 16 total observations, the DAC official enode list showed 28 unique enodes and 28 unique IPs. The observed target port remained within [28657]. Enode count ranged from 7 to 15, with an average of 12.31.

The dataset combines partial manual observations from the pre-watcher period with automated GitHub Actions snapshots after the watcher was deployed.

This summary provides a structured basis for analyzing bootstrap peer rotation, persistent official enodes, IP recurrence, provider hints, ASN hints, and possible infrastructure maturation patterns.

## 2. Observation Scope

| Metric | Value |
| --- | --- |
| Manual backfill snapshots | 14 |
| Automated watcher snapshots | 2 |
| Total observations | 16 |
| First observation | Fri May 15 12:00:01 AM CEST 2026 |
| Latest observation | Mon Jun  1 08:00:02 AM CEST 2026 |
| Target ports observed | 28657 |
| Unique enodes | 28 |
| Unique IPs | 28 |

## 3. Manual Backfill Context

Before the automated watcher was deployed, enode observations were collected manually.

The manual backfill dataset preserves those earlier observations as structured JSON.

| Manual Dataset Metric | Value |
| --- | --- |
| Observation completeness | partial_manual_archive |
| First manual snapshot | Fri May 15 12:00:01 AM CEST 2026 |
| Last manual snapshot | Sun May 31 12:00:02 PM CEST 2026 |
| Total manual snapshots | 14 |
| Unique enodes in manual archive | 28 |
| Minimum enode count | 7 |
| Maximum enode count | 15 |
| Target ports observed | 28657 |

> Missing dates in the manual archive represent missed observation windows, not confirmed absence of infrastructure changes.

## 4. Latest Automated Watcher State

| Latest Field | Value |
| --- | --- |
| Generated at source | Mon Jun  1 08:00:02 AM CEST 2026 |
| Checked at UTC | 2026-06-01T07:27:25.922854+00:00 |
| Target port | 28657 |
| Previous total | 12 |
| Current total | 13 |
| Added count | 1 |
| Removed count | 0 |
| Unchanged count | 12 |
| Change severity | LOW |
| Severity reason | Small enode rotation detected: 1 added and 0 removed. |

Latest AI-style summary:

> DAC official enode list changed: 1 enodes added, 0 removed, and 12 remained unchanged. Current total: 13 enodes.

Rotation interpretation: **Small bootstrap peer rotation detected.**

Technical impact: This appears to be a minor peer-list refresh.

Recommended action: No urgent action is required, but the snapshot is preserved for history.

## 5. Enode Count Statistics

| Statistic | Value |
| --- | --- |
| Minimum enode count | 7 |
| Maximum enode count | 15 |
| Average enode count | 12.31 |

## 6. Most Persistent Enodes

| Enode | IP | Port | Appearances | Ratio | Phases Seen |
| --- | --- | --- | --- | --- | --- |
| enode://637ec7dff7....243:28657 | 213.136.82.243 | 28657 | 16 | 1.0 | automated_watcher, manual_backfill |
| enode://9652549979...7.30:28657 | 157.173.127.30 | 28657 | 16 | 1.0 | automated_watcher, manual_backfill |
| enode://a59112afa4...7.31:28657 | 157.173.127.31 | 28657 | 16 | 1.0 | automated_watcher, manual_backfill |
| enode://09b8b08d71....204:28657 | 206.189.127.204 | 28657 | 15 | 0.9375 | automated_watcher, manual_backfill |
| enode://98910c2d56...9.27:28657 | 161.97.89.27 | 28657 | 15 | 0.9375 | automated_watcher, manual_backfill |
| enode://27386ed9cc...7.21:28657 | 157.173.127.21 | 28657 | 13 | 0.8125 | automated_watcher, manual_backfill |
| enode://52a3c25ccb...3.98:28657 | 217.76.53.98 | 28657 | 12 | 0.75 | manual_backfill |
| enode://d764df8af4...7.91:28657 | 207.154.217.91 | 28657 | 11 | 0.6875 | automated_watcher, manual_backfill |
| enode://21159ac612....213:28657 | 173.212.217.213 | 28657 | 11 | 0.6875 | automated_watcher, manual_backfill |
| enode://737b868121....128:28657 | 168.144.140.128 | 28657 | 7 | 0.4375 | manual_backfill |

## 7. Most Persistent IPs

| IP | Provider | ASN | Confidence | Appearances | Ratio | Phases Seen | First Seen | Last Seen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 213.136.82.243 | Contabo | AS51167 | HIGH | 16 | 1.0 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 157.173.127.30 | Unknown | None | LOW | 16 | 1.0 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 157.173.127.31 | Unknown | None | LOW | 16 | 1.0 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 206.189.127.204 | DigitalOcean | AS14061 | HIGH | 15 | 0.9375 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 161.97.89.27 | Contabo | AS51167 | HIGH | 15 | 0.9375 | automated_watcher, manual_backfill | Sat May 16 08:00:01 PM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 157.173.127.21 | Unknown | None | LOW | 13 | 0.8125 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 217.76.53.98 | Unknown | None | LOW | 12 | 0.75 | manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Sun May 31 12:00:02 PM CEST 2026 |
| 207.154.217.91 | Unknown | None | LOW | 11 | 0.6875 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 173.212.217.213 | Contabo | AS51167 | HIGH | 11 | 0.6875 | automated_watcher, manual_backfill | Wed May 20 08:00:02 PM CEST 2026 | Mon Jun  1 08:00:02 AM CEST 2026 |
| 168.144.140.128 | Unknown | None | LOW | 7 | 0.4375 | manual_backfill | Sat May 16 08:00:01 PM CEST 2026 | Fri May 29 04:00:01 AM CEST 2026 |

## 8. Provider / ASN Hint Summary

Provider and ASN values in this section are heuristic hints based on static IP prefix matching.

They should be treated as enrichment for infrastructure analysis, not final verified ASN truth.

| Detection Field | Value |
| --- | --- |
| Method | static_prefix_heuristic |
| Machine learning used | False |
| Live ASN lookup used | False |
| Confidence note | Provider and ASN values are heuristic hints based on static IP prefix matching. Treat as enrichment, not final verified ASN truth. |

| Provider | ASN | Type | Country Hint | Confidence | Unique IPs | IPs |
| --- | --- | --- | --- | --- | --- | --- |
| Contabo | AS51167 | VPS | Germany / Global | HIGH | 3 | 161.97.89.27, 173.212.217.213, 213.136.82.243 |
| DigitalOcean | AS14061 | VPS | Global | HIGH | 1 | 206.189.127.204 |
| Hetzner | AS24940 | VPS / Dedicated | Germany / Finland | HIGH | 1 | 95.216.70.180 |
| OVHcloud | AS16276 | VPS / Dedicated | France / Europe | HIGH | 1 | 152.228.141.231 |
| Unknown | Unknown | Unknown | Unknown | LOW | 22 | 1.54.141.106, 113.173.209.213, 118.71.126.107, 145.223.99.167, 156.67.104.212, 157.173.127.18, 157.173.127.21, 157.173.127.22, 157.173.127.30, 157.173.127.31, 168.144.140.128, 173.249.42.5, 185.190.143.54, 194.163.186.161, 194.60.201.112, 207.154.217.91, 217.76.53.98, 38.49.213.251, 5.104.86.129, 5.9.116.21, 84.46.253.182, 95.111.227.13 |

## 9. Anomaly Detection Summary

| Anomaly Metric | Value |
| --- | --- |
| Anomaly count | 5 |
| Highest severity | HIGH |
| Severity counts | {'HIGH': 5} |
| Anomaly type counts | {'LARGE_ENODE_COUNT_DROP': 1, 'HIGH_REMOVAL_EVENT': 1, 'AGGRESSIVE_ROTATION': 3} |

The anomaly layer highlights observations that may indicate unusually large peer rotation, sharp enode count changes, low continuity, or unexpected target port behavior.

Recommended action: Use these anomaly events as candidates for deeper manual review and future technical reporting.

## 10. Detected Anomaly Events

| Type | Severity | Index | Phase | Generated At | Previous | Current | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LARGE_ENODE_COUNT_DROP | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | Official enode count decreased by 6 from 13 to 7. |
| HIGH_REMOVAL_EVENT | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | 7 enodes were removed from a previous total of 13. |
| AGGRESSIVE_ROTATION | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | Large rotation intensity detected: 1 added and 7 removed. |
| AGGRESSIVE_ROTATION | HIGH | 8 | manual_backfill | Sat May 23 12:00:02 PM CEST 2026 | 12 | 12 | Large rotation intensity detected: 4 added and 4 removed. |
| AGGRESSIVE_ROTATION | HIGH | 11 | manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | 12 | 14 | Large rotation intensity detected: 5 added and 3 removed. |

## 11. Observation Timeline

| Index | Phase | Generated At | Port | Total | Added | Removed | Severity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | 28657 | 11 | 11 | 0 | None |
| 2 | manual_backfill | Sat May 16 08:00:01 PM CEST 2026 | 28657 | 14 | 4 | 1 | None |
| 3 | manual_backfill | Sun May 17 04:00:01 PM CEST 2026 | 28657 | 13 | 1 | 2 | None |
| 4 | manual_backfill | Mon May 18 08:00:02 AM CEST 2026 | 28657 | 13 | 1 | 1 | None |
| 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 28657 | 7 | 1 | 7 | None |
| 6 | manual_backfill | Wed May 20 08:00:02 PM CEST 2026 | 28657 | 12 | 5 | 0 | None |
| 7 | manual_backfill | Fri May 22 12:00:01 AM CEST 2026 | 28657 | 12 | 1 | 1 | None |
| 8 | manual_backfill | Sat May 23 12:00:02 PM CEST 2026 | 28657 | 12 | 4 | 4 | None |
| 9 | manual_backfill | Sun May 24 04:00:01 AM CEST 2026 | 28657 | 9 | 0 | 3 | None |
| 10 | manual_backfill | Mon May 25 04:00:01 AM CEST 2026 | 28657 | 12 | 3 | 0 | None |
| 11 | manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | 28657 | 14 | 5 | 3 | None |
| 12 | manual_backfill | Fri May 29 04:00:01 AM CEST 2026 | 28657 | 14 | 0 | 0 | None |
| 13 | manual_backfill | Sat May 30 12:00:02 PM CEST 2026 | 28657 | 14 | 1 | 1 | None |
| 14 | manual_backfill | Sun May 31 12:00:02 PM CEST 2026 | 28657 | 15 | 2 | 1 | None |
| 15 | automated_watcher | Mon Jun  1 04:00:01 AM CEST 2026 | 28657 | 12 | 12 | 0 | None |
| 16 | automated_watcher | Mon Jun  1 08:00:02 AM CEST 2026 | 28657 | 13 | 1 | 0 | LOW |

## 12. Technical Interpretation

The current dataset shows a transition from manual observation into automated infrastructure monitoring.

The official enode list shows visible peer rotation across the observation period, while the target port remains consistent at `28657`.

Provider and ASN hints add an additional infrastructure-enrichment layer by grouping observed IPs into likely hosting providers or ASN categories where static prefix matching is available.

The anomaly layer detected selected high-impact rotation events, but these should be interpreted as review signals rather than direct evidence of network failure.

In a testnet environment, enode rotation may reflect infrastructure maintenance, bootstrap peer refreshes, scaling experiments, or network maturation.

## 13. Conclusion

DAC Enode Intelligence Watcher now provides a structured evidence pipeline for official enode observation.

The project currently supports:

- manual pre-watcher archive preservation
- automated enode monitoring
- JSON snapshot generation
- severity classification
- AI-style summary generation
- rotation intelligence aggregation
- anomaly detection
- report-ready Markdown generation
- heuristic provider / ASN hint enrichment

This report can be used as a draft foundation for future DAC Testnet infrastructure technical reports.

---

Generated by `generate_technical_report.py`

Maintainer: **JERUZZALEM — DAC Infra Tester**
