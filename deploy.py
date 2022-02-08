# install py-solc-x for compiling solidity file
# Deployed on Ganache-CLI
import os
import json
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc
install_solc("0.6.0")

load_dotenv()

# Getting file
with open("./SimpleStorage.sol", 'r') as file:
    simple_storage_file = file.read()

# Compile our solidity code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                }
            }
        }
    },
    solc_version="0.6.0",
)

with open("compiled__code.json", 'w') as file:
    json.dump(compiled_sol, file)

# get bytecode
# here we are just extracting the data from our compiled solidity code
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache

# HTTP Provider (for connecting to blockchain)
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
print("Blockchain Connected....")
# Our credentials
chain_id = 1337
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)
# This will print <class 'web3._utils.datatypes.Contract'>
print("Contract created using bytecode and abi")
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1. Build a Transaction
# 2. Sign a Transaction
# 3. Send a Transaction

# transaction building
transaction = SimpleStorage.constructor().buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price
})
print("Transaction build successfull 🎯")

# signing the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
# print(signed_transaction)

# sending the signed transaction
transaction_hash = w3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)

# wait for block confirmations
transaction_recipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
# print(transaction_recipt)
print("Transaction success ✅")

# Working with the Contract ->

# for working with contract we always need :
# * Contract Address
# * Contract ABI

# Getting the deployed contract
simple_storage = w3.eth.contract(
    address=transaction_recipt.contractAddress, abi=abi)

print("Contract for interaction initialised 🗳️")

# We can interact in two ways with our Contract :
# Call -> Simulate making the call and getting the value (no state change involved)
# Transact -> actually make a state change

# initial value of favoriteNumber (from contract)
print("-------------------------------------------")
print("Initial value (Favorite Number) : ")
print(simple_storage.functions.retrieve().call())
print("-------------------------------------------")
# print(simple_storage.functions.store(15).call())

# how to make a transaction on our contract
storage_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1,
    "gasPrice": w3.eth.gas_price
})
signed_storage_transaction = w3.eth.account.sign_transaction(
    storage_transaction, private_key=private_key
)
send_storage_transaction = w3.eth.send_raw_transaction(
    signed_storage_transaction.rawTransaction)
print("Store(15) transaction done ✅")

transaction_recipt = w3.eth.wait_for_transaction_receipt(
    send_storage_transaction)
print("Transaction Recipt ->")
print(transaction_recipt)

print("-------------------------------------------")
print("Final value (Favorite Number) : ")
print(simple_storage.functions.retrieve().call())
print("-------------------------------------------")
