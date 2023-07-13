#!/usr/bin/python3

import pytest
from brownie.convert import to_bytes


def test_multisig_sends(multisig, accounts):
    alice = accounts[0]
    bob = accounts[1]
    eve = accounts[2]
    # fund the multisig
    init_alice_balance = alice.balance()
    init_eve_balance = eve.balance()
    init_multisig_balance = multisig.balance()
    amount_to_fund = 10**20
    alice.transfer(to=multisig, amount=amount_to_fund)
    mid_alice_balance = alice.balance()
    assert (
        mid_alice_balance < init_alice_balance
    ), "Multisig funder's balance should decrease"
    mid_multisig_balance = multisig.balance()
    assert (
        mid_multisig_balance > init_multisig_balance
    ), "Multisig's balance should increase after the funding tx"
    _to = eve
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": alice})
    assert (
        mid_alice_balance - alice.balance() < val
    ), "Submitting transaction costs Alice paymentAmount"
    # confirm the tx
    multisig.confirmTransaction(0, {"from": alice})
    multisig.confirmTransaction(0, {"from": bob})
    final_alice_balance = alice.balance()
    # we know the above works from other tests so skipping the asserts here
    response = multisig.executeTransaction(0)
    _tx = multisig.getTransaction(0)
    assert _tx[3] == True, "Tx should have been executed"
    assert (
        alice.balance() == final_alice_balance
    ), "Owner balance decreases after multisig tx execution"
    assert (
        init_eve_balance < eve.balance()
    ), "Destination address should have more balance after tx execution"
    assert mid_multisig_balance > multisig.balance(), "Multisig balance should decrease"
