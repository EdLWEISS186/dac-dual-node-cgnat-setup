# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-04T16:59:50.793517+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-04T16:59:50.793517+00:00 |
| Overall status | PARTIAL_OUTAGE |
| Overall summary | At least one endpoint is unhealthy while other monitored endpoints remain reachable. |
| Healthy endpoints | 2 |
| Degraded endpoints | 0 |
| Unhealthy endpoints | 1 |
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
| Official Public RPC | UNHEALTHY | Public RPC failed all JSON-RPC checks. |
| Explorer Web | HEALTHY | Explorer web returned HTTP 200 and recognizable explorer content. |
| Primary Explorer API | HEALTHY | Explorer API responded successfully to supported stats endpoint. |

## 4. Public RPC Details

| Field | Value |
|---|---|
| RPC status | UNHEALTHY |
| Chain ID | N/A |
| Latest block hex | N/A |
| Latest block decimal | N/A |
| Average response time | 965 ms |
| Maximum response time | 1329 ms |
| Response class | MODERATE |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | False | N/A | N/A | ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |
| eth_blockNumber | False | 502 | N/A | N/A |
| web3_clientVersion | False | 502 | N/A | N/A |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 721 ms | avg=581 ms, max=620 ms |
| Response class | MODERATE | MODERATE |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 11 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-04T16-59-50-793517+00-00-health.json |
| Overall status counts | DEGRADED: 3, HEALTHY: 3, PARTIAL_OUTAGE: 5 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 3, HEALTHY: 3, UNHEALTHY: 5 |
| explorer_web | HEALTHY: 11 |
| primary_explorer_api | HEALTHY: 11 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
| 1 | 2026-06-04T09-54-55-772035+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 2 | 2026-06-04T09-59-08-192048+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 3 | 2026-06-04T09-59-48-937274+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 4 | 2026-06-04T10-00-10-486388+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 5 | 2026-06-04T10-02-58-023788+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 6 | 2026-06-04T11-35-39-447567+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 7 | 2026-06-04T11-36-10-013189+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 8 | 2026-06-04T11-38-16-082796+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 9 | 2026-06-04T11-38-26-409385+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 10 | 2026-06-04T11-50-50-288397+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 11 | 2026-06-04T16-59-50-793517+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |

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
