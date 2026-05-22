const axios = require('axios');

const {
  DAC_API
} = require('../config/api');

async function getTransactionCount(
  address
) {

  try {

    const response =
      await axios.get(
        DAC_API,
        {
          params: {
            module: 'account',
            action: 'txlist',
            address,
            startblock: 0,
            endblock: 99999999,
            sort: 'asc'
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

    return response.data.result.length;

  } catch (err) {

    console.error(
      'Transaction API Error:',
      err.message
    );

    return 0;
  }
}

module.exports = {
  getTransactionCount
};
