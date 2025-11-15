import json
from web3 import Web3

# -----------------------------
# 1. HARD-CODED BLOCKCHAIN INFO
# -----------------------------

# Hardhat local RPC
RPC_URL = "http://127.0.0.1:8545"

# Your Hardhat Account #0
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ACCOUNT_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

# -----------------------------
# 2. CONNECT WEB3
# -----------------------------

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Convert private key into usable account
account = w3.eth.account.from_key(PRIVATE_KEY)

# -----------------------------
# 3. LOAD DEPLOYED CONTRACT INFO
# -----------------------------

with open("backend/deployedInfo.json") as f:
    info = json.load(f)

contract_address = info["address"]

# Load Solidity ABI
with open("artifacts/contracts/HealthRecords.sol/HealthRecords.json") as f:
    abi = json.load(f)["abi"]

contract = w3.eth.contract(address=contract_address, abi=abi)

# -----------------------------
# 4. FUNCTION → Write To Blockchain
# -----------------------------

def add_report_on_chain(patient_id, ipfs_cid, encrypted_key):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    tx = contract.functions.uploadReport(
        patient_id, ipfs_cid, encrypted_key
    ).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "nonce": nonce,
        "gas": 3000000
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # IMPORTANT FIX HERE
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()

def get_reports_from_chain(patient_id: str):
    """
    Returns list of reports for patient_id.
    Each item is a dict: { "patient_id", "ipfs_cid", "encrypted_key", "timestamp" }
    """
    # call the contract view function
    raw = contract.functions.getReports(patient_id).call()

    results = []
    # raw is list of tuples: (patientId, ipfsCid, encryptedKey, timestamp)
    for item in raw:
        # item[3] might be int or Hex--convert to int if necessary
        results.append({
            "patient_id": item[0],
            "ipfs_cid": item[1],
            "encrypted_key": item[2],
            "timestamp": int(item[3])
        })
    return results