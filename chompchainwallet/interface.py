import os
import json
import requests
import pickle
import falcon
import getpass

from .address import Address
from pymerkle import MerkleTree

class Wallet:

    def __init__(self):
        self.keys = {
            ".cc.priv": None,
            ".cc.pub": None
        }
        self.wallet_dir = os.path.expanduser("~/.wallet")
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
            with open(f"{self.wallet_dir}/{key}", "rb") as fh:
                self.keys[key] = pickle.load(fh)

    """
    TEMPORARILY DEPRECATING; ADDRESSES MIGHT OBSOLETE ORIGINAL APPROACH
    def __broadcast_keys(self) -> bool:
        url = "https://dir.chain.chompe.rs/keys"  # the actual URL to send the keys
        payload = {
            "user": "username",  # Replace with the actual username
            "key": {
                "public_key": str(self.keys[".cc.pub"])
            }
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return True
            raise
        except requests.exceptions.RequestException as e:
            return False
    """

    def __make_key_tree(self) -> MerkleTree:
        """ Make full tree from key """
        tree = MerkleTree()
        for value in self.keys[".cc.pub"].h:
            tree.append_entry(str(value))
        return tree

    def sign(self, transaction: str = ""):
        """ Signs transaction with private key? """
        return self.keys[".cc.priv"].sign(
            transaction.encode("utf-8")
        ).hex()
