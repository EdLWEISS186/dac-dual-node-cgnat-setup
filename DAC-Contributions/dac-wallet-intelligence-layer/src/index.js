module.exports = {

  // Core
  ...require('./core/balance'),
  ...require('./core/nft'),
  ...require('./core/transactions'),
  ...require('./core/transfers'),

  // Analytics
  ...require('./analytics/activity'),

  // Intelligence
  ...require('./intelligence/portfolio'),
  ...require('./intelligence/reputation'),
  ...require('./intelligence/wallet'),

  // Formatter
  ...require('./formatter/report')
};
