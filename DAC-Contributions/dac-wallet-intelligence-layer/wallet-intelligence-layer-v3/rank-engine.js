/*
 * Wallet Intelligence Layer v3.0.0 — Wallet Rank Intelligence
 *
 * Helper-only rank engine.
 * No separate input.
 * No separate button.
 * The main wallet checker calls this module and merges rank data into the normal result.
 */

(function () {
  const SUMMARY_URL = "./data/wallet-rank-summary.json";
  const INDEX_URL = "./data/wallet-rank-index.json";

  const METRICS = [
    { key: "tx_count", rankKey: "tx_count", label: "Transactions", suffix: "tx" },
    { key: "gas_used", rankKey: "gas_used", label: "Gas Used", suffix: "gas" },
    { key: "native_volume", rankKey: "native_volume", label: "Native Volume", suffix: "DACC" },
    { key: "native_balance", rankKey: "native_balance", label: "Native Balance", suffix: "DACC" },
    { key: "estimated_stake", rankKey: "estimated_stake", label: "Estimated Stake", suffix: "DACC" },
    { key: "nft_holdings", rankKey: "nft_holdings", label: "NFT Holdings", suffix: "NFTs" },
    { key: "collection_diversity", rankKey: "collection_diversity", label: "Collection Diversity", suffix: "collections" },
    { key: "reputation_score", rankKey: "reputation_score", label: "Reputation Score", suffix: "/100" },
    { key: "sybil_risk_score", rankKey: "low_sybil_risk", label: "Low-Risk Profile", suffix: "risk score" }
  ];

  let loadPromise = null;
  let rankSummary = null;
  let rankIndex = {};

  function isValidAddress(value) {
    return /^0x[a-fA-F0-9]{40}$/.test((value || "").trim());
  }

  function normalizeAddress(value) {
    return (value || "").trim().toLowerCase();
  }

  async function fetchJson(url, fallback) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.warn("[Wallet Rank Intelligence]", error);
      return fallback;
    }
  }

  async function load() {
    if (!loadPromise) {
      loadPromise = Promise.all([
        fetchJson(SUMMARY_URL, null),
        fetchJson(INDEX_URL, {})
      ]).then(([summary, index]) => {
        rankSummary = summary;
        rankIndex = index && typeof index === "object" ? index : {};
        return { summary: rankSummary, index: rankIndex };
      });
    }

    return loadPromise;
  }

  async function getProfile(address) {
    await load();

    if (!isValidAddress(address)) {
      return {
        status: "INVALID_ADDRESS",
        summary: rankSummary,
        profile: null,
        metrics: METRICS
      };
    }

    const normalized = normalizeAddress(address);
    const profile = rankIndex[normalized];
    const total = rankSummary && Number(rankSummary.total_ranked_wallets || 0);

    if (!profile) {
      return {
        status: total > 0 ? "NOT_INDEXED" : "EMPTY_INDEX",
        summary: rankSummary,
        profile: null,
        metrics: METRICS
      };
    }

    return {
      status: "READY",
      summary: rankSummary,
      profile,
      metrics: METRICS
    };
  }

  window.WalletRankIntelligence = {
    load,
    getProfile,
    metrics: METRICS
  };

  document.addEventListener("DOMContentLoaded", () => {
    load();
  });
})();
