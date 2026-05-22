function buildReputationScore({

  nativeBalance = 0,
  transactionCount = 0,
  totalCollections = 0,
  totalNFTs = 0

}) {

  let score = 0;

  if (transactionCount >= 1000) {
    score += 40;
  } else if (transactionCount >= 500) {
    score += 30;
  } else if (transactionCount >= 100) {
    score += 20;
  } else {
    score += 10;
  }

  if (totalCollections >= 10) {
    score += 25;
  } else if (totalCollections >= 5) {
    score += 15;
  } else {
    score += 5;
  }

  if (totalNFTs >= 200) {
    score += 20;
  } else if (totalNFTs >= 100) {
    score += 15;
  } else {
    score += 5;
  }

  if (nativeBalance >= 5) {
    score += 15;
  } else if (nativeBalance >= 1) {
    score += 10;
  } else {
    score += 5;
  }

  let rating =
    'LOW';

  if (score >= 90) {
    rating = 'ELITE';
  } else if (score >= 75) {
    rating = 'HIGH';
  } else if (score >= 50) {
    rating = 'MEDIUM';
  }

  let trustProfile =
    'STANDARD USER';

  if (
    transactionCount > 1000 &&
    totalCollections > 10
  ) {
    trustProfile =
      'ADVANCED TESTNET PARTICIPANT';
  }

  let sybilRisk =
    'HIGH';

  if (score >= 90) {
    sybilRisk = 'LOW';
  } else if (score >= 70) {
    sybilRisk = 'MEDIUM';
  }

  return {

    reputationScore:
      score,

    rating,

    trustProfile,

    sybilRisk
  };
}

module.exports = {
  buildReputationScore
};
