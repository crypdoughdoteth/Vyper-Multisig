#!/usr/bin/python3

from brownie import Multisig, accounts, network

N = 2


def main():
    return Multisig.deploy(N, [accounts[0], accounts[1]], {"from": accounts[0]})
