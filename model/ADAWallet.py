from model.Wallet import Wallet
import requests

class ADAWallet(Wallet):

    def __init__(self, _scannerAPI, _priceAPI, _wallet_address, _asset_symbol, _asset_decimals):
        self.wallet_address = _wallet_address
        self.scannerAPI = _scannerAPI
        self.priceAPI = _priceAPI
        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals
        stake_address = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/addresses/{}".format(_wallet_address), 
                                     headers={"project_id":_scannerAPI}).json()
        self.stake_address = stake_address["stake_address"]

    def get_staked_assets(self):
        # Return staked asset balance using BlockFrost
        staked = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/accounts/{}".format(self.stake_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(staked["controlled_amount"]) / 10**self.asset_decimals

    def get_stake_rewards(self):
        # Return staked asset rewards using BlockFrost
        staked = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/accounts/{}".format(self.stake_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(staked["rewards_sum"]) / 10**self.asset_decimals

    def get_balance(self):
        # Return asset balance using BlockFrost
        balance = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/addresses/{}".format(self.wallet_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(balance["amount"][0]["quantity"]) / 10**self.asset_decimals

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
