# Web3 python - Simple Storage

## Compiling the Solidity Code from Python

```python
# install py-solc-x for compiling solidity file
import json
from solcx import compile_standard, install_solc
install_solc("0.6.0")

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
```

- First we open the file
- then compile the code using the above compile_standard syntax
- Then dump the contents into a new file named “compiled_sol” using json.dump

## Getting our ByteCode and ABI

In order to deploy our contract we need the byte code and abi and we will get it from our compiled_sol

```python
# install py-solc-x for compiling solidity file
import json
from solcx import compile_standard, install_solc
install_solc("0.6.0")

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
```

# Now we need something in which we are going to deploy our code virtually so we will do it using “Ganache”

[Truffle Suite - Truffle Suite](https://trufflesuite.com/ganache/)

Download It

- Now we will click on Quickstart Button in Ganache
- We will get a screen like this

![Screenshot 2022-02-05 at 7.32.33 PM.png](Web3%20python%20-%20Simple%20Storage%2059346cc950614329ac52723f5783e7a6/Screenshot_2022-02-05_at_7.32.33_PM.png)

- Install [Web3.py](http://Web3.py)

```bash
pip install web3
```

## Now we will see how we will connect our blockchain contract with a network  (Ganache)→

1. Import Web3 Library in our code

```python
from web3 import Web3
```

1. create a HTTP Provider and connect to blockchain 

```python
w3 = Web3(Web3.HTTPProvider("network_link_here"))
# Here we are connected to our Ganache network
```

1. Write your creds

```python
# Our credentials
chain_id = 1337
my_address = "your_address"
private_key = "your_private_key"
```

1. Create a contract in python

```python
# Create Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)
# This will print <class 'web3._utils.datatypes.Contract'>
```

1. Get the nonce (It is defined as the total number of transactions done on an account)

```python
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
```

## How to send a transaction →

1. Build a transaction
2. Sign a transaction
3. send the transaction

```python
# transaction building
transaction = SimpleStorage.constructor().buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price
})
# print(transaction)

# signing the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
# print(signed_transaction)

# sending the signed transaction
transaction_hash = w3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)

# wait for block confirmations
transaction_recipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(transaction_recipt)
```

# Working with the contract →

For working with contract we need :

- Contract Address
- Contract ABI

1. Getting the deployed contract Address

```python
# Getting the deployed contract
simple_storage = w3.eth.contract(
    address=transaction_recipt.contractAddress, abi=abi)
```

1. We can interact in two ways with our Contract :
- Call → Simulate making the call and getting the value (no state change involved)
- Transact -> actually make a state change

Call Functions

```python
print(simple_storage.functions.retrieve().call())
```

Transact Functions

```python
# how to make a transaction on our contract
storage_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1, # using nonce + 1,beacuse nonce value is already used once so we have to change it in order to make a transaction
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
```

# Final Code →

```python
# install py-solc-x for compiling solidity file
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
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
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
```

### Output →

```python
Blockchain Connected....
Contract created using bytecode and abi
Transaction build successfull 🎯
Transaction success ✅
Contract for interaction initialised 🗳️
-------------------------------------------
Initial value (Favorite Number) : 
0
-------------------------------------------
Store(15) transaction done ✅
Transaction Recipt ->
AttributeDict({'transactionHash': HexBytes('0x4b6a97ff70a77c5ce62c6e59e9d6d8a02a0af629fb192b7fc32ad48b18b78050'), 'transactionIndex': 0, 'blockHash': HexBytes('0xf6b1bca9c9ca1290798cec30a0b90fd872be0459e3030f63f184b3df9d2f0e84'), 'blockNumber': 16, 'from': '0x3e8683715c1455d051Cd0BFf6f6e087b29823529', 'to': '0xd302C0D225B08f4ed5dEE368902F247353629C45', 'gasUsed': 41518, 'cumulativeGasUsed': 41518, 'contractAddress': None, 'logs': [], 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
-------------------------------------------
Final value (Favorite Number) : 
15
-------------------------------------------
```

![Screenshot 2022-02-05 at 11.42.51 PM.png](Web3%20python%20-%20Simple%20Storage%2059346cc950614329ac52723f5783e7a6/Screenshot_2022-02-05_at_11.42.51_PM.png)

# Yay!! We have integrated our First Contract with Python  🎉🍻