# DAC Wallet Intelligence Layer v1

Client-side wallet intelligence checker for DAC Testnet.

## Flow

User pastes a wallet address, clicks **Check**, and the web app reads public DAC testnet data from:

- `https://exptest.dachain.tech/api` as the primary DAC Explorer source
- `https://rpctest.dachain.tech/` as limited RPC fallback

No wallet connection, no signing, no private key.

## Files

```text
wallet-intelligence.html
wallet-intelligence.css
wallet-intelligence.js
```

## Data modules

Primary Explorer mode reads:

```text
balance     -> Proof of Native Funds
tokenlist   -> Proof of Assets Engine
txlist      -> Activity Analytics
tokennfttx  -> NFT transfer activity
```

Then it generates:

```text
Activity Analytics v1
Portfolio Intelligence v1
Reputation Scoring v1
Wallet Intelligence Layer v1
```

## Failure policy

This app does not generate random or mock wallet scores in production.

```text
Full explorer data   -> full wallet intelligence
Partial explorer data -> partial profile only, no full score
Explorer down         -> try RPC fallback
RPC fallback          -> native proof only, no score
Explorer + RPC down   -> error message + Retry button
```

## Deploy

Copy the three source files into your GitHub Pages folder, for example:

```text
Sender-Web/
  wallet-intelligence.html
  wallet-intelligence.css
  wallet-intelligence.js
```

Then open:

```text
https://<username>.github.io/<repo>/Sender-Web/wallet-intelligence.html
```
