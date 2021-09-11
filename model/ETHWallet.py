from model.Wallet import Wallet
from web3 import Web3
import requests

class ETHWallet(Wallet):

    ETH_address = "0x0000000000000000000000000000000000000000"

    def __init__(self, _infuraAPI, _priceAPI, _wallet_address, _asset_symbol, _asset_decimals, _asset_contract_address, _asset_contract_abi=None):
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{}'.format(_infuraAPI)))
        self.priceAPI = _priceAPI
        self.isToken = False
        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals
        self.wallet_address = _wallet_address
        # if the asset is not ETH, instantiate ETH token with contract address and abi
        if _asset_contract_address != self.ETH_address:
            self.token = self.web3.eth.contract(address=_asset_contract_address, abi=_asset_contract_abi)
            self.isToken = True
    
    def get_balance(self):
        # Return balance of ETH or token using Web3
        if self.isToken:
            return self.token.functions.balanceOf(self.wallet_address).call() / 10**self.asset_decimals
        return self.web3.eth.getBalance(self.wallet_address) / 10**self.asset_decimals

    def get_asset_price(self):
        # Return asset price from CoinMarketCap
        price = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", 
                             headers={'X-CMC_PRO_API_KEY': self.priceAPI}, 
                             params={"symbol":self.asset_symbol}).json()
        return float(price["data"][self.asset_symbol]["quote"]["USD"]["price"])

    def get_wallet_value(self):
        return self.get_asset_price() * self.get_balance()

    def get_asset_symbol(self):
        return self.asset_symbol
