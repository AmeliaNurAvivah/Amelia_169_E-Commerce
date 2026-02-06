from abc import ABC, abstractmethod
from domain.entities.entities import Produk, KeranjangItem

class ProdukRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Produk]:
        pass

    @abstractmethod
    def get_by_id(self, produk_id: int) -> Produk:
        pass


class KeranjangRepository(ABC):

    @abstractmethod
    def add_item(self, produk_id: int, jumlah: int):
        pass

    @abstractmethod
    def get_items(self) -> list[KeranjangItem]:
        pass

    @abstractmethod
    def delete_item(self, item_id: int):
        pass

    @abstractmethod
    def clear(self):
        pass
