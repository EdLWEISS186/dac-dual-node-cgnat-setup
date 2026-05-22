function printWalletReport(
  report
) {

  console.log(
    '\n=== DAC Testnet Wallet Intelligence Layer v1 ===\n'
  );

  console.log(
    '🟢 WALLET PROFILE\n'
  );

  console.log(
    `Wallet Address      : ${report.wallet}`
  );

  console.log(
    `Native Balance      : ${report.portfolio.nativeBalance} tDACC`
  );

  console.log(
    `Transactions        : ${report.transactionCount}`
  );

  console.log(
    `NFT Transfers       : ${report.portfolio.activity.totalTransfers}`
  );

  console.log(
    `Collections         : ${report.portfolio.totalCollections}`
  );

  console.log(
    `NFT Holdings        : ${report.portfolio.totalNFTs}\n`
  );

  console.log(
    '📊 ACTIVITY ANALYTICS\n'
  );

  console.log(
    `Activity Level      : ${report.portfolio.activity.activityLevel}`
  );

  console.log(
    `Engagement Type     : ${report.portfolio.activity.engagementType}`
  );

  console.log(
    `NFT Participation   : ${report.portfolio.activity.nftParticipationRatio}`
  );

  console.log(
    `Diversity Score     : ${report.portfolio.activity.diversityScore}\n`
  );

  console.log(
    '💼 PORTFOLIO INTELLIGENCE\n'
  );

  console.log(
    `Portfolio Style     : ${report.portfolio.portfolioStyle}`
  );

  console.log(
    `Wallet Archetype    : ${report.portfolio.walletArchetype}`
  );

  console.log(
    `Top Collection      : ${report.portfolio.topCollection?.name || 'N/A'}`
  );

  console.log(
    `Top Holdings        : ${report.portfolio.topCollection?.amount || 0}`
  );

  console.log(
    `Concentration       : ${report.portfolio.concentration.percentage}%`
  );

  console.log(
    `Concentration Level : ${report.portfolio.concentration.level}\n`
  );

  console.log(
    '🏆 REPUTATION SCORING\n'
  );

  console.log(
    `Reputation Score    : ${report.reputation.reputationScore}/100`
  );

  console.log(
    `Reputation Level    : ${report.reputation.rating}`
  );

  console.log(
    `Trust Profile       : ${report.reputation.trustProfile}`
  );

  console.log(
    `Sybil Risk          : ${report.reputation.sybilRisk}\n`
  );

  console.log(
    '🧠 RAW WALLET INTELLIGENCE JSON\n'
  );

  console.log(
    JSON.stringify(
      report,
      null,
      2
    )
  );
}

module.exports = {
  printWalletReport
};
