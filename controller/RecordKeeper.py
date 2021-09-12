import pandas as pd
from datetime import datetime

class RecordKeeper():

    def __init__(self, _positions_filename):
        self.positions_filename = _positions_filename

    def get_latest_positions(self):
        df = pd.read_csv(self.positions_filename)
        return df[df["Date"] == max(df["Date"])]

    def update_positions(self, _portfolio):
        # Record value of positions to positions.csv
        wallets = _portfolio.get_wallets()
        today = datetime.now()
        positions_df = pd.DataFrame(list(zip([today for x in wallets], 
                                             [wallet.get_asset_symbol() for wallet in wallets],
                                             [wallet.get_balance() for wallet in wallets], 
                                             [wallet.get_asset_price() for wallet in wallets])),
                                    columns=["Date", "Asset", "Balance", "Price"])
        positions_df["Value"] = positions_df["Balance"] * positions_df["Price"]

        df = pd.read_csv(self.positions_filename)
        if df is None:
            positions_df.to_csv(self.positions_filename, index=False)
        else:
            concat = pd.concat([df, positions_df])
            concat.to_csv(self.positions_filename, index=False)

        return True

    def update_transactions(self):
        # Add any new transactions to transactions.csv
        pass

    def get_positions_filename(self):
        return self.positions_filename
