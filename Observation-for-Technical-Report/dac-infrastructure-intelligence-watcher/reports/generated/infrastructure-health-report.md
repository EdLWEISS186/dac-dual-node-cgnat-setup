# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-09T22:56:17.684087+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-09T22:56:17.684087+00:00 |
| Overall status | HEALTHY |
| Overall summary | All monitored DAC infrastructure endpoints are healthy. |
| Healthy endpoints | 3 |
| Degraded endpoints | 0 |
| Unhealthy endpoints | 0 |
| Total endpoints | 3 |

## 2. Monitoring Scope

| Component | URL |
|---|---|
| Official Public RPC | https://rpctest.dachain.tech/ |
| Explorer Web | https://exptest.dachain.tech/ |
| Primary Explorer API | https://exptest.dachain.tech/api |
| Timeout seconds | 15 |

## 3. Endpoint Status Summary

| Endpoint | Status | Summary |
|---|---|---|
| Official Public RPC | HEALTHY | Public RPC responded to required and optional JSON-RPC checks. |
| Explorer Web | HEALTHY | Explorer web returned HTTP 200 and recognizable explorer content. |
| Primary Explorer API | HEALTHY | Explorer API responded successfully to supported stats endpoint. |

## 4. Public RPC Details

| Field | Value |
|---|---|
| RPC status | HEALTHY |
| Chain ID | 21894 |
| Chain ID hex | 0x5586 |
| Latest block hex | 0xe4a705 |
| Latest block decimal | 14984965 |
| Average response time | 3297 ms |
| Maximum response time | 4713 ms |
| Response class | SLOW |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | True | 200 | 0x5586 | N/A |
| eth_blockNumber | True | 200 | 0xe4a705 | N/A |
| web3_clientVersion | True | 200 | gdacnode/DAC Testnet RPC 03/v1.10.5-stable-e4023222/linux-amd64/go1.25.1 | N/A |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 632 ms | avg=489 ms, max=496 ms |
| Response class | MODERATE | FAST |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 28 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-09T21-23-45-229029+00-00-health.json |
| Overall status counts | DEGRADED: 11, HEALTHY: 12, PARTIAL_OUTAGE: 5 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 11, HEALTHY: 12, UNHEALTHY: 5 |
| explorer_web | HEALTHY: 28 |
| primary_explorer_api | HEALTHY: 28 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
| 9 | 2026-06-04T11-38-26-409385+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 10 | 2026-06-04T11-50-50-288397+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 11 | 2026-06-04T16-59-50-793517+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 12 | 2026-06-04T17-34-38-689983+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 13 | 2026-06-04T17-39-38-929050+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 14 | 2026-06-04T19-47-12-825324+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 15 | 2026-06-06T12-16-24-339927+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 16 | 2026-06-06T15-41-44-603473+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 17 | 2026-06-07T08-29-35-513958+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 18 | 2026-06-07T10-41-05-109781+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 19 | 2026-06-07T12-12-00-907268+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 20 | 2026-06-07T17-06-43-581492+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 21 | 2026-06-08T01-59-16-847351+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 22 | 2026-06-08T06-47-13-271825+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 23 | 2026-06-09T01-30-52-519172+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 24 | 2026-06-09T05-51-55-728730+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 25 | 2026-06-09T12-21-12-097443+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 26 | 2026-06-09T15-36-15-483799+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 27 | 2026-06-09T17-35-46-336066+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 28 | 2026-06-09T21-23-45-229029+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |

## 8. Interpretation Notes

- RPC health is based on JSON-RPC POST checks, not HTTP GET root behavior.
- Explorer API root returning a validation error for missing module/action is treated as reachability evidence.
- Explorer API proxy module is not assumed to be supported.
- This health summary is an independent observation aid and not an official DAC service status page.

## 9. Report-Use Notes

This report is intended as supporting material for DAC Testnet infrastructure observation.

It can be used to review service-level health windows, public RPC reliability, explorer availability, explorer API reachability, partial infrastructure states, and recovery behavior.

It should not be treated as an official DAC service status page.

---

Prepared by **JERUZZALEM — DAC Infra Tester**.
