from model.Wallet import Wallet
from web3 import Web3
import requests

class ETHWallet(Wallet):

    def __init__(self, _scannerAPI, _priceAPI, _transactionAPI, _wallet_address, _asset_symbol, _asset_decimals, _asset_contract_address, _asset_contract_abi=None):
        
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{}'.format(_scannerAPI)))
        self.priceAPI = _priceAPI
        self.transactionAPI = _transactionAPI

        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals
        self.isToken = False
        if _asset_contract_address != "0x0000000000000000000000000000000000000000":
            self.token = self.web3.eth.contract(address=_asset_contract_address, abi=_asset_contract_abi)
            self.isToken = True
            
        self.wallet_address = _wallet_address
    
    def get_balance(self):
        # Return balance of ETH or token using Web3
        if self.isToken:
            return self.token.functions.balanceOf(self.wallet_address).call() / 10 ** self.asset_decimals
        return self.web3.eth.getBalance(self.wallet_address) / 10 ** self.asset_decimals

    def get_transactions(self):
        if self.isToken:
            return  requests.get("https://api.etherscan.io/api?module=account&action=tokentx&address={}&startblock=0&endblock=999999999&sort=asc&apikey={}".format(self.wallet_address, self.transactionAPI)).json()
        return requests.get("https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&sort=asc&apikey={}".format(self.wallet_address, self.transactionAPI)).json()
