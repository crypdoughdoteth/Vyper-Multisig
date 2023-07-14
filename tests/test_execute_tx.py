#!/usr/bin/python3

import pytest
from brownie.convert import to_bytes
from brownie import reverts


def test_signed_executes(multisig, accounts):
    # fund the multisig
    amount_to_fund = 10**20
    accounts[4].transfer(to=multisig, amount=amount_to_fund)
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    multisig.confirmTransaction(0, {"from": accounts[1]})
    # we know the above works from other tests so skipping the asserts here
    response = multisig.executeTransaction(0)
    _tx = multisig.getTransaction(0)
    assert _tx[3] == True, "Tx should have been executed"


def test_insufficient_balance(multisig, accounts):
    # fund the multisig
    amount_to_fund = 10**18
    accounts[4].transfer(to=multisig, amount=amount_to_fund)
    _to = accounts[2]
    val = 10**19
    assert multisig.balance() < val
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    multisig.confirmTransaction(0, {"from": accounts[1]})
    # we know the above works from other tests so skipping the asserts here
    with reverts():
        response = multisig.executeTransaction(0)


def test_not_enough_signatures(multisig, accounts):
    # fund the multisig
    amount_to_fund = 10**20
    accounts[4].transfer(to=multisig, amount=amount_to_fund)
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    # we know the above works from other tests so skipping the asserts here
    with reverts():
        response = multisig.executeTransaction(0)


def test_not_enough_signatures_after_revoke(multisig, accounts):
    # fund the multisig
    amount_to_fund = 10**20
    accounts[4].transfer(to=multisig, amount=amount_to_fund)
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    multisig.confirmTransaction(0, {"from": accounts[1]})
    # we know the above works from other tests so skipping the asserts here
    # revoke the confirmation
    multisig.revokeConfirmation(0, {"from": accounts[0]})
    with reverts():
        response = multisig.executeTransaction(0)
