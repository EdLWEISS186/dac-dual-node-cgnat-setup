function buildPortfolioProfile({

  nativeBalance = 0,
  nftCollections = [],
  analytics = {}

}) {

  const totalNFTs =
    nftCollections.reduce(
      (sum, item) =>
        sum + Number(item.totalNFTs || 0),
      0
    );

  const topCollection =
    nftCollections.reduce(
      (top, item) =>
        !top ||
        Number(item.totalNFTs) >
        Number(top.totalNFTs)
          ? item
          : top,
      null
    );

  const concentration =
    topCollection && totalNFTs > 0
      ? (
          Number(topCollection.totalNFTs) /
          totalNFTs
        ) * 100
      : 0;

  let concentrationLevel =
    'LOW';

  if (concentration >= 50) {
    concentrationLevel = 'HIGH';
  } else if (concentration >= 25) {
    concentrationLevel = 'MEDIUM';
  }

  let portfolioStyle =
    'BALANCED';

  if (
    totalNFTs > 100 &&
    nftCollections.length > 10
  ) {
    portfolioStyle = 'NFT HEAVY';
  }

  let walletArchetype =
    'STANDARD USER';

  if (
    analytics.engagementType ===
    'ADVANCED TESTNET USER'
  ) {
    walletArchetype =
      'ADVANCED ECOSYSTEM USER';
  }

  return {

    nativeBalance,

    totalCollections:
      nftCollections.length,

    totalNFTs,

    collections:
      nftCollections,

    topCollection:
      topCollection
        ? {
            name:
              topCollection.collectionName,

            symbol:
              topCollection.symbol,

            amount:
              Number(topCollection.totalNFTs)
          }
        : null,

    concentration: {
      percentage:
        concentration.toFixed(2),

      level:
        concentrationLevel
    },

    portfolioStyle,

    walletArchetype,

    activity:
      analytics
  };
}

module.exports = {
  buildPortfolioProfile
};
