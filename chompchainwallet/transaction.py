import json
import hashlib
from datetime import datetime
from ..wallet.wallet import Wallet

class Transaction:

    def __init__(self, to: str = "", from: str = "", **kwargs):
        """ Constructor """
        self.data = kwargs

        setattr(self, "from", from)

        hash = hashlib.new('sha256')
        hash.update(self.__str__().encode())
        setattr(self, "hash", hash.hexdigest())

        time = datetime.now().timestamp()
        setattr(self, "timestamp", time)

        wallet = Wallet()
        setattr(self,"signature",wallet.sign(str(self)))

    def to_dict(self) -> dict:
        """ Returns dictionary repr of object properties """
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__, separators = (',', ':'))
