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

---

## Health Report Summary Layer

v1.1.0 adds a generated Markdown report layer for infrastructure health summaries.

Generator:

    generate_health_report.py

Generated output:

    reports/generated/infrastructure-health-report.md

The report summarizes:

- latest overall infrastructure health
- monitoring scope
- endpoint status summary
- public RPC details
- explorer web and explorer API details
- snapshot history summary
- recent endpoint-level health timeline
- interpretation notes
- report-use notes

The report is generated from existing JSON outputs:

    data/latest.json
    data/snapshots/*.json

The report is deterministic. It uses the latest watcher state timestamp from `data/latest.json`, not wall-clock generation time. This prevents unnecessary workflow commits when the underlying health state has not changed.

---

## Static Health Dashboard Layer

v1.2.0 adds a static dashboard layer for visual infrastructure health inspection.

Dashboard entry point:

    dashboard/index.html

Generated dashboard data:

    dashboard/data/health-dashboard-data.json

Dashboard data builder:

    generate_dashboard_data.py

The dashboard summarizes:

- latest overall infrastructure health
- endpoint availability status
- endpoint response-time class
- public RPC status and latest block information
- explorer web status and response time
- explorer API status and response time
- overall health-state distribution
- endpoint history counts
- health-state timeline
- interpretation notes

The dashboard is static and reads from generated JSON data. It is designed to work through a local HTTP server or GitHub Pages.

The dashboard uses the local project asset:

    assets/JERUZZALEM-Infra_Tester.png


---

## GitHub Actions Automation

Workflow file:

    .github/workflows/dac-infrastructure-intelligence-watcher.yml

Current schedule:

    */15 * * * *

Current workflow steps:

    infrastructure_health.py
    generate_health_report.py
    generate_dashboard_data.py

The workflow checks DAC public infrastructure health, updates tracked JSON outputs when endpoint-level health state changes, regenerates the Markdown health report, and commits generated changes back to the repository when needed.

---

## Version Notes

| Version | Summary |
|---|---|
| v1.0.0 | Initial public RPC, explorer web, and explorer API health watcher |
| v1.1.0 | Deterministic Markdown health report summary layer |
| v1.2.0 | Static infrastructure health dashboard layer |
