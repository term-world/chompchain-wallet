from pymerkle import MerkleTree

class Address:

    def __init__(self, public_key: MerkleTree, network: str = "100x"):
        """ Constructor """
        self.prefix = network
        self.value = public_key.root.decode()

    def __repr__(self) -> str:
        """ Representation """
        return f"{self.prefix}{self.value}"

    def __str__(self) -> str:
        """ String representation """
        return f"{self.prefix}{self.value}"
