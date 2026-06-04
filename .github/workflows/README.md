# GitHub Actions Workflows

This folder contains GitHub Actions workflow definitions for this repository.

GitHub Actions reads workflow files only from:

```
.github/workflows/
```

Workflow files usually use the `.yml` or `.yaml` extension.

---

## Current Workflows

### DAC Enode Watcher

Workflow file:

```
dac-enode-watcher.yml
```

Related project:

[DAC Enode Intelligence Watcher](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Observation-for-Technical-Report/dac-enode-intelligence-watcher)

Purpose:

This workflow powers the automated DAC Enode Intelligence Watcher pipeline.

It runs the watcher on a scheduled interval and rebuilds the generated observation outputs used by the dashboard and technical reports.

Current schedule:

```
*/15 * * * *
```

This means the workflow is scheduled to run every 15 minutes.

The workflow can also be triggered manually from the GitHub Actions tab.

---

## What This Workflow Does

The DAC Enode Watcher workflow currently performs the following steps:

```
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
```

In simple terms, this workflow:

* checks the public DAC Testnet enode source
* detects added, removed, and unchanged enodes
* tracks target port consistency
* updates the latest watcher state
* creates historical JSON snapshots when meaningful changes occur
* rebuilds rotation intelligence summaries
* rebuilds anomaly detection summaries
* rebuilds provider concentration summaries
* regenerates Markdown, JSON, and PDF reports
* updates dashboard data
* commits generated output changes back to the repository when needed

---

## Why This Folder Exists

The `.github/workflows/` folder is a standard GitHub automation folder.

It is not a separate project folder.

It acts as the automation control layer for this repository.

Without this folder, GitHub Actions will not know how to run the scheduled watcher.

The actual watcher project, scripts, dashboard, generated data, and report tools are located here:

[Observation-for-Technical-Report/dac-enode-intelligence-watcher](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Observation-for-Technical-Report/dac-enode-intelligence-watcher)

---

## Additional Workflow

### DAC Infrastructure Intelligence Watcher

Workflow file:

    dac-infrastructure-intelligence-watcher.yml

Related project:

[DAC Infrastructure Intelligence Watcher](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Observation-for-Technical-Report/dac-infrastructure-intelligence-watcher)

Purpose:

This workflow powers the standalone DAC Infrastructure Intelligence Watcher.

It monitors public DAC infrastructure services beyond the official enode registry, including the official public RPC, explorer web frontend, and primary explorer API.

Current schedule:

    */15 * * * *

This means the workflow is scheduled to run every 15 minutes.

The workflow can also be triggered manually from the GitHub Actions tab.

---

## What This Workflow Does

The DAC Infrastructure Intelligence Watcher workflow currently performs the following steps:

    infrastructure_health.py
    generate_health_report.py
    generate_dashboard_data.py

In simple terms, this workflow:

- checks the official DAC public RPC endpoint
- checks JSON-RPC method availability
- checks latest block availability through public RPC
- checks explorer web frontend availability
- checks explorer API reachability
- classifies endpoint-level availability health
- classifies endpoint-level response-time class
- classifies overall infrastructure health
- refreshes `data/latest.json`
- creates health snapshots when endpoint-level health state changes
- regenerates `reports/generated/infrastructure-health-report.md`
- regenerates `dashboard/data/health-dashboard-data.json`
- supports the static dashboard at `dashboard/index.html`
- commits generated output changes back to the repository when needed

The actual watcher project, script, generated data, and future report tools are located here:

[Observation-for-Technical-Report/dac-infrastructure-intelligence-watcher](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Observation-for-Technical-Report/dac-infrastructure-intelligence-watcher)


---

## Important Notes

Do not move `dac-enode-watcher.yml` outside this folder.

Do not move `dac-infrastructure-intelligence-watcher.yml` outside this folder.

If the workflow file is moved to another folder, GitHub Actions will stop detecting it.

Do not commit secrets, passwords, SMTP credentials, or tokens into this folder.

Secrets should be configured through GitHub repository settings.

---

## Maintainer

JERUZZALEM — DAC Infra Tester
