import requests

class Wallet():

    def get_balance(self):
        pass

    def get_asset_price(self):
        # Return asset price using CoinMarketCap
        price = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", 
                             headers={'X-CMC_PRO_API_KEY': self.priceAPI}, 
                             params={"symbol":self.asset_symbol}).json()
        return float(price["data"][self.asset_symbol]["quote"]["USD"]["price"])

    def get_transactions(self):
        pass

    def get_asset_symbol(self):
        return self.asset_symbol
