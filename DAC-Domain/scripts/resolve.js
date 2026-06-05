const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

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
    throw new Error("DOMAIN_NAME is required. Example: DOMAIN_NAME=jeruzzalem.dac npm run resolve:dac");
  }

  const lower = rawName.trim().toLowerCase();

  if (lower.endsWith(".dac")) {
    return lower;
  }

  return `${lower}.dac`;
}

function formatDate(timestamp) {
  if (!timestamp || Number(timestamp) === 0) {
    return "N/A";
  }

  return new Date(Number(timestamp) * 1000).toISOString();
}

async function main() {
  const deployment = loadDeployment();
  const domainName = normalizeDomain(process.env.DOMAIN_NAME);

  const registry = await hre.ethers.getContractAt(
    "DACDomainRegistry",
    deployment.contractAddress
  );

  console.log("Resolving .dac domain...");
  console.log("Domain:", domainName);
  console.log("Registry:", deployment.contractAddress);

  const record = await registry.getRecord(domainName);

  if (record.owner === hre.ethers.ZeroAddress) {
    console.log("Status: not registered");
    return;
  }

  console.log("Owner:", record.owner);
  console.log("Target:", record.target);
  console.log("Registered At:", formatDate(record.registeredAt));
  console.log("Updated At:", formatDate(record.updatedAt));
  console.log("Expires At:", formatDate(record.expiresAt));
  console.log("Registration Years:", record.registrationYears.toString());
  console.log("Active:", record.active);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
