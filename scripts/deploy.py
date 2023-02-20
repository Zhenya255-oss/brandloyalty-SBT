from brownie import BrandLoyalty, accounts, config
import json, requests, os, typing as tp
from pinata import Pinata
from flask import request


base_json_folder = config["pinata"]["base-json-folder"]
base_json_file = config["pinata"]["base-json-file"]
base_json_uri = config["pinata"]["base-json-uri"]

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
headers = {
    "pinata_api_key": config["pinata"]["api-keys"],
    "pinata_secret_api_key": config["pinata"]["api-private"],
    "pinata_access_token": config["pinata"]["access-token"]
}

### json utilities ###

def update_json(file_path, brand_names, brand_vals, token_id):
    with open(file_path, 'r') as fp:
        information = json.load(fp)
        attributes = information["attributes"]
        brand_count = 0
        total_brands = 4
        for attribute in attributes:
            update_fields(attribute, brand_names[brand_count], brand_vals[brand_count])
            brand_count += 1
            if brand_count == 5:
                break
        with open(file_path[0:-5] + str(token_id) + ".json", 'w') as fp:
            json.dump(information, fp, indent=2)

def update_fields(attr_dict, brand_name, brand_count):
    attr_dict["trait_type"] = brand_name
    attr_dict["value"] = brand_count

### pinata utilities ###

def upload_file_to_pinata(filepath):
    
    pinata = Pinata(config["pinata"]["api-keys"],config["pinata"]["api-private"], config["pinata"]["access-token"])
    result = pinata.pin_file(config["pinata"]["base-json-file"])
    return result["data"]["IpfsHash"]

def main():
    
    ### initialize accounts and brands
    admin = accounts[0]
    buyer = accounts[1]
    brand1 = accounts[2]
    brand2 = accounts[3]
    brand3 = accounts[4]
    brand4 = accounts[5]
    brand5 = accounts[6]

    ### deploy smart contract/get the latest deployed
    contract = BrandLoyalty.deploy({"from": admin})
    # get the latest smart contract
    #contract = BrandLoyalty[-1]
    
    ### get a transaction cost
    contract_fee = contract.cost()
    payment = 1 *10**18
    total_funds_transfer = contract_fee + payment
    
    ### add brands to a smart contract
    contract.addBrand(brand1, "Nike")
    contract.addBrand(brand2, "Adidas")
    contract.addBrand(brand3, "Reebok")
    contract.addBrand(brand4, "Lululemon")
    contract.addBrand(brand5, "Puma")

    ### fetch brand names
    brand_name_list = []
    brand1_name = contract.brandName(str(contract.brandIAddress(0)))
    brand_name_list.append(brand1_name)
    brand2_name = contract.brandName(str(contract.brandIAddress(1)))
    brand_name_list.append(brand2_name)
    brand3_name = contract.brandName(str(contract.brandIAddress(2)))
    brand_name_list.append(brand3_name)
    brand4_name = contract.brandName(str(contract.brandIAddress(3)))
    brand_name_list.append(brand4_name)
    brand5_name = contract.brandName(str(contract.brandIAddress(4)))
    brand_name_list.append(brand5_name)

    ### mint new token of a brand group and buy
    mint_cost = 0.01 *10**18
    contract.safeMint(buyer, base_json_uri, {"from": buyer, "value": mint_cost})
    contract.buy(brand1, {"from": buyer, "value": total_funds_transfer})

    ### fetch loyalty data
    brand_counter_list = []
    brand_counter_list = list (contract.BrandLoyalty(buyer))

    ### generate new ipfs json file
    token_id = contract.ownerId(buyer)
    update_json(base_json_file, brand_name_list, brand_counter_list, token_id)

    ### upload to pinata
    ipfs_hash = upload_file_to_pinata(base_json_folder)

    ### update SBT
    token_id = contract.ownerId(buyer)
    uri = "https://gateway.pinata.cloud/ipfs/" + ipfs_hash
    contract.updateSBT(uri, token_id)
    
    #soul.safeMint(accounts[1], "https://gateway.pinata.cloud/ipfs/QmVcHY1ix3dKCtAvzJqEGJv78QSLcJXSpjGk8KZ7UUEEZT", {"from": admin, "value": cost})
    #mn = Moodnet[-1]
    #print(mn)
    #print(soul.getSoul(accounts[1],int(1)))
    # soul.mint(admin)


    