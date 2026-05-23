"use strict";

// ======================================================
// DAC Wallet Intelligence Layer v1
// DAC Sender-inspired UI version.
// No wallet connection, no signing, no mock score.
// ======================================================

const DAC_EXPLORER_API = "https://exptest.dachain.tech/api";
const DAC_RPC_URL = "https://rpctest.dachain.tech/";
const DAC_CHAIN_ID = 21894;
const NATIVE_SYMBOL = "tDACC";
const REQUEST_TIMEOUT_MS = 18000;

const SCORING_POLICY = Object.freeze({
  version: "WIL-v1.2.0",
  policyId: "WIL-2026-05-v1.2.0",
  status: "LOCKED",
  model: "versioned-reputation-scoring-v1.2.0",
  maxScore: 100,
  components: Object.freeze({
    transactionScore: Object.freeze({
      maxPoints: 40,
      thresholds: Object.freeze([
        { condition: "txCount >= 1000", points: 40 },
        { condition: "txCount >= 500", points: 30 },
        { condition: "txCount >= 100", points: 20 },
        { condition: "txCount < 100", points: 10 },
      ]),
    }),
    nftDiversityScore: Object.freeze({
      maxPoints: 25,
      thresholds: Object.freeze([
        { condition: "totalCollections >= 10", points: 25 },
        { condition: "totalCollections >= 5", points: 15 },
        { condition: "totalCollections < 5", points: 5 },
      ]),
    }),
    nftHoldingsScore: Object.freeze({
      maxPoints: 20,
      thresholds: Object.freeze([
        { condition: "totalNFTs >= 200", points: 20 },
        { condition: "totalNFTs >= 100", points: 15 },
        { condition: "totalNFTs < 100", points: 5 },
      ]),
    }),
    nativeBalanceScore: Object.freeze({
      maxPoints: 15,
      thresholds: Object.freeze([
        { condition: "nativeBalance >= 5", points: 15 },
        { condition: "nativeBalance >= 1", points: 10 },
        { condition: "nativeBalance < 1", points: 5 },
      ]),
    }),
  }),
  labels: Object.freeze({
    reputationLevel: Object.freeze([
      { condition: "score >= 90", label: "ELITE" },
      { condition: "score >= 75", label: "HIGH" },
      { condition: "score >= 50", label: "MEDIUM" },
      { condition: "score < 50", label: "LOW" },
    ]),
    sybilRisk: Object.freeze([
      { condition: "score >= 90", label: "LOW" },
      { condition: "score >= 70", label: "MEDIUM" },
      { condition: "score < 70", label: "HIGH" },
    ]),
  }),
  note:
    "Community-defined scoring heuristic. Not an official DAC reputation, eligibility, or Sybil system.",
});


const state = {
  lastAddress: "",
  lastOutput: null,
  blockHistory: [],
};

const el = {
  walletInput: document.getElementById("walletInput"),
  checkButton: document.getElementById("checkButton"),
  retryButton: document.getElementById("retryButton"),
  copyJsonButton: document.getElementById("copyJsonButton"),

  statusPanel: document.getElementById("statusPanel"),
  statusIcon: document.getElementById("statusIcon"),
  statusLabel: document.getElementById("statusLabel"),
  statusMessage: document.getElementById("statusMessage"),

  resultPanel: document.getElementById("resultPanel"),
  resultTitle: document.getElementById("resultTitle"),
  resultSubtitle: document.getElementById("resultSubtitle"),
  modePill: document.getElementById("modePill"),

  nativeBalanceValue: document.getElementById("nativeBalanceValue"),
  nativeBalanceSource: document.getElementById("nativeBalanceSource"),
  transactionsValue: document.getElementById("transactionsValue"),
  transactionsSource: document.getElementById("transactionsSource"),
  collectionsValue: document.getElementById("collectionsValue"),
  collectionsSource: document.getElementById("collectionsSource"),
  nftHoldingsValue: document.getElementById("nftHoldingsValue"),
  nftHoldingsSource: document.getElementById("nftHoldingsSource"),

  activityLevelValue: document.getElementById("activityLevelValue"),
  engagementTypeValue: document.getElementById("engagementTypeValue"),
  nftParticipationValue: document.getElementById("nftParticipationValue"),
  diversityScoreValue: document.getElementById("diversityScoreValue"),

  portfolioStyleValue: document.getElementById("portfolioStyleValue"),
  walletArchetypeValue: document.getElementById("walletArchetypeValue"),
  topCollectionValue: document.getElementById("topCollectionValue"),
  concentrationValue: document.getElementById("concentrationValue"),

  reputationScoreValue: document.getElementById("reputationScoreValue"),
  reputationLevelValue: document.getElementById("reputationLevelValue"),
  trustProfileValue: document.getElementById("trustProfileValue"),
  sybilRiskValue: document.getElementById("sybilRiskValue"),

  collectionCountLabel: document.getElementById("collectionCountLabel"),
  collectionsList: document.getElementById("collectionsList"),
  rawJsonOutput: document.getElementById("rawJsonOutput"),
  scoreBreakdownGrid: document.getElementById("scoreBreakdownGrid"),
  scoringPolicyLabel: document.getElementById("scoringPolicyLabel"),
  scoreExplanation: document.getElementById("scoreExplanation"),
  policyIdValue: document.getElementById("policyIdValue"),
  policyStatusValue: document.getElementById("policyStatusValue"),
  policyMaxScoreValue: document.getElementById("policyMaxScoreValue"),
  policyEngineValue: document.getElementById("policyEngineValue"),
};

window.addEventListener("load", () => {
  setTimeout(initChainStats, 800);
});

el.checkButton.addEventListener("click", () => {
  checkWalletFromInput();
});

el.retryButton.addEventListener("click", () => {
  if (state.lastAddress) {
    checkWallet(state.lastAddress);
  } else {
    checkWalletFromInput();
  }
});

el.walletInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    checkWalletFromInput();
  }
});

el.copyJsonButton.addEventListener("click", async () => {
  if (!state.lastOutput) return;

  try {
    await navigator.clipboard.writeText(JSON.stringify(state.lastOutput, null, 2));
    setStatus("success", "Copied", "Raw JSON output copied to clipboard.", "✓");
  } catch {
    setStatus("partial", "Copy Failed", "Browser clipboard access was unavailable.", "!");
  }
});

function checkWalletFromInput() {
  const address = el.walletInput.value.trim();
  checkWallet(address);
}

async function checkWallet(address) {
  resetView();

  if (!isValidEvmAddress(address)) {
    setStatus(
      "error",
      "Invalid Address",
      "Please paste a valid EVM address starting with 0x and containing 40 hexadecimal characters.",
      "×"
    );
    return;
  }

  state.lastAddress = address;

  setLoading(true);
  setStatus(
    "loading",
    "Checking",
    "Reading DAC Explorer data: balance, tokenlist, txlist, and NFT transfers.",
    "◈"
  );

  try {
    const explorerResult = await getExplorerSnapshot(address);

    if (explorerResult.status === "FULL") {
      const output = buildFullWalletIntelligence(address, explorerResult.data);
      renderFullOutput(output);
      setStatus(
        "success",
        "Full Intelligence Ready",
        "DAC Explorer returned all required modules. Full wallet intelligence was generated.",
        "✓"
      );
      return;
    }

    if (explorerResult.status === "PARTIAL") {
      const output = buildPartialExplorerOutput(address, explorerResult);
      renderPartialOutput(output);
      setStatus(
        "partial",
        "Partial Explorer Data",
        "Some DAC Explorer modules failed or returned invalid data. No full reputation score was generated.",
        "!"
      );
      return;
    }

    throw new Error("Explorer did not return usable data.");
  } catch (explorerError) {
    console.warn("Explorer primary failed:", explorerError);

    setStatus(
      "loading",
      "Explorer Unavailable",
      "DAC Explorer could not be reached. Trying limited DAC RPC fallback for native proof only.",
      "◈"
    );

    try {
      const rpcOutput = await buildRpcFallbackOutput(address, explorerError);
      renderRpcFallbackOutput(rpcOutput);
      setStatus(
        "fallback",
        "RPC Fallback Mode",
        "DAC Explorer is unavailable, but DAC RPC is reachable. Showing native proof only; no score was generated.",
        "!"
      );
    } catch (rpcError) {
      console.error("RPC fallback failed:", rpcError);
      const failedOutput = buildFailedOutput(address, explorerError, rpcError);
      renderFailureOutput(failedOutput);
      setStatus(
        "error",
        "Explorer / RPC Unavailable",
        "No verified data could be loaded. No wallet score was generated. Please retry in a few moments.",
        "×"
      );
    }
  } finally {
    setLoading(false);
  }
}

// ======================================================
// Explorer data layer
// ======================================================

async function getExplorerSnapshot(address) {
  const tasks = {
    nativeBalance: () => getNativeBalanceFromExplorer(address),
    nftCollections: () => getNftCollectionsFromExplorer(address),
    transactionCount: () => getTransactionCountFromExplorer(address),
    nftTransfers: () => getNftTransfersFromExplorer(address),
  };

  const entries = await Promise.all(
    Object.entries(tasks).map(async ([key, task]) => {
      try {
        const value = await task();
        return [key, { ok: true, value, source: "DAC Explorer" }];
      } catch (error) {
        return [
          key,
          {
            ok: false,
            value: null,
            source: "DAC Explorer",
            error: normalizeError(error),
          },
        ];
      }
    })
  );

  const modules = Object.fromEntries(entries);
  const okCount = Object.values(modules).filter((item) => item.ok).length;

  if (okCount === 4) {
    return {
      status: "FULL",
      mode: "EXPLORER_PRIMARY",
      source: "DAC Explorer",
      modules,
      data: {
        nativeBalance: modules.nativeBalance.value,
        nftCollections: modules.nftCollections.value,
        transactionCount: modules.transactionCount.value,
        nftTransfers: modules.nftTransfers.value,
      },
    };
  }

  if (okCount > 0) {
    return {
      status: "PARTIAL",
      mode: "EXPLORER_PRIMARY_PARTIAL",
      source: "DAC Explorer",
      modules,
      warning:
        "Full wallet intelligence requires native balance, NFT collections, transaction history, and NFT transfer modules.",
    };
  }

  throw new Error("DAC Explorer returned no usable modules.");
}

async function explorerRequest(params) {
  const url = new URL(DAC_EXPLORER_API);

  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });

  const response = await fetchWithTimeout(url.toString(), {}, REQUEST_TIMEOUT_MS);

  if (!response.ok) {
    throw new Error(`Explorer HTTP ${response.status}`);
  }

  const data = await response.json();

  if (!data || typeof data !== "object" || !("result" in data)) {
    throw new Error("Explorer returned invalid response shape.");
  }

  return data;
}

async function getNativeBalanceFromExplorer(address) {
  const data = await explorerRequest({
    module: "account",
    action: "balance",
    address,
  });

  if (data.status !== "1" || data.result === undefined || data.result === null) {
    throw new Error(data.message || "Explorer balance module failed.");
  }

  return decimalWeiToNumber(data.result);
}

async function getNftCollectionsFromExplorer(address) {
  const data = await explorerRequest({
    module: "account",
    action: "tokenlist",
    address,
  });

  const result = normalizeExplorerArrayResult(data);

  return result
    .filter((item) => item && item.type === "ERC-721")
    .map((item) => ({
      name: item.name || item.collection || "Unknown Collection",
      symbol: item.symbol || "UNKNOWN",
      balance: Number(item.balance || item.amount || 0),
      contractAddress: item.contractAddress || item.contract || "",
    }))
    .filter((item) => item.balance > 0)
    .sort((a, b) => Number(b.balance) - Number(a.balance));
}

async function getTransactionCountFromExplorer(address) {
  const data = await explorerRequest({
    module: "account",
    action: "txlist",
    address,
    startblock: 0,
    endblock: 99999999,
    sort: "asc",
  });

  return normalizeExplorerArrayResult(data).length;
}

async function getNftTransfersFromExplorer(address) {
  const data = await explorerRequest({
    module: "account",
    action: "tokennfttx",
    address,
  });

  return normalizeExplorerArrayResult(data).length;
}

function normalizeExplorerArrayResult(data) {
  if (Array.isArray(data.result)) {
    return data.result;
  }

  const message = `${data.message || ""} ${data.result || ""}`.toLowerCase();
  const noRecords =
    message.includes("no records") ||
    message.includes("no transactions") ||
    message.includes("not found") ||
    message.includes("empty");

  if (data.status === "0" && noRecords) {
    return [];
  }

  if (data.result === "" || data.result === null) {
    return [];
  }

  throw new Error(data.message || "Explorer array module returned invalid data.");
}

// ======================================================
// RPC fallback layer
// ======================================================

async function buildRpcFallbackOutput(address, explorerError) {
  const [balanceHex, txCountHex] = await Promise.all([
    rpcCall("eth_getBalance", [address, "latest"]),
    rpcCall("eth_getTransactionCount", [address, "latest"]),
  ]);

  const nativeBalance = hexWeiToNumber(balanceHex);
  const outgoingTransactionCount = hexToNumber(txCountHex);

  return {
    wallet: address,
    status: "RPC_FALLBACK",
    mode: "RPC_FALLBACK_NATIVE_ONLY",
    chain: {
      name: "DAC Testnet",
      chainId: DAC_CHAIN_ID,
    },
    source: {
      primary: "DAC Explorer",
      fallback: "DAC RPC",
      explorerEndpoint: DAC_EXPLORER_API,
      rpcEndpoint: DAC_RPC_URL,
    },
    warning:
      "DAC Explorer is unavailable. RPC fallback can only verify native balance and RPC nonce/outgoing transaction count. NFT portfolio, NFT transfers, reputation score, and Sybil risk were not generated.",
    explorerError: normalizeError(explorerError),
    nativeBalance: {
      token: NATIVE_SYMBOL,
      balance: nativeBalance,
      source: "DAC RPC",
    },
    rpcActivity: {
      outgoingTransactionCount,
      source: "DAC RPC eth_getTransactionCount",
      note: "This is RPC nonce/outgoing transaction count, not full explorer tx history.",
    },
    metrics: null,
    activityAnalytics: null,
    portfolioIntelligence: null,
    reputationScoring: null,
  };
}

async function rpcCall(method, params) {
  const response = await fetchWithTimeout(
    DAC_RPC_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: Date.now(),
        method,
        params,
      }),
    },
    REQUEST_TIMEOUT_MS
  );

  if (!response.ok) {
    throw new Error(`RPC HTTP ${response.status}`);
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error.message || "RPC returned an error.");
  }

  if (!("result" in data)) {
    throw new Error("RPC returned invalid response shape.");
  }

  return data.result;
}

// ======================================================
// Intelligence engines
// ======================================================

function buildFullWalletIntelligence(address, data) {
  const nativeBalance = data.nativeBalance;
  const nftCollections = data.nftCollections;
  const txCount = data.transactionCount;
  const nftTransfers = data.nftTransfers;

  const totalCollections = nftCollections.length;
  const totalNFTs = nftCollections.reduce(
    (sum, nft) => sum + Number(nft.balance || 0),
    0
  );

  const activityAnalytics = buildActivityAnalytics(
    txCount,
    nftTransfers,
    totalCollections,
    totalNFTs
  );

  const portfolioIntelligence = buildPortfolioProfile(
    nativeBalance,
    totalCollections,
    totalNFTs,
    nftCollections
  );

  const reputationScoring = buildReputationScore({
    nativeBalance,
    txCount,
    totalCollections,
    totalNFTs,
  });

  return {
    wallet: address,
    status: "FULL",
    mode: "EXPLORER_PRIMARY",
    chain: {
      name: "DAC Testnet",
      chainId: DAC_CHAIN_ID,
    },
    source: {
      primary: "DAC Explorer",
      explorerEndpoint: DAC_EXPLORER_API,
    },
    nativeBalance: {
      token: NATIVE_SYMBOL,
      balance: nativeBalance,
    },
    metrics: {
      totalTransactions: txCount,
      nftTransfers,
      totalCollections,
      totalNFTs,
    },
    activityAnalytics,
    portfolioIntelligence,
    reputationScoring,
    nftCollections: nftCollections.map((nft) => ({
      collection: nft.name,
      symbol: nft.symbol,
      contract: nft.contractAddress,
      amount: Number(nft.balance || 0),
    })),
    generatedAt: new Date().toISOString(),
  };
}

function buildActivityAnalytics(txCount, nftTransfers, totalCollections, totalNFTs) {
  let activityLevel = "LOW";

  if (txCount >= 1000) {
    activityLevel = "VERY HIGH";
  } else if (txCount >= 500) {
    activityLevel = "HIGH";
  } else if (txCount >= 100) {
    activityLevel = "MEDIUM";
  }

  let engagementType = "CASUAL USER";

  if (txCount > 500 && totalCollections >= 10) {
    engagementType = "ECOSYSTEM PARTICIPANT";
  }

  if (txCount > 1000 && totalNFTs > 100) {
    engagementType = "ADVANCED TESTNET USER";
  }

  const nftParticipationRatio =
    txCount > 0 ? `${((nftTransfers / txCount) * 100).toFixed(2)}%` : "0.00%";

  let diversityScore = "LOW";

  if (totalCollections >= 10) {
    diversityScore = "HIGH";
  } else if (totalCollections >= 5) {
    diversityScore = "MEDIUM";
  }

  return {
    activityLevel,
    engagementType,
    nftParticipationRatio,
    diversityScore,
  };
}

function buildPortfolioProfile(
  nativeBalance,
  totalCollections,
  totalNFTs,
  nftCollections
) {
  const sortedCollections = [...nftCollections].sort(
    (a, b) => Number(b.balance || 0) - Number(a.balance || 0)
  );

  const topCollection = sortedCollections[0] || null;

  const concentration =
    topCollection && totalNFTs > 0
      ? (Number(topCollection.balance || 0) / totalNFTs) * 100
      : 0;

  let concentrationLevel = "LOW";

  if (concentration >= 50) {
    concentrationLevel = "HIGH";
  } else if (concentration >= 25) {
    concentrationLevel = "MEDIUM";
  }

  let portfolioStyle = totalNFTs > 0 ? "BALANCED" : "NO NFT ASSETS";

  if (totalNFTs > 100 && totalCollections > 10) {
    portfolioStyle = "NFT HEAVY";
  }

  let walletArchetype = "STANDARD USER";

  if (nativeBalance > 5 && totalNFTs > 100) {
    walletArchetype = "ADVANCED ECOSYSTEM USER";
  }

  return {
    totalCollections,
    totalNFTs,
    topCollection: topCollection
      ? {
          name: topCollection.name,
          symbol: topCollection.symbol,
          amount: Number(topCollection.balance || 0),
        }
      : null,
    concentration: {
      percentage: concentration.toFixed(2),
      level: concentrationLevel,
    },
    portfolioStyle,
    walletArchetype,
  };
}

function buildReputationScore({
  nativeBalance,
  txCount,
  totalCollections,
  totalNFTs,
}) {
  const transactionScore =
    txCount >= 1000 ? 40 : txCount >= 500 ? 30 : txCount >= 100 ? 20 : 10;

  const nftDiversityScore =
    totalCollections >= 10 ? 25 : totalCollections >= 5 ? 15 : 5;

  const nftHoldingsScore =
    totalNFTs >= 200 ? 20 : totalNFTs >= 100 ? 15 : 5;

  const nativeBalanceScore =
    nativeBalance >= 5 ? 15 : nativeBalance >= 1 ? 10 : 5;

  const score =
    transactionScore +
    nftDiversityScore +
    nftHoldingsScore +
    nativeBalanceScore;

  let reputationLevel = "LOW";

  if (score >= 90) {
    reputationLevel = "ELITE";
  } else if (score >= 75) {
    reputationLevel = "HIGH";
  } else if (score >= 50) {
    reputationLevel = "MEDIUM";
  }

  let trustProfile = "STANDARD USER";

  if (txCount > 1000 && totalCollections > 10) {
    trustProfile = "ADVANCED TESTNET PARTICIPANT";
  }

  let sybilRisk = "HIGH";

  if (score >= 90) {
    sybilRisk = "LOW";
  } else if (score >= 70) {
    sybilRisk = "MEDIUM";
  }

  const breakdown = [
    {
      key: "transactionScore",
      name: "Transaction Score",
      points: transactionScore,
      maxPoints: 40,
      metric: txCount,
      metricLabel: "transactions",
      condition:
        txCount >= 1000
          ? "txCount >= 1000"
          : txCount >= 500
            ? "txCount >= 500"
            : txCount >= 100
              ? "txCount >= 100"
              : "txCount < 100",
    },
    {
      key: "nftDiversityScore",
      name: "NFT Diversity Score",
      points: nftDiversityScore,
      maxPoints: 25,
      metric: totalCollections,
      metricLabel: "collections",
      condition:
        totalCollections >= 10
          ? "totalCollections >= 10"
          : totalCollections >= 5
            ? "totalCollections >= 5"
            : "totalCollections < 5",
    },
    {
      key: "nftHoldingsScore",
      name: "NFT Holdings Score",
      points: nftHoldingsScore,
      maxPoints: 20,
      metric: totalNFTs,
      metricLabel: "NFT holdings",
      condition:
        totalNFTs >= 200
          ? "totalNFTs >= 200"
          : totalNFTs >= 100
            ? "totalNFTs >= 100"
            : "totalNFTs < 100",
    },
    {
      key: "nativeBalanceScore",
      name: "Native Balance Score",
      points: nativeBalanceScore,
      maxPoints: 15,
      metric: nativeBalance,
      metricLabel: "tDACC",
      condition:
        nativeBalance >= 5
          ? "nativeBalance >= 5"
          : nativeBalance >= 1
            ? "nativeBalance >= 1"
            : "nativeBalance < 1",
    },
  ];

  return {
    reputationScore: score,
    reputationLevel,
    trustProfile,
    sybilRisk,
    scoringPolicy: SCORING_POLICY,
    breakdown,
  };
}

// ======================================================
// Partial / failure outputs
// ======================================================

function buildPartialExplorerOutput(address, explorerResult) {
  const modules = explorerResult.modules;

  const nativeBalance = modules.nativeBalance.ok ? modules.nativeBalance.value : null;
  const nftCollections = modules.nftCollections.ok ? modules.nftCollections.value : null;
  const transactionCount = modules.transactionCount.ok
    ? modules.transactionCount.value
    : null;
  const nftTransfers = modules.nftTransfers.ok ? modules.nftTransfers.value : null;

  const totalCollections = Array.isArray(nftCollections) ? nftCollections.length : null;
  const totalNFTs = Array.isArray(nftCollections)
    ? nftCollections.reduce((sum, nft) => sum + Number(nft.balance || 0), 0)
    : null;

  return {
    wallet: address,
    status: "PARTIAL",
    mode: "EXPLORER_PRIMARY_PARTIAL",
    chain: {
      name: "DAC Testnet",
      chainId: DAC_CHAIN_ID,
    },
    source: {
      primary: "DAC Explorer",
      explorerEndpoint: DAC_EXPLORER_API,
    },
    availableData: {
      nativeBalance: modules.nativeBalance.ok,
      nftCollections: modules.nftCollections.ok,
      transactionCount: modules.transactionCount.ok,
      nftTransfers: modules.nftTransfers.ok,
    },
    moduleErrors: Object.fromEntries(
      Object.entries(modules)
        .filter(([, item]) => !item.ok)
        .map(([key, item]) => [key, item.error])
    ),
    warning:
      "Full reputation score was not generated because one or more required explorer modules could not be verified.",
    nativeBalance: nativeBalance === null ? null : { token: NATIVE_SYMBOL, balance: nativeBalance },
    metrics: {
      totalTransactions: transactionCount,
      nftTransfers,
      totalCollections,
      totalNFTs,
    },
    activityAnalytics: null,
    portfolioIntelligence: null,
    reputationScoring: null,
    nftCollections: Array.isArray(nftCollections)
      ? nftCollections.map((nft) => ({
          collection: nft.name,
          symbol: nft.symbol,
          contract: nft.contractAddress,
          amount: Number(nft.balance || 0),
        }))
      : null,
    generatedAt: new Date().toISOString(),
  };
}

function buildFailedOutput(address, explorerError, rpcError) {
  return {
    wallet: address,
    status: "FAILED",
    mode: "NO_VERIFIED_DATA",
    chain: {
      name: "DAC Testnet",
      chainId: DAC_CHAIN_ID,
    },
    source: {
      primary: "DAC Explorer",
      fallback: "DAC RPC",
      explorerEndpoint: DAC_EXPLORER_API,
      rpcEndpoint: DAC_RPC_URL,
    },
    error: {
      code: "EXPLORER_AND_RPC_UNAVAILABLE",
      message:
        "No verified data could be loaded. No wallet score was generated.",
      explorer: normalizeError(explorerError),
      rpc: normalizeError(rpcError),
    },
    data: null,
    generatedAt: new Date().toISOString(),
  };
}

// ======================================================
// Rendering
// ======================================================

function renderFullOutput(output) {
  state.lastOutput = output;
  el.resultPanel.classList.remove("hidden");
  el.retryButton.classList.add("hidden");
  el.copyJsonButton.classList.remove("hidden");

  el.resultTitle.textContent = "Wallet Intelligence Profile";
  el.resultSubtitle.textContent = shortenAddress(output.wallet);
  el.modePill.textContent = "Explorer Primary";

  setMetric(
    el.nativeBalanceValue,
    el.nativeBalanceSource,
    `${formatNumber(output.nativeBalance.balance, 8)} ${output.nativeBalance.token}`,
    "DAC Explorer"
  );
  setMetric(
    el.transactionsValue,
    el.transactionsSource,
    formatInteger(output.metrics.totalTransactions),
    "txlist"
  );
  setMetric(
    el.collectionsValue,
    el.collectionsSource,
    formatInteger(output.metrics.totalCollections),
    "tokenlist"
  );
  setMetric(
    el.nftHoldingsValue,
    el.nftHoldingsSource,
    formatInteger(output.metrics.totalNFTs),
    "ERC-721 holdings"
  );

  el.activityLevelValue.textContent = output.activityAnalytics.activityLevel;
  el.engagementTypeValue.textContent = output.activityAnalytics.engagementType;
  el.nftParticipationValue.textContent =
    output.activityAnalytics.nftParticipationRatio;
  el.diversityScoreValue.textContent = output.activityAnalytics.diversityScore;

  el.portfolioStyleValue.textContent =
    output.portfolioIntelligence.portfolioStyle;
  el.walletArchetypeValue.textContent =
    output.portfolioIntelligence.walletArchetype;
  el.topCollectionValue.textContent = output.portfolioIntelligence.topCollection
    ? `${output.portfolioIntelligence.topCollection.name} (${output.portfolioIntelligence.topCollection.amount})`
    : "No NFT assets";
  el.concentrationValue.textContent = `${output.portfolioIntelligence.concentration.percentage}% / ${output.portfolioIntelligence.concentration.level}`;

  el.reputationScoreValue.textContent = `${output.reputationScoring.reputationScore}/100`;
  el.reputationLevelValue.textContent = output.reputationScoring.reputationLevel;
  el.trustProfileValue.textContent = output.reputationScoring.trustProfile;
  el.sybilRiskValue.textContent = output.reputationScoring.sybilRisk;

  renderScoringBreakdown(output.reputationScoring);
  renderCollections(output.nftCollections || []);
  renderJson(output);
}

function renderPartialOutput(output) {
  state.lastOutput = output;
  el.resultPanel.classList.remove("hidden");
  el.retryButton.classList.remove("hidden");
  el.copyJsonButton.classList.remove("hidden");

  el.resultTitle.textContent = "Partial Wallet Profile";
  el.resultSubtitle.textContent =
    `${shortenAddress(output.wallet)} • full score not generated`;
  el.modePill.textContent = "Partial Explorer Data";

  setMetric(
    el.nativeBalanceValue,
    el.nativeBalanceSource,
    output.nativeBalance
      ? `${formatNumber(output.nativeBalance.balance, 8)} ${output.nativeBalance.token}`
      : "Unavailable",
    output.availableData.nativeBalance ? "DAC Explorer" : "Module failed"
  );
  setMetric(
    el.transactionsValue,
    el.transactionsSource,
    output.metrics.totalTransactions === null
      ? "Unavailable"
      : formatInteger(output.metrics.totalTransactions),
    output.availableData.transactionCount ? "txlist" : "Module failed"
  );
  setMetric(
    el.collectionsValue,
    el.collectionsSource,
    output.metrics.totalCollections === null
      ? "Unavailable"
      : formatInteger(output.metrics.totalCollections),
    output.availableData.nftCollections ? "tokenlist" : "Module failed"
  );
  setMetric(
    el.nftHoldingsValue,
    el.nftHoldingsSource,
    output.metrics.totalNFTs === null
      ? "Unavailable"
      : formatInteger(output.metrics.totalNFTs),
    output.availableData.nftCollections ? "ERC-721 holdings" : "Module failed"
  );

  fillUnavailableModules("Not generated");
  renderScoringUnavailable("Not generated because one or more required explorer modules failed.");
  renderCollections(output.nftCollections || []);
  renderJson(output);
}

function renderRpcFallbackOutput(output) {
  state.lastOutput = output;
  el.resultPanel.classList.remove("hidden");
  el.retryButton.classList.remove("hidden");
  el.copyJsonButton.classList.remove("hidden");

  el.resultTitle.textContent = "Native Proof Only";
  el.resultSubtitle.textContent =
    `${shortenAddress(output.wallet)} • RPC fallback mode`;
  el.modePill.textContent = "RPC Fallback";

  setMetric(
    el.nativeBalanceValue,
    el.nativeBalanceSource,
    `${formatNumber(output.nativeBalance.balance, 8)} ${output.nativeBalance.token}`,
    "DAC RPC eth_getBalance"
  );
  setMetric(
    el.transactionsValue,
    el.transactionsSource,
    formatInteger(output.rpcActivity.outgoingTransactionCount),
    "RPC nonce / outgoing tx count"
  );
  setMetric(el.collectionsValue, el.collectionsSource, "Unavailable", "Explorer required");
  setMetric(el.nftHoldingsValue, el.nftHoldingsSource, "Unavailable", "Explorer required");

  fillUnavailableModules("RPC fallback");
  renderScoringUnavailable("Not generated in RPC fallback mode. Explorer data is required for full scoring.");
  renderCollections([]);
  renderJson(output);
}

function renderFailureOutput(output) {
  state.lastOutput = output;
  el.resultPanel.classList.remove("hidden");
  el.retryButton.classList.remove("hidden");
  el.copyJsonButton.classList.remove("hidden");

  el.resultTitle.textContent = "No Verified Data";
  el.resultSubtitle.textContent =
    `${shortenAddress(output.wallet)} • retry required`;
  el.modePill.textContent = "Failed";

  setMetric(el.nativeBalanceValue, el.nativeBalanceSource, "Unavailable", "Explorer / RPC down");
  setMetric(el.transactionsValue, el.transactionsSource, "Unavailable", "Explorer / RPC down");
  setMetric(el.collectionsValue, el.collectionsSource, "Unavailable", "Explorer down");
  setMetric(el.nftHoldingsValue, el.nftHoldingsSource, "Unavailable", "Explorer down");

  fillUnavailableModules("No verified data");
  renderScoringUnavailable("No verified explorer or RPC data was available.");
  renderCollections([]);
  renderJson(output);
}

function fillUnavailableModules(reason) {
  el.reputationScoreValue.textContent = "—";
  el.reputationLevelValue.textContent = "Unavailable";

  el.activityLevelValue.textContent = reason;
  el.engagementTypeValue.textContent = "Unavailable";
  el.nftParticipationValue.textContent = "Unavailable";
  el.diversityScoreValue.textContent = "Unavailable";

  el.portfolioStyleValue.textContent = reason;
  el.walletArchetypeValue.textContent = "Unavailable";
  el.topCollectionValue.textContent = "Unavailable";
  el.concentrationValue.textContent = "Unavailable";

  el.trustProfileValue.textContent = "Unavailable";
  el.sybilRiskValue.textContent = "Unavailable";
}



function renderScoringPolicy(policy) {
  const safePolicy = policy || SCORING_POLICY;

  if (el.scoringPolicyLabel) {
    el.scoringPolicyLabel.textContent = safePolicy.version || "WIL-v1.2.0";
  }

  if (el.policyIdValue) {
    el.policyIdValue.textContent = safePolicy.policyId || "WIL-2026-05-v1.2.0";
  }

  if (el.policyStatusValue) {
    el.policyStatusValue.textContent = safePolicy.status || "LOCKED";
  }

  if (el.policyMaxScoreValue) {
    el.policyMaxScoreValue.textContent = String(safePolicy.maxScore || 100);
  }

  if (el.policyEngineValue) {
    el.policyEngineValue.textContent = safePolicy.model || "versioned-reputation-scoring-v1.2.0";
  }
}


function renderScoringBreakdown(reputationScoring) {
  if (!el.scoreBreakdownGrid || !reputationScoring || !Array.isArray(reputationScoring.breakdown)) {
    renderScoringUnavailable("No transparent scoring breakdown available.");
    return;
  }

  renderScoringPolicy(reputationScoring.scoringPolicy || SCORING_POLICY);

  el.scoreBreakdownGrid.innerHTML = reputationScoring.breakdown
    .map((item) => {
      const pct = item.maxPoints > 0 ? Math.min(100, (item.points / item.maxPoints) * 100) : 0;
      const metricValue =
        typeof item.metric === "number" && !Number.isInteger(item.metric)
          ? formatNumber(item.metric, 8)
          : formatInteger(item.metric);

      return `
        <article class="breakdown-item">
          <div class="breakdown-top">
            <div class="breakdown-name">${escapeHtml(item.name)}</div>
            <div class="breakdown-points">${item.points}/${item.maxPoints}</div>
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" style="width:${pct.toFixed(1)}%"></div>
          </div>
          <div class="breakdown-condition">
            Metric: <strong>${metricValue}</strong> ${escapeHtml(item.metricLabel)}<br>
            Rule: <code>${escapeHtml(item.condition)}</code>
          </div>
          <span class="breakdown-label">${escapeHtml(item.key)}</span>
        </article>
      `;
    })
    .join("");

  if (el.scoreExplanation) {
    el.scoreExplanation.textContent =
      "This score is generated from four transparent components under a locked scoring policy. The labels and thresholds are community-defined and are not official DAC eligibility criteria.";
  }
}

function renderScoringUnavailable(reason) {
  if (!el.scoreBreakdownGrid) return;

  renderScoringPolicy(SCORING_POLICY);

  el.scoreBreakdownGrid.innerHTML = `
    <div class="empty-state compact">
      <div class="empty-icon">◇</div>
      <div class="empty-title">Scoring unavailable</div>
      <div class="empty-sub">${escapeHtml(reason)}</div>
    </div>
  `;

  if (el.scoreExplanation) {
    el.scoreExplanation.textContent =
      "Transparent scoring requires full explorer data. No score is generated from partial, fallback, mock, or random data.";
  }
}

function renderCollections(collections) {
  if (!collections.length) {
    el.collectionCountLabel.textContent = "No verified NFT collection data";
    el.collectionsList.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">✦</div>
        <div class="empty-title">No NFT collection data</div>
        <div class="empty-sub">NFT collections are unavailable until DAC Explorer tokenlist data can be verified.</div>
      </div>
    `;
    return;
  }

  el.collectionCountLabel.textContent = `${collections.length} collection(s)`;

  el.collectionsList.innerHTML = collections
    .map(
      (item, index) => `
        <div class="collection-row">
          <div class="collection-index">${index + 1}</div>
          <div>
            <div class="collection-name">
              ${escapeHtml(item.collection || "Unknown")}
              <span class="collection-symbol">${escapeHtml(item.symbol || "UNKNOWN")}</span>
            </div>
            <div class="collection-contract">${escapeHtml(item.contract || "")}</div>
          </div>
          <div class="collection-amount">
            <strong>${formatInteger(item.amount || 0)}</strong>
            <small>Holdings</small>
          </div>
        </div>
      `
    )
    .join("");
}

function renderJson(output) {
  el.rawJsonOutput.textContent = JSON.stringify(output, null, 2);
}

// ======================================================
// Chain live stats
// ======================================================

async function initChainStats() {
  try {
    const latestHex = await rpcCall("eth_blockNumber", []);
    const latestNum = hexToNumber(latestHex);

    const fetches = [];
    for (let i = 4; i >= 0; i--) {
      const blockNum = Math.max(0, latestNum - i);
      fetches.push(rpcCall("eth_getBlockByNumber", [numberToHex(blockNum), false]));
    }

    const blocks = await Promise.all(fetches);
    state.blockHistory = blocks
      .filter(Boolean)
      .map((block) => ({
        number: hexToNumber(block.number),
        timestamp: hexToNumber(block.timestamp),
        txCount: Array.isArray(block.transactions) ? block.transactions.length : 0,
      }));

    await updateChainStats();
    setInterval(updateChainStats, 13000);
  } catch (error) {
    console.warn("Chain stats unavailable:", error);
    setStatsDead();
  }
}

async function updateChainStats() {
  try {
    const start = performance.now();
    const latestHex = await rpcCall("eth_blockNumber", []);
    const latency = Math.round(performance.now() - start);
    const latestNum = hexToNumber(latestHex);
    const block = await rpcCall("eth_getBlockByNumber", [latestHex, false]);

    if (!block) {
      throw new Error("Latest block unavailable.");
    }

    state.blockHistory.push({
      number: latestNum,
      timestamp: hexToNumber(block.timestamp),
      txCount: Array.isArray(block.transactions) ? block.transactions.length : 0,
    });

    const unique = new Map();
    for (const item of state.blockHistory) unique.set(item.number, item);
    state.blockHistory = [...unique.values()].sort((a, b) => a.number - b.number).slice(-5);

    let tps = "—";
    let blockTime = "—";

    if (state.blockHistory.length >= 2) {
      const oldest = state.blockHistory[0];
      const newest = state.blockHistory[state.blockHistory.length - 1];
      const elapsed = newest.timestamp - oldest.timestamp;

      if (elapsed > 0) {
        const txs = state.blockHistory.slice(1).reduce((sum, item) => sum + item.txCount, 0);
        tps = (txs / elapsed).toFixed(2);
        blockTime = `${(elapsed / (state.blockHistory.length - 1)).toFixed(1)}s`;
      }
    }

    let gas = "—";
    try {
      const gasHex = await rpcCall("eth_gasPrice", []);
      gas = `${formatGwei(gasHex)} Gwei`;
    } catch {
      gas = "—";
    }

    setStat("s-block", `#${latestNum.toLocaleString()}`);
    setStat("s-tps", tps, tps === "—" ? null : parseFloat(tps) < 1 ? "warn" : "good");
    setStat("s-bt", blockTime);
    setStat("s-lat", `${latency}ms`, latency < 200 ? "good" : latency < 600 ? "warn" : "bad");
    setStat("s-gas", gas);
    setLive(true);
  } catch (error) {
    console.warn("Chain stats update failed:", error);
    setStatsDead();
  }
}

function setStat(id, value, cls = null) {
  const node = document.getElementById(id);
  if (!node) return;
  node.textContent = value;
  node.className = `sval${cls ? ` ${cls}` : ""}`;
}

function setLive(isLive) {
  const dot = document.getElementById("s-dot");
  const label = document.getElementById("s-live");
  if (!dot || !label) return;

  if (isLive) {
    dot.classList.remove("dead");
    label.textContent = "LIVE";
    label.style.color = "var(--green)";
  } else {
    dot.classList.add("dead");
    label.textContent = "OFFLINE";
    label.style.color = "var(--text-dim)";
  }
}

function setStatsDead() {
  setLive(false);
  ["s-block", "s-tps", "s-bt", "s-lat", "s-gas"].forEach((id) => setStat(id, "—"));
}

// ======================================================
// Utilities
// ======================================================

async function fetchWithTimeout(url, options = {}, timeoutMs = REQUEST_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs}ms.`);
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

function decimalWeiToNumber(value) {
  return weiBigIntToNumber(BigInt(String(value)));
}

function hexWeiToNumber(hexValue) {
  return weiBigIntToNumber(BigInt(hexValue));
}

function weiBigIntToNumber(wei) {
  const base = 10n ** 18n;
  const whole = wei / base;
  const fraction = wei % base;
  const fractionString = fraction.toString().padStart(18, "0").slice(0, 8);
  return Number(`${whole.toString()}.${fractionString}`);
}

function hexToNumber(hexValue) {
  return Number(BigInt(hexValue || "0x0"));
}

function numberToHex(value) {
  return `0x${Number(value).toString(16)}`;
}

function formatGwei(hexWei) {
  const wei = BigInt(hexWei || "0x0");
  const gwei = Number(wei) / 1e9;
  return gwei.toFixed(2);
}

function isValidEvmAddress(address) {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

function normalizeError(error) {
  if (!error) {
    return {
      name: "UnknownError",
      message: "Unknown error",
    };
  }

  return {
    name: error.name || "Error",
    message: error.message || String(error),
  };
}

function setLoading(isLoading) {
  el.checkButton.disabled = isLoading;
  el.checkButton.textContent = isLoading ? "Checking..." : "Check";
  el.walletInput.disabled = isLoading;
}

function setStatus(type, label, message, icon = "◈") {
  el.statusPanel.className = `status-panel ${type}`;
  el.statusLabel.textContent = label;
  el.statusMessage.textContent = message;
  el.statusIcon.textContent = icon;
}

function setMetric(valueElement, sourceElement, value, source) {
  valueElement.textContent = value;
  sourceElement.textContent = source;
}

function resetView() {
  el.resultPanel.classList.add("hidden");
  el.retryButton.classList.add("hidden");
  el.copyJsonButton.classList.add("hidden");
  state.lastOutput = null;
  if (el.scoreBreakdownGrid) {
    el.scoreBreakdownGrid.innerHTML = `
      <div class="empty-state compact">
        <div class="empty-icon">◇</div>
        <div class="empty-title">No scoring data yet</div>
        <div class="empty-sub">Score components will appear after a full explorer check.</div>
      </div>
    `;
  }
  renderScoringPolicy(SCORING_POLICY);
  if (el.scoreExplanation) {
    el.scoreExplanation.textContent =
      "Full reputation scoring is generated only when all required explorer modules are verified.";
  }
  renderJson({});
}

function formatNumber(value, maxDecimals = 8) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "Unavailable";
  }

  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: maxDecimals,
  });
}

function formatInteger(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "Unavailable";
  }

  return Number(value).toLocaleString();
}

function shortenAddress(address) {
  if (!address || address.length < 12) return address || "";
  return `${address.slice(0, 8)}...${address.slice(-4)}`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return entities[char];
  });
}
