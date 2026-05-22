const {
  getNativeBalance
} = require('./src');

(async () => {

  const balance =
    await getNativeBalance(
      '0xYourWalletAddress'
    );

  console.log(balance);

})();
