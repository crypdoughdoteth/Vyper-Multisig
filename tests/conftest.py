#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def multisig(Multisig, accounts):
    N = 2
    owners = [accounts[0], accounts[1]]
    return Multisig.deploy(N, owners, {"from": accounts[0]})
