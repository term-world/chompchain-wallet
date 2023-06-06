import json
import hashlib
from datetime import datetime
from .interface import Wallet

class Transaction:

    def __init__(self, to_addr: str = "", from_addr = "",  **kwargs):
        """ Constructor """

        wallet = Wallet()

        self.data = kwargs
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
