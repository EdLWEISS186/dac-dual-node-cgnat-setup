# DAC Infrastructure Intelligence Watcher

Independent DAC Testnet infrastructure health and availability watcher by **JERUZZALEM — DAC Infra Tester**.

This project monitors public DAC infrastructure endpoints beyond the official enode registry.

It is separated from the DAC Enode Intelligence Watcher because this watcher focuses on service availability, RPC responsiveness, explorer reachability, and multi-source infrastructure health.

---

## Monitoring Scope

Current v1.0.0 endpoints:

| Component | URL | Purpose |
|---|---|---|
| Official Public RPC | https://rpctest.dachain.tech/ | JSON-RPC health and block availability |
| Explorer Web | https://exptest.dachain.tech/ | Explorer frontend availability |
| Primary Explorer API | https://exptest.dachain.tech/api | Explorer API reachability and supported endpoint checks |

---

## Current Focus

v1.0.0 focuses on:

- public RPC health monitoring
- explorer web availability monitoring
- explorer API availability monitoring
- response status tracking
- response latency tracking
- JSON health snapshots
- report-ready infrastructure health summaries

---

## Why This Project Is Separate

The existing DAC Enode Intelligence Watcher focuses on:

- official enode registry monitoring
- enode rotation
- peer list changes
- provider / ASN / infrastructure signal analysis
- enode-based dashboard and reports

This project focuses on:

- public RPC health
- explorer frontend availability
- explorer API reachability
- service-level health signals
- future multi-source infrastructure correlation

Keeping the projects separate makes each watcher easier to maintain, audit, and explain.

---

## Planned Output Files

    data/latest.json
    data/snapshots/*.json
    reports/generated/

---

## Interpretation Notes

This watcher is an observation aid.

It is not an official DAC service status page.

Endpoint status, latency, and health labels should be treated as independent technical observations, not official infrastructure guarantees.

---

## Maintainer

JERUZZALEM — DAC Infra Tester
