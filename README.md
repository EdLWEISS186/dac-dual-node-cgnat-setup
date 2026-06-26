# WIL v3 Rank Data Temporarily Invalidated

This branch intentionally does not currently publish rank shards.

Reason:
The previous full rank snapshot was generated from an incomplete WIL indexed universe.
Expected parity for WIL v3 is:

- Explorer-visible wallets == Indexed wallets
- Network total transactions == Processed transactions

Until parity is restored and verified, rank shards must not be reused.
