const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

const PRICES = {
  1: "5",
  2: "8",
  3: "10"
};

function loadDeployment() {
  const deploymentPath = path.join(__dirname, "..", "deployments", "dac-testnet.json");

  if (!fs.existsSync(deploymentPath)) {
    throw new Error("Deployment metadata not found. Run npm run deploy:dac first.");
  }

  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));

  if (!deployment.contractAddress) {
    throw new Error("Contract address missing in deployments/dac-testnet.json.");
  }

  return deployment;
}

function normalizeDomain(rawName) {
  if (!rawName) {
    throw new Error("DOMAIN_NAME is required. Example: DOMAIN_NAME=jeruzzalem.dac npm run register:dac");
  }

  const lower = rawName.trim().toLowerCase();

  if (lower.endsWith(".dac")) {
    return lower;
  }

  return `${lower}.dac`;
}

async function main() {
  const deployment = loadDeployment();

  const domainName = normalizeDomain(process.env.DOMAIN_NAME);
  const registrationYears = Number(process.env.REGISTRATION_YEARS || "1");

  if (![1, 2, 3].includes(registrationYears)) {
    throw new Error("REGISTRATION_YEARS must be 1, 2, or 3.");
  }

  const price = hre.ethers.parseEther(PRICES[registrationYears]);

  const [registrant] = await hre.ethers.getSigners();

  if (!registrant) {
    throw new Error("No registrant wallet found. Check PRIVATE_KEY in .env.");
  }

  const registry = await hre.ethers.getContractAt(
    "DACDomainRegistry",
    deployment.contractAddress,
    registrant
  );

  console.log("Registering .dac domain...");
  console.log("Domain:", domainName);
  console.log("Years:", registrationYears);
  console.log("Price:", PRICES[registrationYears], "DACC");
  console.log("Registrant:", registrant.address);
  console.log("Registry:", deployment.contractAddress);

  const available = await registry.isAvailable(domainName);

  if (!available) {
    throw new Error(`${domainName} is not available.`);
  }

  const tx = await registry.register(domainName, registrationYears, {
    value: price
  });

  console.log("Submitted TX:", tx.hash);

  const receipt = await tx.wait();

  console.log("Registered:", domainName);
  console.log("Block:", receipt.blockNumber);
  console.log("Explorer:", `${deployment.explorerUrl}/tx/${tx.hash}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
