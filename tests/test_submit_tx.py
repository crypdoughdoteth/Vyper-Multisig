#!/usr/bin/python3

import pytest
from brownie.convert import to_bytes
from brownie import reverts


def test_tx_count_incremented(multisig, accounts):
    init_tx_num = multisig.getTransactionCount()
    _to = accounts[2]
    val = 10**19
    _bytes = b"\x01"
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    assert multisig.getTransactionCount() > init_tx_num


def test_only_submitted(multisig, accounts):
    _to = accounts[2]
    val = 10**19
    _bytes = to_bytes("0x01")
    multisig.submitTransaction(_to, val, _bytes, {"from": accounts[0]})
    _tx = multisig.getTransaction(0)
    assert _tx[0] == _to, "Destination address not matching"
    assert _tx[1] == val, "Value not matching"
    # not sure if below is actually the desired behavior.
    # The _tx[2] object is of type <class 'brownie.convert.datatypes.HexString'>
    # which is different than the bytes type passed
    # but maybe it's how the EVM works under the hood
    assert to_bytes(_tx[2]) == _bytes, "Tx data not matching"
    assert _tx[3] == False, "Tx shouldn't have been executed"
    assert _tx[4] == 0, "Tx should not have been signed"
