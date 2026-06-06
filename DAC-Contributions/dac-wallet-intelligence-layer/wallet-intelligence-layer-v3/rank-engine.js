/*
 * Wallet Intelligence Layer v3.0.0 — Wallet Rank Intelligence
 *
 * Hybrid helper:
 * - Fetches real-time Explorer API network snapshot.
 * - Reads generated rank summary/index only when a valid custom index exists.
 * - Does not create a separate input or button.
 * - Main wallet checker calls this helper and renders one integrated rank section.
 */

(function () {
  const EXPLORER_STATS_URL = "https://exptest.dachain.tech/api/v2/stats";
  const SUMMARY_URL = "./data/wallet-rank-summary.json";
  const INDEX_URL = "./data/wallet-rank-index.json";

  const METRICS = [
    { key: "native_funds", rankKey: "native_funds", label: "Native Funds", suffix: "DACC" },
    { key: "transactions", rankKey: "transactions", label: "Transactions", suffix: "tx" },
    { key: "gas_used", rankKey: "gas_used", label: "Gas Used", suffix: "gas" },
    { key: "native_volume", rankKey: "native_volume", label: "Native Volume", suffix: "DACC" },
    { key: "nft_holdings", rankKey: "nft_holdings", label: "NFT Holdings", suffix: "NFTs" },
    { key: "collection_diversity", rankKey: "collection_diversity", label: "Collection Diversity", suffix: "collections" },
    { key: "reputation_score", rankKey: "reputation_score", label: "Reputation Score", suffix: "/100" },
    { key: "low_sybil_risk", rankKey: "low_sybil_risk", label: "Low-Risk Profile", suffix: "risk score" },
    { key: "overall_rank", rankKey: "overall_rank", label: "Overall Wallet Rank", suffix: "score" }
  ];

  let loadPromise = null;
  let networkSnapshot = null;
  let rankSummary = null;
  let rankIndex = {};
  let rankShardCache = {};

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

  function buildNetworkSnapshot(stats) {
    if (!stats || typeof stats !== "object") {
      return {
        status: "UNAVAILABLE",
        source: EXPLORER_STATS_URL
      };
    }

    return {
      status: "READY",
      source: EXPLORER_STATS_URL,
      total_addresses: stats.total_addresses || null,
      total_transactions: stats.total_transactions || null,
      transactions_today: stats.transactions_today || null,
      gas_used_today: stats.gas_used_today || null,
      total_blocks: stats.total_blocks || null,
      average_block_time: stats.average_block_time || null,
      network_utilization_percentage: stats.network_utilization_percentage || null,
      gas_prices: stats.gas_prices || null,
      gas_price_updated_at: stats.gas_price_updated_at || null
    };
  }

  function isShardedIndex(index) {
    return Boolean(index && typeof index === "object" && index.mode === "SHARDED" && index.directory);
  }

  function getAddressShard(address) {
    const normalized = normalizeAddress(address);
    return normalized.slice(2, 4);
  }

  async function fetchRankShard(address) {
    if (!isShardedIndex(rankIndex)) return null;

    const shard = getAddressShard(address);
    if (!shard) return null;

    if (rankShardCache[shard]) {
      return rankShardCache[shard];
    }

    const directory = String(rankIndex.directory || "data/rank-shards").replace(/^\.?\//, "");
    const shardUrl = `./${directory}/${shard}.json`;
    const payload = await fetchJson(shardUrl, {});
    rankShardCache[shard] = payload && typeof payload === "object" ? payload : {};
    return rankShardCache[shard];
  }

  function hasValidCustomRankIndex(summary, index) {
    if (!summary || !index || typeof index !== "object") return false;
    if (summary.status === "HYBRID_MODEL_PENDING_VALID_INDEX") return false;

    if (isShardedIndex(index)) {
      return Boolean(summary.rank_shards && summary.rank_shards.directory);
    }

    return Object.keys(index).length > 0;
  }

  async function load() {
    if (!loadPromise) {
      loadPromise = Promise.all([
        fetchJson(EXPLORER_STATS_URL, null),
        fetchJson(SUMMARY_URL, null),
        fetchJson(INDEX_URL, {})
      ]).then(([stats, summary, index]) => {
        networkSnapshot = buildNetworkSnapshot(stats);
        rankSummary = summary;
        rankIndex = index && typeof index === "object" ? index : {};
        return {
          networkSnapshot,
          summary: rankSummary,
          index: rankIndex,
          hasValidIndex: hasValidCustomRankIndex(rankSummary, rankIndex)
        };
      });
    }

    return loadPromise;
  }

  async function getProfile(address) {
    const loaded = await load();
    const hasValidIndex = loaded.hasValidIndex;

    if (!isValidAddress(address)) {
      return {
        status: "INVALID_ADDRESS",
        networkSnapshot,
        summary: rankSummary,
        profile: null,
        metrics: METRICS,
        hasValidIndex
      };
    }

    const normalized = normalizeAddress(address);

    if (!hasValidIndex) {
      return {
        status: "PENDING_VALID_INDEX",
        networkSnapshot,
        summary: rankSummary,
        profile: null,
        metrics: METRICS,
        hasValidIndex: false
      };
    }

    let profile = null;

    if (isShardedIndex(rankIndex)) {
      const shardPayload = await fetchRankShard(normalized);
      profile = shardPayload ? shardPayload[normalized] : null;
    } else {
      profile = rankIndex[normalized];
    }

    if (!profile) {
      return {
        status: "NOT_INDEXED",
        networkSnapshot,
        summary: rankSummary,
        profile: null,
        metrics: METRICS,
        hasValidIndex: true
      };
    }

    return {
      status: "READY",
      networkSnapshot,
      summary: rankSummary,
      profile,
      metrics: METRICS,
      hasValidIndex: true
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
