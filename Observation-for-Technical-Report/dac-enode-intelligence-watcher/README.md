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

```text
Manual observation
        ↓
Risk of missed updates
        ↓
Automated watcher
        ↓
Structured JSON snapshots
        ↓
Email result and technical evidence
```

This allows future enode evolution analysis to be based on more consistent historical data.

---

## Purpose

The purpose of this project is not only to send notifications.

The main purpose is to support a technical observation workflow:

```text
Observe official source
        ↓
Collect structured enode data
        ↓
Analyze infrastructure-level changes
        ↓
Generate result
        ↓
Store evidence and notify the observer
```

The watcher helps preserve historical evidence by recording:

* current official enode list
* newly added enodes
* removed enodes
* unchanged enodes
* target P2P port
* target port changes
* source generated timestamp
* watcher check timestamp
* structured JSON snapshots for later review

This makes the observation process more consistent, repeatable, and useful for future technical reports.

---

## Why This Matters

Official enode changes can reflect infrastructure-level activity such as:

* bootstrap peer rotation
* network maintenance
* public peer refresh
* node replacement
* infrastructure scaling
* testnet maturation
* target port consistency or migration

A single manual observation may miss these changes.

By storing historical snapshots, this project makes it possible to review how the official enode list evolves over time.

---

## Monitoring Target

Target page:

```text
https://enodes.dachain.tech/testnet/
```

Observed source format:

```text
Generated: Mon Jun 1 12:00:01 AM CEST 2026 | Target Port: 28657

admin.addPeer("enode://...@IP:28657");
```

---

## Output Files

The watcher stores data in:

```text
data/latest.json
data/snapshots/
```

### `latest.json`

Contains the latest observed state.

This file acts as the comparison baseline for the next scheduled check.

### `data/snapshots/*.json`

Contains historical snapshots created when:

* the watcher runs for the first time
* new enodes are added
* existing enodes are removed
* the target port changes

These snapshots provide a historical record for future infrastructure analysis.

---

## Change Detection Logic

The watcher compares the current official enode list against the previous `latest.json`.

It tracks:

```text
added
removed
unchanged
target_port_changed
previous_target_port
current_target_port
```

If no enode or target-port change is detected, no new snapshot is created.

This prevents unnecessary noise while preserving meaningful infrastructure changes.

---

## GitHub Actions Schedule

The watcher is executed by GitHub Actions every 3 hours:

```yaml
cron: "0 */3 * * *"
```

It can also be triggered manually from the GitHub Actions tab.

---

## Email Notification

When a meaningful change is detected, the watcher sends an email notification containing:

* source URL
* generated time from the official source page
* checked timestamp in UTC
* previous total enode count
* current total enode count
* added enodes
* removed enodes
* unchanged enodes
* target port status
* snapshot file path

Email credentials are stored securely using GitHub Actions repository secrets.

Required secrets:

```text
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASS
EMAIL_FROM
EMAIL_TO
```

---

## Current Intelligence Layer

In the current version, the intelligence layer is deterministic and rule-based.

It does not rely on a machine learning model.

The watcher performs structured infrastructure observation by:

* extracting official enode data
* parsing node ID, IP, and port
* comparing the current state with the previous snapshot
* classifying enodes as added, removed, or unchanged
* detecting target port changes
* generating structured output for reporting

This makes the system suitable for technical monitoring and evidence preservation.

---

## Current Status

The current version already supports:

* official DAC enode page monitoring
* scheduled GitHub Actions execution every 3 hours
* manual workflow execution
* email notification
* JSON snapshot generation
* latest state tracking
* historical snapshot preservation
* added, removed, and unchanged enode classification
* target port change detection

---

## Future Upgrade Direction

Future versions may extend this watcher into a broader infrastructure intelligence system.

Possible upgrades include:

* change severity classification
* AI-assisted summary generation
* anomaly detection
* enode rotation pattern analysis
* public RPC health monitoring
* explorer availability monitoring
* infrastructure status dashboard
* automated technical report draft generation

These upgrades are optional and will depend on future observation needs.

---

## Security Notes

Do not commit email passwords, SMTP credentials, `.env` files, or tokens.

The project `.gitignore` excludes:

```text
venv/
__pycache__/
*.pyc
.env
```

Watcher-generated JSON files under `data/` are intentionally tracked for technical observation history.

---

## Disclaimer

This is an independent community-built observation tool.

It is not an official DAC Labs tool and does not represent official DAC infrastructure policy.

The watcher only observes publicly available enode data and stores snapshots for technical reporting purposes.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
