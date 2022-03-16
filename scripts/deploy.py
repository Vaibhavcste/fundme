from brownie import fundme,accounts,network,config,MockV3Aggregator
from scripts.helpful_scripts import get_account,deploy_mocks,LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fundme():
    print(f"current network is {network.show_active()}")
    account=get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price"]
    else:
       deploy_mocks()
       price_feed_address = MockV3Aggregator[-1].address
    fund_me=fundme.deploy(price_feed_address, # <--- before there was "0x8A..ect"
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    print(f"deployed at {fund_me.address}")

def main():
    deploy_fundme()