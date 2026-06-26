# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-26T19:14:49.072671+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-26T19:14:49.072671+00:00 |
| Overall status | DEGRADED |
| Overall summary | All monitored endpoints are reachable, but at least one endpoint is degraded. |
| Healthy endpoints | 2 |
| Degraded endpoints | 1 |
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
| Official Public RPC | DEGRADED | Public RPC is reachable, but one or more JSON-RPC checks failed. |
| Explorer Web | HEALTHY | Explorer web returned HTTP 200 and recognizable explorer content. |
| Primary Explorer API | HEALTHY | Explorer API responded successfully to supported stats endpoint. |

## 4. Public RPC Details

| Field | Value |
|---|---|
| RPC status | DEGRADED |
| Chain ID | N/A |
| Chain ID hex | N/A |
| Latest block hex | 0xe6218f |
| Latest block decimal | 15081871 |
| Average response time | 12444 ms |
| Maximum response time | 15053 ms |
| Response class | SLOW |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | False | N/A | N/A | HTTPSConnectionPool(host='rpctest.dachain.tech', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<HTTPSConnection(host='rpctest.dachain.tech', port=443) at 0x7f389d267410>, 'Connection to rpctest.dachain.tech timed out. (connect timeout=15)')) |
| eth_blockNumber | True | 200 | 0xe6218f | N/A |
| web3_clientVersion | False | N/A | N/A | HTTPSConnectionPool(host='rpctest.dachain.tech', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<HTTPSConnection(host='rpctest.dachain.tech', port=443) at 0x7f389c525b10>, 'Connection to rpctest.dachain.tech timed out. (connect timeout=15)')) |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 807 ms | avg=587 ms, max=651 ms |
| Response class | MODERATE | MODERATE |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 65 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-26T11-20-30-135425+00-00-health.json |
| Overall status counts | DEGRADED: 26, HEALTHY: 28, PARTIAL_OUTAGE: 11 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 26, HEALTHY: 28, UNHEALTHY: 11 |
| explorer_web | HEALTHY: 65 |
| primary_explorer_api | HEALTHY: 65 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
| 46 | 2026-06-18T14-34-01-163762+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 47 | 2026-06-18T17-47-21-319826+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 48 | 2026-06-19T00-07-49-114576+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 49 | 2026-06-19T05-22-45-224068+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 50 | 2026-06-19T13-33-33-772138+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 51 | 2026-06-19T16-20-47-830658+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 52 | 2026-06-21T07-05-49-768754+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 53 | 2026-06-21T10-45-15-026750+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 54 | 2026-06-22T16-01-14-927486+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 55 | 2026-06-22T21-50-02-920913+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 56 | 2026-06-23T05-34-47-341574+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 57 | 2026-06-23T08-46-04-761597+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 58 | 2026-06-24T16-00-28-478127+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 59 | 2026-06-24T18-06-14-278129+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 60 | 2026-06-25T07-53-39-662511+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 61 | 2026-06-25T10-36-00-952733+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 62 | 2026-06-25T15-44-39-846328+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 63 | 2026-06-25T19-29-25-516852+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 64 | 2026-06-26T08-18-53-347052+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 65 | 2026-06-26T11-20-30-135425+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |

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
