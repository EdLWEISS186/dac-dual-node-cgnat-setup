const axios = require('axios');

const {
  DAC_API
} = require('../config/api');

async function getNativeBalance(
  address
) {

  try {

    const response =
      await axios.get(
        DAC_API,
        {
          params: {
            module: 'account',
            action: 'balance',
            address
          },

          timeout: 15000
        }
      );

    if (
      !response.data ||
      response.data.status !== '1'
    ) {

      return 0;
    }

    const wei =
      BigInt(response.data.result);

    return Number(
      (
        Number(wei) / 1e18
      ).toFixed(8)
    );

  } catch (err) {

    console.error(
      'Balance API Error:',
      err.message
    );

    return 0;
  }
}

module.exports = {
  getNativeBalance
};
