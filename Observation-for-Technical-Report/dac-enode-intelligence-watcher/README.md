# DAC Enode Intelligence Watcher

Community-built observation tool by **JERUZZALEM — DAC Infra Tester**.

This project monitors the official DAC Testnet public enode page:

https://enodes.dachain.tech/testnet/

It automatically checks the official enode list, detects infrastructure-level changes, sends email notifications, and stores historical JSON snapshots inside this repository.

---

## Purpose

The DAC official public enode list may change over time. Because the page can update periodically, manual observation can miss previous states.

This watcher helps preserve historical evidence by recording:

- current official enode list
- newly added enodes
- removed enodes
- unchanged enodes
- target P2P port
- source generated timestamp
- watcher check timestamp

This is intended for technical observation and future reporting, not for modifying the DAC network.

---

## Monitoring Target

Target page:

    https://enodes.dachain.tech/testnet/

Observed source format:

    Generated: Mon Jun 1 12:00:01 AM CEST 2026 | Target Port: 28657

    admin.addPeer("enode://...@IP:28657");

---

## Output Files

The watcher stores data in:

    data/latest.json
    data/snapshots/

### latest.json

Contains the latest observed state.

### data/snapshots/*.json

Contains historical snapshots created when:

- the watcher runs for the first time
- new enodes are added
- existing enodes are removed
- the target port changes

---

## Change Detection Logic

The watcher compares the current official enode list against the previous `latest.json`.

It tracks:

- added
- removed
- unchanged
- target_port_changed
- previous_target_port
- current_target_port

If no enode or target-port change is detected, no new snapshot is created.

---

## GitHub Actions Schedule

The watcher is executed by GitHub Actions every 3 hours:

    cron: "0 */3 * * *"

It can also be triggered manually from the GitHub Actions tab.

---

## Email Notification

When a change is detected, the watcher sends an email notification containing:

- source URL
- generated time from source page
- checked timestamp in UTC
- previous total enode count
- current total enode count
- added enodes
- removed enodes
- unchanged enodes
- target port status
- snapshot file path

Email credentials are stored securely using GitHub Actions repository secrets.

Required secrets:

- SMTP_HOST
- SMTP_PORT
- SMTP_USER
- SMTP_PASS
- EMAIL_FROM
- EMAIL_TO

---

## Security Notes

Do not commit email passwords, SMTP credentials, `.env` files, or tokens.

The project `.gitignore` excludes:

- venv/
- __pycache__/
- *.pyc
- .env

Watcher-generated JSON files under `data/` are intentionally tracked for technical observation history.

---

## Disclaimer

This is an independent community-built observation tool.

It is not an official DAC Labs tool and does not represent official DAC infrastructure policy. The watcher only observes publicly available enode data and stores snapshots for technical reporting purposes.

---

## Maintainer

**JERUZZALEM — DAC Infra Tester**
