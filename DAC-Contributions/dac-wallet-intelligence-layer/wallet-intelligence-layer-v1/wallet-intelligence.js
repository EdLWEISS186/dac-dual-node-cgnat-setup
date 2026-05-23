"use strict";

// ======================================================
// DAC Wallet Intelligence Layer v1
// DAC Sender-inspired UI version.
// No wallet connection, no signing, no mock score.
// ======================================================

const DAC_EXPLORER_API = "https://exptest.dachain.tech/api";
const DAC_RPC_URL = "https://rpctest.dachain.tech/";
const DAC_CHAIN_ID = 21894;
const NATIVE_SYMBOL = "DACC";
const REQUEST_TIMEOUT_MS = 18000;
const APP_VERSION = "v1.4.2";
const HISTORY_BLOCK_TIMESTAMP_RPC_LIMIT = 90;

const DACC_STAKING_CONTRACT = "0x3691A78bE270dB1f3b1a86177A8f23F89A8Cef24";
const STAKE_BALANCE_OF_SELECTOR = "0x70a08231"; // optional balanceOf(address) read
const STAKE_FUNCTION_SELECTOR = "0x3a4b66f1";
const UNSTAKE_FUNCTION_SELECTOR = "0x2e17de78";



const KNOWN_COLLECTION_REGISTRY = Object.freeze([
  Object.freeze({
    id: "dac-inception-rank",
    name: "DAC Inception Rank",
    symbol: "RANK",
    standard: "DRC-721",
    contract: "0xB36ab4c2Bd6aCfC36e9D6c53F39F4301901Bd647",
    category: "official-dac-inception-progress-badge",
    role: "Progress badge / rank NFT",
    source: "DAC Inception dashboard / DAC Explorer",
    scoringEffect: "reputation-score-component",
    note:
      "Known collection registry entry. Detection does not modify the locked v1.2.0 reputation score.",
    rankThresholds: Object.freeze([
      { rank: "CADET", qe: 0 },
      { rank: "COMMANDO", qe: 1000 },
      { rank: "SEAL", qe: 2000 },
      { rank: "SHADOW UNIT", qe: 5000 },
      { rank: "VANGUARD", qe: 10000 },
      { rank: "SENTINEL", qe: 25000 },
      { rank: "SOVEREIGN", qe: 50000 },
      { rank: "WARRIOR", qe: 100000 },
      { rank: "ARCHITECT", qe: 200000 },
      { rank: "INTERCEPTOR", qe: 300000 },
      { rank: "PHANTOM", qe: 400000 },
      { rank: "CIPHER", qe: 500000 },
      { rank: "CROWN", qe: 750000 },
    ]),
  }),
]);


function getRankScoreByBadgeCount(rankBadgeCount) {
  const count = Number(rankBadgeCount || 0);

  if (count >= 13) return { points: 30, inferredRank: "CROWN", rule: "rankBadgeCount >= 13" };
  if (count >= 12) return { points: 28, inferredRank: "CIPHER", rule: "rankBadgeCount >= 12" };
  if (count >= 11) return { points: 27, inferredRank: "PHANTOM", rule: "rankBadgeCount >= 11" };
  if (count >= 10) return { points: 25, inferredRank: "INTERCEPTOR", rule: "rankBadgeCount >= 10" };
  if (count >= 9) return { points: 23, inferredRank: "ARCHITECT", rule: "rankBadgeCount >= 9" };
  if (count >= 8) return { points: 21, inferredRank: "WARRIOR", rule: "rankBadgeCount >= 8" };
  if (count >= 7) return { points: 19, inferredRank: "SOVEREIGN", rule: "rankBadgeCount >= 7" };
  if (count >= 6) return { points: 16, inferredRank: "SENTINEL", rule: "rankBadgeCount >= 6" };
  if (count >= 5) return { points: 13, inferredRank: "VANGUARD", rule: "rankBadgeCount >= 5" };
  if (count >= 4) return { points: 10, inferredRank: "SHADOW UNIT", rule: "rankBadgeCount >= 4" };
  if (count >= 3) return { points: 8, inferredRank: "SEAL", rule: "rankBadgeCount >= 3" };
  if (count >= 2) return { points: 6, inferredRank: "COMMANDO", rule: "rankBadgeCount >= 2" };
  if (count >= 1) return { points: 3, inferredRank: "CADET", rule: "rankBadgeCount >= 1" };

  return { points: 0, inferredRank: "NONE", rule: "rankBadgeCount = 0" };
}



function getNativeFundsScore(nativeBalance) {
  const amount = Number(nativeBalance || 0);

  if (amount >= 100) return { points: 15, tier: "100+ DACC", rule: "nativeBalance >= 100" };
  if (amount >= 75) return { points: 14, tier: "75+ DACC", rule: "nativeBalance >= 75" };
  if (amount >= 50) return { points: 12, tier: "50+ DACC", rule: "nativeBalance >= 50" };
  if (amount >= 25) return { points: 9, tier: "25+ DACC", rule: "nativeBalance >= 25" };
  if (amount >= 10) return { points: 6, tier: "10+ DACC", rule: "nativeBalance >= 10" };
  if (amount >= 5) return { points: 4, tier: "5+ DACC", rule: "nativeBalance >= 5" };

  return { points: 2, tier: "<5 DACC", rule: "nativeBalance < 5" };
}

function getStakedDaccScore(stakedDacc) {
  const amount = Number(stakedDacc || 0);

  if (amount >= 200) return { points: 20, tier: "200+ DACC", rule: "stakedDacc >= 200" };
  if (amount >= 150) return { points: 18, tier: "150+ DACC", rule: "stakedDacc >= 150" };
  if (amount >= 100) return { points: 15, tier: "100+ DACC", rule: "stakedDacc >= 100" };
  if (amount >= 50) return { points: 11, tier: "50+ DACC", rule: "stakedDacc >= 50" };
  if (amount >= 20) return { points: 7, tier: "20+ DACC", rule: "stakedDacc >= 20" };
  if (amount >= 10) return { points: 4, tier: "10+ DACC", rule: "stakedDacc >= 10" };

  return { points: 0, tier: "<10 DACC", rule: "stakedDacc < 10" };
}

const SCORING_POLICY = Object.freeze({
  version: "WIL-v1.3.3",
  policyId: "WIL-2026-05-v1.3.3",
  status: "LOCKED",
  model: "stake-aware-reputation-scoring-v1.3.3",
  maxScore: 100,
  components: Object.freeze({
    transactionScore: Object.freeze({
      maxPoints: 20,
      thresholds: Object.freeze([
        { condition: "txCount >= 1000", points: 20 },
        { condition: "txCount >= 500", points: 15 },
        { condition: "txCount >= 100", points: 10 },
        { condition: "txCount < 100", points: 5 },
      ]),
    }),
    nftDiversityScore: Object.freeze({
      maxPoints: 10,
      thresholds: Object.freeze([
        { condition: "totalCollections >= 10", points: 10 },
        { condition: "totalCollections >= 5", points: 6 },
        { condition: "totalCollections < 5", points: 2 },
      ]),
    }),
    nftHoldingsScore: Object.freeze({
      maxPoints: 10,
      thresholds: Object.freeze([
        { condition: "totalNFTs >= 200", points: 10 },
        { condition: "totalNFTs >= 100", points: 7 },
        { condition: "totalNFTs < 100", points: 3 },
      ]),
    }),
    nativeBalanceScore: Object.freeze({
      maxPoints: 15,
      thresholds: Object.freeze([
        { condition: "nativeBalance >= 100", points: 15 },
        { condition: "nativeBalance >= 75", points: 14 },
        { condition: "nativeBalance >= 50", points: 12 },
        { condition: "nativeBalance >= 25", points: 9 },
        { condition: "nativeBalance >= 10", points: 6 },
        { condition: "nativeBalance >= 5", points: 4 },
        { condition: "nativeBalance < 5", points: 2 },
      ]),
    }),
    daccStakeScore: Object.freeze({
      maxPoints: 20,
      contract: "0x3691A78bE270dB1f3b1a86177A8f23F89A8Cef24",
      thresholds: Object.freeze([
        { condition: "stakedDacc >= 200", points: 20 },
        { condition: "stakedDacc >= 150", points: 18 },
        { condition: "stakedDacc >= 100", points: 15 },
        { condition: "stakedDacc >= 50", points: 11 },
        { condition: "stakedDacc >= 20", points: 7 },
        { condition: "stakedDacc >= 10", points: 4 },
        { condition: "stakedDacc < 10", points: 0 },
      ]),
    }),
    dacInceptionRankScore: Object.freeze({
      maxPoints: 25,
      thresholds: Object.freeze([
        { condition: "rankBadgeCount >= 13", inferredRank: "CROWN", points: 25 },
        { condition: "rankBadgeCount >= 12", inferredRank: "CIPHER", points: 24 },
        { condition: "rankBadgeCount >= 11", inferredRank: "PHANTOM", points: 23 },
        { condition: "rankBadgeCount >= 10", inferredRank: "INTERCEPTOR", points: 21 },
        { condition: "rankBadgeCount >= 9", inferredRank: "ARCHITECT", points: 20 },
        { condition: "rankBadgeCount >= 8", inferredRank: "WARRIOR", points: 18 },
        { condition: "rankBadgeCount >= 7", inferredRank: "SOVEREIGN", points: 16 },
        { condition: "rankBadgeCount >= 6", inferredRank: "SENTINEL", points: 14 },
        { condition: "rankBadgeCount >= 5", inferredRank: "VANGUARD", points: 11 },
        { condition: "rankBadgeCount >= 4", inferredRank: "SHADOW UNIT", points: 9 },
        { condition: "rankBadgeCount >= 3", inferredRank: "SEAL", points: 7 },
        { condition: "rankBadgeCount >= 2", inferredRank: "COMMANDO", points: 5 },
        { condition: "rankBadgeCount >= 1", inferredRank: "CADET", points: 3 },
        { condition: "rankBadgeCount = 0", inferredRank: "NONE", points: 0 },
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
    "Community-defined scoring heuristic. v1.3.3 uses stake/unstake transaction-flow classification for DACC staking when a verified staking getter is unavailable. This is not an official DAC reputation, eligibility, or Sybil system.",
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
  stakedDaccValue: document.getElementById("stakedDaccValue"),
  stakedDaccSource: document.getElementById("stakedDaccSource"),
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
  inceptionRankValue: document.getElementById("inceptionRankValue"),
  stakedDaccProfileValue: document.getElementById("stakedDaccProfileValue"),

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
  knownRegistryStatusLabel: document.getElementById("knownRegistryStatusLabel"),
  rankDetectionCard: document.getElementById("rankDetectionCard"),
  rankDetectionStatus: document.getElementById("rankDetectionStatus"),
  rankDetectionDetail: document.getElementById("rankDetectionDetail"),
  rankContractShort: document.getElementById("rankContractShort"),
  rankThresholdsList: document.getElementById("rankThresholdsList"),
  historicalModeLabel: document.getElementById("historicalModeLabel"),
  historicalWindowRow: document.getElementById("historicalWindowRow"),
  historicalNote: document.getElementById("historicalNote"),
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
      output.historicalActivity = await getHistoricalActivitySafely(address);
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
      output.historicalActivity = await getHistoricalActivitySafely(address);
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
    stakedDacc: () => getStakedDaccFromExplorer(address),
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

  if (okCount === 5) {
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
        stakedDacc: modules.stakedDacc.value,
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
        "Full wallet intelligence requires native balance, NFT collections, transaction history, NFT transfer, and DACC staking modules.",
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


async function getStakedDaccFromExplorer(address) {
  const results = await Promise.allSettled([
    getStakedDaccFromBalanceOf(address),
    getStakedDaccFromStakeFlowClassifier(address),
  ]);

  const direct = results[0].status === "fulfilled" ? results[0].value : null;
  const classifier = results[1].status === "fulfilled" ? results[1].value : null;

  // Prefer the stake-flow classifier when it has observed stake/unstake flow,
  // because the staking contract is not verified and balanceOf(address) may not
  // be the correct getter for current stake.
  if (classifier && classifier.flowTxCount > 0) {
    return {
      ...classifier,
      directContractRead: direct || null,
      source: direct && direct.amount === classifier.amount
        ? "DAC Explorer stake-flow classifier + matching direct contract read"
        : "DAC Explorer stake-flow classifier",
      confidence: direct && direct.amount === classifier.amount
        ? "VERY_HIGH"
        : classifier.rewardTraceAvailable
          ? "HIGH"
          : "MEDIUM_HIGH",
    };
  }

  if (direct && direct.amount > 0) {
    return {
      ...direct,
      confidence: "VERY_HIGH",
      note:
        "Direct contract read returned a positive value. This is treated as current stake, but exact semantics depend on the staking contract getter.",
    };
  }

  if (classifier) {
    return classifier;
  }

  if (direct) {
    return direct;
  }

  const errors = results
    .filter((item) => item.status === "rejected")
    .map((item) => normalizeError(item.reason));

  throw new Error(`Staked DACC module failed: ${JSON.stringify(errors)}`);
}

async function getStakedDaccFromBalanceOf(address) {
  const data = STAKE_BALANCE_OF_SELECTOR + encodeAddressParam(address);
  const result = await rpcCall("eth_call", [
    {
      to: DACC_STAKING_CONTRACT,
      data,
    },
    "latest",
  ]);

  if (!isValidUint256Hex(result)) {
    throw new Error("Staking contract balanceOf(address) returned invalid data.");
  }

  return {
    amount: hexWeiToNumber(result),
    source: "DAC RPC balanceOf(address)",
    mode: "DIRECT_CONTRACT_READ",
    contract: DACC_STAKING_CONTRACT,
    confidence: "VERY_HIGH",
  };
}

async function getStakedDaccFromStakeFlowClassifier(address) {
  const data = await explorerRequest({
    module: "account",
    action: "txlist",
    address,
    startblock: 0,
    endblock: 99999999,
    sort: "asc",
  });

  const txs = normalizeExplorerArrayResult(data);
  const wallet = normalizeAddress(address);
  const stakingContract = normalizeAddress(DACC_STAKING_CONTRACT);

  let totalStakeInWei = 0n;
  let totalUnstakeOutWei = 0n;
  let unclassifiedContractInWei = 0n;
  let stakeTxCount = 0;
  let unstakeTxCount = 0;
  const flowHashes = [];

  for (const tx of txs) {
    const from = normalizeAddress(tx.from);
    const to = normalizeAddress(tx.to);
    const input = normalizeInput(tx.input || tx.data || "");
    const value = parseBigIntValue(tx.value || "0");
    const hash = tx.hash || tx.transactionHash;

    if (from !== wallet || to !== stakingContract) {
      continue;
    }

    if (input.startsWith(STAKE_FUNCTION_SELECTOR) && value > 0n) {
      totalStakeInWei += value;
      stakeTxCount += 1;
      if (hash) flowHashes.push(hash);
      continue;
    }

    if (input.startsWith(UNSTAKE_FUNCTION_SELECTOR)) {
      const decodedAmount = decodeFirstUint256FromInput(input);

      if (decodedAmount !== null) {
        totalUnstakeOutWei += decodedAmount;
        unstakeTxCount += 1;
        if (hash) flowHashes.push(hash);
      }

      continue;
    }

    // Safety bucket: value sent to the staking contract without recognized selector.
    // This is not used for current stake scoring, but is kept in raw output.
    if (value > 0n) {
      unclassifiedContractInWei += value;
    }
  }

  const estimatedCurrentStakeWei =
    totalStakeInWei > totalUnstakeOutWei
      ? totalStakeInWei - totalUnstakeOutWei
      : 0n;

  const rewardInfo = await getStakeRewardFlow(address, flowHashes);

  return {
    amount: weiBigIntToNumber(estimatedCurrentStakeWei),
    source: "DAC Explorer stake/unstake transaction-flow classifier",
    mode: "STAKE_FLOW_CLASSIFIER",
    contract: DACC_STAKING_CONTRACT,
    confidence: rewardInfo.available ? "HIGH" : "MEDIUM_HIGH",
    stakeSelector: STAKE_FUNCTION_SELECTOR,
    unstakeSelector: UNSTAKE_FUNCTION_SELECTOR,
    totalStakeIn: weiBigIntToNumber(totalStakeInWei),
    totalUnstakeOut: weiBigIntToNumber(totalUnstakeOutWei),
    estimatedCurrentStake: weiBigIntToNumber(estimatedCurrentStakeWei),
    rewardReceived: rewardInfo.available ? weiBigIntToNumber(rewardInfo.rewardWei) : null,
    contractOutTotal: rewardInfo.available ? weiBigIntToNumber(rewardInfo.contractOutWei) : null,
    rewardTraceAvailable: rewardInfo.available,
    rewardReadMode: rewardInfo.mode,
    stakeTxCount,
    unstakeTxCount,
    flowTxCount: stakeTxCount + unstakeTxCount,
    unclassifiedContractIn: weiBigIntToNumber(unclassifiedContractInWei),
    note:
      "Estimated current stake is calculated as total recognized stake-in minus decoded unstake-out. Contract-to-wallet internal transfers are separated as reward/return flow and are not subtracted from stake unless decoded from the unstake calldata.",
  };
}

async function getStakeRewardFlow(address, flowHashes) {
  if (!flowHashes.length) {
    return {
      available: false,
      mode: "NO_FLOW_TX",
      rewardWei: 0n,
      contractOutWei: 0n,
    };
  }

  const wallet = normalizeAddress(address);
  const stakingContract = normalizeAddress(DACC_STAKING_CONTRACT);
  const hashSet = new Set(flowHashes.map((hash) => normalizeHash(hash)));

  // First try legacy Etherscan-compatible internal tx API by address.
  try {
    const data = await explorerRequest({
      module: "account",
      action: "txlistinternal",
      address,
      startblock: 0,
      endblock: 99999999,
      sort: "asc",
    });

    const internalTxs = normalizeExplorerArrayResult(data);
    const rewardWei = sumContractOutToWallet(internalTxs, wallet, stakingContract, hashSet);

    return {
      available: true,
      mode: "LEGACY_TXLISTINTERNAL_BY_ADDRESS",
      rewardWei,
      contractOutWei: rewardWei,
    };
  } catch (error) {
    console.warn("Legacy internal tx by address failed:", error);
  }

  // Then try Blockscout v2 internal transaction route per hash.
  try {
    let rewardWei = 0n;

    for (const hash of flowHashes.slice(-30)) {
      const internalTxs = await explorerV2Request(
        `/api/v2/transactions/${encodeURIComponent(hash)}/internal-transactions`
      );

      rewardWei += sumContractOutToWallet(
        normalizeBlockscoutItems(internalTxs),
        wallet,
        stakingContract,
        new Set([normalizeHash(hash)])
      );
    }

    return {
      available: true,
      mode: "BLOCKSCOUT_V2_INTERNAL_TXS_BY_HASH",
      rewardWei,
      contractOutWei: rewardWei,
    };
  } catch (error) {
    console.warn("Blockscout v2 internal tx by hash failed:", error);
  }

  return {
    available: false,
    mode: "INTERNAL_TRACE_UNAVAILABLE",
    rewardWei: 0n,
    contractOutWei: 0n,
  };
}

async function explorerV2Request(path) {
  const response = await fetchWithTimeout(
    `https://exptest.dachain.tech${path}`,
    {},
    REQUEST_TIMEOUT_MS
  );

  if (!response.ok) {
    throw new Error(`Explorer v2 HTTP ${response.status}`);
  }

  return response.json();
}

function normalizeBlockscoutItems(data) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.items)) return data.items;
  if (data && Array.isArray(data.result)) return data.result;
  return [];
}

function sumContractOutToWallet(items, wallet, stakingContract, hashSet) {
  let total = 0n;

  for (const item of items) {
    const from = normalizeAddress(item.from && item.from.hash ? item.from.hash : item.from);
    const to = normalizeAddress(item.to && item.to.hash ? item.to.hash : item.to);
    const value = parseBigIntValue(item.value || "0");
    const hash = normalizeHash(
      item.transactionHash || item.transaction_hash || item.txHash || item.hash
    );

    if (from === stakingContract && to === wallet && value > 0n) {
      if (!hashSet.size || !hash || hashSet.has(hash)) {
        total += value;
      }
    }
  }

  return total;
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
    appVersion: APP_VERSION,
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
  const stakedDacc = data.stakedDacc;

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

  const knownCollectionRegistry = buildKnownCollectionSignals(nftCollections);
  const rankSignal = getRankSignalFromRegistry(knownCollectionRegistry);

  const reputationScoring = buildReputationScore({
    nativeBalance,
    txCount,
    totalCollections,
    totalNFTs,
    rankBadgeCount: rankSignal ? rankSignal.holdings : 0,
    stakedDacc: stakedDacc ? stakedDacc.amount : 0,
  });

  return {
    wallet: address,
    appVersion: APP_VERSION,
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
    stakedDacc: {
      token: "DACC",
      amount: stakedDacc ? stakedDacc.amount : 0,
      source: stakedDacc ? stakedDacc.source : "Unavailable",
      mode: stakedDacc ? stakedDacc.mode : "UNAVAILABLE",
      confidence: stakedDacc ? stakedDacc.confidence : "UNAVAILABLE",
      contract: DACC_STAKING_CONTRACT,
      stakeSelector: stakedDacc ? stakedDacc.stakeSelector : undefined,
      unstakeSelector: stakedDacc ? stakedDacc.unstakeSelector : undefined,
      totalStakeIn: stakedDacc ? stakedDacc.totalStakeIn : undefined,
      totalUnstakeOut: stakedDacc ? stakedDacc.totalUnstakeOut : undefined,
      estimatedCurrentStake: stakedDacc ? stakedDacc.estimatedCurrentStake : undefined,
      rewardReceived: stakedDacc ? stakedDacc.rewardReceived : undefined,
      contractOutTotal: stakedDacc ? stakedDacc.contractOutTotal : undefined,
      rewardTraceAvailable: stakedDacc ? stakedDacc.rewardTraceAvailable : undefined,
      rewardReadMode: stakedDacc ? stakedDacc.rewardReadMode : undefined,
      stakeTxCount: stakedDacc ? stakedDacc.stakeTxCount : undefined,
      unstakeTxCount: stakedDacc ? stakedDacc.unstakeTxCount : undefined,
      flowTxCount: stakedDacc ? stakedDacc.flowTxCount : undefined,
      unclassifiedContractIn: stakedDacc ? stakedDacc.unclassifiedContractIn : undefined,
      directContractRead: stakedDacc ? stakedDacc.directContractRead : undefined,
      note: stakedDacc ? stakedDacc.note : undefined,
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
    knownCollectionRegistry,
    nftCollections: nftCollections.map((nft) => ({
      collection: nft.name,
      symbol: nft.symbol,
      contract: nft.contractAddress,
      amount: Number(nft.balance || 0),
      knownCollection: getKnownCollectionByContract(nft.contractAddress),
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
  rankBadgeCount = 0,
  stakedDacc = 0,
}) {
  const transactionScore =
    txCount >= 1000 ? 20 : txCount >= 500 ? 15 : txCount >= 100 ? 10 : 5;

  const nftDiversityScore =
    totalCollections >= 10 ? 10 : totalCollections >= 5 ? 6 : 2;

  const nftHoldingsScore =
    totalNFTs >= 200 ? 10 : totalNFTs >= 100 ? 7 : 3;

  const nativeScore = getNativeFundsScore(nativeBalance);
  const nativeBalanceScore = nativeScore.points;

  const stakeScore = getStakedDaccScore(stakedDacc);
  const daccStakeScore = stakeScore.points;

  const rankScore = getRankScoreByBadgeCount(rankBadgeCount);
  const dacInceptionRankScore = Math.min(rankScore.points, 25);

  const score =
    transactionScore +
    nftDiversityScore +
    nftHoldingsScore +
    nativeBalanceScore +
    daccStakeScore +
    dacInceptionRankScore;

  let reputationLevel = "LOW";

  if (score >= 90) {
    reputationLevel = "ELITE";
  } else if (score >= 75) {
    reputationLevel = "HIGH";
  } else if (score >= 50) {
    reputationLevel = "MEDIUM";
  }

  let trustProfile = "STANDARD USER";

  if (rankBadgeCount >= 6 && stakedDacc >= 50) {
    trustProfile = "VERIFIED INCEPTION PARTICIPANT";
  }

  if (txCount > 1000 && totalCollections > 10 && rankBadgeCount >= 6 && stakedDacc >= 100) {
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
      maxPoints: 20,
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
      maxPoints: 10,
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
      maxPoints: 10,
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
      name: "Native Funds Score",
      points: nativeBalanceScore,
      maxPoints: 15,
      metric: nativeBalance,
      metricLabel: "DACC",
      condition: nativeScore.rule,
      tier: nativeScore.tier,
    },
    {
      key: "daccStakeScore",
      name: "DACC Stake Score",
      points: daccStakeScore,
      maxPoints: 20,
      metric: stakedDacc,
      metricLabel: "staked DACC",
      condition: stakeScore.rule,
      tier: stakeScore.tier,
    },
    {
      key: "dacInceptionRankScore",
      name: "DAC Inception Rank Score",
      points: dacInceptionRankScore,
      maxPoints: 25,
      metric: rankBadgeCount,
      metricLabel: "RANK badge(s)",
      condition: rankScore.rule,
      inferredRank: rankScore.inferredRank,
    },
  ];

  return {
    reputationScore: score,
    reputationLevel,
    trustProfile,
    sybilRisk,
    scoringPolicy: SCORING_POLICY,
    nativeFundsSignal: {
      balance: nativeBalance,
      tier: nativeScore.tier,
      points: nativeBalanceScore,
      maxPoints: 15,
      rule: nativeScore.rule,
    },
    officialStakeSignal: {
      contract: DACC_STAKING_CONTRACT,
      stakedDacc,
      tier: stakeScore.tier,
      points: daccStakeScore,
      maxPoints: 20,
      rule: stakeScore.rule,
    },
    officialRankSignal: {
      contract: KNOWN_COLLECTION_REGISTRY[0].contract,
      rankBadgeCount,
      inferredRank: rankScore.inferredRank,
      points: dacInceptionRankScore,
      maxPoints: 25,
      rule: rankScore.rule,
    },
    breakdown,
  };
}// ======================================================
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
  const stakedDacc = modules.stakedDacc && modules.stakedDacc.ok ? modules.stakedDacc.value : null;

  const totalCollections = Array.isArray(nftCollections) ? nftCollections.length : null;
  const totalNFTs = Array.isArray(nftCollections)
    ? nftCollections.reduce((sum, nft) => sum + Number(nft.balance || 0), 0)
    : null;

  return {
    wallet: address,
    appVersion: APP_VERSION,
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
      stakedDacc: Boolean(modules.stakedDacc && modules.stakedDacc.ok),
    },
    moduleErrors: Object.fromEntries(
      Object.entries(modules)
        .filter(([, item]) => !item.ok)
        .map(([key, item]) => [key, item.error])
    ),
    warning:
      "Full reputation score was not generated because one or more required explorer modules could not be verified.",
    nativeBalance: nativeBalance === null ? null : { token: NATIVE_SYMBOL, balance: nativeBalance },
    stakedDacc:
      stakedDacc === null
        ? null
        : {
            token: "DACC",
            amount: stakedDacc.amount,
            source: stakedDacc.source,
            mode: stakedDacc.mode,
            confidence: stakedDacc.confidence,
            contract: DACC_STAKING_CONTRACT,
            stakeSelector: stakedDacc.stakeSelector,
            unstakeSelector: stakedDacc.unstakeSelector,
            totalStakeIn: stakedDacc.totalStakeIn,
            totalUnstakeOut: stakedDacc.totalUnstakeOut,
            estimatedCurrentStake: stakedDacc.estimatedCurrentStake,
            rewardReceived: stakedDacc.rewardReceived,
            contractOutTotal: stakedDacc.contractOutTotal,
            rewardTraceAvailable: stakedDacc.rewardTraceAvailable,
            rewardReadMode: stakedDacc.rewardReadMode,
            stakeTxCount: stakedDacc.stakeTxCount,
            unstakeTxCount: stakedDacc.unstakeTxCount,
            flowTxCount: stakedDacc.flowTxCount,
            unclassifiedContractIn: stakedDacc.unclassifiedContractIn,
            directContractRead: stakedDacc.directContractRead,
            note: stakedDacc.note,
          },
    metrics: {
      totalTransactions: transactionCount,
      nftTransfers,
      totalCollections,
      totalNFTs,
    },
    activityAnalytics: null,
    portfolioIntelligence: null,
    reputationScoring: null,
    knownCollectionRegistry: Array.isArray(nftCollections)
      ? buildKnownCollectionSignals(nftCollections)
      : null,
    nftCollections: Array.isArray(nftCollections)
      ? nftCollections.map((nft) => ({
          collection: nft.name,
          symbol: nft.symbol,
          contract: nft.contractAddress,
          amount: Number(nft.balance || 0),
          knownCollection: getKnownCollectionByContract(nft.contractAddress),
        }))
      : null,
    generatedAt: new Date().toISOString(),
  };
}

function buildFailedOutput(address, explorerError, rpcError) {
  return {
    wallet: address,
    appVersion: APP_VERSION,
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


function normalizeAddress(value) {
  return String(value || "").trim().toLowerCase();
}

function getKnownCollectionByContract(contractAddress) {
  const normalized = normalizeAddress(contractAddress);

  if (!normalized) return null;

  return (
    KNOWN_COLLECTION_REGISTRY.find(
      (item) => normalizeAddress(item.contract) === normalized
    ) || null
  );
}

function buildKnownCollectionSignals(nftCollections) {
  const matched = [];

  for (const registryItem of KNOWN_COLLECTION_REGISTRY) {
    const collection = nftCollections.find(
      (item) => normalizeAddress(item.contractAddress) === normalizeAddress(registryItem.contract)
    );

    const holdings = collection ? Number(collection.balance || 0) : 0;
    const rankScore = getRankScoreByBadgeCount(holdings);

    matched.push({
      ...registryItem,
      detected: Boolean(collection && holdings > 0),
      holdings,
      inferredRank: rankScore.inferredRank,
      rankScore: rankScore.points,
      maxRankScore: 30,
      rankScoreRule: rankScore.rule,
      explorerCollectionName: collection ? collection.name : null,
      explorerSymbol: collection ? collection.symbol : null,
    });
  }

  return {
    registryVersion: "known-collection-registry-v1.3.3",
    source: "Community-maintained known collection registry",
    scoringEffect: "reputation-score-component",
    note:
      "DAC Inception Rank is included as a 30-point component in the locked WIL-v1.3.3 reputation score.",
    matched,
  };
}



function getInceptionRankLabel(output) {
  const signal = output && output.reputationScoring && output.reputationScoring.officialRankSignal;

  if (!signal) return "Unavailable";

  if (!signal.rankBadgeCount || signal.rankBadgeCount <= 0 || signal.inferredRank === "NONE") {
    return "Not Detected";
  }

  return `${signal.inferredRank} (${signal.rankBadgeCount} RANK)`;
}



async function getHistoricalActivitySafely(address) {
  try {
    return await getHistoricalActivityFromExplorer(address);
  } catch (error) {
    console.warn("Historical activity windowing failed:", error);

    return {
      status: "UNAVAILABLE",
      mode: "UNAVAILABLE",
      confidence: "LOW",
      error: normalizeError(error),
      note:
        "Historical windows could not be generated from the available explorer data.",
      windows: buildEmptyHistoricalWindows(),
      generatedAt: new Date().toISOString(),
    };
  }
}

async function getHistoricalActivityFromExplorer(address) {
  const [txResult, nftResult] = await Promise.allSettled([
    explorerRequest({
      module: "account",
      action: "txlist",
      address,
      startblock: 0,
      endblock: 99999999,
      sort: "asc",
    }),
    explorerRequest({
      module: "account",
      action: "tokennfttx",
      address,
    }),
  ]);

  const txs =
    txResult.status === "fulfilled"
      ? normalizeExplorerArrayResult(txResult.value)
      : [];

  const nftTxs =
    nftResult.status === "fulfilled"
      ? normalizeExplorerArrayResult(nftResult.value)
      : [];

  if (!txs.length && !nftTxs.length) {
    return {
      status: "READY",
      mode: "NO_ACTIVITY_RETURNED",
      confidence: "MEDIUM",
      note:
        "Explorer returned no transaction or NFT transfer rows for this wallet.",
      windows: buildHistoricalWindows({
        txs: [],
        nftTxs: [],
        nowSeconds: Math.floor(Date.now() / 1000),
      }),
      dataCoverage: {
        txRows: 0,
        nftTransferRows: 0,
        timestampedTxRows: 0,
        timestampedNftRows: 0,
      },
      generatedAt: new Date().toISOString(),
    };
  }

  const timestampResolution = await resolveHistoricalTimestamps([...txs, ...nftTxs]);

  const enrichedTxs = txs.map((tx) => ({
    ...tx,
    __timestamp: getResolvedTimestamp(tx, timestampResolution.blockTimestampMap),
  }));

  const enrichedNftTxs = nftTxs.map((tx) => ({
    ...tx,
    __timestamp: getResolvedTimestamp(tx, timestampResolution.blockTimestampMap),
  }));

  const timestampedTxRows = enrichedTxs.filter((tx) => Number.isFinite(tx.__timestamp)).length;
  const timestampedNftRows = enrichedNftTxs.filter((tx) => Number.isFinite(tx.__timestamp)).length;

  const hasDirectTimestamp =
    [...txs, ...nftTxs].some((tx) => Number.isFinite(readTimestampSeconds(tx)));

  const mode = hasDirectTimestamp
    ? "TIMESTAMP_BASED"
    : timestampResolution.mode;

  const confidence =
    mode === "TIMESTAMP_BASED"
      ? "HIGH"
      : mode === "BLOCK_TIMESTAMP_FALLBACK"
        ? "MEDIUM"
        : mode === "BLOCK_TIMESTAMP_FALLBACK_LIMITED"
          ? "LOW_MEDIUM"
          : "LOW";

  return {
    status: "READY",
    mode,
    confidence,
    windows: buildHistoricalWindows({
      txs: enrichedTxs,
      nftTxs: enrichedNftTxs,
      nowSeconds: Math.floor(Date.now() / 1000),
    }),
    dataCoverage: {
      txRows: txs.length,
      nftTransferRows: nftTxs.length,
      timestampedTxRows,
      timestampedNftRows,
      blockTimestampResolved: timestampResolution.resolvedCount,
      blockTimestampRequested: timestampResolution.requestedCount,
      blockTimestampLimit: HISTORY_BLOCK_TIMESTAMP_RPC_LIMIT,
    },
    note: getHistoricalModeNote(mode),
    generatedAt: new Date().toISOString(),
  };
}

async function resolveHistoricalTimestamps(rows) {
  const rowsWithoutTimestamp = rows.filter((row) => !Number.isFinite(readTimestampSeconds(row)));
  const blockNumbers = [
    ...new Set(
      rowsWithoutTimestamp
        .map((row) => normalizeBlockNumber(row.blockNumber || row.block_number))
        .filter((value) => value !== null)
    ),
  ];

  if (!blockNumbers.length) {
    return {
      mode: "NO_TIMESTAMP_AVAILABLE",
      blockTimestampMap: {},
      requestedCount: 0,
      resolvedCount: 0,
    };
  }

  const limitedBlockNumbers = blockNumbers.slice(-HISTORY_BLOCK_TIMESTAMP_RPC_LIMIT);
  const blockTimestampMap = {};

  await Promise.all(
    limitedBlockNumbers.map(async (blockNumber) => {
      try {
        const block = await rpcCall("eth_getBlockByNumber", [numberToHex(blockNumber), false]);

        if (block && block.timestamp) {
          blockTimestampMap[String(blockNumber)] = hexToNumber(block.timestamp);
        }
      } catch (error) {
        console.warn(`Block timestamp fallback failed for block ${blockNumber}:`, error);
      }
    })
  );

  const resolvedCount = Object.keys(blockTimestampMap).length;

  return {
    mode:
      blockNumbers.length > HISTORY_BLOCK_TIMESTAMP_RPC_LIMIT
        ? "BLOCK_TIMESTAMP_FALLBACK_LIMITED"
        : "BLOCK_TIMESTAMP_FALLBACK",
    blockTimestampMap,
    requestedCount: blockNumbers.length,
    resolvedCount,
  };
}

function buildHistoricalWindows({ txs, nftTxs, nowSeconds }) {
  const definitions = [
    { key: "7d", label: "7D", seconds: 7 * 24 * 60 * 60 },
    { key: "30d", label: "30D", seconds: 30 * 24 * 60 * 60 },
    { key: "allTime", label: "All Time", seconds: null },
  ];

  return Object.fromEntries(
    definitions.map((definition) => {
      const minTimestamp =
        definition.seconds === null ? null : nowSeconds - definition.seconds;

      const txWindow = filterRowsByWindow(txs, minTimestamp);
      const nftWindow = filterRowsByWindow(nftTxs, minTimestamp);
      const stakeWindow = buildStakeWindowMetrics(txWindow);

      return [
        definition.key,
        {
          label: definition.label,
          windowSeconds: definition.seconds,
          transactions: txWindow.length,
          nftTransfers: nftWindow.length,
          stakeEvents: stakeWindow.stakeEvents,
          unstakeEvents: stakeWindow.unstakeEvents,
          stakeIn: stakeWindow.stakeIn,
          unstakeOut: stakeWindow.unstakeOut,
          netStakeFlow: stakeWindow.netStakeFlow,
        },
      ];
    })
  );
}

function buildStakeWindowMetrics(txs) {
  const walletStakeTxs = txs.filter((tx) => {
    const to = normalizeAddress(tx.to);
    return to === normalizeAddress(DACC_STAKING_CONTRACT);
  });

  let stakeInWei = 0n;
  let unstakeOutWei = 0n;
  let stakeEvents = 0;
  let unstakeEvents = 0;

  for (const tx of walletStakeTxs) {
    const input = normalizeInput(tx.input || tx.data || "");
    const value = parseBigIntValue(tx.value || "0");

    if (input.startsWith(STAKE_FUNCTION_SELECTOR) && value > 0n) {
      stakeInWei += value;
      stakeEvents += 1;
      continue;
    }

    if (input.startsWith(UNSTAKE_FUNCTION_SELECTOR)) {
      const decodedAmount = decodeFirstUint256FromInput(input);

      if (decodedAmount !== null) {
        unstakeOutWei += decodedAmount;
        unstakeEvents += 1;
      }
    }
  }

  const netWei = stakeInWei > unstakeOutWei ? stakeInWei - unstakeOutWei : 0n;

  return {
    stakeEvents,
    unstakeEvents,
    stakeIn: weiBigIntToNumber(stakeInWei),
    unstakeOut: weiBigIntToNumber(unstakeOutWei),
    netStakeFlow: weiBigIntToNumber(netWei),
  };
}

function filterRowsByWindow(rows, minTimestamp) {
  if (minTimestamp === null) return rows;

  return rows.filter((row) => Number.isFinite(row.__timestamp) && row.__timestamp >= minTimestamp);
}

function readTimestampSeconds(row) {
  const direct =
    row.timeStamp ||
    row.timestamp ||
    row.block_timestamp ||
    row.blockTimestamp ||
    row.date;

  if (!direct) return null;

  if (typeof direct === "number") {
    return direct > 1e12 ? Math.floor(direct / 1000) : Math.floor(direct);
  }

  const text = String(direct).trim();

  if (/^\d+$/.test(text)) {
    const num = Number(text);
    return num > 1e12 ? Math.floor(num / 1000) : Math.floor(num);
  }

  const parsed = Date.parse(text);

  if (Number.isFinite(parsed)) {
    return Math.floor(parsed / 1000);
  }

  return null;
}

function getResolvedTimestamp(row, blockTimestampMap) {
  const direct = readTimestampSeconds(row);

  if (Number.isFinite(direct)) {
    return direct;
  }

  const blockNumber = normalizeBlockNumber(row.blockNumber || row.block_number);

  if (blockNumber === null) {
    return null;
  }

  const fallback = blockTimestampMap[String(blockNumber)];

  return Number.isFinite(fallback) ? fallback : null;
}

function normalizeBlockNumber(value) {
  if (value === null || value === undefined || value === "") return null;

  try {
    if (typeof value === "number") return value;
    const text = String(value).trim();
    return text.startsWith("0x") || text.startsWith("0X")
      ? Number(BigInt(text))
      : Number(text);
  } catch {
    return null;
  }
}

function buildEmptyHistoricalWindows() {
  return {
    "7d": emptyHistoricalWindow("7D"),
    "30d": emptyHistoricalWindow("30D"),
    allTime: emptyHistoricalWindow("All Time"),
  };
}

function emptyHistoricalWindow(label) {
  return {
    label,
    windowSeconds: null,
    transactions: null,
    nftTransfers: null,
    stakeEvents: null,
    unstakeEvents: null,
    stakeIn: null,
    unstakeOut: null,
    netStakeFlow: null,
  };
}

function getHistoricalModeNote(mode) {
  switch (mode) {
    case "TIMESTAMP_BASED":
      return "Explorer rows include timestamp data. Windows are calculated directly from transaction timestamps. Stake Tx Count is transaction count; Net Staked is the net DACC amount staked.";
    case "BLOCK_TIMESTAMP_FALLBACK":
      return "Explorer rows did not fully include timestamp data. The checker resolved block timestamps through RPC. Stake Tx Count is transaction count; Net Staked is the net DACC amount staked.";
    case "BLOCK_TIMESTAMP_FALLBACK_LIMITED":
      return "Explorer rows did not fully include timestamp data. Only the most recent block timestamps were resolved to avoid excessive RPC requests. Stake Tx Count is transaction count; Net Staked is the net DACC amount staked.";
    case "NO_TIMESTAMP_AVAILABLE":
      return "Explorer rows did not include timestamp or block data usable for historical windowing.";
    case "NO_ACTIVITY_RETURNED":
      return "Explorer returned no activity rows for this wallet.";
    default:
      return "Historical activity support was auto-detected from explorer response data.";
  }
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
    el.stakedDaccValue,
    el.stakedDaccSource,
    output.stakedDacc ? `${formatNumber(output.stakedDacc.amount, 8)} DACC` : "Unavailable",
    output.stakedDacc
      ? `${output.stakedDacc.mode || "STAKE_SIGNAL"} · ${output.stakedDacc.confidence || "UNKNOWN"}`
      : "Unavailable"
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
  if (el.inceptionRankValue) {
    el.inceptionRankValue.textContent = getInceptionRankLabel(output);
  }
  if (el.stakedDaccProfileValue) {
    el.stakedDaccProfileValue.textContent = output.stakedDacc
      ? `${formatNumber(output.stakedDacc.amount, 2)} DACC · ${output.stakedDacc.confidence || "UNKNOWN"}`
      : "Unavailable";
  }
  el.sybilRiskValue.textContent = output.reputationScoring.sybilRisk;

  renderHistoricalActivity(output.historicalActivity);
  renderScoringBreakdown(output.reputationScoring);
  renderKnownCollectionRegistry(output.knownCollectionRegistry);
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
    el.stakedDaccValue,
    el.stakedDaccSource,
    output.stakedDacc
      ? `${formatNumber(output.stakedDacc.amount, 8)} DACC`
      : "Unavailable",
    output.availableData.stakedDacc
      ? `${output.stakedDacc.mode || "STAKE_SIGNAL"} · ${output.stakedDacc.confidence || "UNKNOWN"}`
      : "Module failed"
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
  renderHistoricalActivity(output.historicalActivity);
  renderScoringUnavailable("Not generated because one or more required explorer modules failed.");
  renderKnownCollectionRegistry(output.knownCollectionRegistry);
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
  setMetric(el.stakedDaccValue, el.stakedDaccSource, "Unavailable", "Explorer/contract read required");
  setMetric(el.collectionsValue, el.collectionsSource, "Unavailable", "Explorer required");
  setMetric(el.nftHoldingsValue, el.nftHoldingsSource, "Unavailable", "Explorer required");

  fillUnavailableModules("RPC fallback");
  renderHistoricalActivity(null);
  renderScoringUnavailable("Not generated in RPC fallback mode. Explorer data is required for full scoring.");
  renderKnownCollectionRegistry(null);
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
  setMetric(el.stakedDaccValue, el.stakedDaccSource, "Unavailable", "Explorer / RPC down");
  setMetric(el.transactionsValue, el.transactionsSource, "Unavailable", "Explorer / RPC down");
  setMetric(el.collectionsValue, el.collectionsSource, "Unavailable", "Explorer down");
  setMetric(el.nftHoldingsValue, el.nftHoldingsSource, "Unavailable", "Explorer down");

  fillUnavailableModules("No verified data");
  renderHistoricalActivity(null);
  renderScoringUnavailable("No verified explorer or RPC data was available.");
  renderKnownCollectionRegistry(null);
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
  if (el.inceptionRankValue) {
    el.inceptionRankValue.textContent = "Unavailable";
  }
  if (el.stakedDaccProfileValue) {
    el.stakedDaccProfileValue.textContent = "Unavailable";
  }
  el.sybilRiskValue.textContent = "Unavailable";
}





function getRankSignalFromRegistry(registry) {
  if (!registry || !Array.isArray(registry.matched)) return null;

  return (
    registry.matched.find((item) => item.id === "dac-inception-rank") || null
  );
}



function renderHistoricalActivity(historicalActivity) {
  if (!el.historicalWindowRow) return;

  if (!historicalActivity || !historicalActivity.windows) {
    if (el.historicalModeLabel) {
      el.historicalModeLabel.textContent = "Not checked";
    }

    el.historicalWindowRow.innerHTML = `
      <article class="history-window-card muted">
        <div class="history-window-title">No data yet</div>
        <div class="history-window-sub">Run a wallet check to calculate 7D / 30D / All Time activity windows.</div>
      </article>
    `;

    if (el.historicalNote) {
      el.historicalNote.textContent =
        "Historical windows are calculated from explorer timestamps when available. Stake Tx Count shows transaction count, while Net Staked shows the net DACC amount staked.";
    }

    return;
  }

  if (el.historicalModeLabel) {
    el.historicalModeLabel.textContent = `${historicalActivity.mode || "UNKNOWN"} · ${historicalActivity.confidence || "UNKNOWN"}`;
  }

  const windows = [
    historicalActivity.windows["7d"],
    historicalActivity.windows["30d"],
    historicalActivity.windows.allTime,
  ].filter(Boolean);

  el.historicalWindowRow.innerHTML = windows
    .map((window) => {
      return `
        <article class="history-window-card">
          <div class="history-window-title">
            ${escapeHtml(window.label)}
            <small>${window.windowSeconds ? "RECENT" : "LIFETIME"}</small>
          </div>
          <div class="history-metrics">
            <div class="history-metric">
              <span>Transactions</span>
              <strong>${formatNullableInteger(window.transactions)}</strong>
            </div>
            <div class="history-metric">
              <span>NFT Transfers</span>
              <strong>${formatNullableInteger(window.nftTransfers)}</strong>
            </div>
            <div class="history-metric">
              <span>Stake Tx Count</span>
              <strong>${formatNullableInteger(window.stakeEvents)}</strong>
            </div>
            <div class="history-metric">
              <span>Unstake Tx Count</span>
              <strong>${formatNullableInteger(window.unstakeEvents)}</strong>
            </div>
          </div>
          ${
            window.label === "All Time"
              ? `<div class="history-current-stake">
                  Estimated Current Stake: <strong>${formatNullableNumber(window.netStakeFlow, 4)} DACC</strong>
                </div>`
              : ""
          }
          <div class="history-stake-line">
            Net Staked: <strong>${formatNullableNumber(window.netStakeFlow, 4)} DACC</strong><br>
            Stake In: ${formatNullableNumber(window.stakeIn, 4)} DACC · Stake Out: ${formatNullableNumber(window.unstakeOut, 4)} DACC
          </div>
        </article>
      `;
    })
    .join("");

  if (el.historicalNote) {
    const coverage = historicalActivity.dataCoverage
      ? ` Coverage: ${formatInteger(historicalActivity.dataCoverage.timestampedTxRows || 0)}/${formatInteger(historicalActivity.dataCoverage.txRows || 0)} tx rows timestamped, ${formatInteger(historicalActivity.dataCoverage.timestampedNftRows || 0)}/${formatInteger(historicalActivity.dataCoverage.nftTransferRows || 0)} NFT rows timestamped.`
      : "";

    el.historicalNote.textContent = `${historicalActivity.note || "Historical windows generated."}${coverage}`;
  }
}

function formatNullableInteger(value) {
  return value === null || value === undefined ? "—" : formatInteger(value);
}

function formatNullableNumber(value, maxDecimals = 4) {
  return value === null || value === undefined ? "—" : formatNumber(value, maxDecimals);
}


function renderKnownCollectionRegistry(registry) {
  const rankEntry = KNOWN_COLLECTION_REGISTRY[0];
  const signal =
    registry && Array.isArray(registry.matched)
      ? registry.matched.find((item) => item.id === "dac-inception-rank")
      : null;

  if (el.knownRegistryStatusLabel) {
    el.knownRegistryStatusLabel.textContent = registry
      ? registry.registryVersion || "known-collection-registry-v1.3.3"
      : "Community registry v1.3.3";
  }

  if (el.rankContractShort) {
    el.rankContractShort.textContent = shortenAddress(rankEntry.contract);
    el.rankContractShort.title = rankEntry.contract;
  }

  if (el.rankDetectionCard) {
    el.rankDetectionCard.classList.remove("detected", "not-detected");
    el.rankDetectionCard.classList.add(signal && signal.detected ? "detected" : "not-detected");
  }

  if (el.rankDetectionStatus) {
    el.rankDetectionStatus.textContent =
      signal && signal.detected ? "Detected" : registry ? "Not Detected" : "Not Checked";
  }

  if (el.rankDetectionDetail) {
    if (signal && signal.detected) {
      el.rankDetectionDetail.innerHTML =
        `${signal.holdings} RANK badge holding(s) found.` +
        `<span class="rank-detected-line">Inferred rank: <span class="rank-highlight">${escapeHtml(signal.inferredRank)}</span> · Rank score: ${signal.rankScore}/25.</span>`;
    } else if (registry) {
      el.rankDetectionDetail.textContent =
        "No DAC Inception Rank badge detected in the current explorer tokenlist response.";
    } else {
      el.rankDetectionDetail.textContent =
        "Run a wallet check to detect known DAC badge ownership.";
    }
  }

  renderRankThresholds(rankEntry.rankThresholds, signal && signal.detected);
}

function renderRankThresholds(thresholds, detected) {
  if (!el.rankThresholdsList) return;

  el.rankThresholdsList.innerHTML = thresholds
    .map((item) => {
      const cls = detected ? "detected" : "";
      return `
        <div class="rank-threshold-row ${cls}">
          <span>${escapeHtml(item.rank)}</span>
          <span>${formatInteger(item.qe)} QE</span>
        </div>
      `;
    })
    .join("");
}


function renderScoringPolicy(policy) {
  const safePolicy = policy || SCORING_POLICY;

  if (el.scoringPolicyLabel) {
    el.scoringPolicyLabel.textContent = safePolicy.version || "WIL-v1.3.3";
  }

  if (el.policyIdValue) {
    el.policyIdValue.textContent = safePolicy.policyId || "WIL-2026-05-v1.3.3";
  }

  if (el.policyStatusValue) {
    el.policyStatusValue.textContent = safePolicy.status || "LOCKED";
  }

  if (el.policyMaxScoreValue) {
    el.policyMaxScoreValue.textContent = String(safePolicy.maxScore || 100);
  }

  if (el.policyEngineValue) {
    el.policyEngineValue.textContent = safePolicy.model || "rank-aware-reputation-scoring-v1.3.3";
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
      "This score is generated from six transparent components under a locked scoring policy: transaction activity, NFT diversity, NFT holdings, native funds, DACC stake-flow signal, and DAC Inception Rank. The stake signal uses recognized stake-in minus decoded unstake-out where direct contract getter data is unavailable. The labels and thresholds are community-defined and are not official DAC eligibility criteria.";
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
              ${
                item.knownCollection
                  ? `<span class="known-collection-badge">Known DAC</span>`
                  : ""
              }
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



function normalizeInput(value) {
  const text = String(value || "").trim().toLowerCase();

  if (!text) return "0x";

  return text.startsWith("0x") ? text : `0x${text}`;
}

function normalizeHash(value) {
  return String(value || "").trim().toLowerCase();
}

function parseBigIntValue(value) {
  if (typeof value === "bigint") return value;

  const text = String(value || "0").trim();

  if (!text) return 0n;

  try {
    return text.startsWith("0x") || text.startsWith("0X")
      ? BigInt(text)
      : BigInt(text);
  } catch {
    return 0n;
  }
}

function decodeFirstUint256FromInput(input) {
  const normalized = normalizeInput(input);
  const raw = normalized.replace(/^0x/, "");

  if (raw.length < 8 + 64) {
    return null;
  }

  const firstArg = raw.slice(8, 8 + 64);

  if (!/^[0-9a-fA-F]{64}$/.test(firstArg)) {
    return null;
  }

  return BigInt(`0x${firstArg}`);
}


function encodeAddressParam(address) {
  return String(address || "").toLowerCase().replace(/^0x/, "").padStart(64, "0");
}

function isValidUint256Hex(value) {
  return /^0x[0-9a-fA-F]{64}$/.test(String(value || ""));
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
  renderKnownCollectionRegistry(null);
  renderHistoricalActivity(null);
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
