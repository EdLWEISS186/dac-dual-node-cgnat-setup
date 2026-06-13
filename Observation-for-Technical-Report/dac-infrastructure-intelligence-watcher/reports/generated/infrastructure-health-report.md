# DAC Infrastructure Intelligence Watcher — Health Report

Generated from latest watcher state UTC: **2026-06-13T17:43:45.241764+00:00**

This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.

It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.

---

## 1. Latest Overall Health

| Field | Value |
|---|---|
| Project | DAC Infrastructure Intelligence Watcher |
| Watcher version | v1.0.0 |
| Report layer version | v1.1.0 |
| Checked at UTC | 2026-06-13T17:43:45.241764+00:00 |
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
| Chain ID hex | N/A |
| Latest block hex | N/A |
| Latest block decimal | N/A |
| Average response time | 324 ms |
| Maximum response time | 336 ms |
| Response class | FAST |

| Method | OK | HTTP Status | Result | Error |
|---|---:|---:|---|---|
| eth_chainId | False | N/A | N/A | HTTPSConnectionPool(host='rpctest.dachain.tech', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)'))) |
| eth_blockNumber | False | N/A | N/A | HTTPSConnectionPool(host='rpctest.dachain.tech', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)'))) |
| web3_clientVersion | False | N/A | N/A | HTTPSConnectionPool(host='rpctest.dachain.tech', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)'))) |

## 5. Explorer Details

| Field | Explorer Web | Primary Explorer API |
|---|---|---|
| Status | HEALTHY | HEALTHY |
| OK | True | True |
| HTTP / validation | 200 | root_validation=True, stats_ok=True |
| Response time | 825 ms | avg=525 ms, max=623 ms |
| Response class | MODERATE | MODERATE |
| Title / API URL | DAC Inception Testnet blockchain explorer - View DAC Inception Testnet stats | https://exptest.dachain.tech/api |

## 6. Snapshot History Summary

| Field | Value |
|---|---|
| Snapshot count | 37 |
| First snapshot | 2026-06-04T09-54-55-772035+00-00-health.json |
| Latest snapshot | 2026-06-13T17-43-45-241764+00-00-health.json |
| Overall status counts | DEGRADED: 15, HEALTHY: 16, PARTIAL_OUTAGE: 6 |

| Endpoint | Status counts |
|---|---|
| official_public_rpc | DEGRADED: 15, HEALTHY: 16, UNHEALTHY: 6 |
| explorer_web | HEALTHY: 37 |
| primary_explorer_api | HEALTHY: 37 |

## 7. Recent Snapshot Timeline

| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |
|---:|---|---|---|---|---|
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
| 35 | 2026-06-13T10-43-09-685105+00-00-health.json | DEGRADED | DEGRADED | HEALTHY | HEALTHY |
| 36 | 2026-06-13T12-15-24-292365+00-00-health.json | HEALTHY | HEALTHY | HEALTHY | HEALTHY |
| 37 | 2026-06-13T17-43-45-241764+00-00-health.json | PARTIAL_OUTAGE | UNHEALTHY | HEALTHY | HEALTHY |

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
