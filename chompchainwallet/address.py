import pymerkle
from Crypto.Hash import keccak

class Address:

    def __init__(self, public_key: list = [], network: str = "100x"):
        """ Constructor """
        self.prefix = network
        self.key_values = public_key

    def __derive_address(self) -> str:
        tree = pymerkle.MerkleTree()
        for val in key_values:
            tree.append_entry(str(val))
        return tree.root

    @property
    def value(self):
        """ Getter for address value """
        return f"{self.prefix}{self._value}"

    @value.setter
    def value(self, pub_key: EccKey):
        """ Setter for address value """
        self._value = self.__derive_address(pub_key)

    def __str__(self) -> str:
        """ String representation """
        return f"{self.prefix}{self._value}"
