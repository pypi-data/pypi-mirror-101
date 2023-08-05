import http.client
import json
from tatumpython.validator import blockchain as blockchain_validator
import requests
import os
from dotenv import load_dotenv
from bip_utils import Bip39EntropyGenerator, Bip39MnemonicGenerator, Bip39WordsNum, Bip39MnemonicValidator, Bip39SeedGenerator
from pywallet import wallet
import mnemonic as eth_mnemonic
import pprint
import binascii
import mnemonic
import bip32utils
import hashlib
import base58
import time

from web3 import Web3, IPCProvider
load_dotenv()

# web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/0fb2f5e906884367b08fdec2e556b4c1'))

# web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/5ff8e077421744bca6c544a5e56756df"))



# print(web3.isConnected())

# account_1 = "0xbc0eeF3EA8D30588a2d73AaAa8BA63267F03F66d"
# account_2 = "0x3d57AFe9Ee276D6E502Dee0D431133410A24d745"
# private_key_1 = "f846ca52e73d4edb43f12fcad3e47712700efa2d342c701e50188ca271e5f8fd"

# nonce = web3.eth.getTransactionCount(account_1)

# tx = {
#         'to': account_2,
#         'value': web3.toWei(1, 'ether'),
#         'gas': 2000000,
#         'gasPrice': web3.toWei('50', 'gwei'),
#         'nonce': nonce,
        # 'chainId': 3, #https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids
        # nastavit pro testnet a mainnet
# }

# signed_txn = web3.eth.account.signTransaction(tx, private_key_1)
# tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
# print(web3.toHex(tx_hash))

# address = web3.toChecksumAddress('0xCce01eD49A624F4F5206dc2cCb908075547306eb')

# web3.eth.defaultAccount = web3.eth.accounts[0] #who create contract
# abi = json.loads('[{"constant":true,"inputs":[],"name":"getCurrentOpinion","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_soapboxer","type":"address"}],"name":"isApproved","outputs":[{"name":"approved","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_opinion","type":"string"}],"name":"broadcastOpinion","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_soapboxer","type":"address"},{"indexed":false,"name":"_opinion","type":"string"}],"name":"OpinionBroadcast","type":"event"}]')
# byte_code= '608060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680635f1d90ae146100c0578063673448dd14610150578063805c2b6c146101ab575b66470de4df8200003411156100be5760016000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055505b005b3480156100cc57600080fd5b506100d561022c565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101155780820151818401526020810190506100fa565b50505050905090810190601f1680156101425780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561015c57600080fd5b50610191600480360381019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506102ce565b604051808215151515815260200191505060405180910390f35b3480156101b757600080fd5b50610212600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610323565b604051808215151515815260200191505060405180910390f35b606060018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102c45780601f10610299576101008083540402835291602001916102c4565b820191906000526020600020905b8154815290600101906020018083116102a757829003601f168201915b5050505050905090565b60008060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff169050919050565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561048457816001908051906020019061038c92919061048e565b507fcda4350c176dee701be26e34bb6ddef641e5f6847b5ff6ca83ccca7faa85ddaf336001604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018060200182810382528381815460018160011615610100020316600290048152602001915080546001816001161561010002031660029004801561046c5780601f106104415761010080835404028352916020019161046c565b820191906000526020600020905b81548152906001019060200180831161044f57829003601f168201915b5050935050505060405180910390a160019050610489565b600090505b919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106104cf57805160ff19168380011785556104fd565b828001600101855582156104fd579182015b828111156104fc5782518255916020019190600101906104e1565b5b50905061050a919061050e565b5090565b61053091905b8082111561052c576000816000905550600101610514565b5090565b905600a165627a7a72305820e1048c48b1c3fdcb61f121c5dc1c2db485b2a98d1461a28be351104f41063e5a0029'
# Contract = web3.eth.contract(abi=abi, bytecode=byte_code)
# deploy s mými argumenty a pak už si volám metody ze smlouvy
# tx_hash = Contract.constructor().transact()
# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# print(tx_receipt)







# contract_address = '0x0C0db1Eeb7c420eBebf34C50c80da0C6361688d7'
# wallet_private_key = '0xc2b15388fcc36ce104842dcf9c18dcd5dd87f765f511e569a4037965afd92845'
# wallet_address = '0x5911774BC465d36135516D60bDAA361bb8587aF1'
# Because we’re using some features of Web3.py that haven’t been fully audited for security, we need to call w3.eth.enable_unaudited_features() to acknowledge that we’re aware that bad things might happen
# web3.eth.enable_unaudited_features()

ganache_url = os.environ['Ganache_url']
web3 = Web3(Web3.HTTPProvider(ganache_url))

conn = http.client.HTTPSConnection(os.environ['API_URL'])
API_KEY = os.environ['API_KEY']

def headers(for_post = False):
    if for_post:
        return {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }
    else:
        return {
            'x-api-key': API_KEY
            }

def generate_ethereum_wallet(query_params={}):
    if blockchain_validator.generate_litecoin_wallet(query_params):
        if query_params != {}:
            mnemonic = query_params['mnemonic']
        else:
            mnemonic = wallet.generate_mnemonic(strength=256)

        if Bip39MnemonicValidator(mnemonic).Validate():
            w = wallet.create_wallet(network="ETH", seed=mnemonic, children=1)
            return {"xpriv": w['xprivate_key'].decode("utf-8"), 
                    "xpub": w['xpublic_key'].decode("utf-8") , 
                    "mnemonic": mnemonic}
        else:
            return 'Mnemonic is not valid!'

def generate_ethereum_account_address_from_extended_public_key(path_params):
    if blockchain_validator.generate_deposit_address_from_extended_public_key(path_params):
        w = wallet.create_address(network="ETH", xpub=path_params['xpub'], child=path_params['index'])
        return {"address": w['address']}

def generate_ethereum_private_key(body_params):
    if blockchain_validator.generate_private_key(body_params):
        if Bip39MnemonicValidator(body_params['mnemonic']).Validate():
            mobj = mnemonic.Mnemonic("english")
            seed = mobj.to_seed(body_params['mnemonic'])

            bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
            bip32_child_key_obj = bip32_root_key_obj.ChildKey(
                44 + bip32utils.BIP32_HARDEN
            ).ChildKey(
                60 + bip32utils.BIP32_HARDEN
            ).ChildKey(
                0 + bip32utils.BIP32_HARDEN
            ).ChildKey(0).ChildKey(body_params['index'])

            wif = bip32_child_key_obj.WalletImportFormat()

            first_encode = base58.b58decode(wif)
            private_key_full = binascii.hexlify(first_encode)
            private_key = '0x' + private_key_full[2:-10].decode("utf-8")
            return {
                'key': private_key,
            }
        else:
            return 'Mnemonic is not valid!'

def web3_http_driver(body_params):
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/v3/ethereum/web3/{}".format(API_KEY), body_params, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_current_block():
    conn.request("GET", "/v3/ethereum/block/current", headers=headers())
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_block_by_hash(path_params):
    if blockchain_validator.ethereum_get_block_hash(path_params):
        conn.request("GET", "/v3/ethereum/block/{}".format(path_params['hash']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_account_balance(path_params):
    if blockchain_validator.get_ethereum_account_balance(path_params):
        conn.request("GET", "/v3/ethereum/account/balance/{}".format(path_params['address']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_erc20_account_balance(path_params, query_params = {}):
    if blockchain_validator.get_ethereum_erc20_account_balance(path_params, query_params):
        currency = ''
        contractAddress = ''
        if 'currency' in query_params.keys():
            currency = "currency={}".format(query_params['currency'])
        if 'contractAddress' in query_params.keys():
            currency = "contractAddress={}".format(query_params['contractAddress'])
        conn.request("GET", "/v3/ethereum/account/balance/erc20/{}?{}&{}".format(path_params['address'], contractAddress, currency), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_transaction(path_params):
    if blockchain_validator.get_block_by_hash_or_height(path_params):
        conn.request("GET", "/v3/ethereum/transaction/{}".format(path_params['hash']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_count_of_outgoing_ethereum_transactions(path_params):
    if blockchain_validator.get_count_of_outgoing_ethereum_transactions(path_params):
        conn.request("GET", "/v3/ethereum/transaction/count/{}".format(path_params['address']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_transactions_by_address(path_params, query_params):
    if blockchain_validator.get_transaction_by_address(path_params, query_params):
        if len(query_params) != 1:
            conn.request("GET", "/v3/ethereum/transaction/address/{}?pageSize={}&offset={}".format(path_params['address'], query_params['pageSize'], query_params['offset']), headers=headers())
        else:
            conn.request("GET", "/v3/ethereum/transaction/address/{}?pageSize={}".format(path_params['address'], query_params['pageSize']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def send_ethereum_erc20_from_account_to_account(body_params):
    # https://hackernoon.com/ethereum-smart-contracts-in-python-a-comprehensive-ish-guide-771b03990988
    # http://remix.ethereum.org/#optimize=false&evmVersion=null&version=soljson-v0.6.6+commit.6c089d02.js
    if blockchain_validator.send_ethereum_erc20_from_account_to_account(body_params):  
        
        amount_in_wei = web3.toWei(body_params['amount'],'ether')
        nonce = web3.eth.getTransactionCount(os.environ['from'])
    # kde získám nonce nebo adresu smlouvy?
        txn_dict = {
                'to': body_params['to'],
                'value': amount_in_wei,
                'gas': int(body_params['fee']['gasLimit']),
                'gasPrice': web3.toWei(body_params['fee']['gasPrice'], 'gwei'),
                'nonce': nonce,
                # 'chainId': 3, #https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids
                # nastavit pro testnet a mainnet
        }

        signed_txn = web3.eth.account.signTransaction(txn_dict, body_params['fromPrivateKey'])
    # broadcast na tatum api
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return(txn_hash.hex()[2:])
   

def invoke_smart_contract_method(body_params):
    if blockchain_validator.invoke_smart_contract_method(body_params):
        contract = web3.eth.contract(abi=body_params['methodABI'],address=body_params['contractAddress'])
        if(len(body_params['params'])==0):
          if('name'== body_params['methodName']):
            return({'data': contract.functions.name().call()})
          if('symbol' == body_params['methodName']):
            return({'data':contract.functions.symbol().call()})
          if('decimals' == body_params['methodName']):
            return({'data':contract.functions.decimals().call()})
          if('totalSupply' == body_params['methodName']):
            return({'data':contract.functions.totalSupply().call()})
        else:
          if('balanceOf' == body_params['methodName']):
            return({'data':contract.functions.balanceOf(body_params['params']['address']).call()})    

def deploy_ethereum_erc20_smart_contract(body_params): 
    if blockchain_validator.deploy_ethereum_erc20_smart_contract(body_params):
        abi = json.loads('[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_decimals","type":"uint256"},{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
        bytecode = '0x60806040523480156200001157600080fd5b506040516200101c3803806200101c833981810160405260808110156200003757600080fd5b81019080805160405193929190846401000000008211156200005857600080fd5b838201915060208201858111156200006f57600080fd5b82518660018202830111640100000000821117156200008d57600080fd5b8083526020830192505050908051906020019080838360005b83811015620000c3578082015181840152602081019050620000a6565b50505050905090810190601f168015620000f15780820380516001836020036101000a031916815260200191505b50604052602001805160405193929190846401000000008211156200011557600080fd5b838201915060208201858111156200012c57600080fd5b82518660018202830111640100000000821117156200014a57600080fd5b8083526020830192505050908051906020019080838360005b838110156200018057808201518184015260208101905062000163565b50505050905090810190601f168015620001ae5780820380516001836020036101000a031916815260200191505b5060405260200180519060200190929190805190602001909291905050508360019080519060200190620001e4929190620002fa565b508260009080519060200190620001fd929190620002fa565b50816002819055508060038190555080600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055507fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60003383604051808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001935050505060405180910390a150505050620003a9565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200033d57805160ff19168380011785556200036e565b828001600101855582156200036e579182015b828111156200036d57825182559160200191906001019062000350565b5b5090506200037d919062000381565b5090565b620003a691905b80821115620003a257600081600090555060010162000388565b5090565b90565b610c6380620003b96000396000f3fe608060405234801561001057600080fd5b50600436106100935760003560e01c8063313ce56711610066578063313ce5671461022557806370a082311461024357806395d89b411461029b578063a9059cbb1461031e578063dd62ed3e1461038457610093565b806306fdde0314610098578063095ea7b31461011b57806318160ddd1461018157806323b872dd1461019f575b600080fd5b6100a06103fc565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100e05780820151818401526020810190506100c5565b50505050905090810190601f16801561010d5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6101676004803603604081101561013157600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919050505061049a565b604051808215151515815260200191505060405180910390f35b6101896105c6565b6040518082815260200191505060405180910390f35b61020b600480360360608110156101b557600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506105cc565b604051808215151515815260200191505060405180910390f35b61022d6107e5565b6040518082815260200191505060405180910390f35b6102856004803603602081101561025957600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506107eb565b6040518082815260200191505060405180910390f35b6102a3610834565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156102e35780820151818401526020810190506102c8565b50505050905090810190601f1680156103105780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b61036a6004803603604081101561033457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506108d2565b604051808215151515815260200191505060405180910390f35b6103e66004803603604081101561039a57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506108e9565b6040518082815260200191505060405180910390f35b60018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156104925780601f1061046757610100808354040283529160200191610492565b820191906000526020600020905b81548152906001019060200180831161047557829003601f168201915b505050505081565b600081600560003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055507f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925338484604051808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001935050505060405180910390a16001905092915050565b60035481565b600081600560008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205410156106c0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260168152602001807f496e73756666696369656e7420616c6c6f77616e63650000000000000000000081525060200191505060405180910390fd5b61074f82600560008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461097090919063ffffffff16565b600560008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506107da84848461098d565b600190509392505050565b60025481565b6000600460008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108ca5780601f1061089f576101008083540402835291602001916108ca565b820191906000526020600020905b8154815290600101906020018083116108ad57829003601f168201915b505050505081565b60006108df33848461098d565b6001905092915050565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905092915050565b60008282111561097f57600080fd5b818303905080905092915050565b80600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015610a42576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260148152602001807f496e73756666696369656e742062616c616e636500000000000000000000000081525060200191505060405180910390fd5b610a9481600460008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461097090919063ffffffff16565b600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610b2981600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054610c1090919063ffffffff16565b600460008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055507fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef838383604051808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001935050505060405180910390a1505050565b6000818301905082811015610c2457600080fd5b8090509291505056fea26469706673582212207eb0f0486d27c5319179c35cb94906b79b838ba9f0ca467d8d54d03313e661fa64736f6c63430006010033'
        token = web3.eth.contract(abi=abi,bytecode=bytecode)
        # here from address means from with account we want to deploy smart contract
        tx = token.constructor(body_params['name'],body_params['symbol'],body_params['digits'],int(body_params['supply'])).transact({'from':body_params['address']})
        return ({'txId ': tx.hex()[2:], 'failed':'false'})

def deploy_ethereum_erc721_smart_contract(body_params):
    if blockchain_validator.deploy_ethereum_erc721_smart_contract(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/erc721/deploy", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def mint_ethereum_erc721(body_params):
    if blockchain_validator.mint_ethereum_erc721(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/erc721/mint", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def transfer_ethereum_erc721_token(body_params):
    if blockchain_validator.transfer_ethereum_erc721_token(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/erc721/transaction", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def mint_ethereum_erc721_multiple_tokens(body_params):
    if blockchain_validator.mint_ethereum_erc721_multiple_tokens(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/erc721/mint", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def burn_ethereum_erc721(body_params):
    if blockchain_validator.burn_ethereum_erc721(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/erc721/burn", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_erc721_account_balance(path_params):
    if blockchain_validator.get_ethereum_erc721_account_balance(path_params):
        conn.request("GET", "/v3/ethereum/erc721/balance/{}/{}".format(path_params['address'], path_params['contractAddress']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_erc721_token(path_params):
    if blockchain_validator.get_ethereum_erc721_token(path_params):
        conn.request("GET", "/v3/ethereum/erc721/token/{}/{}/{}".format(path_params['address'],path_params['index'], path_params['contractAddress']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_erc721_token_metadata(path_params):
    if blockchain_validator.get_ethereum_erc721_token_metadata(path_params):
        conn.request("GET", "/v3/ethereum/erc721/metadata/{}/{}".format(path_params['token'], path_params['contractAddress']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def get_ethereum_erc721_token_owner(path_params):
    if blockchain_validator.get_ethereum_erc721_token_metadata(path_params):
        conn.request("GET", "/v3/ethereum/erc721/owner/{}/{}".format(path_params['token'], path_params['contractAddress']), headers=headers())
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def broadcast_signed_ethereum_transaction(body_params):
    if blockchain_validator.broadcast_signed_transaction(body_params):
        body_params = json.dumps(body_params)
        conn.request("POST", "/v3/ethereum/broadcast", body_params, headers=headers(for_post=True))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

def estimate_ethereum_transaction_fees(body_params):
    if blockchain_validator.estimate_ethereum_transaction_fees(body_params):
        gaslimit = web3.eth.estimateGas({"from":body_params["from"],"to":body_params["to"],"amount":body_params["amount"]})
        gasprice = web3.eth.gasPrice
        return({"gasLimit":gaslimit,"gasPrice":gasprice})

def transfer_ethereum_erc20(body_params):
    if blockchain_validator.transfer_ethereum_erc20(body_params):
        abi = json.loads('[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_decimals","type":"uint256"},{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
        # after deploying the contract we will get contract address I have used local blockchain ganache
        address = web3.toChecksumAddress(body_params['contractAddress'])
        contract = web3.eth.contract(abi= abi ,address = address)
        # here from address is contract created account address
        tx = contract.functions.transfer(body_params['to'],int(body_params['amount'])).transact({'from': os.environ['from']}) 
        return({'txId ': tx.hex()[2:], 'failed':'false'})

