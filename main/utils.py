from web3 import Web3
import json
import os

ganache_connection = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_connection))

def getInfoToken():
    infoToken = {}
    File = json.load(open('blockc/build/contracts/GreenToken.json'))
    
    Abi = File['abi']
    addr = '0x08EAaa39E5566c9545927E1D00D5e9f70Ec6e2B3'  #<-----------put here contract address

    infoToken['abi'] = json.dumps(Abi)
    infoToken['address'] = addr
    
    return infoToken
    
#create a new wallet for the customer
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
    
    infAdm['balance'] = instance.functions.balanceOf("0x65e9CB765eb38Bdd7D2B6eb7E4412c112029F0f9").call()
    
    return infAdm

