from brownie import fundme
from scripts.helpful_scripts import get_account


def fund():
    print("funding...")
    fund_me = fundme[-1]
    account = get_account()
    print(f"fetched account {fund_me}")
    entrance_fee = fund_me.getEntranceFee()
    #entrance_fee=25000000000000000
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.pay({"from": account, "value": entrance_fee+200000, 'gas_limit': 6721975, "allow_revert":True})


def withdraw():
    print("withdrawing...")
    fund_me = fundme[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
