const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  if (!deployer) {
    throw new Error("No deployer wallet found. Check PRIVATE_KEY in .env.");
  }

  const network = await hre.ethers.provider.getNetwork();
  const balance = await hre.ethers.provider.getBalance(deployer.address);

  console.log("Deploying DACDomainRegistry...");
  console.log("Network:", hre.network.name);
  console.log("Chain ID:", network.chainId.toString());
  console.log("Deployer:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(balance), "DACC");

  const Registry = await hre.ethers.getContractFactory("DACDomainRegistry");
  const registry = await Registry.deploy();

  await registry.waitForDeployment();

  const contractAddress = await registry.getAddress();
  const deploymentTx = registry.deploymentTransaction();

  console.log("DACDomainRegistry deployed:", contractAddress);
  console.log("Deployment TX:", deploymentTx.hash);

  const output = {
    network: "DAC Testnet",
    hardhatNetwork: hre.network.name,
    chainId: Number(network.chainId),
    rpcUrl: process.env.DAC_RPC_URL || "https://rpctest.dachain.tech/",
    explorerUrl: "https://exptest.dachain.tech",
    explorerApiUrl: "https://exptest.dachain.tech/api",
    contractName: "DACDomainRegistry",
    contractAddress,
    deploymentTxHash: deploymentTx.hash,
    deployer: deployer.address,
    deployedAt: new Date().toISOString(),
    pricing: {
      "1_year": "5 DACC",
      "2_years": "8 DACC",
      "3_years": "10 DACC"
    },
    tld: ".dac"
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
