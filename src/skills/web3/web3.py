#!/usr/bin/env python3
"""
Web3 Skill Module
Provides comprehensive Web3 and blockchain development capabilities including
smart contracts, decentralized applications, blockchain integration, and
cryptocurrency technologies.

This skill handles blockchain architecture, smart contract development,
decentralized finance (DeFi), non-fungible tokens (NFTs), and Web3 infrastructure.
"""

import os
import re
import json
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging
import hashlib
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Web3Skill:
    """Web3 skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Web3 skill.
        
        Args:
            config: Configuration dictionary with Web3 settings
        """
        self.config = config or {}
        self.blockchains = ['ethereum', 'polygon', 'binance_smart_chain', 'solana', 'avalanche']
        self.contracts = ['erc20', 'erc721', 'erc1155', 'defi', 'dao', 'staking']
        self.tools = ['solidity', 'hardhat', 'truffle', 'web3js', 'ethersjs', 'foundry']
        self.concepts = ['smart_contracts', 'decentralized_apps', 'tokenomics', 'oracles', 'layer2']
        
    def analyze_web3_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze a Web3 project to understand its structure and components.
        
        Args:
            project_path: Path to the Web3 project directory
        
        Returns:
            Dictionary containing project analysis
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze project files
            project_info = self._analyze_project_files(project_dir)
            
            # Detect blockchain and tools
            blockchain = self._detect_blockchain(project_dir)
            tools = self._detect_web3_tools(project_dir)
            
            # Analyze smart contracts
            contracts = self._analyze_smart_contracts(project_dir)
            
            # Check for Web3-specific issues
            issues = self._check_web3_issues(project_dir, blockchain)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "project_info": project_info,
                "blockchain": blockchain,
                "tools": tools,
                "contracts": contracts,
                "issues": issues,
                "recommendations": self._generate_web3_recommendations(blockchain, contracts, issues)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze Web3 project: {str(e)}"}
    
    def create_smart_contract(self, contract_name: str, contract_type: str = "erc20",
                            blockchain: str = "ethereum", 
                            features: List[str] = None) -> Dict[str, Any]:
        """
        Create a new smart contract.
        
        Args:
            contract_name: Name of the contract
            contract_type: Type of contract (erc20, erc721, erc1155, defi, dao, staking)
            blockchain: Target blockchain
            features: Additional features to include
        
        Returns:
            Dictionary containing contract files and instructions
        """
        try:
            # Generate contract files based on type and blockchain
            if contract_type.lower() == "erc20":
                contract_files = self._generate_erc20_contract(contract_name, blockchain, features)
            elif contract_type.lower() == "erc721":
                contract_files = self._generate_erc721_contract(contract_name, blockchain, features)
            elif contract_type.lower() == "erc1155":
                contract_files = self._generate_erc1155_contract(contract_name, blockchain, features)
            elif contract_type.lower() == "defi":
                contract_files = self._generate_defi_contract(contract_name, blockchain, features)
            elif contract_type.lower() == "dao":
                contract_files = self._generate_dao_contract(contract_name, blockchain, features)
            elif contract_type.lower() == "staking":
                contract_files = self._generate_staking_contract(contract_name, blockchain, features)
            else:
                return {"error": f"Unsupported contract type: {contract_type}"}
            
            return {
                "status": "success",
                "contract_name": contract_name,
                "contract_type": contract_type,
                "blockchain": blockchain,
                "features": features or [],
                "files": contract_files,
                "instructions": self._get_contract_instructions(contract_type, blockchain)
            }
            
        except Exception as e:
            return {"error": f"Failed to create smart contract: {str(e)}"}
    
    def implement_decentralized_app(self, app_type: str = "defi",
                                  blockchain: str = "ethereum",
                                  frontend: str = "react") -> Dict[str, Any]:
        """
        Implement a decentralized application.
        
        Args:
            app_type: Type of dApp (defi, nft_marketplace, dao, gaming, social)
            blockchain: Target blockchain
            frontend: Frontend framework (react, vue, angular, svelte)
        
        Returns:
            Dictionary containing dApp implementation
        """
        try:
            # Generate dApp files based on type and blockchain
            if app_type.lower() == "defi":
                app_files = self._generate_defi_dapp(blockchain, frontend)
            elif app_type.lower() == "nft_marketplace":
                app_files = self._generate_nft_marketplace(blockchain, frontend)
            elif app_type.lower() == "dao":
                app_files = self._generate_dao_dapp(blockchain, frontend)
            else:
                return {"error": f"Unsupported dApp type: {app_type}"}
            
            return {
                "status": "success",
                "app_type": app_type,
                "blockchain": blockchain,
                "frontend": frontend,
                "files": app_files,
                "instructions": self._get_dapp_instructions(app_type, blockchain, frontend)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement dApp: {str(e)}"}
    
    def deploy_smart_contract(self, contract_path: str, 
                            blockchain: str = "ethereum",
                            network: str = "testnet") -> Dict[str, Any]:
        """
        Deploy a smart contract to a blockchain network.
        
        Args:
            contract_path: Path to the contract file
            blockchain: Target blockchain
            network: Network type (testnet, mainnet, local)
        
        Returns:
            Dictionary containing deployment information
        """
        try:
            contract_file = Path(contract_path)
            if not contract_file.exists():
                return {"error": f"Contract file does not exist: {contract_path}"}
            
            # Compile contract
            compilation_result = self._compile_contract(contract_file, blockchain)
            
            if not compilation_result["success"]:
                return {"error": f"Contract compilation failed: {compilation_result.get('error')}"}
            
            # Deploy contract
            deployment_result = self._deploy_contract(compilation_result, blockchain, network)
            
            return {
                "status": "success",
                "contract_path": str(contract_file),
                "blockchain": blockchain,
                "network": network,
                "compilation": compilation_result,
                "deployment": deployment_result,
                "contract_address": deployment_result.get("contract_address"),
                "transaction_hash": deployment_result.get("transaction_hash")
            }
            
        except Exception as e:
            return {"error": f"Failed to deploy smart contract: {str(e)}"}
    
    def implement_tokenomics(self, token_name: str, token_symbol: str,
                           total_supply: int, blockchain: str = "ethereum") -> Dict[str, Any]:
        """
        Implement tokenomics for a cryptocurrency token.
        
        Args:
            token_name: Name of the token
            token_symbol: Symbol of the token
            total_supply: Total token supply
            blockchain: Target blockchain
        
        Returns:
            Dictionary containing tokenomics implementation
        """
        try:
            # Generate token contract with tokenomics
            token_files = self._generate_tokenomics_token(
                token_name, token_symbol, total_supply, blockchain
            )
            
            # Generate token distribution plan
            distribution_plan = self._generate_token_distribution(
                total_supply, blockchain
            )
            
            # Generate economic model
            economic_model = self._generate_economic_model(
                token_name, token_symbol, total_supply, blockchain
            )
            
            return {
                "status": "success",
                "token_name": token_name,
                "token_symbol": token_symbol,
                "total_supply": total_supply,
                "blockchain": blockchain,
                "files": token_files,
                "distribution_plan": distribution_plan,
                "economic_model": economic_model,
                "instructions": self._get_tokenomics_instructions(token_name, blockchain)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement tokenomics: {str(e)}"}
    
    def integrate_oracle(self, oracle_type: str = "chainlink",
                        blockchain: str = "ethereum",
                        data_source: str = "price_feed") -> Dict[str, Any]:
        """
        Integrate oracle services for smart contracts.
        
        Args:
            oracle_type: Type of oracle (chainlink, band, redstone)
            blockchain: Target blockchain
            data_source: Type of data source (price_feed, randomness, weather)
        
        Returns:
            Dictionary containing oracle integration
        """
        try:
            # Generate oracle integration files
            if oracle_type.lower() == "chainlink":
                oracle_files = self._generate_chainlink_oracle(blockchain, data_source)
            elif oracle_type.lower() == "band":
                oracle_files = self._generate_band_oracle(blockchain, data_source)
            else:
                return {"error": f"Unsupported oracle type: {oracle_type}"}
            
            return {
                "status": "success",
                "oracle_type": oracle_type,
                "blockchain": blockchain,
                "data_source": data_source,
                "files": oracle_files,
                "instructions": self._get_oracle_instructions(oracle_type, blockchain, data_source)
            }
            
        except Exception as e:
            return {"error": f"Failed to integrate oracle: {str(e)}"}
    
    def _analyze_project_files(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze Web3 project files and structure."""
        project_info = {
            "name": "",
            "version": "",
            "blockchain": "",
            "contracts": [],
            "tests": [],
            "scripts": [],
            "configurations": []
        }
        
        # Look for blockchain-specific files
        if (project_dir / "hardhat.config.js").exists():
            project_info["blockchain"] = "ethereum"
        elif (project_dir / "truffle-config.js").exists():
            project_info["blockchain"] = "ethereum"
        elif (project_dir / "foundry.toml").exists():
            project_info["blockchain"] = "ethereum"
        
        # Analyze project structure
        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix in [".sol"]:
                    project_info["contracts"].append(str(item))
                elif item.suffix in [".js", ".ts"] and "test" in item.name:
                    project_info["tests"].append(str(item))
                elif item.suffix in [".js", ".ts"] and any(keyword in item.name.lower() 
                    for keyword in ["deploy", "script", "task"]):
                    project_info["scripts"].append(str(item))
        
        return project_info
    
    def _detect_blockchain(self, project_dir: Path) -> str:
        """Detect the blockchain used in the project."""
        if (project_dir / "hardhat.config.js").exists():
            return "ethereum"
        elif (project_dir / "truffle-config.js").exists():
            return "ethereum"
        elif (project_dir / "foundry.toml").exists():
            return "ethereum"
        elif (project_dir / "Anchor.toml").exists():
            return "solana"
        return "unknown"
    
    def _detect_web3_tools(self, project_dir: Path) -> List[str]:
        """Detect Web3 development tools used in the project."""
        tools = []
        
        if (project_dir / "hardhat.config.js").exists():
            tools.append("hardhat")
        if (project_dir / "truffle-config.js").exists():
            tools.append("truffle")
        if (project_dir / "foundry.toml").exists():
            tools.append("foundry")
        if (project_dir / "package.json").exists():
            try:
                with open(project_dir / "package.json", 'r') as f:
                    package_data = json.load(f)
                deps = package_data.get("dependencies", {})
                dev_deps = package_data.get("devDependencies", {})
                
                if "ethers" in deps or "ethers" in dev_deps:
                    tools.append("ethersjs")
                if "web3" in deps or "web3" in dev_deps:
                    tools.append("web3js")
                if "@openzeppelin/contracts" in deps:
                    tools.append("openzeppelin")
            except:
                pass
        
        return tools
    
    def _analyze_smart_contracts(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze smart contracts in the project."""
        contracts = {
            "erc20": [],
            "erc721": [],
            "erc1155": [],
            "defi": [],
            "dao": [],
            "utility": [],
            "security_issues": []
        }
        
        for contract_file in project_dir.rglob("*.sol"):
            try:
                with open(contract_file, 'r') as f:
                    content = f.read()
                
                # Detect contract type
                if "ERC20" in content or "IERC20" in content:
                    contracts["erc20"].append(str(contract_file))
                elif "ERC721" in content or "IERC721" in content:
                    contracts["erc721"].append(str(contract_file))
                elif "ERC1155" in content or "IERC1155" in content:
                    contracts["erc1155"].append(str(contract_file))
                elif any(keyword in content.lower() for keyword in ["stake", "yield", "farm"]):
                    contracts["defi"].append(str(contract_file))
                elif any(keyword in content.lower() for keyword in ["govern", "proposal", "vote"]):
                    contracts["dao"].append(str(contract_file))
                else:
                    contracts["utility"].append(str(contract_file))
                
                # Check for security issues
                security_checks = self._check_contract_security(content)
                if security_checks:
                    contracts["security_issues"].extend([
                        f"{contract_file}: {issue}" for issue in security_checks
                    ])
                    
            except Exception as e:
                logger.warning(f"Could not analyze contract {contract_file}: {e}")
        
        return contracts
    
    def _check_web3_issues(self, project_dir: Path, blockchain: str) -> List[str]:
        """Check for Web3-specific issues."""
        issues = []
        
        # Check for missing security measures
        if not any(project_dir.rglob("*audit*")):
            issues.append("No security audit files found")
        
        # Check for proper error handling
        for contract_file in project_dir.rglob("*.sol"):
            try:
                with open(contract_file, 'r') as f:
                    content = f.read()
                
                if "require(" not in content and "revert(" not in content:
                    issues.append(f"Missing error handling in {contract_file.name}")
                    
            except:
                pass
        
        # Check for gas optimization
        if blockchain == "ethereum":
            issues.append("Consider implementing gas optimization techniques")
        
        return issues
    
    def _generate_web3_recommendations(self, blockchain: str, contracts: Dict, issues: List[str]) -> List[str]:
        """Generate Web3 development recommendations."""
        recommendations = []
        
        if blockchain == "ethereum":
            recommendations.extend([
                "Use Layer 2 solutions for gas optimization",
                "Implement proper access controls",
                "Add comprehensive testing suite",
                "Consider formal verification for critical contracts"
            ])
        
        if contracts["erc20"]:
            recommendations.append("Implement ERC20 security best practices")
        
        if contracts["erc721"]:
            recommendations.append("Add ERC721 metadata and enumeration")
        
        return recommendations + issues
    
    def _generate_erc20_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate ERC20 token contract."""
        features = features or []
        
        # Base ERC20 contract
        erc20_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is ERC20, Ownable {{
    uint8 private _decimals = 18;
    
    constructor(string memory name_, string memory symbol_, uint256 initialSupply_) 
        ERC20(name_, symbol_) {{
        _mint(msg.sender, initialSupply_ * 10**_decimals);
    }}
    
    function decimals() public view virtual override returns (uint8) {{
        return _decimals;
    }}
    
    function mint(address to, uint256 amount) public onlyOwner {{
        _mint(to, amount);
    }}
    
    function burn(uint256 amount) public {{
        _burn(msg.sender, amount);
    }}
}}
"""
        
        # Add features
        if "pausable" in features:
            erc20_content = erc20_content.replace(
                "import \"@openzeppelin/contracts/token/ERC20/ERC20.sol\";",
                "import \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol\";"
            )
            erc20_content = erc20_content.replace(
                "contract {name} is ERC20, Ownable {",
                f"contract {name} is ERC20Pausable, Ownable {{"
            )
            erc20_content += """
    function pause() public onlyOwner {
        _pause();
    }
    
    function unpause() public onlyOwner {
        _unpause();
    }
    
    function _beforeTokenTransfer(address from, address to, uint256 amount)
        internal
        whenNotPaused
        override
    {
        super._beforeTokenTransfer(from, to, amount);
    }
"""
        
        if "burnable" in features:
            erc20_content = erc20_content.replace(
                "import \"@openzeppelin/contracts/token/ERC20/ERC20.sol\";",
                "import \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol\";"
            )
            erc20_content = erc20_content.replace(
                "contract {name} is ERC20, Ownable {",
                f"contract {name} is ERC20Burnable, Ownable {{"
            )
        
        return {f"{name}.sol": erc20_content}
    
    def _generate_erc721_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate ERC721 NFT contract."""
        features = features or []
        
        erc721_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract {name} is ERC721, Ownable {{
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    
    string private _baseURIextended;
    
    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {{
        _baseURIextended = "";
    }}
    
    function safeMint(address to) public onlyOwner {{
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
    }}
    
    function _baseURI() internal view virtual override returns (string memory) {{
        return _baseURIextended;
    }}
    
    function setBaseURI(string calldata baseURI_) external onlyOwner {{
        _baseURIextended = baseURI_;
    }}
    
    function withdraw() public onlyOwner {{
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }}
}}
"""
        
        return {f"{name}.sol": erc721_content}
    
    def _generate_erc1155_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate ERC1155 multi-token contract."""
        features = features or []
        
        erc1155_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is ERC1155, Ownable {{
    uint256 public constant TOKEN_1 = 0;
    uint256 public constant TOKEN_2 = 1;
    
    constructor() ERC1155("") {{
        _mint(msg.sender, TOKEN_1, 1000, "");
        _mint(msg.sender, TOKEN_2, 500, "");
    }}
    
    function setURI(string memory newuri) public onlyOwner {{
        _setURI(newuri);
    }}
    
    function mint(address account, uint256 id, uint256 amount, bytes memory data)
        public
        onlyOwner
    {{
        _mint(account, id, amount, data);
    }}
    
    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public
        onlyOwner
    {{
        _mintBatch(to, ids, amounts, data);
    }}
}}
"""
        
        return {f"{name}.sol": erc1155_content}
    
    def _generate_defi_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate DeFi contract."""
        features = features or []
        
        defi_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract {name} is Ownable {{
    using SafeMath for uint256;
    
    IERC20 public token;
    uint256 public rewardRate = 1 ether; // 1 token per second
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;
    
    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;
    mapping(address => uint256) private _balances;
    
    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);
    
    constructor(address _token) {{
        token = IERC20(_token);
    }}
    
    function stake(uint256 amount) external {{
        _balances[msg.sender] = _balances[msg.sender].add(amount);
        lastUpdateTime = block.timestamp;
        token.transferFrom(msg.sender, address(this), amount);
        emit Staked(msg.sender, amount);
    }}
    
    function withdraw(uint256 amount) external {{
        _balances[msg.sender] = _balances[msg.sender].sub(amount);
        lastUpdateTime = block.timestamp;
        token.transfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }}
    
    function claimReward() external {{
        updateReward(msg.sender);
        uint256 reward = rewards[msg.sender];
        if (reward > 0) {{
            rewards[msg.sender] = 0;
            token.transfer(msg.sender, reward);
            emit RewardPaid(msg.sender, reward);
        }}
    }}
    
    function updateReward(address account) public {{
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = lastTimeRewardApplicable();
        if (account != address(0)) {{
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }}
    }}
    
    function lastTimeRewardApplicable() public view returns (uint256) {{
        return block.timestamp;
    }}
    
    function rewardPerToken() public view returns (uint256) {{
        if (totalSupply() == 0) {{
            return rewardPerTokenStored;
        }}
        return
            rewardPerTokenStored.add(
                block.timestamp
                    .sub(lastUpdateTime)
                    .mul(rewardRate)
                    .mul(1e18)
                    .div(totalSupply())
            );
    }}
    
    function earned(address account) public view returns (uint256) {{
        return
            _balances[account]
                .mul(rewardPerToken().sub(userRewardPerTokenPaid[account]))
                .div(1e18)
                .add(rewards[account]);
    }}
    
    function totalSupply() public view returns (uint256) {{
        return token.balanceOf(address(this));
    }}
}}
"""
        
        return {f"{name}.sol": defi_content}
    
    def _generate_dao_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate DAO contract."""
        features = features or []
        
        dao_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is Ownable {{
    IERC20 public governanceToken;
    uint256 public proposalCount = 0;
    uint256 public votingPeriod = 7 days;
    
    struct Proposal {{
        uint256 id;
        string description;
        uint256 startTime;
        uint256 endTime;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        mapping(address => bool) voted;
    }}
    
    mapping(uint256 => Proposal) public proposals;
    mapping(address => uint256) public tokenBalance;
    
    event ProposalCreated(uint256 indexed id, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, bool vote);
    event ProposalExecuted(uint256 indexed id);
    
    constructor(address _token) {{
        governanceToken = IERC20(_token);
    }}
    
    function createProposal(string memory _description) external {{
        require(governanceToken.balanceOf(msg.sender) > 0, "Must hold governance tokens");
        
        proposalCount++;
        Proposal storage proposal = proposals[proposalCount];
        
        proposal.id = proposalCount;
        proposal.description = _description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        
        emit ProposalCreated(proposalCount, _description);
    }}
    
    function vote(uint256 proposalId, bool support) external {{
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.startTime, "Voting not started");
        require(block.timestamp <= proposal.endTime, "Voting ended");
        require(!proposal.voted[msg.sender], "Already voted");
        require(governanceToken.balanceOf(msg.sender) > 0, "Must hold governance tokens");
        
        proposal.voted[msg.sender] = true;
        
        if (support) {{
            proposal.yesVotes++;
        }} else {{
            proposal.noVotes++;
        }}
        
        emit Voted(proposalId, msg.sender, support);
    }}
    
    function executeProposal(uint256 proposalId) external onlyOwner {{
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp > proposal.endTime, "Voting not finished");
        require(!proposal.executed, "Already executed");
        require(proposal.yesVotes > proposal.noVotes, "Proposal rejected");
        
        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }}
}}
"""
        
        return {f"{name}.sol": dao_content}
    
    def _generate_staking_contract(self, name: str, blockchain: str, features: List[str]) -> Dict[str, str]:
        """Generate staking contract."""
        features = features or []
        
        staking_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is Ownable {{
    IERC20 public stakingToken;
    IERC20 public rewardToken;
    
    uint256 public rewardRate = 1 ether; // 1 token per second
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;
    
    struct Staker {{
        uint256 amount;
        uint256 rewardDebt;
    }}
    
    mapping(address => Staker) public stakers;
    uint256 public totalStaked;
    
    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 amount);
    
    constructor(address _stakingToken, address _rewardToken) {{
        stakingToken = IERC20(_stakingToken);
        rewardToken = IERC20(_rewardToken);
    }}
    
    function stake(uint256 amount) external {{
        updateReward(msg.sender);
        
        stakers[msg.sender].amount = stakers[msg.sender].amount.add(amount);
        totalStaked = totalStaked.add(amount);
        
        stakingToken.transferFrom(msg.sender, address(this), amount);
        emit Staked(msg.sender, amount);
    }}
    
    function withdraw(uint256 amount) external {{
        updateReward(msg.sender);
        
        stakers[msg.sender].amount = stakers[msg.sender].amount.sub(amount);
        totalStaked = totalStaked.sub(amount);
        
        stakingToken.transfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }}
    
    function claimReward() external {{
        updateReward(msg.sender);
        uint256 reward = stakers[msg.sender].rewardDebt;
        
        if (reward > 0) {{
            stakers[msg.sender].rewardDebt = 0;
            rewardToken.transfer(msg.sender, reward);
            emit RewardClaimed(msg.sender, reward);
        }}
    }}
    
    function updateReward(address account) public {{
        if (totalStaked > 0) {{
            rewardPerTokenStored = rewardPerToken();
        }}
        lastUpdateTime = block.timestamp;
        
        stakers[account].rewardDebt = earned(account);
    }}
    
    function rewardPerToken() public view returns (uint256) {{
        if (totalStaked == 0) {{
            return rewardPerTokenStored;
        }}
        return
            rewardPerTokenStored.add(
                block.timestamp
                    .sub(lastUpdateTime)
                    .mul(rewardRate)
                    .mul(1e18)
                    .div(totalStaked)
            );
    }}
    
    function earned(address account) public view returns (uint256) {{
        return
            stakers[account].amount
                .mul(rewardPerToken().sub(stakers[account].rewardDebt))
                .div(1e18)
                .add(stakers[account].rewardDebt);
    }}
}}
"""
        
        return {f"{name}.sol": staking_content}
    
    def _get_contract_instructions(self, contract_type: str, blockchain: str) -> str:
        """Get instructions for using the generated contract."""
        return f"""To deploy the {contract_type} contract on {blockchain}:
1. Install required dependencies (Hardhat/Truffle, OpenZeppelin)
2. Configure network settings in deployment script
3. Compile the contract using your chosen framework
4. Deploy to testnet/mainnet using deployment script
5. Verify the contract on block explorer
6. Test functionality using provided test scripts"""
    
    def _generate_defi_dapp(self, blockchain: str, frontend: str) -> Dict[str, str]:
        """Generate DeFi dApp implementation."""
        # Smart contract
        contract_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DeFiApp is Ownable {
    IERC20 public token;
    uint256 public poolBalance;
    
    struct User {
        uint256 balance;
        uint256 rewards;
        uint256 lastClaim;
    }
    
    mapping(address => User) public users;
    
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);
    
    constructor(address _token) {
        token = IERC20(_token);
    }
    
    function deposit(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        
        users[msg.sender].balance += amount;
        poolBalance += amount;
        
        token.transferFrom(msg.sender, address(this), amount);
        emit Deposited(msg.sender, amount);
    }
    
    function withdraw(uint256 amount) external {
        require(users[msg.sender].balance >= amount, "Insufficient balance");
        
        users[msg.sender].balance -= amount;
        poolBalance -= amount;
        
        token.transfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }
    
    function claimRewards() external {
        uint256 rewards = calculateRewards(msg.sender);
        require(rewards > 0, "No rewards to claim");
        
        users[msg.sender].rewards = 0;
        users[msg.sender].lastClaim = block.timestamp;
        
        token.transfer(msg.sender, rewards);
        emit RewardsClaimed(msg.sender, rewards);
    }
    
    function calculateRewards(address user) public view returns (uint256) {
        uint256 timeElapsed = block.timestamp - users[user].lastClaim;
        uint256 rewards = users[user].balance * timeElapsed * 1 ether / 86400 / 100; // 1% daily
        return rewards;
    }
}
"""
        
        # Frontend integration
        if frontend == "react":
            frontend_content = """import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import DeFiApp from './DeFiApp.json';

const DeFiAppInterface = () => {
    const [provider, setProvider] = useState(null);
    const [signer, setSigner] = useState(null);
    const [contract, setContract] = useState(null);
    const [account, setAccount] = useState('');
    const [balance, setBalance] = useState('0');
    const [rewards, setRewards] = useState('0');
    const [depositAmount, setDepositAmount] = useState('');
    
    const contractAddress = 'YOUR_CONTRACT_ADDRESS';
    
    useEffect(() => {
        connectWallet();
    }, []);
    
    const connectWallet = async () => {
        if (window.ethereum) {
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(contractAddress, DeFiApp.abi, signer);
            
            setProvider(provider);
            setSigner(signer);
            setContract(contract);
            
            const address = await signer.getAddress();
            setAccount(address);
            
            updateUserInfo(address);
        }
    };
    
    const updateUserInfo = async (userAddress) => {
        if (contract) {
            const userBalance = await contract.users(userAddress);
            setBalance(ethers.utils.formatEther(userBalance.balance));
            setRewards(ethers.utils.formatEther(userBalance.rewards));
        }
    };
    
    const deposit = async () => {
        if (contract && depositAmount) {
            const amount = ethers.utils.parseEther(depositAmount);
            const tx = await contract.deposit(amount);
            await tx.wait();
            updateUserInfo(account);
        }
    };
    
    const withdraw = async () => {
        if (contract) {
            const tx = await contract.withdraw(ethers.utils.parseEther(balance));
            await tx.wait();
            updateUserInfo(account);
        }
    };
    
    const claimRewards = async () => {
        if (contract) {
            const tx = await contract.claimRewards();
            await tx.wait();
            updateUserInfo(account);
        }
    };
    
    return (
        <div>
            <h1>DeFi App</h1>
            <p>Connected: {account}</p>
            <div>
                <input 
                    type="number" 
                    value={depositAmount}
                    onChange={(e) => setDepositAmount(e.target.value)}
                    placeholder="Deposit amount"
                />
                <button onClick={deposit}>Deposit</button>
            </div>
            <div>
                <p>Balance: {balance} tokens</p>
                <p>Rewards: {rewards} tokens</p>
                <button onClick={claimRewards}>Claim Rewards</button>
                <button onClick={withdraw}>Withdraw</button>
            </div>
        </div>
    );
};

export default DeFiAppInterface;
"""
        
        return {
            "DeFiApp.sol": contract_content,
            "DeFiAppInterface.jsx": frontend_content
        }
    
    def _generate_nft_marketplace(self, blockchain: str, frontend: str) -> Dict[str, str]:
        """Generate NFT marketplace implementation."""
        # Smart contract
        contract_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTMarketplace is Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    
    struct MarketItem {
        uint256 tokenId;
        address payable seller;
        address payable owner;
        uint256 price;
        bool sold;
    }
    
    ERC721 public nftContract;
    uint256 public listingFee = 0.025 ether;
    mapping(uint256 => MarketItem) public idToMarketItem;
    
    event MarketItemCreated (
        uint256 indexed tokenId,
        address seller,
        address owner,
        uint256 price,
        bool sold
    );
    
    event MarketItemSold (
        uint256 indexed tokenId,
        address seller,
        address buyer,
        uint256 price,
        bool sold
    );
    
    constructor(address _nftContract) {
        nftContract = ERC721(_nftContract);
    }
    
    function createMarketItem(uint256 tokenId, uint256 price) public payable {
        require(price > 0, "Price must be greater than 0");
        require(msg.value == listingFee, "Listing fee must be paid");
        
        nftContract.transferFrom(msg.sender, address(this), tokenId);
        idToMarketItem[tokenId] = MarketItem(
            tokenId,
            payable(msg.sender),
            payable(address(this)),
            price,
            false
        );
        
        emit MarketItemCreated(tokenId, msg.sender, address(this), price, false);
    }
    
    function createMarketSale(uint256 tokenId) public payable {
        uint256 price = idToMarketItem[tokenId].price;
        address seller = idToMarketItem[tokenId].seller;
        
        require(msg.value == price, "Please submit the asking price");
        
        idToMarketItem[tokenId].seller.transfer(msg.value);
        nftContract.transferFrom(address(this), msg.sender, tokenId);
        idToMarketItem[tokenId].owner = payable(msg.sender);
        idToMarketItem[tokenId].sold = true;
        
        _tokenIdCounter.increment();
        
        emit MarketItemSold(tokenId, seller, msg.sender, price, true);
    }
    
    function fetchMarketItems() public view returns (MarketItem[] memory) {
        uint256 itemCount = _tokenIdCounter.current();
        uint256 unsoldItemCount = _tokenIdCounter.current() - 1;
        uint256 currentIndex = 0;
        
        MarketItem[] memory items = new MarketItem[](unsoldItemCount);
        for (uint256 i = 0; i < itemCount; i++) {
            if (idToMarketItem[i + 1].owner == address(this)) {
                uint256 currentId = i + 1;
                MarketItem storage currentItem = idToMarketItem[currentId];
                items[currentIndex] = currentItem;
                currentIndex += 1;
            }
        }
        return items;
    }
}
"""
        
        return {
            "NFTMarketplace.sol": contract_content,
            "MarketplaceInterface.jsx": "// Frontend implementation would go here"
        }
    
    def _generate_dao_dapp(self, blockchain: str, frontend: str) -> Dict[str, str]:
        """Generate DAO dApp implementation."""
        # Smart contract
        contract_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DAO is Ownable {
    IERC20 public governanceToken;
    uint256 public proposalCount = 0;
    uint256 public votingPeriod = 7 days;
    
    struct Proposal {
        uint256 id;
        string description;
        uint256 startTime;
        uint256 endTime;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        mapping(address => bool) voted;
    }
    
    mapping(uint256 => Proposal) public proposals;
    
    event ProposalCreated(uint256 indexed id, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, bool vote);
    event ProposalExecuted(uint256 indexed id);
    
    constructor(address _token) {
        governanceToken = IERC20(_token);
    }
    
    function createProposal(string memory _description) external {
        require(governanceToken.balanceOf(msg.sender) > 0, "Must hold governance tokens");
        
        proposalCount++;
        Proposal storage proposal = proposals[proposalCount];
        
        proposal.id = proposalCount;
        proposal.description = _description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        
        emit ProposalCreated(proposalCount, _description);
    }
    
    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.startTime, "Voting not started");
        require(block.timestamp <= proposal.endTime, "Voting ended");
        require(!proposal.voted[msg.sender], "Already voted");
        require(governanceToken.balanceOf(msg.sender) > 0, "Must hold governance tokens");
        
        proposal.voted[msg.sender] = true;
        
        if (support) {
            proposal.yesVotes++;
        } else {
            proposal.noVotes++;
        }
        
        emit Voted(proposalId, msg.sender, support);
    }
    
    function executeProposal(uint256 proposalId) external onlyOwner {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp > proposal.endTime, "Voting not finished");
        require(!proposal.executed, "Already executed");
        require(proposal.yesVotes > proposal.noVotes, "Proposal rejected");
        
        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }
}
"""
        
        return {
            "DAO.sol": contract_content,
            "DAOInterface.jsx": "// Frontend implementation would go here"
        }
    
    def _get_dapp_instructions(self, app_type: str, blockchain: str, frontend: str) -> str:
        """Get instructions for implementing the dApp."""
        return f"""To implement the {app_type} dApp on {blockchain} with {frontend}:
1. Set up development environment (Node.js, blockchain client)
2. Create smart contracts using Solidity
3. Deploy contracts to testnet/mainnet
4. Set up frontend project with {frontend} framework
5. Integrate Web3.js or Ethers.js for blockchain interaction
6. Implement wallet connection (MetaMask, WalletConnect)
7. Add UI components for user interaction
8. Test thoroughly before deployment"""
    
    def _compile_contract(self, contract_file: Path, blockchain: str) -> Dict[str, Any]:
        """Compile smart contract."""
        try:
            # This would typically use Hardhat, Truffle, or Foundry
            # For now, return a mock compilation result
            return {
                "success": True,
                "abi": "mock_abi",
                "bytecode": "mock_bytecode",
                "compiler_version": "0.8.0"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _deploy_contract(self, compilation_result: Dict, blockchain: str, network: str) -> Dict[str, Any]:
        """Deploy smart contract to blockchain."""
        try:
            # This would typically use deployment scripts
            # For now, return a mock deployment result
            return {
                "success": True,
                "contract_address": "0xMockContractAddress123456789",
                "transaction_hash": "0xMockTransactionHash123456789",
                "gas_used": 21000
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_tokenomics_token(self, name: str, symbol: str, supply: int, blockchain: str) -> Dict[str, str]:
        """Generate token with comprehensive tokenomics."""
        token_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is ERC20, Ownable {{
    uint8 private _decimals = 18;
    uint256 public constant MAX_SUPPLY = {supply} * 10**18;
    
    // Token distribution
    uint256 public constant TEAM_ALLOCATION = MAX_SUPPLY * 20 / 100;    // 20%
    uint256 public constant ECOSYSTEM_ALLOCATION = MAX_SUPPLY * 25 / 100; // 25%
    uint256 public constant STAKING_REWARDS = MAX_SUPPLY * 35 / 100;     // 35%
    uint256 public constant LIQUIDITY = MAX_SUPPLY * 10 / 100;           // 10%
    uint256 public constant PUBLIC_SALE = MAX_SUPPLY * 10 / 100;         // 10%
    
    // Vesting schedules
    uint256 public teamVestingStart;
    uint256 public teamVestingDuration = 24 weeks;
    
    address public teamWallet;
    address public ecosystemWallet;
    address public stakingWallet;
    address public liquidityWallet;
    
    constructor(address _teamWallet, address _ecosystemWallet, address _stakingWallet, address _liquidityWallet) 
        ERC20("{name}", "{symbol}") {{
        
        teamWallet = _teamWallet;
        ecosystemWallet = _ecosystemWallet;
        stakingWallet = _stakingWallet;
        liquidityWallet = _liquidityWallet;
        
        teamVestingStart = block.timestamp;
        
        // Mint initial supply
        _mint(address(this), MAX_SUPPLY);
        
        // Allocate tokens (held in contract, will be released via vesting)
        // This is a simplified version - real implementation would use vesting contracts
    }}
    
    function decimals() public view virtual override returns (uint8) {{
        return _decimals;
    }}
    
    function releaseTeamTokens() external onlyOwner {{
        require(block.timestamp >= teamVestingStart, "Vesting not started");
        
        // Simplified vesting logic
        uint256 elapsed = block.timestamp - teamVestingStart;
        uint256 vestedPercentage = (elapsed * 100) / teamVestingDuration;
        
        if (vestedPercentage >= 100) {{
            vestedPercentage = 100;
        }}
        
        uint256 tokensToRelease = (TEAM_ALLOCATION * vestedPercentage) / 100;
        _transfer(address(this), teamWallet, tokensToRelease);
    }}
    
    function allocateTokens() external onlyOwner {{
        _transfer(address(this), ecosystemWallet, ECOSYSTEM_ALLOCATION);
        _transfer(address(this), stakingWallet, STAKING_REWARDS);
        _transfer(address(this), liquidityWallet, LIQUIDITY);
    }}
}}
"""
        
        return {f"{name}.sol": token_content}
    
    def _generate_token_distribution(self, total_supply: int, blockchain: str) -> Dict[str, Any]:
        """Generate token distribution plan."""
        distribution = {
            "total_supply": total_supply,
            "allocation": {
                "team": {
                    "percentage": 20,
                    "amount": total_supply * 0.2,
                    "vesting": "24 months linear vesting with 6 month cliff"
                },
                "ecosystem": {
                    "percentage": 25,
                    "amount": total_supply * 0.25,
                    "vesting": "Released based on ecosystem milestones"
                },
                "staking_rewards": {
                    "percentage": 35,
                    "amount": total_supply * 0.35,
                    "vesting": "Released gradually to staking pools"
                },
                "liquidity": {
                    "percentage": 10,
                    "amount": total_supply * 0.1,
                    "vesting": "Immediate for DEX liquidity"
                },
                "public_sale": {
                    "percentage": 10,
                    "amount": total_supply * 0.1,
                    "vesting": "Immediate for public sale"
                }
            },
            "tokenomics_features": [
                "Deflationary mechanism through buyback and burn",
                "Staking rewards for long-term holders",
                "Governance rights for token holders",
                "Revenue sharing from platform fees"
            ]
        }
        
        return distribution
    
    def _generate_economic_model(self, name: str, symbol: str, supply: int, blockchain: str) -> Dict[str, Any]:
        """Generate economic model for the token."""
        model = {
            "token_name": name,
            "token_symbol": symbol,
            "total_supply": supply,
            "economic_model": {
                "utility": [
                    "Governance voting rights",
                    "Staking rewards",
                    "Transaction fee discounts",
                    "Access to premium features",
                    "Revenue sharing"
                ],
                "incentives": [
                    "Early adopter bonuses",
                    "Long-term staking rewards",
                    "Referral program rewards",
                    "Liquidity mining incentives"
                ],
                "deflationary_mechanisms": [
                    "Transaction fee burn",
                    "Buyback and burn from revenue",
                    "Token buyback from profits"
                ],
                "inflationary_controls": [
                    "Fixed maximum supply",
                    "Controlled staking rewards emission",
                    "Timelocked team tokens"
                ]
            },
            "revenue_streams": [
                "Transaction fees",
                "Premium feature subscriptions",
                "Liquidity provision fees",
                "Governance proposal fees"
            ]
        }
        
        return model
    
    def _get_tokenomics_instructions(self, token_name: str, blockchain: str) -> str:
        """Get instructions for implementing tokenomics."""
        return f"""To implement {token_name} tokenomics on {blockchain}:
1. Deploy the token contract with proper allocation
2. Set up vesting contracts for team and ecosystem tokens
3. Create staking contracts for reward distribution
4. Establish liquidity pools on DEXs
5. Implement governance mechanisms
6. Set up buyback and burn mechanisms
7. Create monitoring and reporting systems"""
    
    def _generate_chainlink_oracle(self, blockchain: str, data_source: str) -> Dict[str, str]:
        """Generate Chainlink oracle integration."""
        oracle_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract {data_source.capitalize()}Oracle {{
    AggregatorV3Interface internal dataFeed;
    
    constructor() {{
        // Mainnet ETH/USD price feed
        if (block.chainid == 1) {{
            dataFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43F91BA7dECb302319d7D2C63B5);
        }}
        // Kovan testnet ETH/USD price feed
        else if (block.chainid == 42) {{
            dataFeed = AggregatorV3Interface(0x9326BFA0262b7F02220C71946C0c732e0f0b1f1c);
        }}
    }}
    
    function getLatestPrice() public view returns (int) {{
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = dataFeed.latestRoundData();
        return price;
    }}
    
    function getDecimals() public view returns (uint8) {{
        return dataFeed.decimals();
    }}
}}

contract PriceConsumer {{
    AggregatorV3Interface internal priceFeed;
    
    constructor() {{
        // Mainnet ETH/USD price feed
        if (block.chainid == 1) {{
            priceFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43F91BA7dECb302319d7D2C63B5);
        }}
        // Kovan testnet ETH/USD price feed
        else if (block.chainid == 42) {{
            priceFeed = AggregatorV3Interface(0x9326BFA0262b7F02220C71946C0c732e0f0b1f1c);
        }}
    }}
    
    function getThePrice() public view returns (int) {{
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }}
}}
"""
        
        return {f"{data_source}_oracle.sol": oracle_content}
    
    def _generate_band_oracle(self, blockchain: str, data_source: str) -> Dict[str, str]:
        """Generate Band Protocol oracle integration."""
        oracle_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IBandOracle {{
    function getReferenceData(string calldata _base, string calldata _quote) external view returns (uint256, uint256);
    function getReferenceDataBulk(string[] calldata _bases, string[] calldata _quotes) external view returns (uint256[] memory, uint256[] memory);
}}

contract {data_source.capitalize()}BandOracle {{
    IBandOracle public bandOracle;
    address public oracleAddress;
    
    constructor(address _oracleAddress) {{
        oracleAddress = _oracleAddress;
        bandOracle = IBandOracle(_oracleAddress);
    }}
    
    function getPrice(string memory base, string memory quote) public view returns (uint256) {{
        (uint256 price, ) = bandOracle.getReferenceData(base, quote);
        return price;
    }}
    
    function getPriceBulk(string[] memory bases, string[] memory quotes) public view returns (uint256[] memory) {{
        (uint256[] memory prices, ) = bandOracle.getReferenceDataBulk(bases, quotes);
        return prices;
    }}
}}
"""
        
        return {f"{data_source}_band_oracle.sol": oracle_content}
    
    def _get_oracle_instructions(self, oracle_type: str, blockchain: str, data_source: str) -> str:
        """Get instructions for oracle integration."""
        return f"""To integrate {oracle_type} oracle for {data_source} on {blockchain}:
1. Deploy the oracle contract to your target network
2. Configure the oracle with appropriate data feed addresses
3. Set up subscription or request mechanisms for data updates
4. Implement fallback mechanisms for data availability
5. Test oracle integration thoroughly
6. Monitor oracle performance and update configurations as needed"""
    
    def _check_contract_security(self, content: str) -> List[str]:
        """Check contract for common security issues."""
        issues = []
        
        # Check for reentrancy vulnerabilities
        if "transfer(" in content and "transferFrom(" in content:
            if not any(pattern in content for pattern in ["nonReentrant", "lock", "mutex"]):
                issues.append("Potential reentrancy vulnerability - consider using nonReentrant modifier")
        
        # Check for unchecked math operations
        if "uint" in content and not "SafeMath" in content:
            issues.append("Consider using SafeMath for arithmetic operations")
        
        # Check for proper access control
        if "onlyOwner" not in content and "AccessControl" not in content:
            issues.append("Missing access control for sensitive functions")
        
        # Check for proper input validation
        if "require(" not in content and "revert(" not in content:
            issues.append("Missing input validation")
        
        return issues


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "web3",
        "description": "Provides comprehensive Web3 and blockchain development capabilities",
        "version": "1.0.0",
        "domain": "web3",
        "functions": [
            {
                "name": "analyze_web3_project",
                "description": "Analyze a Web3 project to understand its structure and components"
            },
            {
                "name": "create_smart_contract",
                "description": "Create smart contracts for various blockchain use cases"
            },
            {
                "name": "implement_decentralized_app",
                "description": "Implement decentralized applications (dApps)"
            },
            {
                "name": "deploy_smart_contract",
                "description": "Deploy smart contracts to blockchain networks"
            },
            {
                "name": "implement_tokenomics",
                "description": "Implement comprehensive tokenomics for cryptocurrency tokens"
            },
            {
                "name": "integrate_oracle",
                "description": "Integrate oracle services for smart contracts"
            }
        ]
    }

def execute_function(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a function from this skill.
    
    Args:
        function_name: Name of the function to execute
        arguments: Arguments for the function
    
    Returns:
        Function execution result
    """
    skill = Web3Skill()
    
    if function_name == "analyze_web3_project":
        project_path = arguments.get("project_path")
        return skill.analyze_web3_project(project_path)
    elif function_name == "create_smart_contract":
        contract_name = arguments.get("contract_name")
        contract_type = arguments.get("contract_type", "erc20")
        blockchain = arguments.get("blockchain", "ethereum")
        features = arguments.get("features", [])
        return skill.create_smart_contract(contract_name, contract_type, blockchain, features)
    elif function_name == "implement_decentralized_app":
        app_type = arguments.get("app_type", "defi")
        blockchain = arguments.get("blockchain", "ethereum")
        frontend = arguments.get("frontend", "react")
        return skill.implement_decentralized_app(app_type, blockchain, frontend)
    elif function_name == "deploy_smart_contract":
        contract_path = arguments.get("contract_path")
        blockchain = arguments.get("blockchain", "ethereum")
        network = arguments.get("network", "testnet")
        return skill.deploy_smart_contract(contract_path, blockchain, network)
    elif function_name == "implement_tokenomics":
        token_name = arguments.get("token_name")
        token_symbol = arguments.get("token_symbol")
        total_supply = arguments.get("total_supply", 1000000)
        blockchain = arguments.get("blockchain", "ethereum")
        return skill.implement_tokenomics(token_name, token_symbol, total_supply, blockchain)
    elif function_name == "integrate_oracle":
        oracle_type = arguments.get("oracle_type", "chainlink")
        blockchain = arguments.get("blockchain", "ethereum")
        data_source = arguments.get("data_source", "price_feed")
        return skill.integrate_oracle(oracle_type, blockchain, data_source)
    else:
        return {"error": f"Unknown function: {function_name}"}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP-compatible invoke function for the Web3 skill.
    
    Args:
        payload: Dictionary containing function name and arguments
    
    Returns:
        Function execution result
    """
    function_name = payload.get("function_name")
    arguments = payload.get("arguments", {})
    
    return execute_function(function_name, arguments)

if __name__ == "__main__":
    # Test the skill
    skill = Web3Skill()
    
    print("Testing Web3 Skill...")
    
    # Test contract creation
    result = skill.create_smart_contract("MyToken", "erc20", "ethereum", ["pausable", "burnable"])
    print(f"Contract creation result: {result}")
    
    # Test dApp implementation
    result = skill.implement_decentralized_app("defi", "ethereum", "react")
    print(f"dApp implementation result: {result}")
