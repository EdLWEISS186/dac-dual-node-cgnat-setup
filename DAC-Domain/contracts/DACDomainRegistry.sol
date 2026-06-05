// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

/**
 * @title DACDomainRegistry
 * @notice Experimental explorer-friendly .dac domain registry for DAC Testnet.
 * @dev Community-built testnet infrastructure experiment. Not an official DAC name service.
 */
contract DACDomainRegistry {
    string public constant TLD = ".dac";

    uint256 public constant MIN_NAME_LENGTH = 5;  // a.dac
    uint256 public constant MAX_NAME_LENGTH = 64;

    uint256 public constant PRICE_ONE_YEAR = 5 ether;
    uint256 public constant PRICE_TWO_YEARS = 8 ether;
    uint256 public constant PRICE_THREE_YEARS = 10 ether;

    address public contractOwner;

    struct DomainRecord {
        address owner;
        address target;
        uint256 registeredAt;
        uint256 updatedAt;
        uint256 expiresAt;
        uint8 registrationYears;
    }

    mapping(string => DomainRecord) private records;
    mapping(address => string[]) private ownerDomains;
    mapping(address => string) private primaryDomainByOwner;

    /**
     * @dev Explorer-friendly event pattern:
     * - nameHash is indexed for filtering.
     * - name is non-indexed so explorers can display the readable .dac name.
     */
    event DomainRegistered(
        bytes32 indexed nameHash,
        string name,
        address indexed owner,
        address indexed target,
        uint8 registrationYears,
        uint256 expiresAt,
        uint256 pricePaid,
        uint256 timestamp
    );

    event DomainRenewed(
        bytes32 indexed nameHash,
        string name,
        address indexed owner,
        uint8 addedYears,
        uint256 newExpiresAt,
        uint256 pricePaid,
        uint256 timestamp
    );

    event DomainTargetUpdated(
        bytes32 indexed nameHash,
        string name,
        address indexed owner,
        address oldTarget,
        address newTarget,
        uint256 timestamp
    );

    event PrimaryDomainSet(
        address indexed owner,
        bytes32 indexed nameHash,
        string name,
        uint256 timestamp
    );

    event PrimaryDomainCleared(
        address indexed owner,
        bytes32 indexed oldNameHash,
        string oldName,
        uint256 timestamp
    );

    modifier onlyContractOwner() {
        require(msg.sender == contractOwner, "Not contract owner");
        _;
    }

    modifier onlyDomainOwner(string memory name) {
        require(records[name].owner == msg.sender, "Not domain owner");
        require(records[name].expiresAt > block.timestamp, "Domain expired");
        _;
    }

    constructor() {
        contractOwner = msg.sender;
    }

    function register(string memory name, uint8 registrationYears) external payable {
        require(_isValidName(name), "Invalid .dac domain name");
        require(_isAvailable(name), "Domain already registered");
        require(_isValidDuration(registrationYears), "Invalid registration duration");

        uint256 requiredPrice = getRegistrationPrice(registrationYears);
        require(msg.value >= requiredPrice, "Insufficient DACC payment");

        uint256 expiresAt = block.timestamp + (uint256(registrationYears) * 365 days);

        records[name] = DomainRecord({
            owner: msg.sender,
            target: msg.sender,
            registeredAt: block.timestamp,
            updatedAt: block.timestamp,
            expiresAt: expiresAt,
            registrationYears: registrationYears
        });

        ownerDomains[msg.sender].push(name);

        emit DomainRegistered(
            _nameHash(name),
            name,
            msg.sender,
            msg.sender,
            registrationYears,
            expiresAt,
            msg.value,
            block.timestamp
        );
    }

    function renew(string memory name, uint8 addedYears) external payable onlyDomainOwner(name) {
        require(_isValidDuration(addedYears), "Invalid renewal duration");

        uint256 requiredPrice = getRegistrationPrice(addedYears);
        require(msg.value >= requiredPrice, "Insufficient DACC payment");

        uint256 baseTime = records[name].expiresAt > block.timestamp
            ? records[name].expiresAt
            : block.timestamp;

        uint256 newExpiresAt = baseTime + (uint256(addedYears) * 365 days);

        records[name].expiresAt = newExpiresAt;
        records[name].updatedAt = block.timestamp;
        records[name].registrationYears += addedYears;

        emit DomainRenewed(
            _nameHash(name),
            name,
            msg.sender,
            addedYears,
            newExpiresAt,
            msg.value,
            block.timestamp
        );
    }

    function updateTarget(string memory name, address newTarget) external onlyDomainOwner(name) {
        require(newTarget != address(0), "Invalid target address");

        address oldTarget = records[name].target;

        records[name].target = newTarget;
        records[name].updatedAt = block.timestamp;

        emit DomainTargetUpdated(
            _nameHash(name),
            name,
            msg.sender,
            oldTarget,
            newTarget,
            block.timestamp
        );
    }

    function setPrimaryDomain(string memory name) external onlyDomainOwner(name) {
        primaryDomainByOwner[msg.sender] = name;

        emit PrimaryDomainSet(
            msg.sender,
            _nameHash(name),
            name,
            block.timestamp
        );
    }

    function clearPrimaryDomain() external {
        string memory oldName = primaryDomainByOwner[msg.sender];

        primaryDomainByOwner[msg.sender] = "";

        emit PrimaryDomainCleared(
            msg.sender,
            _nameHash(oldName),
            oldName,
            block.timestamp
        );
    }

    function resolve(string memory name) external view returns (address) {
        require(records[name].owner != address(0), "Domain not registered");
        require(records[name].expiresAt > block.timestamp, "Domain expired");

        return records[name].target;
    }

    function getRecord(
        string memory name
    )
        external
        view
        returns (
            address owner,
            address target,
            uint256 registeredAt,
            uint256 updatedAt,
            uint256 expiresAt,
            uint8 registrationYears,
            bool active
        )
    {
        DomainRecord memory record = records[name];

        return (
            record.owner,
            record.target,
            record.registeredAt,
            record.updatedAt,
            record.expiresAt,
            record.registrationYears,
            record.owner != address(0) && record.expiresAt > block.timestamp
        );
    }

    function isAvailable(string memory name) external view returns (bool) {
        return _isAvailable(name);
    }

    function getDomainsByOwner(address owner) external view returns (string[] memory) {
        string[] memory allDomains = ownerDomains[owner];
        uint256 activeCount = 0;

        for (uint256 i = 0; i < allDomains.length; i++) {
            DomainRecord memory record = records[allDomains[i]];

            if (record.owner == owner && record.expiresAt > block.timestamp) {
                activeCount++;
            }
        }

        string[] memory activeDomains = new string[](activeCount);
        uint256 index = 0;

        for (uint256 i = 0; i < allDomains.length; i++) {
            DomainRecord memory record = records[allDomains[i]];

            if (record.owner == owner && record.expiresAt > block.timestamp) {
                activeDomains[index] = allDomains[i];
                index++;
            }
        }

        return activeDomains;
    }

    function getPrimaryDomain(address owner) external view returns (string memory) {
        string memory primaryDomain = primaryDomainByOwner[owner];

        if (bytes(primaryDomain).length == 0) {
            return "";
        }

        DomainRecord memory record = records[primaryDomain];

        if (record.owner != owner || record.expiresAt <= block.timestamp) {
            return "";
        }

        return primaryDomain;
    }

    function getRegistrationPrice(uint8 registrationYears) public pure returns (uint256) {
        if (registrationYears == 1) {
            return PRICE_ONE_YEAR;
        }

        if (registrationYears == 2) {
            return PRICE_TWO_YEARS;
        }

        if (registrationYears == 3) {
            return PRICE_THREE_YEARS;
        }

        revert("Invalid registration duration");
    }

    function getNameHash(string memory name) external pure returns (bytes32) {
        return _nameHash(name);
    }

    function withdraw(address payable recipient) external onlyContractOwner {
        require(recipient != address(0), "Invalid recipient");

        recipient.transfer(address(this).balance);
    }

    function _isAvailable(string memory name) internal view returns (bool) {
        DomainRecord memory record = records[name];

        return record.owner == address(0) || record.expiresAt <= block.timestamp;
    }

    function _isValidDuration(uint8 registrationYears) internal pure returns (bool) {
        return registrationYears == 1 || registrationYears == 2 || registrationYears == 3;
    }

    function _isValidName(string memory name) internal pure returns (bool) {
        bytes memory nameBytes = bytes(name);

        if (nameBytes.length < MIN_NAME_LENGTH) {
            return false;
        }

        if (nameBytes.length > MAX_NAME_LENGTH) {
            return false;
        }

        if (!_hasDacSuffix(nameBytes)) {
            return false;
        }

        return _isValidLabel(nameBytes);
    }

    function _hasDacSuffix(bytes memory nameBytes) internal pure returns (bool) {
        uint256 length = nameBytes.length;

        return (
            nameBytes[length - 4] == 0x2e &&
            nameBytes[length - 3] == 0x64 &&
            nameBytes[length - 2] == 0x61 &&
            nameBytes[length - 1] == 0x63
        );
    }

    function _isValidLabel(bytes memory nameBytes) internal pure returns (bool) {
        uint256 labelLength = nameBytes.length - 4;

        if (labelLength == 0) {
            return false;
        }

        if (nameBytes[0] == 0x2d || nameBytes[labelLength - 1] == 0x2d) {
            return false;
        }

        for (uint256 i = 0; i < labelLength; i++) {
            bytes1 char = nameBytes[i];

            bool isLowercaseLetter = char >= 0x61 && char <= 0x7a;
            bool isNumber = char >= 0x30 && char <= 0x39;
            bool isHyphen = char == 0x2d;

            if (!(isLowercaseLetter || isNumber || isHyphen)) {
                return false;
            }
        }

        return true;
    }

    function _nameHash(string memory name) internal pure returns (bytes32) {
        return keccak256(bytes(name));
    }
}
