# Archive Note — DAC Domain v1 Explorer-Friendly Registry

**Project:** DAC Domain  
**Version:** v1.0.0 — Explorer-Friendly Registry  
**Repository Path:** `DAC-Domain/`  
**Date:** June 5, 2026  
**Network:** DAC Testnet  
**Chain ID:** `21894` / `0x5586`  
**Local RPC Used:** `http://127.0.0.1:8546`  
**TLD:** `.dac`  
**Native Currency:** DACC  

## Summary

DAC Domain v1 was developed after the v0.5 archived prototype proved that a `.dac` registry could function on DAC Testnet.

The purpose of v1 was to improve event readability for explorer logs, technical reporting, and possible future indexing. v0.5 was functionally valid, but its event schema used indexed string values, which are less readable in logs because dynamic indexed values are represented as hashes.

v1 keeps the same registry concept but improves event design by emitting both:

```text
bytes32 indexed nameHash
string name
```

This allows `.dac` names to remain filterable while also being readable as plain event data.

## v1 Contract

```text
Contract: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Deployment TX: 0x4e3ab77b099bb7e2149f17dc9465e5e760c0d3dd96790df11aafce482eeb1c90
Block: 14960256
Deployer: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Nonce: 2631
Gas Price: 100 gwei
```

Local node deployment log:

```text
INFO [06-05|22:57:42.429] Submitted contract creation
hash=0x4e3ab77b099bb7e2149f17dc9465e5e760c0d3dd96790df11aafce482eeb1c90
from=0x870ad63acc507cdfd878F170606d19ae78988AFE
nonce=2631
contract=0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
value=0
```

The recurring `hardhat_metadata` warning remained non-fatal because DAC Testnet local RPC is not a Hardhat network.

## Contract Verification

The v1 contract was verified through direct RPC and ABI reads.

Validation result:

```text
Version: v1.0.0-explorer-friendly
Contract: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Code exists: true
TLD: .dac
Price 1 year: 5.0 DACC
Price 2 years: 8.0 DACC
Price 3 years: 10.0 DACC
NameHash jeruzzalem.dac: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
```

## Domain Registration Test

`jeruzzalem.dac` was registered again on the v1 registry.

```text
Registration TX: 0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce
From: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Value: 5 DACC
Nonce: 2632
```

Local node log:

```text
INFO [06-05|23:26:03.296] Submitted transaction
hash=0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce
from=0x870ad63acc507cdfd878F170606d19ae78988AFE
nonce=2632
recipient=0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
value=5,000,000,000,000,000,000
```

Resolve result:

```text
Resolving .dac domain...
Domain: jeruzzalem.dac
Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Target: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Registered At: 2026-06-05T16:26:17.000Z
Updated At: 2026-06-05T16:26:17.000Z
Expires At: 2027-06-05T16:26:17.000Z
Registration Years: 1
Active: true
```

## Primary Domain Test

The registered domain was set as primary.

```text
Primary Domain TX: 0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a
From: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Nonce: 2633
```

Local node log:

```text
INFO [06-05|23:27:01.094] Submitted transaction
hash=0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a
from=0x870ad63acc507cdfd878F170606d19ae78988AFE
nonce=2633
recipient=0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
value=0
```

## Event Decode Validation

A reproducible event decoder was added:

```text
scripts/decode-events.js
```

Package script:

```text
npm run decode-events:dac
```

Validation command:

```bash
npm run decode-events:dac -- \
  0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce \
  0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a
```

Decoded registration event:

```text
Event: DomainRegistered
nameHash: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
name: jeruzzalem.dac
owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
target: 0x870ad63acc507cdfd878F170606d19ae78988AFE
registrationYears: 1
expiresAt: 1812212777
pricePaid: 5000000000000000000
timestamp: 1780676777
```

Decoded primary-domain event:

```text
Event: PrimaryDomainSet
owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
nameHash: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
name: jeruzzalem.dac
timestamp: 1780676837
```

## v1 Result

v1 successfully achieved the main improvement over v0.5:

```text
v0.5 = functional .dac registry
v1   = functional .dac registry + readable domain event data
```

The domain name `jeruzzalem.dac` is now present as readable event data in decoded logs.

This does not automatically make DAC Explorer replace wallet addresses with `.dac` names across all transactions. That would require explorer-side name service integration or an indexer. However, v1 provides cleaner data for future indexing, reporting, and observation.

## Report-Use Value

v1 is valuable for the technical report because it documents:

- explorer-friendly smart contract event design
- migration from v0.5 prototype to v1 registry
- successful redeployment on DAC Testnet
- local RPC deployment through a self-hosted DAC node
- `.dac` registration on the v1 registry
- primary domain validation
- reproducible event decoding
- readable domain evidence in event logs
- clear distinction between registry data and explorer-wide name replacement

## Files Added or Updated

```text
contracts/DACDomainRegistry.sol
deployments/dac-testnet.json
scripts/deploy-v1.js
scripts/decode-events.js
scripts/register.js
scripts/resolve.js
scripts/deploy.js
scripts/replace-deploy.js
package.json
package-lock.json
src/app.js
docs/archive/dac-domain-v1-explorer-friendly-archive-note.md
```

## Current Status

```text
v0.5: Archived Prototype
v1: Deployed and validated
Active Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Test Domain: jeruzzalem.dac
Primary Domain: jeruzzalem.dac
```
