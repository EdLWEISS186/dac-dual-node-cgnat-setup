/*
 * Wallet Intelligence Layer v3.0.0 — Wallet Rank Intelligence
 * Core statement:
 * v3 turns every verified wallet variable into a comparative public rank signal.
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

  let rankSummary = null;
  let rankIndex = {};

  const $ = (selector) => document.querySelector(selector);

  function isValidAddress(value) {
    return /^0x[a-fA-F0-9]{40}$/.test((value || "").trim());
  }

  function normalizeAddress(value) {
    return (value || "").trim().toLowerCase();
  }

  async function fetchJson(url, fallback) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`${url} returned HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.warn("[Wallet Rank Intelligence]", error);
      return fallback;
    }
  }

  function formatNumber(value) {
    if (value === null || value === undefined || value === "") return "—";

    if (typeof value === "number") {
      return value.toLocaleString(undefined, { maximumFractionDigits: 6 });
    }

    if (typeof value === "string" && /^-?\d+(\.\d+)?$/.test(value)) {
      return Number(value).toLocaleString(undefined, { maximumFractionDigits: 6 });
    }

    return String(value);
  }

  function formatRank(rank, total) {
    if (!rank || Number(rank) <= 0) return "Not ranked";

    const rankText = `#${Number(rank).toLocaleString()}`;
    if (!total || Number(total) <= 0) return rankText;

    return `${rankText} / ${Number(total).toLocaleString()}`;
  }

  function formatPercentile(value) {
    if (value === null || value === undefined || value === "") return "";
    const n = Number(value);
    if (!Number.isFinite(n)) return "";
    return `Top ${n.toFixed(2)}%`;
  }

  function formatTier(tier) {
    if (!tier) return "UNRANKED";
    return String(tier).replaceAll("_", " ");
  }

  function metricValue(wallet, metric) {
    const metrics = wallet.metrics || {};
    return metrics[metric.key];
  }

  function metricRank(wallet, metric) {
    const ranks = wallet.ranks || {};
    return ranks[metric.rankKey] ?? ranks[metric.key];
  }

  function metricPercentile(wallet, metric) {
    const percentiles = wallet.percentiles || {};
    return percentiles[metric.rankKey] ?? percentiles[metric.key];
  }

  function renderSummary() {
    const el = $("#v3-rank-summary");
    if (!el) return;

    const total = rankSummary?.total_ranked_wallets || 0;
    const status = rankSummary?.status || "UNKNOWN";
    const block = rankSummary?.latest_indexed_block || "Not indexed yet";
    const generatedAt = rankSummary?.generated_at || "Unknown";
    const model = rankSummary?.rank_model || "wallet-rank-intelligence-v3.0.0";

    el.innerHTML = `
      <div class="rank-status-grid">
        <span class="rank-status-pill">${status}</span>
        <div class="rank-status-item">
          <span>Rank model</span>
          <strong>${model}</strong>
        </div>
        <div class="rank-status-item">
          <span>Ranked wallets</span>
          <strong>${formatNumber(total)}</strong>
        </div>
        <div class="rank-status-item">
          <span>Latest indexed block</span>
          <strong>${formatNumber(block)}</strong>
        </div>
        <div class="rank-status-item">
          <span>Generated</span>
          <strong>${generatedAt}</strong>
        </div>
      </div>
    `;
  }

  function renderMessage(message, className = "rank-empty") {
    const result = $("#v3-rank-result");
    if (!result) return;
    result.innerHTML = `<p class="${className}">${message}</p>`;
  }

  function renderWalletRank(address) {
    const result = $("#v3-rank-result");
    if (!result) return;

    if (!isValidAddress(address)) {
      renderMessage("Invalid wallet address. Please enter a valid 0x address.", "rank-warning");
      return;
    }

    const normalized = normalizeAddress(address);
    const wallet = rankIndex[normalized];

    if (!wallet) {
      const total = rankSummary?.total_ranked_wallets || 0;
      if (!total) {
        renderMessage(
          "Rank index is ready, but no wallet rankings have been generated yet. Next step: build the chain-wide wallet rank indexer.",
          "rank-empty"
        );
        return;
      }

      renderMessage(
        "This wallet is not found in the current rank index. It may be inactive, not yet indexed, or below the current indexing window.",
        "rank-warning"
      );
      return;
    }

    const totalRanked = wallet.total_ranked_wallets || rankSummary?.total_ranked_wallets || 0;
    const strongestMetric = wallet.strongest_metric || "Not available";
    const weakestMetric = wallet.weakest_metric || "Not available";

    const cards = METRICS.map((metric) => {
      const rawValue = metricValue(wallet, metric);
      const rank = metricRank(wallet, metric);
      const percentile = metricPercentile(wallet, metric);

      return `
        <div class="rank-metric-card">
          <div class="rank-metric-label">${metric.label}</div>
          <div class="rank-metric-value">${formatNumber(rawValue)} ${metric.suffix}</div>
          <div class="rank-metric-rank">${formatRank(rank, totalRanked)}</div>
          <div class="rank-metric-percentile">${formatPercentile(percentile)}</div>
        </div>
      `;
    }).join("");

    result.innerHTML = `
      <div class="rank-wallet-head">
        <div>
          <div class="rank-metric-label">Wallet Rank Profile</div>
          <div class="rank-wallet-address">${wallet.address || normalized}</div>
        </div>
        <span class="rank-status-pill rank-tier">${formatTier(wallet.rank_tier)}</span>
      </div>

      <div class="rank-status-grid" style="margin-bottom: 16px;">
        <div class="rank-status-item">
          <span>Strongest comparative signal</span>
          <strong>${strongestMetric}</strong>
        </div>
        <div class="rank-status-item">
          <span>Weakest comparative signal</span>
          <strong>${weakestMetric}</strong>
        </div>
      </div>

      <div class="rank-grid">${cards}</div>
    `;
  }

  async function initWalletRankIntelligence() {
    rankSummary = await fetchJson(SUMMARY_URL, null);
    rankIndex = await fetchJson(INDEX_URL, {});

    renderSummary();

    const input = $("#v3-rank-address");
    const button = $("#v3-rank-check");

    if (!input || !button) return;

    button.addEventListener("click", () => {
      renderWalletRank(input.value);
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        renderWalletRank(input.value);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", initWalletRankIntelligence);
})();
