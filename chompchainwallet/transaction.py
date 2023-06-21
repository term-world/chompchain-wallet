import os
import json
import hashlib
import requests
from datetime import datetime
from .interface import Wallet

class Transaction:

    def __init__(self, to_addr: str = "", from_addr = "",  **kwargs):
        """ Constructor """

        wallet = Wallet()

        self.data = kwargs

        for field in self.data:
            self.data[field] = self.data[field].encode().decode()

        setattr(self, "to_addr", to_addr)

        if not from_addr:
            setattr(self, "from_addr", str(wallet.address))

        hash = hashlib.new('sha256')
        hash.update(self.__str__().encode())
        setattr(self, "hash", hash.hexdigest())

        time = datetime.now().timestamp()
        setattr(self, "timestamp", time)

        setattr(self,"signature",wallet.sign(str(self)))

    def to_dict(self) -> dict:
        """ Returns dictionary repr of object properties """
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__, separators = (',', ':'))

class CmdTransaction():

    def __init__(self, command: str = ""):
        transact = Transaction(
            to_addr = "0x0",
            cmd = command
        )
        transmit(transact)

def transmit(txn: Transaction = Transaction()):
    response = requests.post(
        "http://cdr.theterm.world:7500/transactions/new",
        data = json.dumps(txn.__dict__)
    )
    # TODO: Create a cache to save transactions in case
    # we lose all connectivity with any node?
