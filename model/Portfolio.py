from controller.RecordKeeper import RecordKeeper
from model.Wallet import Wallet
import pandas as pd

class Portfolio():

    def __init__(self, _wallets, _positions_filename):
        self.recordKeeper = RecordKeeper(_positions_filename)
        self.wallets = _wallets
        self.positions = self.recordKeeper.get_latest_positions()

    def add_wallet(self, _wallet):
        self.wallets = self.wallets.append(_wallet)
        return True

    def remove_wallet(self, _wallet):
        self.wallets.remove(_wallet)
        return True

    def get_positions(self):
        return self.positions

    def update_positions(self):
        self.positions = self.recordKeeper.get_latest_positions()
        self.recordKeeper.update_positions(self)

    def get_wallets(self):
        return self.wallets