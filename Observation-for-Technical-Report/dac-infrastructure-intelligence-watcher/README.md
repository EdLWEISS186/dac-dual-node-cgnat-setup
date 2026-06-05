# DAC Infrastructure Intelligence Watcher

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Watcher](https://img.shields.io/badge/watcher-GitHub%20Actions-blue)
![Reports](https://img.shields.io/badge/reports-Markdown%20%7C%20JSON%20%7C%20PDF-purple)
![Dashboard](https://img.shields.io/badge/dashboard-GitHub%20Pages%20ready-0ea5e9)
![Chain ID](https://img.shields.io/badge/DAC%20Testnet-21894%20%7C%200x5586-orange)
![Maintainer](https://img.shields.io/badge/maintainer-JERUZZALEM-orange)

Community-built DAC Testnet public infrastructure observation, dashboard, comparison, and report export pipeline by **JERUZZALEM — DAC Infra Tester**.

This project monitors DAC public RPC, Explorer Web, and Explorer API endpoints, preserves health snapshots, builds a live static dashboard, and generates reusable Markdown, JSON, and PDF reports for technical infrastructure review.

## Live Links

| Resource | Link |
|---|---|
| Live Dashboard | https://edlweiss186.github.io/dac-dual-node-cgnat-setup/Observation-for-Technical-Report/dac-infrastructure-intelligence-watcher/dashboard/ |
| Repository | https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Observation-for-Technical-Report/dac-infrastructure-intelligence-watcher |
| Official DAC Public RPC | https://rpctest.dachain.tech/ |
| Official DAC Explorer Web | https://exptest.dachain.tech/ |
| Official DAC Explorer API | https://exptest.dachain.tech/api |

---

## Table of Contents

* [Overview](#overview)
* [Background](#background)
* [Why This Matters](#why-this-matters)
* [Monitoring Targets](#monitoring-targets)
* [Current Capabilities](#current-capabilities)
* [Architecture / Data Flow Topology](#architecture--data-flow-topology)
* [Observation Model](#observation-model)
* [Generated Outputs](#generated-outputs)
* [Dashboard](#dashboard)
* [Report Export Stack](#report-export-stack)
* [Observation Window Comparison](#observation-window-comparison)
* [Status & Response-Class Glossary](#status--response-class-glossary)
* [GitHub Actions Automation](#github-actions-automation)
* [Local Usage](#local-usage)
* [Current Generated State](#current-generated-state)
* [Version History](#version-history)
* [Security Notes](#security-notes)
* [Disclaimer](#disclaimer)
* [Maintainer](#maintainer)

---

## Overview

**DAC Infrastructure Intelligence Watcher** is an independent observation tool for DAC Testnet public infrastructure.

It started as a lightweight endpoint health checker and evolved into a complete infrastructure observation pipeline:

* public RPC health monitoring
* explorer web availability monitoring
* explorer API reachability monitoring
* JSON snapshot preservation
* response-time classification
* freshness / stale-state detection
* static dashboard visualization
* dashboard filtering
* dashboard charts
* standard range exports
* custom browser-side exports
* observation window comparison
* Markdown, JSON, and PDF report generation
* status and response-class glossary

The project is designed for infrastructure observation and technical reporting.

It does not make official DAC service-status claims.

---

## Background

DAC testnet participants may rely on different infrastructure surfaces:

* official public RPC
* explorer frontend
* explorer API
* self-hosted local nodes
* locally injected wallet RPC endpoints

A public endpoint can become slow, degraded, or unavailable without directly affecting every tester equally.

This watcher preserves independent observation data so public infrastructure behavior can be reviewed later instead of relying only on memory, screenshots, or one-time checks.

The project turns manual endpoint checking into a repeatable workflow:

```text
Manual endpoint check
        ↓
Risk of missed degradation or recovery
        ↓
Automated watcher
        ↓
Structured JSON snapshots
        ↓
Dashboard + reports + comparison exports
```

---

## Why This Matters

Public infrastructure health changes may reflect:

* RPC availability issues
* RPC response-time degradation
* explorer frontend downtime
* explorer API instability
* chain data visibility issues
* delayed block visibility
* stale dashboard data
* recovery after degraded windows
* differences between availability and response speed

A single observation is not enough to understand infrastructure behavior.

By preserving snapshots and generated reports, this project makes it easier to inspect how DAC public infrastructure behaves over time.

---

## Monitoring Targets

| Component | URL | Purpose |
|---|---|---|
| Official Public RPC | `https://rpctest.dachain.tech/` | JSON-RPC reachability, chain ID, latest block, client version |
| Explorer Web | `https://exptest.dachain.tech/` | Explorer website availability and explorer-signal detection |
| Primary Explorer API | `https://exptest.dachain.tech/api` | Explorer API reachability and supported stats checks |

Known DAC Testnet chain ID:

```text
Decimal: 21894
Hex:     0x5586
```

The dashboard displays `21894` first because it is easier for general readers.
The hex value `0x5586` is preserved as technical detail.

---

## Current Capabilities

The project currently supports:

* scheduled infrastructure health observation
* manual GitHub Actions execution
* latest-state tracking
* historical snapshot preservation
* public RPC JSON-RPC checks
* explorer web checks
* explorer API checks
* chain ID display in decimal and hex
* response-time classification
* overall health classification
* freshness / stale-state indicator
* Markdown health report generation
* static dashboard visualization
* dashboard status filtering
* dashboard response-class filtering
* dashboard charts
* standard 7D / 30D / ALL custom range reports
* standard 7D / 30D / ALL observation comparison reports
* Markdown, JSON, and PDF export outputs
* browser-side custom range export
* browser-side custom observation window comparison export
* status and response-class glossary across UI and reports

Alert notification is intentionally skipped for this project.

The maintainer also runs local node infrastructure and can inject local RPC into wallet usage, so public RPC degradation is useful to observe but not critical enough to require email alerting.

---

## Architecture / Data Flow Topology

Current v1.8.2 topology:

```text
GitHub Actions Scheduler
manual dispatch / scheduled run
        │
        ▼
infrastructure_health.py
- check Official Public RPC
- check Explorer Web
- check Primary Explorer API
- classify endpoint health
- classify overall health
- classify response-time behavior
- update latest.json
- create snapshot when health state changes
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
data/latest.json                              data/snapshots/*.json
latest watcher state                          historical health states
        │                                              │
        └──────────────────────┬───────────────────────┘
                               ▼
generate_health_report.py
- generate latest Markdown health report
                               │
                               ▼
reports/generated/infrastructure-health-report.md
                               │
                               ▼
generate_dashboard_data.py
- build dashboard JSON
- build chart summaries
- build freshness metadata
- build timeline fields
                               │
                               ▼
dashboard/data/health-dashboard-data.json
                               │
                               ▼
dashboard/index.html
- latest health cards
- endpoint cards
- comparison links
- export links
- custom browser exports
- dashboard filters
- dashboard charts
- status glossary
                               │
                               ▼
GitHub Pages Live Dashboard
```

Report and export topology:

```text
data/snapshots/*.json
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
generate_custom_report.py                 generate_comparison_report.py
- 7D custom range report                   - 7D comparison report
- 30D custom range report                  - 30D comparison report
- ALL custom range report                  - ALL comparison report
- Markdown output                          - Markdown output
- JSON output                              - JSON output
        │                                              │
        ▼                                              ▼
reports/generated/custom/*.md             reports/generated/comparison/*.md
reports/generated/custom/*.json           reports/generated/comparison/*.json
        │                                              │
        ▼                                              ▼
generate_pdf_report.py                    generate_comparison_pdf_report.py
- PDF from custom range JSON               - PDF from comparison JSON
        │                                              │
        ▼                                              ▼
reports/generated/custom/*.pdf            reports/generated/comparison/*.pdf
```

GitHub Actions automation:

```text
.github/workflows/dac-infrastructure-intelligence-watcher.yml
        │
        ▼
Scheduled run + manual run
        │
        ▼
infrastructure_health.py
generate_health_report.py
generate_dashboard_data.py
generate_custom_report.py --range 7d --format both
generate_custom_report.py --range 30d --format both
generate_custom_report.py --range all --format both
generate_comparison_report.py --range 7d --format both
generate_comparison_report.py --range 30d --format both
generate_comparison_report.py --range all --format both
generate_pdf_report.py --range 7d
generate_pdf_report.py --range 30d
generate_pdf_report.py --range all
generate_comparison_pdf_report.py --range 7d
generate_comparison_pdf_report.py --range 30d
generate_comparison_pdf_report.py --range all
        │
        ▼
Commit generated outputs only when files change
```

---

## Observation Model

This project separates infrastructure interpretation into three different concepts.

| Concept | Meaning |
|---|---|
| Availability status | Whether an endpoint is reachable and usable |
| Response class | How fast or slow the endpoint responded |
| Freshness status | Whether the latest dashboard data is current enough for review |

Important distinction:

```text
A service can be available but slow.
```

That means `HEALTHY` availability can appear together with `MODERATE` or `SLOW` response class.

Example:

```text
Explorer Web: HEALTHY
Response class: MODERATE
```

This means the endpoint is reachable, but response speed is not classified as fast.

---

## Generated Outputs

Latest state:

```text
data/latest.json
```

Historical snapshots:

```text
data/snapshots/*.json
```

Dashboard data:

```text
dashboard/data/health-dashboard-data.json
```

Main health report:

```text
reports/generated/infrastructure-health-report.md
```

Custom range exports:

```text
reports/generated/custom/infrastructure-report-7d.md
reports/generated/custom/infrastructure-report-7d.json
reports/generated/custom/infrastructure-report-7d.pdf

reports/generated/custom/infrastructure-report-30d.md
reports/generated/custom/infrastructure-report-30d.json
reports/generated/custom/infrastructure-report-30d.pdf

reports/generated/custom/infrastructure-report-all.md
reports/generated/custom/infrastructure-report-all.json
reports/generated/custom/infrastructure-report-all.pdf
```

Observation comparison exports:

```text
reports/generated/comparison/infrastructure-comparison-7d.md
reports/generated/comparison/infrastructure-comparison-7d.json
reports/generated/comparison/infrastructure-comparison-7d.pdf

reports/generated/comparison/infrastructure-comparison-30d.md
reports/generated/comparison/infrastructure-comparison-30d.json
reports/generated/comparison/infrastructure-comparison-30d.pdf

reports/generated/comparison/infrastructure-comparison-all.md
reports/generated/comparison/infrastructure-comparison-all.json
reports/generated/comparison/infrastructure-comparison-all.pdf
```

---

## Dashboard

Dashboard file:

```text
dashboard/index.html
```

Preview locally:

```text
python3 -m http.server 8091 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8091/dashboard/
```

The dashboard should be opened through a local HTTP server or GitHub Pages, not directly through `file://`, because it loads JSON data using `fetch()`.

### Dashboard views

The dashboard includes:

* latest overall infrastructure health
* data freshness indicator
* endpoint health cards
* public RPC chain ID display
* latest block information
* response-time class summaries
* observation window comparison links
* standard range health report exports
* browser-side custom range export
* browser-side custom observation comparison export
* dashboard chart layer
* dashboard filters
* health-state timeline
* status and response-class glossary
* interpretation notes

### Dashboard filters

Current filters:

* overall infrastructure status
* Official Public RPC status
* Explorer Web status
* Primary Explorer API status
* response-time class

### Dashboard charts

Current charts:

* Overall Status Distribution
* Endpoint Status Distribution
* Response Class Distribution
* Overall Health Score Trend

The chart layer uses native HTML, CSS, and JavaScript.
It does not require an external chart library.

### Dashboard exports

Standard range health reports:

* 7D Markdown
* 7D JSON
* 7D PDF
* 30D Markdown
* 30D JSON
* 30D PDF
* ALL Markdown
* ALL JSON
* ALL PDF

Observation window comparison reports:

* 7D Markdown
* 7D JSON
* 7D PDF
* 30D Markdown
* 30D JSON
* 30D PDF
* ALL Markdown
* ALL JSON
* ALL PDF

Custom browser exports:

* Custom Range Export
* Custom Range Observation Window Comparison

Custom browser exports run locally in the browser and are not committed back to the repository.

---

## Report Export Stack

Markdown and JSON are the primary reusable formats.

PDF is the final report packaging layer.

### Markdown and JSON custom range export

Generated by:

```text
generate_custom_report.py
```

Commands:

```text
python generate_custom_report.py --range 7d --format both
python generate_custom_report.py --range 30d --format both
python generate_custom_report.py --range all --format both
```

Supported formats:

```text
--format md
--format json
--format both
```

### Custom range PDF export

Generated by:

```text
generate_pdf_report.py
```

Dependency:

```text
reportlab
```

Commands:

```text
python generate_pdf_report.py --range 7d
python generate_pdf_report.py --range 30d
python generate_pdf_report.py --range all
```

### Browser-side custom export

Available from the dashboard:

```text
Custom Range Export
```

Options:

* From observation
* To observation
* Download Custom Markdown
* Download Custom JSON
* Print / Save Custom PDF

Browser-side custom exports are local downloads and do not write files back to the repository.

---

## Observation Window Comparison

Observation Window Comparison compares two observation windows.

| Window | Meaning |
|---|---|
| Window A | Earlier or baseline observation segment |
| Window B | Later comparison segment |

The comparison layer helps review:

* whether later infrastructure availability improved
* whether later infrastructure availability worsened
* whether the state was mostly unchanged
* whether response-time behavior shifted
* whether endpoint-level status distribution changed

Generated by:

```text
generate_comparison_report.py
```

Commands:

```text
python generate_comparison_report.py --range 7d --format both
python generate_comparison_report.py --range 30d --format both
python generate_comparison_report.py --range all --format both
```

Comparison PDF generated by:

```text
generate_comparison_pdf_report.py
```

Commands:

```text
python generate_comparison_pdf_report.py --range 7d
python generate_comparison_pdf_report.py --range 30d
python generate_comparison_pdf_report.py --range all
```

Browser-side custom comparison is available in the dashboard:

```text
Custom Range Observation Window Comparison
```

Options:

* Window A from observation
* Window A to observation
* Window B from observation
* Window B to observation
* Download Custom Comparison Markdown
* Download Custom Comparison JSON
* Print / Save Custom Comparison PDF

---

## Status & Response-Class Glossary

These labels are used across dashboard UI, Markdown reports, JSON summaries, and PDF exports.

| Status / Class | Meaning |
|---|---|
| HEALTHY | The endpoint or overall infrastructure state is reachable and behaving as expected. |
| DEGRADED | The endpoint is reachable, but one or more checks or response-time indicators show reduced quality. |
| PARTIAL_OUTAGE | At least one monitored endpoint is unavailable or failing while other endpoints remain reachable. |
| UNHEALTHY | The endpoint failed required checks or did not provide usable responses. |
| FAST | The observed response-time class is fast for this watcher context. |
| MODERATE | The observed response-time class is acceptable but not fast. |
| SLOW | The observed response-time class is slow and may indicate degraded user experience. |
| UNKNOWN | The watcher could not classify the response-time state, often because older snapshots did not include this field. |
| N/A | Not available or not applicable for the selected observation, endpoint, or historical snapshot. |

---

## GitHub Actions Automation

Workflow file:

```text
.github/workflows/dac-infrastructure-intelligence-watcher.yml
```

The workflow can be triggered manually from the GitHub Actions tab.

Current pipeline:

```text
infrastructure_health.py
generate_health_report.py
generate_dashboard_data.py
generate_custom_report.py --range 7d --format both
generate_custom_report.py --range 30d --format both
generate_custom_report.py --range all --format both
generate_comparison_report.py --range 7d --format both
generate_comparison_report.py --range 30d --format both
generate_comparison_report.py --range all --format both
generate_pdf_report.py --range 7d
generate_pdf_report.py --range 30d
generate_pdf_report.py --range all
generate_comparison_pdf_report.py --range 7d
generate_comparison_pdf_report.py --range 30d
generate_comparison_pdf_report.py --range all
```

Generated outputs are committed only when files change.

---

## Local Usage

Install dependencies:

```text
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

Run the watcher manually:

```text
python3 infrastructure_health.py
```

Generate main report and dashboard data:

```text
python3 generate_health_report.py
python3 generate_dashboard_data.py
```

Generate custom reports:

```text
python3 generate_custom_report.py --range 7d --format both
python3 generate_custom_report.py --range 30d --format both
python3 generate_custom_report.py --range all --format both
```

Generate comparison reports:

```text
python3 generate_comparison_report.py --range 7d --format both
python3 generate_comparison_report.py --range 30d --format both
python3 generate_comparison_report.py --range all --format both
```

Generate optional PDFs:

```text
.venv/bin/python generate_pdf_report.py --range 7d
.venv/bin/python generate_pdf_report.py --range 30d
.venv/bin/python generate_pdf_report.py --range all

.venv/bin/python generate_comparison_pdf_report.py --range 7d
.venv/bin/python generate_comparison_pdf_report.py --range 30d
.venv/bin/python generate_comparison_pdf_report.py --range all
```

Preview dashboard:

```text
python3 -m http.server 8091 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8091/dashboard/
```

---

## Current Generated State

Current generated state is intentionally stored in repository outputs instead of being hardcoded here.

Review current state from:

```text
data/latest.json
dashboard/data/health-dashboard-data.json
reports/generated/infrastructure-health-report.md
```

Current report bundles:

```text
Custom range Markdown reports: 3
Custom range JSON summaries: 3
Custom range PDF reports: 3

Comparison Markdown reports: 3
Comparison JSON summaries: 3
Comparison PDF reports: 3
```

---

## Version History

| Version | Summary |
|---|---|
| v1.0.0 | Initial infrastructure health watcher |
| v1.1.0 | Deterministic Markdown health report summary layer |
| v1.2.0 | Static infrastructure health dashboard layer |
| v1.3.0 | Dashboard freshness and stale-state indicator layer |
| v1.4.0 | Custom range report generation layer |
| v1.5.0 | Observation window comparison layer |
| v1.5.1 | Dashboard Chain ID decimal display and comparison links |
| v1.6.0 | Richer dashboard filtering layer |
| v1.7.0 | Dashboard chart visualization layer |
| v1.8.0 | Optional PDF export, export links hub, and chart polish |
| v1.8.1 | Observation comparison Markdown / JSON / PDF export parity |
| v1.8.2 | PDF report style alignment and status glossary patch |

---

## Security Notes

Do not commit credentials, `.env` files, access tokens, SMTP passwords, or wallet/private key material.

The project ignores:

* `.venv/`
* `venv/`
* `__pycache__/`
* `*.pyc`
* `.env`

Generated observation artifacts are intentionally tracked because they preserve infrastructure history.

Generated PDFs are treated as binary artifacts through `.gitattributes`.

---

## Disclaimer

This is an independent community-built observation tool.

It is not an official DAC tool and does not represent official DAC infrastructure policy.

The watcher observes publicly reachable DAC testnet infrastructure endpoints and stores snapshots for technical reporting purposes.

Availability labels, response classes, freshness states, and comparison summaries are observation-based. They should not be treated as official DAC service-status claims.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
