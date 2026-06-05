require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const DAC_RPC_URL = process.env.DAC_RPC_URL || "https://rpctest.dachain.tech/";
const PRIVATE_KEY = process.env.PRIVATE_KEY || "";

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    dacTestnet: {
      url: DAC_RPC_URL,
      chainId: 21894,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    }
  },
  paths: {
    sources: "./contracts",
    artifacts: "./artifacts",
    cache: "./cache"
  }
};
