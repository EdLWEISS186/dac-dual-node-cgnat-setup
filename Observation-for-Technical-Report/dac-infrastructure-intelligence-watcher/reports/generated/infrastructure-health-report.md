# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-12T06:18:01.079328+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-12T06:18:01.079328+00:00 |
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
| Latest block hex | 0xe4daee |
| Latest block decimal | 14998254 |
| Average response time | 741 ms |
| Maximum response time | 1156 ms |
| Response class | MODERATE |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | True | 200 | 0x5586 | N/A |
| eth_blockNumber | True | 200 | 0xe4daee | N/A |
| web3_clientVersion | True | 200 | gdacnode/DAC Testnet RPC 04/v1.10.5-stable-e4023222/linux-amd64/go1.25.1 | N/A |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 663 ms | avg=628 ms, max=729 ms |
| Response class | MODERATE | MODERATE |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 34 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-11T00-13-29-727818+00-00-health.json |
| Overall status counts | DEGRADED: 14, HEALTHY: 15, PARTIAL_OUTAGE: 5 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 14, HEALTHY: 15, UNHEALTHY: 5 |
| explorer_web | HEALTHY: 34 |
| primary_explorer_api | HEALTHY: 34 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
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
| 29 | 2026-06-10T12-00-49-579476+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 30 | 2026-06-10T16-06-33-205459+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 31 | 2026-06-10T18-40-39-968153+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 32 | 2026-06-10T21-13-30-728841+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 33 | 2026-06-10T22-57-26-492242+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 34 | 2026-06-11T00-13-29-727818+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |

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
