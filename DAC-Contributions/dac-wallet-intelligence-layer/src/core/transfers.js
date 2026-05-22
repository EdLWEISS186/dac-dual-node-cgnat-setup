const axios = require('axios');

const {
  DAC_API
} = require('../config/api');

async function getNFTTransfers(
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

    return response.data.result;

  } catch (err) {

    console.error(
      'NFT Transfer API Error:',
      err.message
    );

    return [];
  }
}

module.exports = {
  getNFTTransfers
};
