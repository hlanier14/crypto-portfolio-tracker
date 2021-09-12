from controller.RecordKeeper import RecordKeeper
from model.ETHWallet import ETHWallet
from model.ADAWallet import ADAWallet
from model.DOTWallet import DOTWallet
from model.Portfolio import Portfolio
import json

def main():

    # Load credentials from json file
    c = open('data\credentials.json',)
    cred = json.load(c)
    ETH_contract_address = cred["Contract"]["ETH"]
    LINK_contract_address = cred["Contract"]["LINK"]
    LINK_contract_abi = cred["ABI"]["Chainlink"]
    BlockFrostAPI = cred["API"]["BlockFrost"]
    CoinMarketCapAPI = cred["API"]["CoinMarketCap"]
    EtherscanAPI = cred["API"]["Etherscan"]
    InfuraAPI = cred["API"]["Infura"]
    ETH_wallet_address = cred["Wallet"]["ETH"]
    ADA_wallet_address = cred["Wallet"]["ADA"]
    DOT_wallet_address = cred["Wallet"]["DOT"]
    c.close()

    # Create wallet objects
    ETH_wallet = ETHWallet(InfuraAPI, CoinMarketCapAPI, EtherscanAPI, ETH_wallet_address, "ETH", 18, ETH_contract_address)
    LINK_wallet = ETHWallet(InfuraAPI, CoinMarketCapAPI, EtherscanAPI, ETH_wallet_address, "LINK", 18, LINK_contract_address, LINK_contract_abi)
    ADA_wallet = ADAWallet(BlockFrostAPI, CoinMarketCapAPI, ADA_wallet_address, "ADA", 6)
    DOT_wallet = DOTWallet(CoinMarketCapAPI, DOT_wallet_address, "DOT", 10)

    portfolio = Portfolio([ETH_wallet, LINK_wallet, ADA_wallet, DOT_wallet], "data\positions.csv")
    #portfolio.update_positions()
    #positions = portfolio.get_positions()

    # Get transactions


if __name__ == "__main__":
    main()
