# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-30T13:28:33.493377+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-30T13:28:33.493377+00:00 |
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
| Latest block hex | 0xe67626 |
| Latest block decimal | 15103526 |
| Average response time | 5036 ms |
| Maximum response time | 8336 ms |
| Response class | SLOW |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | True | 200 | 0x5586 | N/A |
| eth_blockNumber | True | 200 | 0xe67626 | N/A |
| web3_clientVersion | True | 200 | gdacnode/DAC-Node 05/v1.11.6-stable/linux-amd64/go1.22.12 | N/A |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 629 ms | avg=464 ms, max=472 ms |
| Response class | MODERATE | FAST |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 82 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-30T13-28-33-493377+00-00-health.json |
| Overall status counts | DEGRADED: 34, HEALTHY: 37, PARTIAL_OUTAGE: 11 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 34, HEALTHY: 37, UNHEALTHY: 11 |
| explorer_web | HEALTHY: 82 |
| primary_explorer_api | HEALTHY: 82 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
| 63 | 2026-06-25T19-29-25-516852+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 64 | 2026-06-26T08-18-53-347052+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 65 | 2026-06-26T11-20-30-135425+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 66 | 2026-06-26T20-55-49-405430+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 67 | 2026-06-26T22-06-06-469588+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 68 | 2026-06-26T23-22-07-890400+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 69 | 2026-06-27T13-14-03-249844+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 70 | 2026-06-27T14-55-49-430298+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 71 | 2026-06-27T16-00-02-127479+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 72 | 2026-06-27T17-16-45-438386+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 73 | 2026-06-27T19-57-07-933682+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 74 | 2026-06-27T20-59-11-427839+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 75 | 2026-06-28T06-01-40-043636+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 76 | 2026-06-28T09-30-32-330521+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 77 | 2026-06-28T12-51-16-533873+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 78 | 2026-06-28T14-43-06-952490+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 79 | 2026-06-29T09-24-55-311755+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 80 | 2026-06-29T13-49-24-711303+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 81 | 2026-06-30T08-44-47-357691+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 82 | 2026-06-30T13-28-33-493377+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |

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
