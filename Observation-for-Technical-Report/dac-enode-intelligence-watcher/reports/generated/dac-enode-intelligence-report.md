# DAC Enode Intelligence Watcher — Technical Observation Report

Generated at UTC: `2026-06-09T19:14:36.409581+00:00`

Project: **DAC Enode Intelligence Watcher**

Maintainer: **JERUZZALEM — DAC Infra Tester**

Related previous report:

- `5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation`

---

## 1. Executive Summary

Across 49 total observations, the DAC official enode list showed 33 unique enodes and 33 unique IPs. The observed target port remained within [28657]. Enode count ranged from 7 to 16, with an average of 12.31.

The dataset combines partial manual observations from the pre-watcher period with automated GitHub Actions snapshots after the watcher was deployed.

This summary provides a structured basis for analyzing bootstrap peer rotation, persistent observed enodes, IP recurrence, provider hints, ASN hints, DAC Infrastructure Signals, and possible infrastructure maturation patterns.

## 2. Observation Scope

| Metric | Value |
| --- | --- |
| Manual backfill snapshots | 14 |
| Automated watcher snapshots | 35 |
| Total observations | 49 |
| First observation | Fri May 15 12:00:01 AM CEST 2026 |
| Latest observation | Tue Jun  9 08:00:01 PM CEST 2026 |
| Target ports observed | 28657 |
| Unique enodes | 33 |
| Unique IPs | 33 |

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
| Generated at source | Tue Jun  9 08:00:01 PM CEST 2026 |
| Checked at UTC | 2026-06-09T19:14:36.409581+00:00 |
| Target port | 28657 |
| Previous total | 10 |
| Current total | 11 |
| Added count | 1 |
| Removed count | 0 |
| Unchanged count | 10 |
| Change severity | LOW |
| Severity reason | Small enode rotation detected: 1 added and 0 removed. |

Latest AI-style summary:

> DAC official enode list changed: 1 enodes added, 0 removed, and 10 remained unchanged. Current total: 11 enodes.

Rotation interpretation: **Small bootstrap peer rotation detected.**

Technical impact: This appears to be a minor peer-list refresh.

Recommended action: No urgent action is required, but the snapshot is preserved for history.

## 5. Enode Count Statistics

| Statistic | Value |
| --- | --- |
| Minimum enode count | 7 |
| Maximum enode count | 16 |
| Average enode count | 12.31 |

## 6. Most Persistent Enodes

| Enode | IP | Port | Appearances | Ratio | Phases Seen |
| --- | --- | --- | --- | --- | --- |
| enode://09b8b08d71....204:28657 | 206.189.127.204 | 28657 | 48 | 0.9796 | automated_watcher, manual_backfill |
| enode://637ec7dff7....243:28657 | 213.136.82.243 | 28657 | 46 | 0.9388 | automated_watcher, manual_backfill |
| enode://9652549979...7.30:28657 | 157.173.127.30 | 28657 | 46 | 0.9388 | automated_watcher, manual_backfill |
| enode://21159ac612....213:28657 | 173.212.217.213 | 28657 | 44 | 0.898 | automated_watcher, manual_backfill |
| enode://b3158fbb36....180:28657 | 95.216.70.180 | 28657 | 39 | 0.7959 | automated_watcher, manual_backfill |
| enode://0af12348ee....112:28657 | 194.60.201.112 | 28657 | 39 | 0.7959 | automated_watcher, manual_backfill |
| enode://4cd695fc27...6.21:28657 | 5.9.116.21 | 28657 | 37 | 0.7551 | automated_watcher, manual_backfill |
| enode://d764df8af4...7.91:28657 | 207.154.217.91 | 28657 | 31 | 0.6327 | automated_watcher, manual_backfill |
| enode://e84693f2ae....213:28657 | 113.173.209.213 | 28657 | 31 | 0.6327 | automated_watcher, manual_backfill |
| enode://52a3c25ccb...3.98:28657 | 217.76.53.98 | 28657 | 27 | 0.551 | automated_watcher, manual_backfill |

## 7. Most Persistent IPs

| IP | DAC Signal | Signal Confidence | Peer Identity | Static Provider | Static ASN | Provider Confidence | Live ASN | Live ASN Name | Country | Appearances | Ratio | Phases Seen | First Seen | Last Seen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 206.189.127.204 | Relay-like DAC Node Signal | HIGH | DAC-Node 05 | DigitalOcean | AS14061 | HIGH | AS14061 | DIGITALOCEAN-ASN - DigitalOcean, LLC, US | US | 48 | 0.9796 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 213.136.82.243 | Unlisted Active Peer Signal | MEDIUM | SAPInode | Contabo | AS51167 | HIGH | AS51167 | CONTABO - Contabo GmbH, DE | DE | 46 | 0.9388 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 157.173.127.30 | Authority-like Core Signal | HIGH | DAC Testnet Authority 2 | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 46 | 0.9388 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 173.212.217.213 | Retained Infrastructure Signal | MEDIUM | N/A | Contabo | AS51167 | HIGH | AS51167 | CONTABO - Contabo GmbH, DE | DE | 44 | 0.898 | automated_watcher, manual_backfill | Wed May 20 08:00:02 PM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 95.216.70.180 | Community VPS-like Signal | MEDIUM | Fertal | Hetzner | AS24940 | HIGH | AS24940 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 39 | 0.7959 | automated_watcher, manual_backfill | Sat May 16 08:00:01 PM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 194.60.201.112 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 39 | 0.7959 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 5.9.116.21 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS24940 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 37 | 0.7551 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 207.154.217.91 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS14061 | DIGITALOCEAN-ASN - DigitalOcean, LLC, US | US | 31 | 0.6327 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Tue Jun  9 08:00:01 PM CEST 2026 |
| 113.173.209.213 | Retained Infrastructure Signal | MEDIUM | N/A | Unknown | N/A | LOW | AS45899 | VNPT-AS-VN - VNPT Corp, VN | VN | 31 | 0.6327 | automated_watcher, manual_backfill | Thu May 28 08:00:01 AM CEST 2026 | Tue Jun  9 12:00:01 AM CEST 2026 |
| 217.76.53.98 | Community VPS-like Signal | MEDIUM | whale-vps1 | Unknown | N/A | LOW | AS51167 | CONTABO - Contabo GmbH, DE | DE | 27 | 0.551 | automated_watcher, manual_backfill | Fri May 15 12:00:01 AM CEST 2026 | Tue Jun  9 02:00:01 AM CEST 2026 |

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
| AS14061 | 5 | DIGITALOCEAN-ASN - DigitalOcean, LLC, US | US | 157.230.40.93, 168.144.140.128, 192.241.148.112, 206.189.127.204, 207.154.217.91 |
| AS18403 | 3 | FPT-VN - FPT Telecom Company, VN | VN | 1.54.141.106, 118.71.126.107, 58.187.95.220 |
| AS24940 | 2 | HETZNER-AS - Hetzner Online GmbH, DE | DE | 5.9.116.21, 95.216.70.180 |
| AS141995 | 2 | CAPL-AS-AP - Contabo Asia Private Limited, SG | DE | 156.67.104.212, 5.104.86.129 |
| AS45899 | 1 | VNPT-AS-VN - VNPT Corp, VN | VN | 113.173.209.213 |
| AS16276 | 1 | OVH - OVH SAS, FR | FR | 152.228.141.231 |
| AS63949 | 1 | AKAMAI-LINODE-AP - Akamai Connected Cloud, SG | NL | 139.162.1.250 |
| AS29222 | 1 | Infomaniak-AS - Infomaniak Network SA, CH | CH | 83.228.229.39 |
| AS47583 | 1 | AS-HOSTINGER - Hostinger International Limited, CY | US | 145.223.99.167 |
| AS26832 | 1 | RICAWEBSERVICES - Rica Web Services, CA | US | 38.49.213.251 |

## 9. Provider Concentration / Decentralization Risk Summary

This section is an observation-based heuristic. It is not an official DAC classification and should not be treated as a definitive decentralization measurement.

| Field | Value |
| --- | --- |
| Overall label | ELEVATED |
| Total unique IPs | 33 |
| Headline | Observed infrastructure shows elevated concentration under the current heuristic model. |
| Key observation | Top live ASN is AS51167 with 15 unique IPs (45.45%). |
| Country observation | Top live ASN country code is DE with 18 unique IPs (54.55%). |
| Interpretation | Top live ASN controls at least 35% of observed unique IPs. Observed IPs show notable concentration in one live ASN country code. |
| Recommended action | Use this as an observation aid only. Compare it with registry history, DAC Infrastructure Signal, manual peer identity evidence, live ASN lookup updates, and future watcher snapshots before drawing conclusions. |
| Disclaimer | Provider concentration and decentralization risk summary is an observation-based heuristic. It is based on currently available watcher data, live ASN enrichment, static provider hints, and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification or as a definitive decentralization measurement. |

| Dimension | Top Name | Top Count | Top % | Unknown % | Label |
| --- | --- | --- | --- | --- | --- |
| Live ASN | AS51167 | 15 | 45.45 | 0.0 | MODERATE |
| Live Country | DE | 18 | 54.55 | 0.0 | ELEVATED |
| Static Provider Hint | Unknown | 26 | 78.79 | 78.79 | INCONCLUSIVE |
| DAC Infrastructure Signal | Retained Infrastructure Signal | 9 | 27.27 | 27.27 | LOW |


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
| Retained Infrastructure Signal | 9 | MEDIUM |  | 113.173.209.213, 118.71.126.107, 173.212.217.213, 173.249.42.5, 192.241.148.112, 194.60.201.112, 207.154.217.91, 5.9.116.21, 58.187.95.220 |
| Unknown / No Signal | 9 | LOW |  | 1.54.141.106, 139.162.1.250, 145.223.99.167, 168.144.140.128, 185.190.143.54, 194.163.186.161, 38.49.213.251, 83.228.229.39, 95.111.227.13 |
| Community VPS-like Signal | 4 | MEDIUM | Fertal, whale-vps1, whale-vps2, whale-vps3 | 156.67.104.212, 161.97.89.27, 217.76.53.98, 95.216.70.180 |
| Authority-like Core Signal | 3 | HIGH | DAC Testnet Authority 1, DAC Testnet Authority 2, DAC Testnet Authority 3 | 157.173.127.21, 157.173.127.30, 157.173.127.31 |
| Core Subnet Historical Signal | 2 | MEDIUM |  | 157.173.127.18, 157.173.127.22 |
| Community Node Signal | 1 | MEDIUM | x0rabbit | 5.104.86.129 |
| Internal RPC-like Signal | 1 | HIGH | DAC Testnet RPC 03 | 84.46.253.182 |
| Legacy Relay-like Signal | 1 | MEDIUM | gdacnode legacy build | 152.228.141.231 |
| Provider-backed Observation Signal | 1 | LOW |  | 157.230.40.93 |
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
| DigitalOcean | AS14061 | VPS | Global | HIGH | 2 | 157.230.40.93, 206.189.127.204 |
| Hetzner | AS24940 | VPS / Dedicated | Germany / Finland | HIGH | 1 | 95.216.70.180 |
| OVHcloud | AS16276 | VPS / Dedicated | France / Europe | HIGH | 1 | 152.228.141.231 |
| Unknown | Unknown | Unknown | Unknown | LOW | 26 | 1.54.141.106, 113.173.209.213, 118.71.126.107, 139.162.1.250, 145.223.99.167, 156.67.104.212, 157.173.127.18, 157.173.127.21, 157.173.127.22, 157.173.127.30, 157.173.127.31, 168.144.140.128, 173.249.42.5, 185.190.143.54, 192.241.148.112, 194.163.186.161, 194.60.201.112, 207.154.217.91, 217.76.53.98, 38.49.213.251, 5.104.86.129, 5.9.116.21, 58.187.95.220, 83.228.229.39, 84.46.253.182, 95.111.227.13 |

## 12. Anomaly Detection Summary

| Anomaly Metric | Value |
| --- | --- |
| Anomaly count | 5 |
| Highest severity | HIGH |
| Severity counts | {'HIGH': 5} |
| Anomaly type counts | {'LARGE_ENODE_COUNT_DROP': 1, 'HIGH_REMOVAL_EVENT': 1, 'AGGRESSIVE_ROTATION': 3} |

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
