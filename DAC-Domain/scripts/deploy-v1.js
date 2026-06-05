const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

const GAS_PRICE_GWEI = process.env.GAS_PRICE_GWEI || "100";
const GAS_LIMIT = Number(process.env.GAS_LIMIT || "2500000");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  if (!deployer) {
    throw new Error("No deployer wallet found. Check PRIVATE_KEY in .env.");
  }

  const network = await hre.ethers.provider.getNetwork();
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  const latestNonce = await hre.ethers.provider.getTransactionCount(deployer.address, "latest");
  const pendingNonce = await hre.ethers.provider.getTransactionCount(deployer.address, "pending");
  const gasPrice = hre.ethers.parseUnits(GAS_PRICE_GWEI, "gwei");

  console.log("Deploying DACDomainRegistry v1...");
  console.log("Network:", hre.network.name);
  console.log("Chain ID:", network.chainId.toString());
  console.log("Deployer:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(balance), "DACC");
  console.log("Latest nonce:", latestNonce);
  console.log("Pending nonce:", pendingNonce);
  console.log("Gas price:", GAS_PRICE_GWEI, "gwei");
  console.log("Gas limit:", GAS_LIMIT);

  if (latestNonce !== pendingNonce) {
    throw new Error("Pending nonce detected. Resolve pending tx before deploying v1.");
  }

  const Registry = await hre.ethers.getContractFactory("DACDomainRegistry");

  const registry = await Registry.deploy({
    gasPrice,
    gasLimit: GAS_LIMIT
  });

  const tx = registry.deploymentTransaction();
  const expectedAddress = await registry.getAddress();

  console.log("Deployment TX submitted:", tx.hash);
  console.log("Expected contract:", expectedAddress);
  console.log("Explorer:", `https://exptest.dachain.tech/tx/${tx.hash}`);

  const receipt = await tx.wait();

  console.log("Receipt status:", receipt.status);
  console.log("Block:", receipt.blockNumber);
  console.log("Contract address:", receipt.contractAddress);

  if (receipt.status !== 1) {
    throw new Error("v1 deployment failed.");
  }

  const output = {
    network: "DAC Testnet",
    hardhatNetwork: hre.network.name,
    chainId: Number(network.chainId),
    rpcUrl: process.env.DAC_RPC_URL || "http://127.0.0.1:8546",
    explorerUrl: "https://exptest.dachain.tech",
    explorerApiUrl: "https://exptest.dachain.tech/api",
    contractName: "DACDomainRegistry",
    version: "v1.0.0-explorer-friendly",
    contractAddress: receipt.contractAddress,
    deploymentTxHash: tx.hash,
    deployer: deployer.address,
    deployedAt: new Date().toISOString(),
    previousVersion: {
      version: "v0.5-archived-prototype",
      contractAddress: "0x72BD75723ADA5e37F6bA4b8909864c3bbaBccB63",
      deploymentTxHash: "0xe97e92b860257dacdbb791ad5d12862127d9e8d0b74c28e063df44f2f68968e5"
    },
    pricing: {
      "1_year": "5 DACC",
      "2_years": "8 DACC",
      "3_years": "10 DACC"
    },
    tld: ".dac",
    eventModel: {
      indexedNameHash: "bytes32 indexed nameHash",
      readableName: "string name"
    }
  };

  const outputPath = path.join(__dirname, "..", "deployments", "dac-testnet.json");

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n");

  console.log("Deployment metadata saved:", outputPath);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
