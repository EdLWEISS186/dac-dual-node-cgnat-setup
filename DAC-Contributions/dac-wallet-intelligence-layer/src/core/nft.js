const axios = require('axios');

const {
  DAC_API
} = require('../config/api');

async function getNFTCollections(
  address
) {

  try {

    const response =
      await axios.get(
        DAC_API,
        {
          params: {
            module: 'account',
            action: 'tokennfttx',
            address,
            page: 1,
            offset: 1000,
            sort: 'asc'
          },

          timeout: 15000
        }
      );

    if (
      !response.data ||
      response.data.status !== '1'
    ) {

      return [];
    }

    const collections = {};

    for (
      const tx of response.data.result
    ) {

      const contract =
        tx.contractAddress;

      if (!collections[contract]) {

        collections[contract] = {

          contractAddress:
            contract,

          collectionName:
            tx.tokenName,

          symbol:
            tx.tokenSymbol,

          totalNFTs: 0
        };
      }

      collections[contract]
        .totalNFTs++;
    }

    return Object.values(
      collections
    );

  } catch (err) {

    console.error(
      'NFT API Error:',
      err.message
    );

    return [];
  }
}

module.exports = {
  getNFTCollections
};
