from brownie import network,config,accounts,MockV3Aggregator
from web3 import Web3
DECIMALS=8
STARTING_VAL=200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development", "ganache-local"]
#https://youtu.be/M576WGiDBdQ?t=20789
def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print("Testnet Enabled")
    if len(MockV3Aggregator)<=0:
        print("deploying mocks")
        mock_aggregator=MockV3Aggregator.deploy(DECIMALS,STARTING_VAL,{"from":get_account()})
        print(f"mocks deployed {mock_aggregator}") 
    