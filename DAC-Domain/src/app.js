import { ethers } from "https://cdn.jsdelivr.net/npm/ethers@6.13.4/+esm";

const DAC_CHAIN_ID_DECIMAL = 21894;
const DAC_CHAIN_ID_HEX = "0x5586";
const DAC_RPC_URL = "https://rpctest.dachain.tech/";
const DAC_EXPLORER_URL = "https://exptest.dachain.tech";
const DEFAULT_REGISTRY_ADDRESS = "0x90F07E7EFa772c40B90d68BB54267Ea0658a090F";

const BACKGROUNDS = [
  "./assets/background/bg-1.png",
  "./assets/background/bg-2.png",
  "./assets/background/bg-3.png"
];

const PRICES = {
  1: "5",
  2: "8",
  3: "10"
};

const REGISTRY_ABI = [
  "function register(string name, uint8 registrationYears) payable",
  "function renew(string name, uint8 addedYears) payable",
  "function updateTarget(string name, address newTarget)",
  "function setPrimaryDomain(string name)",
  "function clearPrimaryDomain()",
  "function resolve(string name) view returns (address)",
  "function getRecord(string name) view returns (address owner, address target, uint256 registeredAt, uint256 updatedAt, uint256 expiresAt, uint8 registrationYears, bool active)",
  "function isAvailable(string name) view returns (bool)",
  "function getDomainsByOwner(address owner) view returns (string[] memory)",
  "function getPrimaryDomain(address owner) view returns (string memory)"
];

const els = {
  bgA: document.querySelector(".bg-a"),
  bgB: document.querySelector(".bg-b"),

  walletArea: document.querySelector(".wallet-area"),
  walletBox: document.querySelector("#walletBox"),
  walletMenu: document.querySelector("#walletMenu"),
  disconnectBtn: document.querySelector("#disconnectBtn"),

  registerTabBtn: document.querySelector("#registerTabBtn"),
  managementTabBtn: document.querySelector("#managementTabBtn"),
  registerPanel: document.querySelector("#registerPanel"),
  managementPanel: document.querySelector("#managementPanel"),

  contractAddressInput: document.querySelector("#contractAddressInput"),
  saveContractBtn: document.querySelector("#saveContractBtn"),
  activeContract: document.querySelector("#activeContract"),

  registerLabel: document.querySelector("#registerLabel"),
  registrationPreview: document.querySelector("#registrationPreview"),
  availabilityCard: document.querySelector("#availabilityCard"),
  availabilityIcon: document.querySelector("#availabilityIcon"),
  availabilityTitle: document.querySelector("#availabilityTitle"),
  availabilityDescription: document.querySelector("#availabilityDescription"),
  availabilityMeta: document.querySelector("#availabilityMeta"),
  durationOptions: document.querySelectorAll(".duration-option"),
  totalPrice: document.querySelector("#totalPrice"),
  registerBtn: document.querySelector("#registerBtn"),

  refreshDomainsBtn: document.querySelector("#refreshDomainsBtn"),
  clearPrimaryBtn: document.querySelector("#clearPrimaryBtn"),
  primaryDomainText: document.querySelector("#primaryDomainText"),
  domainList: document.querySelector("#domainList"),
  domainEmptyState: document.querySelector("#domainEmptyState"),

  inlineStatus: document.querySelector("#inlineStatus")
};

let browserProvider;
let signer;
let selectedAddress = null;
let selectedYears = 1;
let typedDomainAvailable = false;
let availabilityTimer = null;

let currentBgIndex = 0;
let showingLayerA = true;

function startBackgroundSlideshow() {
  els.bgA.style.backgroundImage = `url("${BACKGROUNDS[0]}")`;
  els.bgA.classList.add("visible");

  BACKGROUNDS.forEach((src) => {
    const image = new Image();
    image.src = src;
  });

  setInterval(() => {
    currentBgIndex = (currentBgIndex + 1) % BACKGROUNDS.length;

    const nextImage = BACKGROUNDS[currentBgIndex];
    const incoming = showingLayerA ? els.bgB : els.bgA;
    const outgoing = showingLayerA ? els.bgA : els.bgB;

    incoming.style.backgroundImage = `url("${nextImage}")`;
    incoming.classList.add("visible");
    outgoing.classList.remove("visible");

    showingLayerA = !showingLayerA;
  }, 10000);
}

function shortAddress(address) {
  if (!address || !ethers.isAddress(address)) {
    return "Not connected";
  }

  return `${address.slice(0, 8)}...${address.slice(-6)}`;
}

function formatBalance(value) {
  return Number(ethers.formatEther(value)).toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3
  });
}

function formatDate(timestamp) {
  if (!timestamp || Number(timestamp) === 0) {
    return "N/A";
  }

  return new Date(Number(timestamp) * 1000).toLocaleDateString("en-US");
}

function cleanLabel(rawValue) {
  return rawValue
    .trim()
    .toLowerCase()
    .replace(/\.dac$/i, "")
    .replace(/[^a-z0-9-]/g, "")
    .replace(/-{2,}/g, "-");
}

function buildDomain(labelValue) {
  const label = cleanLabel(labelValue);

  if (!label) {
    throw new Error("Domain name is required.");
  }

  if (label.startsWith("-") || label.endsWith("-")) {
    throw new Error("Domain cannot start or end with hyphen.");
  }

  return `${label}.dac`;
}

function setStatus(message, isError = false) {
  els.inlineStatus.textContent = message;
  els.inlineStatus.classList.toggle("error", isError);
}

function getSavedContractAddress() {
  return localStorage.getItem("dacDomainRegistryAddress") || DEFAULT_REGISTRY_ADDRESS;
}

function hasRegistryAddress() {
  return ethers.isAddress(getSavedContractAddress());
}

function saveContractAddress(address) {
  localStorage.setItem("dacDomainRegistryAddress", address);
  els.activeContract.textContent = address;
}

function getContractAddress() {
  const address = getSavedContractAddress();

  if (!address || !ethers.isAddress(address)) {
    throw new Error("Registry contract address is not set or invalid.");
  }

  return address;
}

function getRegistry(readOnly = false) {
  const contractAddress = getContractAddress();

  if (readOnly) {
    const provider = new ethers.JsonRpcProvider(DAC_RPC_URL, DAC_CHAIN_ID_DECIMAL);
    return new ethers.Contract(contractAddress, REGISTRY_ABI, provider);
  }

  if (!signer) {
    throw new Error("Wallet is not connected.");
  }

  return new ethers.Contract(contractAddress, REGISTRY_ABI, signer);
}

function updateRegisterButtonState() {
  const hasDomain = cleanLabel(els.registerLabel.value).length > 0;

  els.registerBtn.disabled = !(hasDomain && hasRegistryAddress() && selectedAddress && typedDomainAvailable);
}

function setAvailabilityState(state, title, description, meta = "") {
  els.registrationPreview.classList.remove("hidden");

  els.availabilityCard.className = `availability-card ${state}`;
  els.availabilityIcon.textContent = state === "available" ? "✓" : state === "unavailable" ? "✕" : "○";
  els.availabilityTitle.textContent = title;
  els.availabilityDescription.textContent = description;
  els.availabilityMeta.innerHTML = meta;

  typedDomainAvailable = state === "available";

  updateRegisterButtonState();
}

function resetAvailabilityState() {
  typedDomainAvailable = false;
  els.registrationPreview.classList.add("hidden");
  updateRegisterButtonState();
}

function switchTab(tab) {
  const isRegister = tab === "register";

  els.registerTabBtn.classList.toggle("active", isRegister);
  els.managementTabBtn.classList.toggle("active", !isRegister);

  els.registerPanel.classList.toggle("active", isRegister);
  els.managementPanel.classList.toggle("active", !isRegister);

  if (!isRegister) {
    loadOwnedDomains();
  }
}

function updateWalletBoxDisconnected() {
  els.walletBox.className = "wallet-box disconnected";
  els.walletBox.innerHTML = `<span>Connect Wallet</span>`;
  hideWalletMenu();
}

function updateWalletBoxConnected(balanceFormatted, address) {
  els.walletBox.className = "wallet-box connected";
  els.walletBox.innerHTML = `
    <span class="wallet-balance">${balanceFormatted} DACC</span>
    <span class="divider-vertical"></span>
    <span class="wallet-address" title="${address}">${shortAddress(address)}</span>
  `;
}

function hideWalletMenu() {
  els.walletMenu.classList.add("hidden");
}

function toggleWalletMenu() {
  if (!selectedAddress) {
    return;
  }

  els.walletMenu.classList.toggle("hidden");
}

async function requestDacNetwork() {
  if (!window.ethereum) {
    throw new Error("No browser wallet found. Please install MetaMask or a compatible wallet.");
  }

  try {
    await window.ethereum.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: DAC_CHAIN_ID_HEX }]
    });
  } catch (switchError) {
    if (switchError.code !== 4902) {
      throw switchError;
    }

    await window.ethereum.request({
      method: "wallet_addEthereumChain",
      params: [
        {
          chainId: DAC_CHAIN_ID_HEX,
          chainName: "DAC Testnet",
          nativeCurrency: {
            name: "DACC",
            symbol: "DACC",
            decimals: 18
          },
          rpcUrls: [DAC_RPC_URL],
          blockExplorerUrls: [DAC_EXPLORER_URL]
        }
      ]
    });
  }
}

async function refreshWalletStatus() {
  if (!browserProvider || !selectedAddress) {
    updateWalletBoxDisconnected();
    return;
  }

  const balance = await browserProvider.getBalance(selectedAddress);
  updateWalletBoxConnected(formatBalance(balance), selectedAddress);
}

async function connectWallet() {
  await requestDacNetwork();

  browserProvider = new ethers.BrowserProvider(window.ethereum);
  signer = await browserProvider.getSigner();
  selectedAddress = await signer.getAddress();

  await refreshWalletStatus();

  setStatus(`Wallet connected: ${shortAddress(selectedAddress)}`);
  updateRegisterButtonState();
}

function disconnectWallet() {
  signer = null;
  browserProvider = null;
  selectedAddress = null;

  updateWalletBoxDisconnected();
  renderDomainList([], "");
  els.primaryDomainText.textContent = "Not selected";
  els.domainEmptyState.textContent =
    "Connect your wallet to view and manage domains associated with your address.";
  els.domainEmptyState.style.display = "block";

  setStatus("Wallet disconnected.");
  updateRegisterButtonState();
}

async function handleWalletBox() {
  if (!selectedAddress) {
    await connectWallet();
    return;
  }

  toggleWalletMenu();
}

async function handleSaveContract() {
  const address = els.contractAddressInput.value.trim();

  if (!ethers.isAddress(address)) {
    throw new Error("Invalid registry contract address.");
  }

  saveContractAddress(address);
  setStatus(`Registry contract saved: ${shortAddress(address)}`);

  if (cleanLabel(els.registerLabel.value)) {
    await checkTypedDomainAvailability();
  }
}

async function checkTypedDomainAvailability() {
  const label = cleanLabel(els.registerLabel.value);

  if (!label) {
    resetAvailabilityState();
    return;
  }

  els.registerLabel.value = label;

  let name;

  try {
    name = buildDomain(label);
  } catch (error) {
    resetAvailabilityState();
    setStatus(error.message, true);
    return;
  }

  if (!hasRegistryAddress()) {
    resetAvailabilityState();
    setStatus("Registry is not active yet. Domain registration will be available after deployment.");
    return;
  }

  setAvailabilityState("neutral", "Checking Availability", `Checking ${name} on DAC Testnet...`);

  try {
    const registry = getRegistry(true);
    const available = await registry.isAvailable(name);
    const record = await registry.getRecord(name);

    if (available) {
      setAvailabilityState(
        "available",
        "Available",
        "This domain is available for registration."
      );
      setStatus(`${name} is available.`);
      return;
    }

    setAvailabilityState(
      "unavailable",
      "Not Available",
      `This domain is already owned by ${shortAddress(record.owner)}.`,
      `Owner: ${shortAddress(record.owner)}<br />Expires: ${formatDate(record.expiresAt)}`
    );

    setStatus(`${name} is not available.`, true);
  } catch (error) {
    resetAvailabilityState();
    setStatus(error.message || String(error), true);
  }
}

function scheduleAvailabilityCheck() {
  clearTimeout(availabilityTimer);

  availabilityTimer = setTimeout(() => {
    checkTypedDomainAvailability();
  }, 450);
}

function handleDurationSelection(button) {
  selectedYears = Number(button.dataset.years);

  els.durationOptions.forEach((option) => option.classList.remove("active"));
  button.classList.add("active");

  els.totalPrice.textContent = `${PRICES[selectedYears]} DACC`;
}

async function handleRegister() {
  if (!selectedAddress) {
    throw new Error("Connect wallet first.");
  }

  const name = buildDomain(els.registerLabel.value);
  const registry = getRegistry(false);
  const price = ethers.parseEther(PRICES[selectedYears]);

  setStatus(`Submitting ${selectedYears} year registration for ${name}...`);

  const tx = await registry.register(name, selectedYears, {
    value: price
  });

  await tx.wait();

  setStatus(`Domain registered: ${name} for ${selectedYears} year(s). TX: ${tx.hash}`);
  els.registerLabel.value = "";
  resetAvailabilityState();
}

function renderDomainList(domains, primaryDomain) {
  els.domainList.innerHTML = "";

  if (!domains.length) {
    els.domainEmptyState.style.display = "block";
    return;
  }

  els.domainEmptyState.style.display = "none";

  domains.forEach((record) => {
    const isPrimary = record.name === primaryDomain;

    const item = document.createElement("article");
    item.className = "domain-item";

    item.innerHTML = `
      <div class="domain-item-top">
        <div>
          <div class="domain-item-name">
            ${record.name}
            ${isPrimary ? '<span class="domain-primary-badge">★</span>' : ""}
          </div>
          <div class="domain-item-meta">
            Target: ${shortAddress(record.target)}<br />
            Expires: ${formatDate(record.expiresAt)}
          </div>
        </div>
      </div>

      <div class="domain-actions">
        <button class="secondary-action set-primary-btn" type="button" ${isPrimary ? "disabled" : ""}>
          ${isPrimary ? "Primary" : "Set Primary"}
        </button>
        <button class="secondary-action renew-btn" type="button">Renew 1 Year</button>
      </div>
    `;

    item.querySelector(".set-primary-btn").addEventListener("click", async () => {
      await setPrimaryDomain(record.name);
    });

    item.querySelector(".renew-btn").addEventListener("click", async () => {
      await renewDomain(record.name, 1);
    });

    els.domainList.appendChild(item);
  });
}

async function loadOwnedDomains() {
  if (!selectedAddress) {
    renderDomainList([], "");
    els.primaryDomainText.textContent = "Not selected";
    els.domainEmptyState.textContent =
      "Connect your wallet to view and manage domains associated with your address.";
    els.domainEmptyState.style.display = "block";
    return;
  }

  if (!hasRegistryAddress()) {
    renderDomainList([], "");
    els.primaryDomainText.textContent = "Not selected";
    els.domainEmptyState.textContent =
      "Domain registry is not active yet. Once the registry is deployed, your owned .dac domains will appear here.";
    els.domainEmptyState.style.display = "block";
    setStatus("Registry is not active yet. Open Advanced Settings after deployment to save the contract address.");
    return;
  }

  const registry = getRegistry(true);
  const domainNames = await registry.getDomainsByOwner(selectedAddress);
  const primaryDomain = await registry.getPrimaryDomain(selectedAddress);

  const records = [];

  for (const name of domainNames) {
    const record = await registry.getRecord(name);

    if (record.active) {
      records.push({
        name,
        owner: record.owner,
        target: record.target,
        expiresAt: record.expiresAt
      });
    }
  }

  els.primaryDomainText.textContent = primaryDomain || "Not selected";
  els.domainEmptyState.textContent =
    "No .dac domains found for this wallet. Register your first .dac domain to start managing your on-chain identity.";

  renderDomainList(records, primaryDomain);

  setStatus(
    records.length
      ? `Loaded ${records.length} active .dac domain(s).`
      : "No owned domains found for the connected wallet."
  );
}

async function setPrimaryDomain(name) {
  const registry = getRegistry(false);

  setStatus(`Setting primary domain: ${name}...`);

  const tx = await registry.setPrimaryDomain(name);
  await tx.wait();

  setStatus(`Primary domain set: ${name}`);
  await loadOwnedDomains();
}

async function clearPrimaryDomain() {
  if (!selectedAddress) {
    throw new Error("Connect wallet first.");
  }

  const registry = getRegistry(false);

  setStatus("Clearing primary domain...");

  const tx = await registry.clearPrimaryDomain();
  await tx.wait();

  setStatus("Primary domain cleared.");
  await loadOwnedDomains();
}

async function renewDomain(name, years) {
  const registry = getRegistry(false);
  const price = ethers.parseEther(PRICES[years]);

  setStatus(`Renewing ${name} for ${years} year...`);

  const tx = await registry.renew(name, years, {
    value: price
  });

  await tx.wait();

  setStatus(`Renewed ${name} for ${years} year. TX: ${tx.hash}`);
  await loadOwnedDomains();
}

function bindAsync(button, handler) {
  button.addEventListener("click", async () => {
    try {
      button.disabled = true;
      await handler();
    } catch (error) {
      console.error(error);
      setStatus(error.message || String(error), true);
    } finally {
      button.disabled = false;
      updateRegisterButtonState();
    }
  });
}

function bindInputCleaner(input) {
  input.addEventListener("input", () => {
    input.value = cleanLabel(input.value);
  });
}

function init() {
  startBackgroundSlideshow();

  const savedContract = getSavedContractAddress();
  els.contractAddressInput.value = savedContract;
  els.activeContract.textContent = savedContract || "Not set";

  els.registerTabBtn.addEventListener("click", () => switchTab("register"));
  els.managementTabBtn.addEventListener("click", () => switchTab("management"));

  bindAsync(els.walletBox, handleWalletBox);
  bindAsync(els.saveContractBtn, handleSaveContract);
  bindAsync(els.registerBtn, handleRegister);
  bindAsync(els.refreshDomainsBtn, loadOwnedDomains);
  bindAsync(els.clearPrimaryBtn, clearPrimaryDomain);

  els.disconnectBtn.addEventListener("click", () => {
    disconnectWallet();
  });

  bindInputCleaner(els.registerLabel);
  els.registerLabel.addEventListener("input", scheduleAvailabilityCheck);

  els.durationOptions.forEach((button) => {
    button.addEventListener("click", () => handleDurationSelection(button));
  });

  document.addEventListener("click", (event) => {
    if (!els.walletArea.contains(event.target)) {
      hideWalletMenu();
    }
  });

  if (window.ethereum) {
    window.ethereum.on("accountsChanged", () => window.location.reload());
    window.ethereum.on("chainChanged", () => window.location.reload());
  }

  updateWalletBoxDisconnected();
  updateRegisterButtonState();
}

init();
