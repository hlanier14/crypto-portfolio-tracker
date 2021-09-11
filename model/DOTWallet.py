from model.Wallet import Wallet
from substrateinterface.base import SubstrateInterface
import requests

class DOTWallet(Wallet):

    def __init__(self, _priceAPI, _wallet_address, _asset_symbol, _asset_decimals):
        self.substrate = SubstrateInterface(url="wss://rpc.polkadot.io")
        self.wallet_address = _wallet_address
        self.priceAPI = _priceAPI
        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals

    def get_balance(self):
        # Return asset balance using Substrate Interface
        balance = self.substrate.query(module='System', 
                                       storage_function='Account', 
                                       params=[self.wallet_address])
        return int(balance.value["data"]["free"]) / 10**self.asset_decimals

    def get_asset_price(self):
        # Return asset price using CoinMarketCap
        price = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", 
                             headers={'X-CMC_PRO_API_KEY': self.priceAPI}, 
                             params={"symbol":self.asset_symbol}).json()
        return float(price["data"][self.asset_symbol]["quote"]["USD"]["price"])

    def get_wallet_value(self):
        return self.get_asset_price() * self.get_balance()

    def get_asset_symbol(self):
        return self.asset_symbol