from model.Wallet import Wallet
from substrateinterface.base import SubstrateInterface
import requests

class DOTWallet(Wallet):

    def __init__(self, _priceAPI, _wallet_address, _asset_symbol, _asset_decimals):

        self.substrate = SubstrateInterface(url="wss://rpc.polkadot.io")
        self.priceAPI = _priceAPI
        
        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals

        self.wallet_address = _wallet_address

    def get_balance(self):
        # Return asset balance using Substrate Interface
        balance = self.substrate.query(module='System', 
                                       storage_function='Account', 
                                       params=[self.wallet_address])
        return int(balance.value["data"]["free"]) / 10 ** self.asset_decimals

    def get_transactions(self):
        # WIP
        balance = self.substrate.query(module='System', 
                                       storage_function='Account', 
                                       params=[self.wallet_address])
        return balance
