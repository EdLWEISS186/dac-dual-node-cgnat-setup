# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-15T20:07:32.425470+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-15T20:07:32.425470+00:00 |
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
| Latest block hex | 0xe52b63 |
| Latest block decimal | 15018851 |
| Average response time | 924 ms |
| Maximum response time | 1106 ms |
| Response class | MODERATE |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | True | 200 | 0x5586 | N/A |
| eth_blockNumber | True | 200 | 0xe52b63 | N/A |
| web3_clientVersion | True | 200 | gdacnode/DAC Testnet RPC 03/v1.10.5-stable-e4023222/linux-amd64/go1.25.1 | N/A |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 476 ms | avg=363 ms, max=364 ms |
| Response class | FAST | FAST |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 44 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-15T20-07-32-425470+00-00-health.json |
| Overall status counts | DEGRADED: 17, HEALTHY: 20, PARTIAL_OUTAGE: 7 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 17, HEALTHY: 20, UNHEALTHY: 7 |
| explorer_web | HEALTHY: 44 |
| primary_explorer_api | HEALTHY: 44 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
| 25 | 2026-06-09T12-21-12-097443+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 26 | 2026-06-09T15-36-15-483799+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 27 | 2026-06-09T17-35-46-336066+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 28 | 2026-06-09T21-23-45-229029+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 29 | 2026-06-10T12-00-49-579476+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 30 | 2026-06-10T16-06-33-205459+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 31 | 2026-06-10T18-40-39-968153+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 32 | 2026-06-10T21-13-30-728841+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 33 | 2026-06-10T22-57-26-492242+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 34 | 2026-06-11T00-13-29-727818+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 35 | 2026-06-13T10-43-09-685105+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 36 | 2026-06-13T12-15-24-292365+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 37 | 2026-06-13T17-43-45-241764+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 38 | 2026-06-13T18-57-21-166839+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 39 | 2026-06-14T02-47-39-011114+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |
| 40 | 2026-06-14T07-17-43-721261+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 41 | 2026-06-14T15-06-02-854660+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 42 | 2026-06-14T17-46-11-842614+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 43 | 2026-06-15T16-32-07-477470+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 44 | 2026-06-15T20-07-32-425470+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |

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
