require('dotenv').config();

const DAC_API =
  process.env.DAC_EXPLORER_API ||
  'https://exptest.dachain.tech/api';

module.exports = {
  DAC_API
};
