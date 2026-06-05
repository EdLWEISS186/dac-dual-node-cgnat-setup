const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

const REPLACE_NONCE = Number(process.env.REPLACE_NONCE || "2627");
const GAS_PRICE_GWEI = process.env.GAS_PRICE_GWEI || "100";

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  if (!deployer) {
    throw new Error("No deployer wallet found. Check PRIVATE_KEY in .env.");
  }

  const network = await hre.ethers.provider.getNetwork();
  const balance = await hre.ethers.provider.getBalance(deployer.address);

  const artifact = await hre.artifacts.readArtifact("DACDomainRegistry");
  const gasPrice = hre.ethers.parseUnits(GAS_PRICE_GWEI, "gwei");

  const expectedContractAddress = hre.ethers.getCreateAddress({
    from: deployer.address,
    nonce: REPLACE_NONCE
  });

  console.log("Replacing pending DACDomainRegistry deployment...");
  console.log("Network:", hre.network.name);
  console.log("Chain ID:", network.chainId.toString());
  console.log("Deployer:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(balance), "DACC");
  console.log("Replacement nonce:", REPLACE_NONCE);
  console.log("Gas price:", GAS_PRICE_GWEI, "gwei");
  console.log("Expected contract:", expectedContractAddress);

  const tx = await deployer.sendTransaction({
    nonce: REPLACE_NONCE,
    data: artifact.bytecode,
    gasLimit: 2500000,
    gasPrice
  });

  console.log("Replacement TX submitted:", tx.hash);
  console.log("Explorer:", `https://exptest.dachain.tech/tx/${tx.hash}`);

  const receipt = await tx.wait();

  console.log("Receipt status:", receipt.status);
  console.log("Block:", receipt.blockNumber);
  console.log("Contract address:", receipt.contractAddress);

  if (receipt.status !== 1) {
    throw new Error("Replacement deployment failed.");
  }

  const output = {
    network: "DAC Testnet",
    hardhatNetwork: hre.network.name,
    chainId: Number(network.chainId),
    rpcUrl: process.env.DAC_RPC_URL || "http://127.0.0.1:8546",
    explorerUrl: "https://exptest.dachain.tech",
    explorerApiUrl: "https://exptest.dachain.tech/api",
    contractName: "DACDomainRegistry",
    contractAddress: receipt.contractAddress,
    deploymentTxHash: tx.hash,
    replacedTxHash: "0x0514ff8cf8949c4885f34da793f4a2ada8b10b3dc02c15be80bd3b981b992af6",
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
