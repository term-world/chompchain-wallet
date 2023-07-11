from pymerkle import InmemoryTree as MerkleTree

class Address:

    def __init__(self, public_key: MerkleTree, network: str = "100x"):
        """ Constructor """
        self.prefix = network
        self.value = str(public_key.root.value)

    def __repr__(self) -> str:
        """ Representation """
        return f"{self.prefix}{self.value}"

    def __str__(self) -> str:
        """ String representation """
        return f"{self.prefix}{self.value}"
