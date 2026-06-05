# DAC Observation for Technical Report

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Scope](https://img.shields.io/badge/scope-DAC%20Infrastructure%20Observation-blue)
![Reports](https://img.shields.io/badge/reports-Markdown%20%7C%20JSON%20%7C%20PDF-purple)
![Dashboards](https://img.shields.io/badge/dashboards-GitHub%20Pages%20ready-0ea5e9)
![Automation](https://img.shields.io/badge/automation-GitHub%20Actions-black)
![Maintainer](https://img.shields.io/badge/maintainer-JERUZZALEM-orange)

Engineering workspace for DAC Testnet infrastructure observation, automated monitoring, dashboard generation, and reusable technical-report material by **JERUZZALEM — DAC Infra Tester**.

This folder contains supporting projects used to observe DAC infrastructure behavior over time, preserve structured evidence, generate dashboards, and export report-ready outputs for public or internal technical review.

---

## Overview

`Observation-for-Technical-Report` is a dedicated workspace for DAC infrastructure observation projects.

The purpose of this folder is to keep technical observation work separate from application code, sender tools, wallet intelligence tools, or node setup material.

It contains monitoring systems, generated datasets, dashboard layers, and technical-report exports that help document how DAC infrastructure behaves during testnet operation.

This workspace is designed around engineering evidence:

* observable public infrastructure state
* structured JSON snapshots
* generated Markdown reports
* generated JSON summaries
* optional PDF exports
* live dashboard views
* repeatable GitHub Actions automation
* report-ready archive material

It does not make official DAC infrastructure claims.

It preserves independent observation material for technical review.

---

## Table of Contents

| # | Project | Function |
|---:|---|---|
| 1 | [DAC Enode Intelligence Watcher](./dac-enode-intelligence-watcher/) | Observes the official DAC Testnet enode source, preserves enode snapshots, analyzes peer rotation, detects anomaly signals, enriches infrastructure hints, and exports dashboard/report material. |
| 2 | [DAC Infrastructure Intelligence Watcher](./dac-infrastructure-intelligence-watcher/) | Observes DAC public RPC, Explorer Web, and Explorer API health, preserves endpoint health snapshots, compares observation windows, and exports Markdown, JSON, and PDF infrastructure reports. |

---

## Why This Folder Exists

DAC infrastructure testing produces useful evidence beyond a single node log or one-time screenshot.

This folder exists to preserve that evidence in a structured way.

Instead of keeping observations only as screenshots, manual notes, or temporary terminal output, each watcher project turns infrastructure signals into reusable data:

```text
Public DAC infrastructure source
        ↓
Watcher / parser / health checker
        ↓
Structured JSON state
        ↓
Historical snapshots
        ↓
Dashboard data
        ↓
Markdown / JSON / PDF reports
        ↓
Technical report archive material
```

This makes the observation process easier to audit, repeat, and explain.

---

## Current Observation Projects

### DAC Enode Intelligence Watcher

Folder:

```text
dac-enode-intelligence-watcher/
```

Primary role:

```text
Official DAC Testnet enode observation and infrastructure intelligence.
```

This project monitors the public DAC enode source and builds historical intelligence around peer-list evolution.

It supports:

* official enode page monitoring
* enode snapshot preservation
* manual backfill history
* added / removed / unchanged enode detection
* target port tracking
* rotation intelligence
* anomaly detection
* provider / ASN enrichment
* DAC Infrastructure Signal inference
* concentration risk summaries
* static dashboard visualization
* Markdown, JSON, and PDF exports

Main value:

```text
Turns public enode changes into structured infrastructure observation material.
```

---

### DAC Infrastructure Intelligence Watcher

Folder:

```text
dac-infrastructure-intelligence-watcher/
```

Primary role:

```text
DAC public RPC, Explorer Web, and Explorer API health observation.
```

This project monitors public DAC infrastructure endpoints and builds report-ready health summaries.

It supports:

* public RPC health checks
* explorer web availability checks
* explorer API reachability checks
* chain ID validation
* response-time classification
* freshness / stale-state detection
* historical health snapshots
* observation window comparison
* dashboard filtering
* dashboard charts
* status and response-class glossary
* Markdown, JSON, and PDF exports

Main value:

```text
Turns endpoint health behavior into structured infrastructure health evidence.
```

---

## Engineering Scope

This workspace focuses on observation and reporting, not production control.

It is intended for:

* infrastructure testing support
* DAC testnet monitoring evidence
* public technical-report preparation
* dashboard-based review
* historical infrastructure behavior analysis
* reproducible report generation

It is not intended to:

* replace official DAC monitoring
* represent official DAC service status
* control DAC infrastructure
* claim infrastructure ownership
* expose private credentials or node secrets

---

## Folder Structure

```text
Observation-for-Technical-Report/
├─ README.md
├─ dac-enode-intelligence-watcher/
│  ├─ dashboard/
│  ├─ data/
│  ├─ reports/
│  ├─ assets/
│  ├─ watcher.py
│  ├─ build_rotation_intelligence.py
│  ├─ build_anomaly_detection.py
│  ├─ build_concentration_risk.py
│  ├─ generate_custom_report.py
│  ├─ generate_pdf_report.py
│  └─ README.md
└─ dac-infrastructure-intelligence-watcher/
   ├─ dashboard/
   ├─ data/
   ├─ reports/
   ├─ assets/
   ├─ infrastructure_health.py
   ├─ generate_health_report.py
   ├─ generate_dashboard_data.py
   ├─ generate_custom_report.py
   ├─ generate_comparison_report.py
   ├─ generate_pdf_report.py
   ├─ generate_comparison_pdf_report.py
   └─ README.md
```

---

## Output Types

Projects in this folder may generate several output types.

| Output Type | Purpose |
|---|---|
| `data/latest.json` | Latest watcher state |
| `data/snapshots/*.json` | Historical observation archive |
| `dashboard/data/*.json` | Static dashboard data |
| `dashboard/index.html` | GitHub Pages-ready dashboard |
| `reports/generated/*.md` | Markdown technical report |
| `reports/generated/**/*.json` | Machine-readable report summary |
| `reports/generated/**/*.pdf` | Shareable final report package |

Generated outputs are intentionally tracked when they preserve observation history or report material.

---

## Automation Model

Watcher projects are designed to run through GitHub Actions.

Typical automation pattern:

```text
Scheduled workflow / manual dispatch
        ↓
Run watcher or health checker
        ↓
Generate JSON state
        ↓
Generate reports
        ↓
Generate dashboard data
        ↓
Generate optional PDFs
        ↓
Commit generated outputs when files change
```

This allows the repository to act as both:

* source code repository
* observation archive
* dashboard host
* report export store

---

## Report-Use Value

This folder supports technical reporting by preserving:

* what was observed
* when it was observed
* which source was checked
* what changed
* what remained stable
* what looked degraded
* what looked healthy
* how the data was transformed into reports

The goal is to make infrastructure observation credible, repeatable, and easy to reference later.

---

## Security Notes

Do not commit:

* private keys
* wallet secrets
* node credentials
* SMTP passwords
* GitHub tokens
* `.env` files
* local-only runtime secrets

Generated public observation files may be committed when they do not expose secrets and are useful for technical reporting.

---

## Disclaimer

This is an independent community-built observation workspace.

It is not an official DAC tool.

It does not represent official DAC infrastructure policy, official DAC service status, or official DAC ownership classification.

All dashboards, reports, summaries, and labels are observation-based and should be treated as technical review material.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
