# DAC Enode Intelligence Watcher

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Watcher](https://img.shields.io/badge/watcher-every%2015%20minutes-blue)
![Reports](https://img.shields.io/badge/reports-Markdown%20%7C%20JSON%20%7C%20PDF-purple)
![Dashboard](https://img.shields.io/badge/dashboard-GitHub%20Pages%20ready-0ea5e9)
![Maintainer](https://img.shields.io/badge/maintainer-JERUZZALEM-orange)

Community-built DAC Testnet enode observation, intelligence, dashboard, and report export pipeline by **JERUZZALEM — DAC Infra Tester**.

This project monitors the public DAC Testnet enode source, preserves historical snapshots, enriches observed infrastructure data, detects rotation and anomaly signals, builds dashboards, and generates reusable Markdown, JSON, and PDF reports.

---

## Table of Contents

- [Overview](#overview)
- [Background](#background)
- [Why This Matters](#why-this-matters)
- [Monitoring Target](#monitoring-target)
- [Current Capabilities](#current-capabilities)
- [Architecture / Data Flow Topology](#architecture--data-flow-topology)
- [Observation Phases](#observation-phases)
- [Generated Outputs](#generated-outputs)
- [Intelligence Layers](#intelligence-layers)
- [Dashboard](#dashboard)
- [Report Export Stack](#report-export-stack)
- [GitHub Actions Automation](#github-actions-automation)
- [Local Usage](#local-usage)
- [Current Generated State](#current-generated-state)
- [Version History](#version-history)
- [Future Upgrade Direction](#future-upgrade-direction)
- [Security Notes](#security-notes)
- [Disclaimer](#disclaimer)
- [Maintainer](#maintainer)

---

## Overview

**DAC Enode Intelligence Watcher** is an independent observation tool for the DAC Testnet public enode page.

It started as a simple automated watcher and evolved into a full observation pipeline:

- official enode monitoring
- JSON snapshot preservation
- manual backfill support
- rotation intelligence
- anomaly detection
- provider / ASN enrichment
- live ASN lookup
- DAC Infrastructure Signal inference
- provider concentration risk summary
- static dashboard visualization
- fixed-range and custom-range report exports
- Markdown, JSON, and optional PDF output

The project is designed for infrastructure observation and technical reporting.

It does not make official DAC ownership claims or definitive decentralization claims.

---

## Background

This project continues earlier manual technical observation work around DAC official enode evolution.

The original manual process depended on screenshots and text captures from the public enode page. That approach was useful for point-in-time evidence, but difficult to follow consistently because the source page can update and previous states are no longer visible.

This watcher turns that manual process into a repeatable automated workflow:

    Manual observation
            ↓
    Risk of missed updates
            ↓
    Automated watcher
            ↓
    Structured JSON snapshots
            ↓
    Intelligence summaries
            ↓
    Dashboard + technical reports

---

## Why This Matters

Official enode changes may reflect infrastructure-level activity such as:

- bootstrap peer rotation
- public peer refresh
- node replacement
- infrastructure scaling
- network maintenance
- testnet maturation
- target port consistency or migration
- unusually large peer-list reduction
- abnormal rotation candidates for review

A single manual observation can miss these changes.

By preserving structured snapshots and derived summaries, this project makes it easier to review how the official enode list evolves over time.

---

## Monitoring Target

Target page:

    https://enodes.dachain.tech/testnet/

Observed source format:

    Generated: Wed Jun 3 12:00:02 PM CEST 2026 | Target Port: 28657

    admin.addPeer("enode://...@IP:28657");

Current watcher schedule:

    */15 * * * *

The watcher runs every 15 minutes through GitHub Actions, with optional manual workflow execution.

GitHub Actions scheduled runs may still experience slight delays depending on platform load, so the project uses source generated time, `checked_at_utc`, and snapshot timestamps for observation ordering.

---

## Current Capabilities

The project currently supports:

- scheduled DAC Testnet enode monitoring
- manual GitHub Actions workflow execution
- email notifications for meaningful changes
- structured latest-state tracking
- automated JSON snapshot preservation
- manual pre-watcher backfill preservation
- added / removed / unchanged enode detection
- target port monitoring
- deterministic change severity classification
- deterministic AI-style summary output
- rotation intelligence across manual and automated observations
- anomaly signal detection
- provider / ASN hint enrichment
- live ASN lookup with cache fallback
- DAC Infrastructure Signal inference
- provider concentration risk summary
- automated Markdown technical report generation
- static dashboard visualization
- dashboard charts
- dashboard export links
- browser-generated custom range exports
- fixed Markdown, JSON, and optional PDF report generation

---

## Architecture / Data Flow Topology

Current v1.9.3 topology:

    Official DAC Enode Source
    https://enodes.dachain.tech/testnet/
            │
            ▼
    watcher.py
    - fetch official enode page
    - parse current enode list
    - detect added / removed / unchanged enodes
    - detect target port changes
    - classify change severity
    - generate deterministic summary
    - send email notification
    - update latest.json
    - create snapshot when meaningful change is detected
            │
            ▼
    data/latest.json
    data/snapshots/*.json
            │
            ▼
    build_rotation_intelligence.py
    - combine manual backfill snapshots
    - combine automated watcher snapshots
    - calculate observation timeline
    - detect persistent enodes and IPs
    - enrich with provider hints
    - enrich with live ASN lookup
    - enrich with DAC Infrastructure Signal
            │
            ├── provider_hints.py
            ├── asn_lookup.py
            └── dac_signal_hints.py
            │
            ▼
    data/rotation-intelligence-summary.json
            │
            ├──────────────────────────────┐
            ▼                              ▼
    build_anomaly_detection.py       build_concentration_risk.py
    - scan observation timeline      - read provider / ASN signals
    - detect large count drops       - read live ASN concentration
    - detect high removal events     - read DAC signal distribution
    - detect aggressive rotation     - calculate concentration label
    - detect target port anomalies   - generate report-ready summary
            │                              │
            ▼                              ▼
    data/anomaly-detection-summary.json    data/concentration-risk-summary.json
            │                              │
            └──────────────┬───────────────┘
                           ▼
    generate_technical_report.py
    - generate full Markdown technical report
                           │
                           ▼
    reports/generated/dac-enode-intelligence-report.md
                           │
                           ├────────────────────────────────────────────┐
                           ▼                                            ▼
    generate_custom_report.py                              dashboard/index.html
    - generate 7D Markdown + JSON                           - latest state
    - generate 30D Markdown + JSON                          - charts
    - generate ALL TIME Markdown + JSON                     - tables
                           │                                - export links
                           ▼                                - custom browser export
    reports/generated/custom/*.md
    reports/generated/custom/*.json
                           │
                           ▼
    generate_pdf_report.py
    - generate optional fixed PDF reports from Markdown
                           │
                           ▼
    reports/generated/custom/*.pdf

GitHub Actions automation:

    .github/workflows/dac-enode-watcher.yml
            │
            ▼
    Scheduled every 15 minutes + manual run
            │
            ▼
    watcher.py
    build_rotation_intelligence.py
    build_anomaly_detection.py
    build_concentration_risk.py
    generate_technical_report.py
    generate_custom_report.py --range 7d --format both
    generate_custom_report.py --range 30d --format both
    generate_custom_report.py --range all --format both
    generate_pdf_report.py --range 7d
    generate_pdf_report.py --range 30d
    generate_pdf_report.py --range all
            │
            ▼
    Commit generated outputs only when files change

---

## Observation Phases

This project separates historical and automated observations into two phases.

    Phase 1 — Manual Observation / Pre-Watcher Backfill
    May 15–31, 2026
    data/manual-backfill/

    Phase 2 — Automated Watcher Observation
    June 1, 2026 onward
    data/latest.json
    data/snapshots/

This separation keeps the dataset clear and prevents historical manual data from overwriting active watcher state.

---

## Generated Outputs

Active watcher output:

    data/latest.json
    data/snapshots/*.json

Manual backfill output:

    manual-archive/
    data/manual-backfill/
    data/manual-backfill/manual-backfill-summary.json

Intelligence summaries:

    data/rotation-intelligence-summary.json
    data/anomaly-detection-summary.json
    data/concentration-risk-summary.json
    data/asn-cache.json

Generated technical report:

    reports/generated/dac-enode-intelligence-report.md

Custom report exports:

    reports/generated/custom/dac-enode-report-7d.md
    reports/generated/custom/dac-enode-report-30d.md
    reports/generated/custom/dac-enode-report-all.md

    reports/generated/custom/dac-enode-report-7d.json
    reports/generated/custom/dac-enode-report-30d.json
    reports/generated/custom/dac-enode-report-all.json

    reports/generated/custom/dac-enode-report-7d.pdf
    reports/generated/custom/dac-enode-report-30d.pdf
    reports/generated/custom/dac-enode-report-all.pdf

---

## Intelligence Layers

### Change Detection

The watcher compares the current official enode list against `data/latest.json`.

It tracks:

- added enodes
- removed enodes
- unchanged enodes
- target port changes
- previous and current totals
- source generated timestamp
- watcher check timestamp

A new automated snapshot is created only when meaningful change is detected.

### Change Severity Classification

Each meaningful change is classified deterministically:

- `INFO`
- `NONE`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

This helps separate minor peer refreshes from major rotation or abnormal conditions.

### AI-Style Summary Layer

The project includes a deterministic summary layer.

It is not a machine learning model.

It turns raw change data into human-readable summaries, technical impact notes, and recommended actions.

### Rotation Intelligence

Generated by:

    build_rotation_intelligence.py

Output:

    data/rotation-intelligence-summary.json

This layer combines manual backfill and automated watcher snapshots into a single observation timeline.

It supports:

- observation timeline analysis
- persistent enode detection
- persistent IP detection
- provider / ASN enrichment
- DAC Infrastructure Signal enrichment
- report-ready summaries

### Anomaly Detection

Generated by:

    build_anomaly_detection.py

Output:

    data/anomaly-detection-summary.json

Current anomaly rules include:

- `NO_ENODES_DETECTED`
- `UNEXPECTED_TARGET_PORT`
- `SHARP_ENODE_COUNT_DROP`
- `LARGE_ENODE_COUNT_DROP`
- `HIGH_REMOVAL_EVENT`
- `AGGRESSIVE_ROTATION`
- `MODERATE_ROTATION_SPIKE`
- `LOW_CONTINUITY_RATIO`
- `WATCHER_HIGH_SEVERITY_SIGNAL`

This layer marks observations as review candidates. It does not automatically conclude that the network is unhealthy.

### Provider / ASN Hint Layer

Generated by:

    provider_hints.py

This is a static heuristic enrichment layer.

It provides:

- `provider_guess`
- `asn_hint`
- `provider_type`
- `country_hint`
- `provider_confidence`
- `provider_detection_method`

Unknown values are intentionally preserved when no static prefix matches.

### Live ASN Lookup Layer

Generated by:

    asn_lookup.py

Cache file:

    data/asn-cache.json

This layer enriches observed IPs with live routing data from Team Cymru WHOIS lookup.

It is workflow-safe:

- cache-aware
- optional
- fallback-safe
- not treated as official ownership evidence

Environment control:

    DAC_LIVE_ASN_LOOKUP=1    enable live lookup
    DAC_LIVE_ASN_LOOKUP=0    disable live lookup

### DAC Infrastructure Signal Layer

Generated by:

    dac_signal_hints.py

This community inference layer uses:

- registry history
- peer identity hints
- persistence / survivorship
- subnet patterns
- provider hints
- manual technical report evidence

Example labels:

- `Authority-like Core Signal`
- `Relay-like DAC Node Signal`
- `Internal RPC-like Signal`
- `Community VPS-like Signal`
- `Community Node Signal`
- `Legacy Relay-like Signal`
- `Unlisted Active Peer Signal`
- `Retained Infrastructure Signal`
- `Core Subnet Historical Signal`
- `Unknown / No Signal`

Important: this is not an official DAC classification.

### Provider Concentration Risk

Generated by:

    build_concentration_risk.py

Output:

    data/concentration-risk-summary.json

The current model checks concentration across:

- live ASN
- live ASN name
- live country
- static provider hint
- static ASN hint
- DAC Infrastructure Signal

Risk labels:

- `LOW`
- `MODERATE`
- `ELEVATED`
- `HIGH`
- `INCONCLUSIVE`

---

## Dashboard

Dashboard file:

    dashboard/index.html

Preview locally:

    python3 -m http.server 8090

Open:

    http://localhost:8090/dashboard/

The dashboard should be opened through a local HTTP server or GitHub Pages, not directly through `file://`, because it loads JSON data using `fetch()`.

### Dashboard views

The dashboard includes:

- latest watcher state
- deterministic summary output
- anomaly summary
- report-ready summary
- provider / ASN summary
- live ASN summary
- DAC Infrastructure Signal summary
- provider concentration summary
- persistent enode and IP tables
- detected anomaly events
- observation timeline

### Dashboard charts

Current charts:

- Enode Count Over Time
- Added vs Removed Per Observation
- Live ASN Distribution
- DAC Infrastructure Signal Distribution
- Anomaly Severity Count
- Manual vs Automated Observations

Chart controls:

- `7D`
- `30D`
- `ALL TIME`

The timeline uses readable source timestamps with 24-hour hints to avoid AM/PM ambiguity.

### Dashboard exports

Static dashboard links:

- 7D / 30D / ALL TIME Markdown
- 7D / 30D / ALL TIME JSON
- 7D / 30D / ALL TIME PDF

Custom browser export:

- From observation
- To observation
- Download Custom Markdown
- Download Custom JSON
- Print / Save Custom PDF

Custom browser exports run locally in the browser and are not committed back to the repository.

---

## Report Export Stack

Markdown and JSON are the primary reusable formats.

PDF is optional final packaging.

### Markdown export

Generated by:

    generate_custom_report.py

Commands:

    python generate_custom_report.py --range 7d
    python generate_custom_report.py --range 30d
    python generate_custom_report.py --range all

### JSON export

Commands:

    python generate_custom_report.py --range 7d --format json
    python generate_custom_report.py --range 30d --format json
    python generate_custom_report.py --range all --format json

Generate both Markdown and JSON:

    python generate_custom_report.py --range 7d --format both
    python generate_custom_report.py --range 30d --format both
    python generate_custom_report.py --range all --format both

### PDF export

Generated by:

    generate_pdf_report.py

Dependency:

    reportlab

Commands:

    python generate_pdf_report.py --range 7d
    python generate_pdf_report.py --range 30d
    python generate_pdf_report.py --range all

---

## GitHub Actions Automation

Workflow file:

    .github/workflows/dac-enode-watcher.yml

Schedule:

    cron: "*/15 * * * *"

The workflow can also be triggered manually from the GitHub Actions tab.

Current pipeline:

    watcher.py
    build_rotation_intelligence.py
    build_anomaly_detection.py
    build_concentration_risk.py
    generate_technical_report.py
    generate_custom_report.py --range 7d --format both
    generate_custom_report.py --range 30d --format both
    generate_custom_report.py --range all --format both
    generate_pdf_report.py --range 7d
    generate_pdf_report.py --range 30d
    generate_pdf_report.py --range all

Generated outputs are committed only when files change.

---

## Local Usage

Install dependencies:

    pip install -r requirements.txt

Run the watcher manually:

    python watcher.py

Rebuild intelligence summaries:

    python build_rotation_intelligence.py
    python build_anomaly_detection.py
    python build_concentration_risk.py

Generate the main technical report:

    python generate_technical_report.py

Generate custom reports:

    python generate_custom_report.py --range 7d --format both
    python generate_custom_report.py --range 30d --format both
    python generate_custom_report.py --range all --format both

Generate optional PDFs:

    python generate_pdf_report.py --range 7d
    python generate_pdf_report.py --range 30d
    python generate_pdf_report.py --range all

Preview dashboard:

    python3 -m http.server 8090

Then open:

    http://localhost:8090/dashboard/

---

## Current Generated State

Latest source time:

    Wed Jun 3 12:00:02 PM CEST 2026

Latest watcher check:

    2026-06-03T10:23:29.960579+00:00

Latest observed state:

    Current enodes: 10
    Added: 0
    Removed: 4
    Unchanged: 10
    Target port: 28657

Current observation scope:

    Total observations: 22
    Manual backfill observations: 14
    Automated watcher observations: 8
    First observation: Fri May 15 12:00:01 AM CEST 2026
    Latest observation: Wed Jun 3 12:00:02 PM CEST 2026

Current anomaly summary:

    Anomaly signals: 5
    Highest severity: HIGH
    Severity counts: HIGH = 5
    Detected types: LARGE_ENODE_COUNT_DROP, HIGH_REMOVAL_EVENT, AGGRESSIVE_ROTATION

Current concentration summary:

    Overall label: ELEVATED
    Top live ASN: AS51167
    Top live ASN share: 51.72%
    Top live country: DE
    Top live country share: 62.07%

Current custom report outputs:

    Markdown reports: 3
    JSON summaries: 3
    PDF reports: 3

---

## Version History

| Version | Summary |
|---|---|
| v1.0 | Automated enode watcher with email notification and JSON snapshots |
| v1.1 | Deterministic change severity classification |
| v1.2 | AI-style deterministic summary layer |
| v1.3 | Enode rotation intelligence from manual + automated observations |
| v1.4 | Rule-based anomaly detection layer |
| v1.5 | Automated Markdown technical report generator |
| v1.6 | Static dashboard layer |
| v1.6.1 | Static Provider / ASN Hint Layer |
| v1.6.2 | DAC Infrastructure Signal Layer |
| v1.6.3 | Optional Live ASN Lookup Layer |
| v1.7 | Provider Concentration / Decentralization Risk Summary |
| v1.8.0 | Core dashboard chart layer |
| v1.8.1 | Distribution dashboard chart layer |
| v1.8.2 | Summary dashboard chart layer |
| v1.9.0 | Custom Markdown report export |
| v1.9.1 | Custom JSON report summary export |
| v1.9.2 | Dashboard export links and custom range export |
| v1.9.3 | Optional PDF export |

---

## Future Upgrade Direction

The current export roadmap is complete through v1.9.3.

Future optional upgrades may include:

- public RPC health monitoring
- explorer availability monitoring
- multi-source DAC infrastructure watcher
- richer dashboard filtering
- richer report templates
- automated comparison between observation windows

---

## Security Notes

Do not commit email passwords, SMTP credentials, `.env` files, or tokens.

The project `.gitignore` excludes:

- `venv/`
- `__pycache__/`
- `*.pyc`
- `.env`
- broad generated JSON patterns unless explicitly force-added where needed

Watcher-generated data files under `data/` are intentionally tracked for technical observation history.

Manual backfill data under `data/manual-backfill/` is also intentionally tracked because it preserves historical pre-watcher observations.

---

## Disclaimer

This is an independent community-built observation tool.

It is not an official DAC tool and does not represent official DAC infrastructure policy.

The watcher observes publicly available enode data and stores snapshots for technical reporting purposes.

Provider, ASN, DAC Infrastructure Signal, and concentration labels are observation-based heuristics. They should not be treated as official DAC node ownership, official DAC classification, or definitive decentralization measurement.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
