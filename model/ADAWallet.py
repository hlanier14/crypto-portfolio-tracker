from model.Wallet import Wallet
import requests

class ADAWallet(Wallet):

    def __init__(self, _scannerAPI, _priceAPI, _wallet_address, _asset_symbol, _asset_decimals):

        self.scannerAPI = _scannerAPI
        self.priceAPI = _priceAPI

        self.asset_symbol = _asset_symbol
        self.asset_decimals = _asset_decimals

        self.wallet_address = _wallet_address
        stake_address = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/addresses/{}".format(_wallet_address), 
                                     headers={"project_id":_scannerAPI}).json()
        self.stake_address = stake_address["stake_address"]

    def get_balance(self):
        # Return asset balance using BlockFrost
        balance = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/addresses/{}".format(self.wallet_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(balance["amount"][0]["quantity"]) / 10 ** self.asset_decimals

    def get_transactions(self):
        hashes = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/addresses/{}/transactions".format(self.wallet_address), 
                              headers={"project_id":self.scannerAPI}).json()
        txns = []
        for hash in hashes:
            # could be many requests
            # check hashes against transactions.csv, only pull hashes not in csv
            txn = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/txs/{}".format(hash["tx_hash"]), 
                               headers={"project_id":self.scannerAPI}).json()
            txns.append(txn)
        return txns

    def get_staked_assets(self):
        # Return staked asset balance using BlockFrost
        staked = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/accounts/{}".format(self.stake_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(staked["controlled_amount"]) / 10 ** self.asset_decimals

    def get_stake_rewards(self):
        # Return staked asset rewards using BlockFrost
        staked = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/accounts/{}".format(self.stake_address), 
                               headers={"project_id":self.scannerAPI}).json()
        return int(staked["rewards_sum"]) / 10 ** self.asset_decimals
