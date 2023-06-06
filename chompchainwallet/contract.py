import os
from couchsurf import Connection
from address import *

CONN = Connection("contracts")
data = CONN.request.query(
    _id = {"op": "EQUALS", "arg": ADDRESS}
)

def owner(self, addr: str = ""):
    pass

def payable(self):
    pass
