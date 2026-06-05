require("dotenv").config();

const fs = require("fs");
const { JsonRpcProvider, Interface } = require("ethers");

const txHashes = process.argv.slice(2);

if (txHashes.length === 0) {
  console.error("Usage: node scripts/decode-events.js <txHash> [txHash...]");
  process.exit(1);
}

const artifact = JSON.parse(
  fs.readFileSync("./artifacts/contracts/DACDomainRegistry.sol/DACDomainRegistry.json", "utf8")
);

async function decodeTx(provider, iface, txHash) {
  const receipt = await provider.getTransactionReceipt(txHash);

  if (!receipt) {
    console.log("\nTX:", txHash);
    console.log("Status: receipt not found");
    return;
  }

  console.log("\nTX:", txHash);
  console.log("Status:", receipt.status);
  console.log("Block:", receipt.blockNumber);
  console.log("Logs:", receipt.logs.length);

  for (const log of receipt.logs) {
    try {
      const parsed = iface.parseLog(log);

      console.log("\nEvent:", parsed.name);

      for (const [key, value] of Object.entries(parsed.args.toObject())) {
        console.log(`${key}:`, value.toString());
      }
    } catch (_) {
      // Skip non-registry logs.
    }
  }
}

async function main() {
  const provider = new JsonRpcProvider(
    process.env.DAC_RPC_URL,
    21894,
    { batchMaxCount: 1 }
  );

  const iface = new Interface(artifact.abi);

  for (const txHash of txHashes) {
    await decodeTx(provider, iface, txHash);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
