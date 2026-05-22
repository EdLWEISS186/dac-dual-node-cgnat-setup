function buildActivityAnalytics(
  transfers = [],
  transactionCount = 0,
  totalCollections = 0
) {

  const totalTransfers =
    transfers.length;

  const incoming =
    transfers.filter(
      tx =>
        tx.to &&
        tx.to !== ''
    ).length;

  const outgoing =
    transfers.filter(
      tx =>
        tx.from &&
        tx.from !== ''
    ).length;

  let activityLevel =
    'LOW';

  if (
    transactionCount > 1000
  ) {

    activityLevel = 'HIGH';

  } else if (
    transactionCount > 300
  ) {

    activityLevel = 'MEDIUM';
  }

  let engagementType =
    'CASUAL USER';

  if (
    transactionCount > 1000
  ) {

    engagementType =
      'ADVANCED TESTNET USER';

  } else if (
    transactionCount > 300
  ) {

    engagementType =
      'ACTIVE USER';
  }

  const nftParticipationRatio =
    transactionCount > 0
      ? (
          totalTransfers /
          transactionCount
        ).toFixed(2)
      : '0.00';

  let diversityScore =
    'LOW';

  if (
    totalCollections >= 10
  ) {

    diversityScore =
      'HIGH';

  } else if (
    totalCollections >= 5
  ) {

    diversityScore =
      'MEDIUM';
  }

  return {

    totalTransfers,

    uniqueCollections:
      totalCollections,

    incomingTransfers:
      incoming,

    outgoingTransfers:
      outgoing,

    activityLevel,

    engagementType,

    nftParticipationRatio,

    diversityScore
  };
}

module.exports = {
  buildActivityAnalytics
};
