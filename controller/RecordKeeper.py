import pandas as pd
from datetime import datetime

class RecordKeeper():

    def __init__(self, _positions_filename):
        self.positions_filename = _positions_filename

    def _get_positions(self, _portfolio):
        # Record value of positions to positions.csv
        wallets = _portfolio.get_wallets()
        today = datetime.now()
        dates = [today for x in wallets]
        assets = []
        balances = []
        prices = []
        for wallet in wallets:
            assets.append(wallet.get_asset_symbol())
            balances.append(wallet.get_balance())
            prices.append(wallet.get_asset_price())
    
        df = pd.DataFrame(list(zip(dates, assets, balances, prices)),
                          columns=["Date", "Asset", "Balance", "Price"])
        df["Value"] = df["Balance"] * df["Price"]
        return df

    def update_positions(self, _portfolio):
        positions_df = self._get_positions(_portfolio)
        df = pd.read_csv(self.positions_filename)
        if df is None:
            positions_df.to_csv(self.positions_filename, index=False)
        else:
            concat = pd.concat([df, positions_df])
            concat.to_csv(self.positions_filename, index=False)
        return True

    def get_latest_positions(self):
        df = pd.read_csv(self.positions_filename)
        return df[df["Date"] == max(df["Date"])]

    def update_transactions(self):
        # Add any new transactions to transactions.csv
        pass

    def get_positions_filename(self):
        return self.positions_filename