#!/usr/bin/python3

import pytest
from brownie.convert import to_bytes
from brownie import reverts


def test_owner_can_sign(multisig, accounts):
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    _tx = multisig.getTransaction(0)
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 1, "Tx should have been signed by 1 owner"
    multisig.confirmTransaction(0, {"from": accounts[1]})
    _tx = multisig.getTransaction(0)
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 2, "Tx should have been signed by 2 owners"


def test_non_owner_cant_sign(multisig, accounts):
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # try signing by non-owner
    with reverts():
        multisig.confirmTransaction(0, {"from": accounts[3]})


def test_owner_can_revoke(multisig, accounts):
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    _tx = multisig.getTransaction(0)
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 1, "Tx should have been signed by 1 owner"
    multisig.revokeConfirmation(0, {"from": accounts[0]})
    _tx = multisig.getTransaction(0)
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 0, "Tx confirmation should have been revoked"


def test_non_owner_cant_revoke(multisig, accounts):
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    # confirm the tx
    multisig.confirmTransaction(0, {"from": accounts[0]})
    _tx = multisig.getTransaction(0)
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 1, "Tx should have been signed by 1 owner"
    with reverts():
        multisig.revokeConfirmation(0, {"from": accounts[3]})
