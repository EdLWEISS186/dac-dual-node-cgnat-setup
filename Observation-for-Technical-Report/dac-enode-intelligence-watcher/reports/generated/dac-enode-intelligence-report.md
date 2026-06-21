# DAC Enode Intelligence Watcher — Technical Observation Report

Generated at UTC: `2026-06-21T13:06:30.628179+00:00`

Project: **DAC Enode Intelligence Watcher**

Maintainer: **JERUZZALEM — DAC Infra Tester**

Related previous report:

- `5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation`

---

## 1. Executive Summary

Across 103 total observations, the DAC official enode list showed 38 unique enodes and 38 unique IPs. The observed target port remained within [28657]. Enode count ranged from 2 to 16, with an average of 11.7.

The dataset combines partial manual observations from the pre-watcher period with automated GitHub Actions snapshots after the watcher was deployed.

This summary provides a structured basis for analyzing bootstrap peer rotation, persistent observed enodes, IP recurrence, provider hints, ASN hints, DAC Infrastructure Signals, and possible infrastructure maturation patterns.

## 2. Observation Scope

| Metric | Value |
| --- | --- |
| Manual backfill snapshots | 14 |
| Automated watcher snapshots | 89 |
| Total observations | 103 |
| First observation | Fri May 15 12:00:01 AM CEST 2026 |
| Latest observation | Sun Jun 21 03:00:02 PM CEST 2026 |
| Target ports observed | 28657 |
| Unique enodes | 38 |
| Unique IPs | 38 |

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
| Generated at source | Sun Jun 21 03:00:02 PM CEST 2026 |
| Checked at UTC | 2026-06-21T13:06:30.628179+00:00 |
| Target port | 28657 |
| Previous total | 12 |
| Current total | 11 |
| Added count | 0 |
| Removed count | 1 |
| Unchanged count | 11 |
| Change severity | LOW |
| Severity reason | Small enode rotation detected: 0 added and 1 removed. |

Latest AI-style summary:

> DAC official enode list changed: 0 enodes added, 1 removed, and 11 remained unchanged. Current total: 11 enodes.

Rotation interpretation: **Small bootstrap peer rotation detected.**

Technical impact: This appears to be a minor peer-list refresh.

Recommended action: No urgent action is required, but the snapshot is preserved for history.

## 5. Enode Count Statistics

| Statistic | Value |
| --- | --- |
| Minimum enode count | 2 |
| Maximum enode count | 16 |
| Average enode count | 11.7 |

## 6. Most Persistent Enodes

| Enode | IP | Port | Appearances | Ratio | Phases Seen |
| --- | --- | --- | --- | --- | --- |
| enode://9652549979...7.30:28657 | 157.173.127.30 | 28657 | 98 | 0.9515 | automated_watcher, manual_backfill |
| enode://09b8b08d71....204:28657 | 206.189.127.204 | 28657 | 95 | 0.9223 | automated_watcher, manual_backfill |
| enode://21159ac612....213:28657 | 173.212.217.213 | 28657 | 85 | 0.8252 | automated_watcher, manual_backfill |
| enode://637ec7dff7....243:28657 | 213.136.82.243 | 28657 | 76 | 0.7379 | automated_watcher, manual_backfill |
| enode://52a3c25ccb...3.98:28657 | 217.76.53.98 | 28657 | 73 | 0.7087 | automated_watcher, manual_backfill |
| enode://0af12348ee....112:28657 | 194.60.201.112 | 28657 | 69 | 0.6699 | automated_watcher, manual_backfill |
| enode://4cd695fc27...6.21:28657 | 5.9.116.21 | 28657 | 67 | 0.6505 | automated_watcher, manual_backfill |
| enode://4ff5ceea9c....231:28657 | 152.228.141.231 | 28657 | 64 | 0.6214 | automated_watcher, manual_backfill |
| enode://b3158fbb36....180:28657 | 95.216.70.180 | 28657 | 63 | 0.6117 | automated_watcher, manual_backfill |
| enode://e84693f2ae....213:28657 | 113.173.209.213 | 28657 | 56 | 0.5437 | automated_watcher, manual_backfill |

## 7. Most Persistent IPs

| IP | DAC Signal | Signal Confidence | Peer Identity | Static Provider | Static ASN | Provider Confidence | Live ASN | Live ASN Name | Country | Appearances | Ratio | Phases Seen | First Seen | Last Seen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 157.173.127.30 | Authority-like Core Signal | HIGH | DAC Testnet Authority 2 | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 98 | 0.9515 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Sun Jun 21 03:00:02 PM CEST 2026 |
| 206.189.127.204 | Relay-like DAC Node Signal | HIGH | DAC-Node 05 | DigitalOcean | AS14061 | HIGH | AS14061 | DIGITALOCEAN-ASN - DigitalOcean, LLC, US | US | 95 | 0.9223 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Sun Jun 21 03:00:02 PM CEST 2026 |
| 173.212.217.213 | Retained Infrastructure Signal | MEDIUM | N/A | Contabo | AS51167 | HIGH | AS51167 | CONTABO - Contabo GmbH, DE | DE | 85 | 0.8252 | automated_watcher, manual_backfill | Wed May 20 08:00:02 PM CEST 2026 | Sun Jun 21 03:00:02 PM CEST 2026 |
| 213.136.82.243 | Unlisted Active Peer Signal | MEDIUM | SAPInode | Contabo | AS51167 | HIGH | AS51167 | CONTABO - Contabo GmbH, DE | DE | 76 | 0.7379 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Wed Jun 17 06:00:02 AM CEST 2026 |
| 217.76.53.98 | Community VPS-like Signal | MEDIUM | whale-vps1 | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 73 | 0.7087 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Sun Jun 21 03:00:02 PM CEST 2026 |
| 194.60.201.112 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 69 | 0.6699 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Wed Jun 17 06:00:02 AM CEST 2026 |
| 5.9.116.21 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS24940 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 67 | 0.6505 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Wed Jun 17 06:00:02 AM CEST 2026 |
| 152.228.141.231 | Legacy Relay-like Signal | MEDIUM | gdacnode legacy build | OVHcloud | AS16276 | HIGH | AS16276 | OVH - OVH SAS, FR | FR | 64 | 0.6214 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Sun Jun 21 03:00:02 PM CEST 2026 |
| 95.216.70.180 | Community VPS-like Signal | MEDIUM | Fertal | Hetzner | AS24940 | HIGH | AS24940 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 63 | 0.6117 | automated_watcher, manual_backfill | Sat May 16 08:00:01 PM CEST 2026 | Mon Jun 15 08:00:01 AM CEST 2026 |
| 113.173.209.213 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS45899 | VNPT-AS-VN - VNPT Corp, VN | VN | 56 | 0.5437 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Sun Jun 21 09:00:01 AM CEST 2026 |

## 8. Live ASN Lookup Summary

Live ASN lookup is used as an enrichment layer only.

ASN and provider names are based on external routing data and should be treated as operational context, not official DAC node ownership.

| Detection Field | Value |
| --- | --- |
| Enabled | True |
| Method | team_cymru_whois_live_lookup |
| Source | team_cymru |
| Cache file | data/asn-cache.json |
| Failure behavior | fallback_to_unknown_without_failing_pipeline |
| Disclaimer | Live ASN lookup is used as an enrichment layer only. ASN and provider names are based on external routing data and should be treated as operational context, not official DAC node ownership. |

| Live ASN | Unique IPs | ASN Name | Country | IPs |
| --- | --- | --- | --- | --- |
| AS51167 | 15 | CONTABO - Contabo GmbH, DE | DE, LT | 157.173.127.18, 157.173.127.21, 157.173.127.22, 157.173.127.30, 157.173.127.31, 161.97.89.27, 173.212.217.213, 173.249.42.5, 185.190.143.54, 194.163.186.161, 194.60.201.112, 213.136.82.243, 217.76.53.98, 84.46.253.182, 95.111.227.13 |
| AS14061 | 6 | DIGITALOCEAN-ASN - DigitalOcean, LLC, US | US | 157.230.40.93, 168.144.140.128, 188.166.164.78, 192.241.148.112, 206.189.127.204, 207.154.217.91 |
| AS18403 | 4 | FPT-VN - FPT Telecom Company, VN | VN | 1.54.141.106, 1.54.143.84, 118.71.126.107, 58.187.95.220 |
| AS24940 | 2 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 5.9.116.21, 95.216.70.180 |
| AS141995 | 2 | CAPL-AS-AP - Contabo Asia Private Limited, SG | DE | 156.67.104.212, 5.104.86.129 |
| AS8452 | 2 | TE-AS - IDDQD-AS, EG | EG | 41.39.22.179, 41.39.226.188 |
| AS16276 | 1 | OVH - OVH SAS, FR | FR | 152.228.141.231 |
| AS45899 | 1 | VNPT-AS-VN - VNPT Corp, VN | VN | 113.173.209.213 |
| AS29222 | 1 | Infomaniak-AS - Infomaniak Network SA, CH | CH | 83.228.229.39 |
| AS63949 | 1 | AKAMAI-LINODE-AP - Akamai Connected Cloud, SG | NL | 139.162.1.250 |
| AS3269 | 1 | ASN-IBSNAZ - Telecom Italia S.p.A., IT | IT | 95.249.175.94 |
| AS47583 | 1 | AS-HOSTINGER - Hostinger International Limited, CY | US | 145.223.99.167 |
| AS26832 | 1 | RICAWEBSERVICES - Rica Web Services, CA | US | 38.49.213.251 |

## 9. Provider Concentration / Decentralization Risk Summary

This section is an observation-based heuristic. It is not an official DAC classification and should not be treated as a definitive decentralization measurement.

| Field | Value |
| --- | --- |
| Overall label | MODERATE |
| Total unique IPs | 38 |
| Headline | Observed infrastructure shows moderate concentration under the current heuristic model. |
| Key observation | Top live ASN is AS51167 with 15 unique IPs (39.47%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (47.37%). |
| Interpretation | Top live ASN controls at least 35% of observed unique IPs. |
| Recommended action | Use this as an observation aid only. Compare it with registry history, DAC Infrastructure Signal, manual peer identity evidence, live ASN lookup updates, and future watcher snapshots before drawing conclusions. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Unknown % | Label |
| --- | --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 39.47 | 0.0 | MODERATE |
| Live Country | DE | 18 | 47.37 | 0.0 | MODERATE |
| Static Provider Hint | Unknown | 30 | 78.95 | 78.95 | INCONCLUSIVE |
| DAC Infrastructure Signal | Retained Infrastructure Signal | 11 | 28.95 | 28.95 | LOW |


## 10. DAC Infrastructure Signal Summary

DAC Infrastructure Signal is a community inference layer based on observed registry history, peer identity strings, persistence, subnet patterns, and provider hints.

It is not an official DAC classification and should not be treated as confirmed node ownership.

| Detection Field | Value |
| --- | --- |
| Method | static_report_evidence_and_observation_heuristic |
| Official ownership claim | False |
| Source reference | Derived from community observation evidence in Report 5: Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation, plus watcher observation history. |
| Disclaimer | DAC Infrastructure Signal is a community inference layer based on observed registry history, peer identity strings, persistence, subnet patterns, and provider hints. It is not an official DAC classification and should not be treated as confirmed node ownership. |

| DAC Infrastructure Signal | Unique IPs | Confidence | Peer Identity Hints | IPs |
| --- | --- | --- | --- | --- |
| Retained Infrastructure Signal | 11 | MEDIUM |  | 113.173.209.213, 118.71.126.107, 139.162.1.250, 173.212.217.213, 173.249.42.5, 192.241.148.112, 194.60.201.112, 207.154.217.91, 5.9.116.21, 58.187.95.220, 83.228.229.39 |
| Unknown / No Signal | 11 | LOW |  | 1.54.141.106, 1.54.143.84, 145.223.99.167, 168.144.140.128, 185.190.143.54, 194.163.186.161, 38.49.213.251, 41.39.22.179, 41.39.226.188, 95.111.227.13, 95.249.175.94 |
| Community VPS-like Signal | 4 | MEDIUM | Fertal, whale-vps1, whale-vps2, whale-vps3 | 156.67.104.212, 161.97.89.27, 217.76.53.98, 95.216.70.180 |
| Authority-like Core Signal | 3 | HIGH | DAC Testnet Authority 1, DAC Testnet Authority 2, DAC Testnet Authority 3 | 157.173.127.21, 157.173.127.30, 157.173.127.31 |
| Core Subnet Historical Signal | 2 | MEDIUM |  | 157.173.127.18, 157.173.127.22 |
| Provider-backed Observation Signal | 2 | LOW |  | 157.230.40.93, 188.166.164.78 |
| Community Node Signal | 1 | MEDIUM | x0rabbit | 5.104.86.129 |
| Internal RPC-like Signal | 1 | HIGH | DAC Testnet RPC 03 | 84.46.253.182 |
| Legacy Relay-like Signal | 1 | MEDIUM | gdacnode legacy build | 152.228.141.231 |
| Relay-like DAC Node Signal | 1 | HIGH | DAC-Node 05 | 206.189.127.204 |
| Unlisted Active Peer Signal | 1 | MEDIUM | SAPInode | 213.136.82.243 |

## 11. Provider / ASN Hint Summary

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
| DigitalOcean | AS14061 | VPS | Global | HIGH | 3 | 157.230.40.93, 188.166.164.78, 206.189.127.204 |
| Hetzner | AS24940 | VPS / Dedicated | Germany / Finland | HIGH | 1 | 95.216.70.180 |
| OVHcloud | AS16276 | VPS / Dedicated | France / Europe | HIGH | 1 | 152.228.141.231 |
| Unknown | Unknown | Unknown | Unknown | LOW | 30 | 1.54.141.106, 1.54.143.84, 113.173.209.213, 118.71.126.107, 139.162.1.250, 145.223.99.167, 156.67.104.212, 157.173.127.18, 157.173.127.21, 157.173.127.22, 157.173.127.30, 157.173.127.31, 168.144.140.128, 173.249.42.5, 185.190.143.54, 192.241.148.112, 194.163.186.161, 194.60.201.112, 207.154.217.91, 217.76.53.98, 38.49.213.251, 41.39.22.179, 41.39.226.188, 5.104.86.129, 5.9.116.21, 58.187.95.220, 83.228.229.39, 84.46.253.182, 95.111.227.13, 95.249.175.94 |

## 12. Anomaly Detection Summary

| Anomaly Metric | Value |
| --- | --- |
| Anomaly count | 12 |
| Highest severity | CRITICAL |
| Severity counts | {'HIGH': 8, 'CRITICAL': 2, 'MEDIUM': 2} |
| Anomaly type counts | {'LARGE_ENODE_COUNT_DROP': 1, 'HIGH_REMOVAL_EVENT': 3, 'AGGRESSIVE_ROTATION': 4, 'SHARP_ENODE_COUNT_DROP': 1, 'LOW_CONTINUITY_RATIO': 1, 'WATCHER_HIGH_SEVERITY_SIGNAL': 1, 'MODERATE_ROTATION_SPIKE': 1} |

The anomaly layer highlights observations that may indicate unusually large peer rotation, sharp enode count changes, low continuity, or unexpected target port behavior.

Recommended action: Use these anomaly events as candidates for deeper manual review and future technical reporting.

## 13. Detected Anomaly Events

| Type | Severity | Index | Phase | Generated At | Previous | Current | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LARGE_ENODE_COUNT_DROP | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | Official enode count decreased by 6 from 13 to 7. |
| HIGH_REMOVAL_EVENT | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | 7 enodes were removed from a previous total of 13. |
| AGGRESSIVE_ROTATION | HIGH | 5 | manual_backfill | Tue May 19 04:00:01 PM CEST 2026 | 13 | 7 | Large rotation intensity detected: 1 added and 7 removed. |
| AGGRESSIVE_ROTATION | HIGH | 8 | manual_backfill | Sat May 23 12:00:02 PM CEST 2026 | 12 | 12 | Large rotation intensity detected: 4 added and 4 removed. |
| AGGRESSIVE_ROTATION | HIGH | 11 | manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | 12 | 14 | Large rotation intensity detected: 5 added and 3 removed. |
| SHARP_ENODE_COUNT_DROP | CRITICAL | 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 10 | 2 | Official enode count dropped sharply from 10 to 2. |
| HIGH_REMOVAL_EVENT | HIGH | 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 10 | 2 | 8 enodes were removed from a previous total of 10. |
| AGGRESSIVE_ROTATION | HIGH | 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 10 | 2 | Large rotation intensity detected: 0 added and 8 removed. |
| LOW_CONTINUITY_RATIO | MEDIUM | 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 10 | 2 | Only 2 of 10 previous enodes remained unchanged. |
| WATCHER_HIGH_SEVERITY_SIGNAL | CRITICAL | 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 10 | 2 | Official enode count dropped sharply from 10 to 2. |
| HIGH_REMOVAL_EVENT | HIGH | 81 | automated_watcher | Wed Jun 17 04:00:02 PM CEST 2026 | 2 | 6 | 1 enodes were removed from a previous total of 2. |
| MODERATE_ROTATION_SPIKE | MEDIUM | 81 | automated_watcher | Wed Jun 17 04:00:02 PM CEST 2026 | 2 | 6 | Moderate rotation spike detected: 5 added and 1 removed. |

## 14. Observation Timeline

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
| 17 | automated_watcher | Mon Jun  1 12:00:02 PM CEST 2026 | 28657 | 9 | 0 | 4 | MEDIUM |
| 18 | automated_watcher | Mon Jun  1 10:00:01 PM CEST 2026 | 28657 | 10 | 1 | 0 | LOW |
| 19 | automated_watcher | Tue Jun  2 06:00:01 AM CEST 2026 | 28657 | 12 | 2 | 0 | LOW |
| 20 | automated_watcher | Tue Jun  2 12:00:01 PM CEST 2026 | 28657 | 12 | 1 | 1 | LOW |
| 21 | automated_watcher | Tue Jun  2 10:00:02 PM CEST 2026 | 28657 | 14 | 2 | 0 | LOW |
| 22 | automated_watcher | Wed Jun  3 12:00:02 PM CEST 2026 | 28657 | 10 | 0 | 4 | MEDIUM |
| 23 | automated_watcher | Wed Jun  3 02:00:03 PM CEST 2026 | 28657 | 8 | 0 | 2 | LOW |
| 24 | automated_watcher | Wed Jun  3 10:00:02 PM CEST 2026 | 28657 | 10 | 2 | 0 | LOW |
| 25 | automated_watcher | Thu Jun  4 12:00:01 AM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 26 | automated_watcher | Thu Jun  4 02:00:01 AM CEST 2026 | 28657 | 12 | 1 | 0 | LOW |
| 27 | automated_watcher | Thu Jun  4 12:00:03 PM CEST 2026 | 28657 | 11 | 0 | 1 | LOW |
| 28 | automated_watcher | Thu Jun  4 06:00:01 PM CEST 2026 | 28657 | 10 | 0 | 1 | LOW |
| 29 | automated_watcher | Sat Jun  6 08:00:01 AM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 30 | automated_watcher | Sat Jun  6 10:00:01 AM CEST 2026 | 28657 | 12 | 1 | 0 | LOW |
| 31 | automated_watcher | Sat Jun  6 02:00:01 PM CEST 2026 | 28657 | 13 | 1 | 0 | LOW |
| 32 | automated_watcher | Sat Jun  6 04:00:01 PM CEST 2026 | 28657 | 14 | 1 | 0 | LOW |
| 33 | automated_watcher | Sat Jun  6 08:00:01 PM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 34 | automated_watcher | Sat Jun  6 10:00:01 PM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 35 | automated_watcher | Sun Jun  7 02:00:01 AM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 36 | automated_watcher | Sun Jun  7 08:00:01 AM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 37 | automated_watcher | Sun Jun  7 10:00:01 AM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 38 | automated_watcher | Sun Jun  7 02:00:01 PM CEST 2026 | 28657 | 15 | 1 | 1 | LOW |
| 39 | automated_watcher | Sun Jun  7 08:00:01 PM CEST 2026 | 28657 | 16 | 1 | 0 | LOW |
| 40 | automated_watcher | Mon Jun  8 06:00:01 AM CEST 2026 | 28657 | 15 | 0 | 1 | LOW |
| 41 | automated_watcher | Mon Jun  8 08:00:01 PM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 42 | automated_watcher | Mon Jun  8 10:00:01 PM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 43 | automated_watcher | Tue Jun  9 12:00:01 AM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 44 | automated_watcher | Tue Jun  9 02:00:01 AM CEST 2026 | 28657 | 12 | 0 | 2 | LOW |
| 45 | automated_watcher | Tue Jun  9 06:00:01 AM CEST 2026 | 28657 | 11 | 0 | 1 | LOW |
| 46 | automated_watcher | Tue Jun  9 10:00:01 AM CEST 2026 | 28657 | 10 | 0 | 1 | LOW |
| 47 | automated_watcher | Tue Jun  9 12:00:01 PM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 48 | automated_watcher | Tue Jun  9 04:00:02 PM CEST 2026 | 28657 | 10 | 0 | 1 | LOW |
| 49 | automated_watcher | Tue Jun  9 08:00:01 PM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 50 | automated_watcher | Tue Jun  9 10:00:01 PM CEST 2026 | 28657 | 12 | 1 | 0 | LOW |
| 51 | automated_watcher | Wed Jun 10 06:00:01 AM CEST 2026 | 28657 | 11 | 0 | 1 | LOW |
| 52 | automated_watcher | Wed Jun 10 10:00:01 AM CEST 2026 | 28657 | 12 | 1 | 0 | LOW |
| 53 | automated_watcher | Wed Jun 10 02:00:01 PM CEST 2026 | 28657 | 13 | 1 | 0 | LOW |
| 54 | automated_watcher | Wed Jun 10 06:00:01 PM CEST 2026 | 28657 | 14 | 1 | 0 | LOW |
| 55 | automated_watcher | Thu Jun 11 12:00:01 AM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 56 | automated_watcher | Thu Jun 11 02:00:01 AM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 57 | automated_watcher | Thu Jun 11 08:00:01 AM CEST 2026 | 28657 | 14 | 1 | 1 | LOW |
| 58 | automated_watcher | Thu Jun 11 12:00:01 PM CEST 2026 | 28657 | 13 | 0 | 1 | LOW |
| 59 | automated_watcher | Thu Jun 11 08:00:01 PM CEST 2026 | 28657 | 14 | 1 | 0 | LOW |
| 60 | automated_watcher | Thu Jun 11 10:00:01 PM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 61 | automated_watcher | Fri Jun 12 04:00:01 PM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 62 | automated_watcher | Fri Jun 12 08:00:01 PM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 63 | automated_watcher | Fri Jun 12 10:00:01 PM CEST 2026 | 28657 | 16 | 1 | 0 | LOW |
| 64 | automated_watcher | Sat Jun 13 12:00:01 AM CEST 2026 | 28657 | 15 | 0 | 1 | LOW |
| 65 | automated_watcher | Sat Jun 13 04:00:01 AM CEST 2026 | 28657 | 16 | 1 | 0 | LOW |
| 66 | automated_watcher | Sat Jun 13 08:00:02 AM CEST 2026 | 28657 | 15 | 0 | 1 | LOW |
| 67 | automated_watcher | Sat Jun 13 10:00:02 PM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 68 | automated_watcher | Sun Jun 14 02:00:01 AM CEST 2026 | 28657 | 15 | 1 | 0 | LOW |
| 69 | automated_watcher | Sun Jun 14 12:00:01 PM CEST 2026 | 28657 | 14 | 0 | 1 | LOW |
| 70 | automated_watcher | Sun Jun 14 02:00:01 PM CEST 2026 | 28657 | 16 | 2 | 0 | LOW |
| 71 | automated_watcher | Sun Jun 14 06:00:01 PM CEST 2026 | 28657 | 14 | 0 | 2 | LOW |
| 72 | automated_watcher | Sun Jun 14 08:00:01 PM CEST 2026 | 28657 | 14 | 1 | 1 | LOW |
| 73 | automated_watcher | Mon Jun 15 08:00:01 AM CEST 2026 | 28657 | 13 | 0 | 1 | LOW |
| 74 | automated_watcher | Mon Jun 15 08:00:02 PM CEST 2026 | 28657 | 11 | 0 | 2 | LOW |
| 75 | automated_watcher | Tue Jun 16 04:00:02 AM CEST 2026 | 28657 | 10 | 0 | 1 | LOW |
| 76 | automated_watcher | Tue Jun 16 02:00:01 PM CEST 2026 | 28657 | 11 | 2 | 1 | MEDIUM |
| 77 | automated_watcher | Tue Jun 16 06:00:01 PM CEST 2026 | 28657 | 8 | 0 | 3 | MEDIUM |
| 78 | automated_watcher | Tue Jun 16 10:00:02 PM CEST 2026 | 28657 | 9 | 1 | 0 | LOW |
| 79 | automated_watcher | Wed Jun 17 06:00:02 AM CEST 2026 | 28657 | 10 | 1 | 0 | LOW |
| 80 | automated_watcher | Wed Jun 17 12:00:01 PM CEST 2026 | 28657 | 2 | 0 | 8 | CRITICAL |
| 81 | automated_watcher | Wed Jun 17 04:00:02 PM CEST 2026 | 28657 | 6 | 5 | 1 | MEDIUM |
| 82 | automated_watcher | Wed Jun 17 06:00:02 PM CEST 2026 | 28657 | 7 | 1 | 0 | LOW |
| 83 | automated_watcher | Wed Jun 17 08:00:01 PM CEST 2026 | 28657 | 7 | 1 | 1 | LOW |
| 84 | automated_watcher | Thu Jun 18 12:00:01 AM CEST 2026 | 28657 | 8 | 1 | 0 | LOW |
| 85 | automated_watcher | Thu Jun 18 08:00:01 AM CEST 2026 | 28657 | 7 | 0 | 1 | LOW |
| 86 | automated_watcher | Thu Jun 18 01:00:01 PM CEST 2026 | 28657 | 10 | 3 | 0 | MEDIUM |
| 87 | automated_watcher | Thu Jun 18 04:00:01 PM CEST 2026 | 28657 | 9 | 1 | 2 | MEDIUM |
| 88 | automated_watcher | Thu Jun 18 07:00:01 PM CEST 2026 | 28657 | 8 | 0 | 1 | LOW |
| 89 | automated_watcher | Fri Jun 19 12:00:02 AM CEST 2026 | 28657 | 9 | 1 | 0 | LOW |
| 90 | automated_watcher | Fri Jun 19 07:00:01 AM CEST 2026 | 28657 | 8 | 0 | 1 | LOW |
| 91 | automated_watcher | Fri Jun 19 11:00:01 AM CEST 2026 | 28657 | 6 | 1 | 3 | MEDIUM |
| 92 | automated_watcher | Fri Jun 19 03:00:02 PM CEST 2026 | 28657 | 9 | 3 | 0 | MEDIUM |
| 93 | automated_watcher | Fri Jun 19 06:00:01 PM CEST 2026 | 28657 | 9 | 1 | 1 | LOW |
| 94 | automated_watcher | Fri Jun 19 08:00:01 PM CEST 2026 | 28657 | 8 | 0 | 1 | LOW |
| 95 | automated_watcher | Fri Jun 19 10:00:01 PM CEST 2026 | 28657 | 8 | 1 | 1 | LOW |
| 96 | automated_watcher | Sat Jun 20 12:00:02 AM CEST 2026 | 28657 | 8 | 1 | 1 | LOW |
| 97 | automated_watcher | Sat Jun 20 05:00:01 AM CEST 2026 | 28657 | 10 | 2 | 0 | LOW |
| 98 | automated_watcher | Sat Jun 20 04:00:02 PM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 99 | automated_watcher | Sat Jun 20 09:00:01 PM CEST 2026 | 28657 | 11 | 1 | 1 | LOW |
| 100 | automated_watcher | Sun Jun 21 12:00:02 AM CEST 2026 | 28657 | 10 | 0 | 1 | LOW |
| 101 | automated_watcher | Sun Jun 21 01:00:01 AM CEST 2026 | 28657 | 11 | 1 | 0 | LOW |
| 102 | automated_watcher | Sun Jun 21 09:00:01 AM CEST 2026 | 28657 | 12 | 1 | 0 | LOW |
| 103 | automated_watcher | Sun Jun 21 03:00:02 PM CEST 2026 | 28657 | 11 | 0 | 1 | LOW |

## 15. Technical Interpretation

The current dataset shows a transition from manual observation into automated infrastructure monitoring.

The official enode list shows visible peer rotation across the observation period, while the target port remains consistent at `28657`.

Provider and ASN hints add an additional infrastructure-enrichment layer by grouping observed IPs into likely hosting providers or ASN categories where static prefix matching is available.

Live ASN lookup adds a routing-data enrichment layer that can reduce Unknown provider/ASN coverage while remaining separate from official ownership claims.

Provider concentration summary adds a cautious heuristic for identifying whether observed IPs appear concentrated across a small number of ASNs, countries, provider hints, or DAC Infrastructure Signal categories.

DAC Infrastructure Signal adds a separate community inference layer for interpreting observed node roles without claiming official ownership.

The anomaly layer detected selected high-impact rotation events, but these should be interpreted as review signals rather than direct evidence of network failure.

In a testnet environment, enode rotation may reflect infrastructure maintenance, bootstrap peer refreshes, scaling experiments, or network maturation.

## 16. Conclusion

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
- DAC Infrastructure Signal enrichment
- optional live ASN lookup enrichment
- provider concentration / decentralization risk heuristic

This report can be used as a draft foundation for future DAC Testnet infrastructure technical reports.

---

Generated by `generate_technical_report.py`

Maintainer: **JERUZZALEM — DAC Infra Tester**
