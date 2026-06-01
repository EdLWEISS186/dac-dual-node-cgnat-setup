# DAC Enode Intelligence Watcher

Community-built observation tool by **JERUZZALEM — DAC Infra Tester**.

This project monitors the official DAC Testnet public enode page:

https://enodes.dachain.tech/testnet/

It automatically observes the official enode list, captures structured data, analyzes changes, sends email notifications, and stores historical JSON snapshots inside this repository.

---

## Background

This project was created as a continuation of the previous technical report:

[5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation](../../Testnet_%28Inception%29_Technical_Reports/5.%20Official%20Enode%20Evolution%20Analysis%20%E2%80%94%20Infrastructure%20Rotation%20%26%20Network%20Maturation.pdf)

That report analyzed the evolution of DAC official enodes as an infrastructure signal, focusing on peer rotation, network maturation, and bootstrap-node behavior over time.

The original report was based on manual observation and point-in-time analysis.

**DAC Enode Intelligence Watcher** extends that work into a continuous observation system.

Instead of manually checking the official enode page and risking missed updates, this watcher automatically captures each meaningful change and preserves it as structured historical data.

---

## Manual Observation Challenge

Before this watcher was created, the official DAC enode list was observed manually by saving screenshots and text files from the public enode page.

This method worked for point-in-time documentation, but it was difficult to follow up consistently because the official enode page can update over time and previous states are no longer visible once the page changes.

As shown below, some observations were successfully captured, while some days could be missed due to manual workload, timing, or limited availability.

![Manual DAC enode observation was difficult to follow up consistently](assets/HardToFollowUp.png)

This is the main reason why **DAC Enode Intelligence Watcher** was created.

The watcher turns manual observation into an automated process by continuously checking the official source, extracting structured enode data, comparing it with the previous snapshot, and preserving meaningful changes as JSON evidence.

Instead of relying only on screenshots and manual text files, the project now creates a repeatable observation pipeline:

    Manual observation
            ↓
    Risk of missed updates
            ↓
    Automated watcher
            ↓
    Structured JSON snapshots
            ↓
    Email result and technical evidence

This allows future enode evolution analysis to be based on more consistent historical data.

---

## Purpose

The purpose of this project is not only to send notifications.

The main purpose is to support a technical observation workflow:

    Observe official source
            ↓
    Collect structured enode data
            ↓
    Analyze infrastructure-level changes
            ↓
    Generate result
            ↓
    Store evidence and notify the observer

The watcher helps preserve historical evidence by recording:

- current official enode list
- newly added enodes
- removed enodes
- unchanged enodes
- target P2P port
- target port changes
- change severity
- severity reason
- AI-style summary
- technical impact
- recommended action
- source generated timestamp
- watcher check timestamp
- structured JSON snapshots for later review

This makes the observation process more consistent, repeatable, and useful for future technical reports.

---

## Why This Matters

Official enode changes can reflect infrastructure-level activity such as:

- bootstrap peer rotation
- network maintenance
- public peer refresh
- node replacement
- infrastructure scaling
- testnet maturation
- target port consistency or migration
- abnormal peer-list reduction
- large infrastructure rotation events

A single manual observation may miss these changes.

By storing historical snapshots, this project makes it possible to review how the official enode list evolves over time.

---

## Observation Phases

This project now contains two observation phases.

    Phase 1 — Manual Observation / Pre-Watcher Backfill
    May 15–31, 2026
    data/manual-backfill/

    Phase 2 — Automated Watcher Observation
    June 1, 2026 onward
    data/latest.json
    data/snapshots/

The manual phase preserves historical data collected before the watcher existed.

The automated phase continues the observation process using GitHub Actions, structured JSON snapshots, change classification, AI-style summaries, and email notifications.

This separation makes the dataset clearer and prevents old manual data from interfering with the active watcher state.

---

## Monitoring Target

Target page:

    https://enodes.dachain.tech/testnet/

Observed source format:

    Generated: Mon Jun 1 12:00:01 AM CEST 2026 | Target Port: 28657

    admin.addPeer("enode://...@IP:28657");

---

## Output Files

The watcher stores active automated observation data in:

    data/latest.json
    data/snapshots/

Additional historical/manual data is stored in:

    manual-archive/
    data/manual-backfill/

### `data/latest.json`

Contains the latest observed state from the automated watcher.

This file acts as the comparison baseline for the next scheduled automated check.

The manual backfill data does not replace or modify `latest.json`.

### `data/snapshots/*.json`

Contains automated watcher snapshots created when:

- the watcher runs for the first time
- new enodes are added
- existing enodes are removed
- the target port changes

Automated snapshots also include the current intelligence fields:

- `change_severity`
- `severity_reason`
- `ai_style_summary`
- `technical_impact`
- `recommended_action`

### `manual-archive/`

Contains the original raw manual observation file:

    manual-archive/Old Data Before Intelligence Watcher Created.txt

This file preserves the original pre-watcher data exactly as collected manually.

### `data/manual-backfill/`

Contains structured JSON snapshots generated from the manual archive.

These files are historical backfill data and are intentionally separated from automated watcher snapshots.

### `data/manual-backfill/manual-backfill-summary.json`

Contains a summary of the manual observation period, including:

- total manual snapshots
- first and last manual observation timestamp
- observed target ports
- unique enode count
- minimum and maximum enode count
- list of manual snapshot files

---

## Manual Backfill Dataset

Before the automated watcher was created, several official DAC enode snapshots had already been collected manually.

Instead of discarding that historical data, the manual observations were preserved and converted into structured JSON backfill data.

This backfill dataset represents the **pre-watcher manual observation period**.

    Manual observation period:
    May 15–31, 2026

The current manual backfill contains:

- 14 manually captured snapshots
- 28 unique enodes observed
- target port observed: `28657`
- first manual snapshot: `Fri May 15 12:00:01 AM CEST 2026`
- last manual snapshot: `Sun May 31 12:00:02 PM CEST 2026`

This dataset is intentionally labeled as a **partial manual archive**.

Missing dates represent missed observation windows, not confirmed absence of infrastructure changes.

---

## Manual Backfill Parser

The parser used to convert the raw manual archive into structured JSON is stored in:

    parse_manual_backfill.py

The parser reads the raw manual archive, extracts each `Generated:` block, parses enode entries, compares each manual snapshot against the previous manual snapshot, and generates structured JSON files.

It tracks:

- manual snapshot index
- source type
- source file
- observation completeness
- data gap note
- generated timestamp from source
- generated date
- generated time
- generated timezone
- target port
- previous target port
- current target port
- target port change status
- previous enode total
- current enode total
- added enodes
- removed enodes
- unchanged enodes
- parsed enode details
- `admin.addPeer(...)` lines
- snapshot file path

This keeps the old manual data compatible with the newer watcher snapshot format while clearly separating manual historical backfill from automated watcher output.

---

## Change Detection Logic

The watcher compares the current official enode list against the previous `latest.json`.

It tracks:

- `added`
- `removed`
- `unchanged`
- `target_port_changed`
- `previous_target_port`
- `current_target_port`

If no enode or target-port change is detected, no new automated snapshot is created.

This prevents unnecessary noise while preserving meaningful infrastructure changes.

---

## Change Severity Classification

The watcher now includes a deterministic severity classification layer.

Each meaningful change is classified into one of the following categories:

- `INFO` — initial baseline snapshot
- `NONE` — no enode or target-port change detected
- `LOW` — small enode rotation
- `MEDIUM` — moderate enode rotation
- `HIGH` — large enode rotation or target port change
- `CRITICAL` — no enodes detected or sharp enode count drop

The generated snapshot includes:

- `change_severity`
- `severity_reason`

Example:

    {
      "change_severity": "LOW",
      "severity_reason": "Small enode rotation detected: 1 added and 0 removed."
    }

This helps future technical reports distinguish between minor peer refreshes, major bootstrap rotation, target-port changes, and possible abnormal states.

---

## AI-Style Summary Layer

The watcher also generates an AI-style interpretation layer.

This is not a machine learning model.

It is a deterministic summary system that converts raw technical changes into human-readable observation output.

Each changed snapshot includes:

- `ai_style_summary`
- `technical_impact`
- `recommended_action`

The AI-style summary may explain:

- whether the change looks like a small peer refresh
- whether the update may indicate infrastructure rotation
- whether the target port changed
- what the possible technical impact is
- what action a node runner or observer may take

Example output:

    DAC official enode list changed: 1 enodes added, 0 removed, and 12 remained unchanged.
    Current total: 13 enodes.

    Rotation interpretation:
    Small bootstrap peer rotation detected.

    Technical impact:
    This appears to be a minor peer-list refresh.

    Recommended action:
    No urgent action is required, but the snapshot is preserved for history.

This makes the watcher more useful for technical observation because the output is not only raw data, but also structured interpretation.

---

## GitHub Actions Schedule

The watcher is executed by GitHub Actions every 3 hours:

    cron: "0 */3 * * *"

It can also be triggered manually from the GitHub Actions tab.

---

## Email Notification

When a meaningful change is detected, the watcher sends an email notification containing:

- source URL
- generated time from the official source page
- checked timestamp in UTC
- previous total enode count
- current total enode count
- added enodes
- removed enodes
- unchanged enodes
- target port status
- change severity
- severity reason
- AI-style summary
- rotation interpretation
- technical impact
- recommended action
- snapshot file path

Email credentials are stored securely using GitHub Actions repository secrets.

Required secrets:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`
- `EMAIL_FROM`
- `EMAIL_TO`

---

## Current Intelligence Layer

The current intelligence layer is deterministic and rule-based.

It does not rely on a machine learning model.

The watcher performs structured infrastructure observation by:

- extracting official enode data
- parsing node ID, IP, and port
- comparing the current state with the previous snapshot
- classifying enodes as added, removed, or unchanged
- detecting target port changes
- classifying change severity
- generating severity reasons
- generating AI-style summaries
- generating technical impact notes
- generating recommended actions
- producing structured output for technical reporting

This makes the system suitable for infrastructure monitoring, evidence preservation, and future report preparation.

---

## Current Status

The current version already supports:

- official DAC enode page monitoring
- scheduled GitHub Actions execution every 3 hours
- manual workflow execution
- email notification
- JSON snapshot generation
- latest state tracking
- historical automated snapshot preservation
- manual pre-watcher backfill preservation
- added, removed, and unchanged enode classification
- target port change detection
- raw manual archive preservation
- manual archive parsing into structured JSON
- change severity classification
- severity reason generation
- AI-style summary generation
- technical impact generation
- recommended action generation

---

## Version Notes

### v1.0 — Automated Enode Watcher

Initial working version.

Features:

- monitor official DAC enode page
- detect added, removed, and unchanged enodes
- detect target port changes
- send email notification
- generate JSON snapshots
- commit snapshot data through GitHub Actions

### v1.1 — Change Severity Classification

Added deterministic classification for enode changes.

New fields:

- `change_severity`
- `severity_reason`

Severity levels:

- `INFO`
- `NONE`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

### v1.2 — AI-Style Summary Layer

Added human-readable interpretation output for each meaningful change.

New fields:

- `ai_style_summary`
- `technical_impact`
- `recommended_action`

This improves the watcher from a raw monitoring bot into a more useful infrastructure observation assistant.

---

## Future Upgrade Direction

Future versions may extend this watcher into a broader infrastructure intelligence system.

Possible upgrades include:

- anomaly detection
- enode rotation pattern analysis
- public RPC health monitoring
- explorer availability monitoring
- infrastructure status dashboard
- automated technical report draft generation
- multi-source DAC Testnet infrastructure watcher

These upgrades are optional and will depend on future observation needs.

---

## Security Notes

Do not commit email passwords, SMTP credentials, `.env` files, or tokens.

The project `.gitignore` excludes:

- `venv/`
- `__pycache__/`
- `*.pyc`
- `.env`

Watcher-generated JSON files under `data/` are intentionally tracked for technical observation history.

Manual backfill JSON files under `data/manual-backfill/` are also intentionally tracked because they preserve historical pre-watcher observations.

---

## Disclaimer

This is an independent community-built observation tool.

It is not an official DAC Labs tool and does not represent official DAC infrastructure policy.

The watcher only observes publicly available enode data and stores snapshots for technical reporting purposes.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
