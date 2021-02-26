from web3 import Web3
import json
import os
from main.models import Contract, Wallet
from shippingToken.settings import ADDR_CONTRACT


ganache_connection = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_connection))


def initializeChain():
    infoGreenToken = json.load(open('blockc/build/contracts/GreenToken.json'))
    infoAbi = infoGreenToken['abi']
    infoBytecode = infoGreenToken['bytecode']
    contract = w3.eth.contract(bytecode=infoBytecode, abi=infoAbi)
    
    admin = w3.eth.accounts[0]
    print(admin)

    txContract = contract.constructor().buildTransaction({
        'from': admin,
        'nonce': w3.eth.getTransactionCount(admin.address),
        'gas': 2000000,
        'gasPrice': w3.toWei('21', 'gwei')
    })

    txSigned = admin.signTransaction(txContract)

    txHash = w3.eth.sendRawTransaction(txSigned.rawTransaction)

    txRec = w3.eth.waitForTransactionReceipt(txHash)
    print(txRec['contractAddress'])

    #save the contract info into db
    depContract = Contract.objects.create(abiC = infoAbi, addressC = txRec['contractAddress']) 
    depContract.save()


def getInfoToken():
    infoToken = {}
    File = json.load(open('blockc/build/contracts/GreenToken.json'))
    
    Abi = File['abi']
    addr = '0x0843d9521D4B01DB9DDA79B79da08453E1B415Fa' #<-----------put here contract address

    infoToken['abi'] = json.dumps(Abi)
    infoToken['address'] = addr

    
    
    return infoToken
    

#create a new wallet for the customer (account[0])
def createNewWallet(passw):
    account = w3.eth.account.create()
    balance = w3.eth.getBalance(account.address)
    cryptKey = account.encrypt(passw)

    #save data into JSON format
    wallData = {
        'address': account.address,
        'balance': balance,
        'cryptKey': cryptKey
    }
        
    return wallData


#method to reward tokens
def receiveToken(address):
    updbalance = {}
    contrToken = getInfoToken()
    instance = w3.eth.contract(abi=contrToken['abi'], address=contrToken['address'])
    
    #get admins address
    admin_account = w3.eth.accounts[0]
    
    #call function into smart contract
    tx_hash = instance.functions.transfer(address, 1).transact({'from': admin_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    updbalance['balance'] = instance.functions.balanceOf(address).call()

    wal = Wallet.objects.get(address=address)
    wal.balance = updbalance['balance']
    wal.state = True
    wal.save()

    print(updbalance['balance'])
    return updbalance['balance']


def getBalance(address):
    bal = {}
    contrToken = getInfoToken()
    instance = w3.eth.contract(abi=contrToken['abi'], address=contrToken['address'])

    bal = instance.functions.balanceOf(address).call()
    return bal


def getAdminInfo():
    infAdm = {}
    contrToken = getInfoToken()
    instance = w3.eth.contract(abi=contrToken['abi'], address=contrToken['address'])
    
    infAdm['address'] = w3.eth.accounts[0]
    infAdm['balance'] = instance.functions.balanceOf(infAdm['address']).call()
    
    return infAdm

