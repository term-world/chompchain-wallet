import os
import json
import requests
import pickle
import getpass
import shutil
import hashlib

import falconsign as falcon

from .address import Address
from pymerkle import InmemoryTree as MerkleTree
from marketplace import Package
from couchsurf import Connection
from datetime import datetime

class Wallet:

    def __init__(self, wallet_dir: str = "~/.wallet"):
        self.keys = {
            ".cc.priv": None,
            ".cc.pub": None
        }
        self.wallet_dir = os.path.expanduser(wallet_dir)
        if not os.path.isdir(self.wallet_dir):
            os.mkdir(self.wallet_dir)
            self.__generate_keys()
            self.__set_permissions()
        self.__load_keys()
        self.keys[".cc.pub"] = self.__make_key_tree()
        self.address = Address(self.keys[".cc.pub"])

    def __generate_keys(self) -> None:
        self.keys[".cc.priv"] = falcon.SecretKey(256)
        self.keys[".cc.pub"] = falcon.PublicKey(self.keys[".cc.priv"])
        for key in self.keys:
            with open(f"{self.wallet_dir}/{key}", "wb") as fh:
                pickle.dump(self.keys[key], fh)

    def __set_permissions(self) -> None:
        os.system(f"chmod 700 {self.wallet_dir}")
        for key in self.keys:
            os.system(f"chmod 600 {self.wallet_dir}/{key}")

    def __load_keys(self) -> dict:
        for key in self.keys:
            try:
                with open(f"{self.wallet_dir}/{key}", "rb") as fh:
                    self.keys[key] = pickle.load(fh)
            except FileNotFoundError:
                # FileNotFoundError handles public-key-only contracts
                continue

    def __make_key_tree(self) -> MerkleTree:
        """ Make full tree from key """
        tree = MerkleTree()
        for value in self.keys[".cc.pub"].h:
            tree.append(bytes(str(value), encoding = 'utf-8'))
        return tree

    def __request_receiver_node(self) -> dict:
        response = requests.get(
            "https://dir.chain.chompe.rs/directory/get" # "boot" node
        )
        node = random.choice(json.loads(response.text))

    def transact(self, to_addr: str = "", data: dict = {}) -> None:
        transaction = Transaction(to_addr = to_addr, **data)
        node_addr = self.__request_receiver_node()
        response = requests.post(
            f"{node_addr['host']}:{node_addr['port']}/transactions/new",
            data = json.dumps(transaction)
        )

    def sign(self, transaction: str = ""):
        """ Signs transaction with private key? """
        return self.keys[".cc.priv"].sign(
            transaction.encode("utf-8")
        ).hex()

class SmartContract(Package):

    def __init__(self, name: str = "", files: any = ""):
        super().__init__(name = name, files = files)
        self.conn = Connection("contracts")

    def __send_to_network(self):
        self.conn.request.put(
            doc_id = self.address,
            doc = {"creator": f"{Wallet().address}"},
            attachment = f"{self.name}.pyz"
        )

    def make(self, options: dict = {}) -> None:
        if not os.path.isdir(self.name):
            for file in self.files:
                self.folder(file)
        wallet_dir  = f"{os.getcwd()}/{self.name}/.wallet"
        self.wallet = Wallet(wallet_dir = wallet_dir)
        self.address = str(self.wallet.address)
        # Copy address into package for later reference
        with open(f"{os.getcwd()}/{self.name}/address.py", "w") as fh:
            fh.write(f"ADDRESS = '{self.address}'")
        # Copy the contract API/decorators into the contract
        shutil.copy(
            f"{os.path.dirname(os.path.abspath(__file__))}/contract.py",
            f"{os.getcwd()}/{self.name}/contract.py"
        )
        # Bounce the private key; it's useless
        shutil.rmtree(f"{os.getcwd()}/{self.name}/.wallet")
        super().make(options = options)
        self.__send_to_network()

class Transaction:

    def __init__(self, wallet: Wallet = Wallet(), to_addr: str = "", **kwargs):
        """ Constructor """

        self.data = kwargs
        setattr(self, "to_addr", to_addr)

        if "from_addr" in kwargs:
            setattr(self, "from_addr", str(kwargs["from_addr"]))
        else:
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
