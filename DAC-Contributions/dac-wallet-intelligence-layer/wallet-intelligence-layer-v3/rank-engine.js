/*
 * Wallet Intelligence Layer v3.6.0 — Wallet Rank Intelligence
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
    { key: "native_funds", rankKey: "native_funds", label: "Native Funds", suffix: "DACC", layout: "metric" },
    { key: "estimated_stake_before_conviction", rankKey: "estimated_stake_before_conviction", label: "DACC Stake", suffix: "DACC", layout: "metric" },
    { key: "transactions", rankKey: "transactions", label: "Transactions", suffix: "tx", layout: "metric" },
    { key: "native_volume", rankKey: "native_volume", label: "Native Volume", suffix: "DACC", layout: "metric" },
    { key: "gas_used", rankKey: "gas_used", label: "Gas Used", suffix: "gas", layout: "metric" },
    { key: "nft_holdings", rankKey: "nft_holdings", label: "NFT Holdings", suffix: "NFTs", layout: "metric" },
    { key: "collection_diversity", rankKey: "collection_diversity", label: "Collection Diversity", suffix: "collections", layout: "metric" },
    { key: "reputation_score", rankKey: "reputation_score", label: "Reputation Score", suffix: "/100", layout: "metric" },
    { key: "low_sybil_risk", rankKey: "low_sybil_risk", label: "Low-Risk Profile", suffix: "risk score", layout: "metric" },
    { key: "official_inception_nfts", rankKey: "official_inception_nfts", label: "Official Testnet Inception NFTs", suffix: "NFTs", layout: "official_signal" },
    { key: "overall_rank", rankKey: "overall_rank", label: "Overall Wallet Rank", suffix: "score", layout: "overall" }
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
    if (!index || typeof index !== "object" || !index.directory) return false;

    const mode = String(index.mode || "");

    return (
      mode === "SHARDED" ||
      mode === "SHARDED_COMPACT_V1" ||
      mode === "SHARDED_COMPACT_V2" ||
      mode === "SHARDED_COMPACT_V3"
    );
  }

  function isCompactShardedIndex(index) {
    if (!index || typeof index !== "object") return false;

    const mode = String(index.mode || "");
    const schema = String(index.record_schema || "");

    return (
      (
        mode === "SHARDED_COMPACT_V1" &&
        schema === "WIL_V3_COMPACT_ARRAY_V1"
      ) ||
      (
        mode === "SHARDED_COMPACT_V2" &&
        schema === "WIL_V3_COMPACT_ARRAY_V2"
      ) ||
      (
        mode === "SHARDED_COMPACT_V3" &&
        schema === "WIL_V3_COMPACT_ARRAY_V3"
      )
    );
  }

  function getAddressShard(address) {
    const normalized = normalizeAddress(address);
    return normalized.slice(2, 4);
  }

  function rankPercentile(rank, total) {
    const numericRank = Number(rank);
    const numericTotal = Number(total);

    if (
      !Number.isFinite(numericRank) ||
      !Number.isFinite(numericTotal) ||
      numericRank <= 0 ||
      numericTotal <= 0
    ) {
      return "NaN";
    }

    return ((numericRank / numericTotal) * 100).toFixed(6);
  }

  function compactRankTier(bestPercent) {
    const numericPercent = Number(bestPercent);

    if (!Number.isFinite(numericPercent)) return "INDEXED";
    if (numericPercent <= 1) return "TOP_1_PERCENT";
    if (numericPercent <= 5) return "TOP_5_PERCENT";
    if (numericPercent <= 10) return "TOP_10_PERCENT";
    if (numericPercent <= 25) return "TOP_25_PERCENT";
    if (numericPercent <= 50) return "TOP_50_PERCENT";

    return "INDEXED";
  }

  function decodeCompactProfile(address, compactRecord) {
    const schema = String(rankIndex.record_schema || "");
    const isV2 = schema === "WIL_V3_COMPACT_ARRAY_V2";
    const isV3 = schema === "WIL_V3_COMPACT_ARRAY_V3";

    const defaultMetricOrder = isV3
      ? [
          "native_funds",
          "estimated_stake_before_conviction",
          "transactions",
          "native_volume",
          "gas_used",
          "nft_holdings",
          "collection_diversity",
          "reputation_score",
          "low_sybil_risk",
          "official_inception_nfts"
        ]
      : isV2
        ? [
            "native_funds",
            "estimated_current_stake",
            "transactions",
            "native_volume",
            "gas_used",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk",
            "official_inception_nfts"
          ]
        : [
            "native_funds",
            "transactions",
            "gas_used",
            "native_volume",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk"
          ];

    const defaultRankOrder = [
      ...defaultMetricOrder,
      "overall_rank"
    ];

    const metricOrder =
      Array.isArray(rankIndex.metric_order) &&
      rankIndex.metric_order.length === defaultMetricOrder.length
        ? rankIndex.metric_order
        : defaultMetricOrder;

    const rankOrder =
      Array.isArray(rankIndex.rank_order) &&
      rankIndex.rank_order.length === defaultRankOrder.length
        ? rankIndex.rank_order
        : defaultRankOrder;

    const expectedLength = (
      metricOrder.length
      + rankOrder.length
    );

    if (
      !Array.isArray(compactRecord) ||
      compactRecord.length !== expectedLength
    ) {
      if (
        compactRecord !== null &&
        compactRecord !== undefined
      ) {
        console.warn(
          "[Wallet Rank Intelligence] Invalid compact rank record:",
          address,
          {
            schema,
            expectedLength,
            actualLength: Array.isArray(compactRecord)
              ? compactRecord.length
              : null
          }
        );
      }

      return null;
    }

    const totalRanked = Number(
      rankIndex.total_ranked_wallets ||
      (rankSummary && rankSummary.total_ranked_wallets) ||
      0
    );

    const metrics = {};
    const ranks = {};
    const percentiles = {};

    metricOrder.forEach((key, index) => {
      metrics[key] = compactRecord[index];
    });

    rankOrder.forEach((key, index) => {
      const rawRank = Number(
        compactRecord[
          metricOrder.length + index
        ]
      );

      const rank = (
        Number.isFinite(rawRank) &&
        rawRank > 0
      )
        ? rawRank
        : null;

      ranks[key] = rank;
      percentiles[key] = rankPercentile(
        rank,
        totalRanked
      );
    });

    if (
      isV2 &&
      metrics.estimated_current_stake !== undefined
    ) {
      metrics.estimated_stake_before_conviction =
        metrics.estimated_current_stake;

      ranks.estimated_stake_before_conviction =
        ranks.estimated_current_stake;

      percentiles.estimated_stake_before_conviction =
        percentiles.estimated_current_stake;
    }

    const strongestMetricOrder = (
      (isV2 || isV3) &&
      Array.isArray(
        rankIndex.small_metric_order
      ) &&
      rankIndex.small_metric_order.length >= 9
    )
      ? rankIndex.small_metric_order
      : metricOrder.filter(
          (key) => (
            key !== "official_inception_nfts"
          )
        );

    let strongestMetric = null;
    let bestPercent = Number.POSITIVE_INFINITY;

    strongestMetricOrder.forEach((key) => {
      const percentile = Number(
        percentiles[key]
      );

      if (
        Number.isFinite(percentile) &&
        percentile < bestPercent
      ) {
        bestPercent = percentile;
        strongestMetric = key === "estimated_current_stake"
          ? "estimated_stake_before_conviction"
          : key;
      }
    });

    const availableVariables =
      Array.isArray(
        rankIndex.available_rank_variables
      )
        ? [...rankIndex.available_rank_variables]
        : [...rankOrder];

    if (
      isV2 &&
      availableVariables.includes("estimated_current_stake") &&
      !availableVariables.includes("estimated_stake_before_conviction")
    ) {
      availableVariables.push("estimated_stake_before_conviction");
    }

    const pendingVariables =
      Array.isArray(
        rankIndex.pending_rank_variables
      )
        ? rankIndex.pending_rank_variables
        : [];

    return {
      address,
      metrics,
      ranks,
      percentiles,
      total_ranked_wallets: totalRanked,
      rank_tier: compactRankTier(
        bestPercent
      ),
      strongest_metric: strongestMetric,
      available_rank_variables: (
        availableVariables
      ),
      pending_rank_variables: (
        pendingVariables
      )
    };
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

    const summaryStatus = String(summary.status || "");
    const indexStatus = String(index.status || "");
    const indexMode = String(index.mode || "");

    if (summary.has_valid_rank_index === false) return false;
    if (index.has_valid_rank_index === false) return false;
    if (summary.status === "HYBRID_MODEL_PENDING_VALID_INDEX") return false;
    if (summaryStatus.startsWith("EXTERNALIZED_STATE")) return false;
    if (indexStatus.startsWith("EXTERNALIZED_STATE")) return false;
    if (indexMode === "EXTERNALIZED_STATE") return false;

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
        const shardRecord = shardPayload
          ? shardPayload[normalized]
          : null;

        profile = isCompactShardedIndex(rankIndex)
          ? decodeCompactProfile(normalized, shardRecord)
          : shardRecord;
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
