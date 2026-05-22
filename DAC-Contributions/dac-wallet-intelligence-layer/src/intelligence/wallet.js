const {
  getNativeBalance
} = require('../core/balance');

const {
  getNFTCollections
} = require('../core/nft');

const {
  getTransactionCount
} = require('../core/transactions');

const {
  getNFTTransfers
} = require('../core/transfers');

const {
  buildActivityAnalytics
} = require('../analytics/activity');

const {
  buildPortfolioProfile
} = require('./portfolio');

const {
  buildReputationScore
} = require('./reputation');

async function buildWalletIntelligence(
  address
) {

  const nativeBalance =
    await getNativeBalance(address);

  const nftCollections =
    await getNFTCollections(address);

  const transactionCount =
    await getTransactionCount(address);

  const transfers =
    await getNFTTransfers(address);

  const totalNFTs =
    nftCollections.reduce(
      (sum, item) =>
        sum + Number(item.totalNFTs || 0),
      0
    );

  const analytics =
    buildActivityAnalytics(
      transfers,
      transactionCount,
      nftCollections.length
    );

  const portfolio =
    buildPortfolioProfile({
      nativeBalance,
      nftCollections,
      analytics
    });

  const reputation =
    buildReputationScore({
      nativeBalance,
      transactionCount,
      totalCollections:
        nftCollections.length,
      totalNFTs
    });

  return {
    wallet: address,
    transactionCount,
    portfolio,
    reputation
  };
}

module.exports = {
  buildWalletIntelligence
};
