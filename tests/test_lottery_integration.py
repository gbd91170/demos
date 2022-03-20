from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery, get_account
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    fund_with_link,
)
from web3 import Web3
import pytest
import time


def test_get_entrance_fee():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee_max = Web3.toWei(0.020, "ether")
    expected_entrance_fee_min = Web3.toWei(0.015, "ether")

    entrance_fee = lottery.getEntranceFee()
    # Test
    assert expected_entrance_fee_max > entrance_fee
    assert expected_entrance_fee_min < entrance_fee


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
