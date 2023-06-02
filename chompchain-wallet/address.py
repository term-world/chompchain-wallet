from Crypto.Hash import keccak
from Crypto.PublicKey.ECC import EccKey

class Address:

    def __init__(self,  public_key: EccKey, network: str = "100x"):
        """ Constructor """
        self.prefix = network
        self.value = public_key

    def __derive_address(self, public_key) -> str:
        pub_key = public_key.export_key(format = 'raw')
        addr_hash = keccak.new(digest_bits=256)
        addr_hash.update(pub_key)
        return addr_hash.hexdigest()[-40:]

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