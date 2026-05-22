const {
  buildWalletIntelligence,
  printWalletReport
} = require('./src');

(async () => {

  const report =
    await buildWalletIntelligence(
      '0x870ad63acc507cdfd878F170606d19ae78988AFE'
    );

  printWalletReport(report);

})();
