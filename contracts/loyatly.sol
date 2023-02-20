// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

import "@openzeppelin/token/ERC721/ERC721.sol";
import "@openzeppelin/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/access/Ownable.sol";
import "@openzeppelin/utils/Counters.sol";


contract BrandLoyalty is ERC721, ERC721URIStorage, Ownable {
    
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("BrandLoyalty", "BL") {
        operator = msg.sender;
        brandCounter = 0;
    }

    address public operator;
    uint256 brandCounter;
    uint256 public cost = 0.05 *10**18;
    uint256 public mint_cost = 0.01 *10**18;

    mapping (address => string) public brandName;
    mapping (string => address) public brandAddress;
    mapping (address => uint256) public brandId;
    mapping (uint256 => address) public brandIAddress;
    mapping (address => uint256) public ownerId;

    struct BrandCounter {
       uint256 brand1;
       uint256 brand2;
       uint256 brand3;
       uint256 brand4;
       uint256 brand5;
       }

    mapping (address => BrandCounter) public BrandLoyalty;

    function addBrand(address brand_address, string memory brand_name) public {
        require (msg.sender == operator, "Only administrator can add new brands");
        
        brandCounter = brandCounter + 1;
        
        brandName[brand_address] = brand_name;
        brandAddress[brand_name] = brand_address;
        brandId[brand_address] = brandCounter;
        brandIAddress[brandCounter] = brand_address;
    }

    function buy(address payable brand_address) public virtual payable {
        require(msg.value >= cost, "Not enough money on your account");
        
        brand_address.transfer(msg.value - cost);
        uint256 brand_counter = brandId[brand_address];
        if (brand_counter == 1) {
            BrandLoyalty[msg.sender].brand1 = BrandLoyalty[msg.sender].brand1 + 1;
        }
        else if (brand_counter == 2) {
            BrandLoyalty[msg.sender].brand2 = BrandLoyalty[msg.sender].brand2 + 1;
        }
        else if (brand_counter == 3) {
            BrandLoyalty[msg.sender].brand3 = BrandLoyalty[msg.sender].brand3 + 1;
        }
        else if (brand_counter == 4) {
            BrandLoyalty[msg.sender].brand4 = BrandLoyalty[msg.sender].brand4 + 1;
        }
        else if (brand_counter == 5) {
            BrandLoyalty[msg.sender].brand5 = BrandLoyalty[msg.sender].brand5 + 1;
        }
        else {
        }
        
    }
    
    function safeMint(address _to, string memory base_uri) public virtual payable {
        require(msg.value >= mint_cost, "Not enough money on your account");
        
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _safeMint(_to, tokenId);
        _setTokenURI(tokenId, base_uri);
        ownerId[_to] = tokenId;
    }

    function updateSBT(string memory uri, uint256 token_Id) public {
        require(msg.sender == operator, "Only owner can update SBT");
        _setTokenURI(token_Id, uri);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

}