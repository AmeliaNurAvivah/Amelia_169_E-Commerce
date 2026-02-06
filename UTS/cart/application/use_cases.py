from domain.repositories.repositories import (
    ProdukRepository,
    KeranjangRepository
)


class TampilkanProdukUseCase:
    def __init__(self, produk_repo: ProdukRepository):
        self.produk_repo = produk_repo

    def execute(self):
        return self.produk_repo.get_all()


class TambahKeranjangUseCase:
    def __init__(self, keranjang_repo: KeranjangRepository):
        self.keranjang_repo = keranjang_repo

    def execute(self, produk_id: int, jumlah: int):
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0")

        self.keranjang_repo.add_item(produk_id, jumlah)


class LihatKeranjangUseCase:
    def __init__(self, keranjang_repo: KeranjangRepository):
        self.keranjang_repo = keranjang_repo

    def execute(self):
        items = self.keranjang_repo.get_items()
        total = sum(item.subtotal for item in items)

        return {
            "items": items,
            "total": total
        }


class HapusItemKeranjangUseCase:
    def __init__(self, keranjang_repo: KeranjangRepository):
        self.keranjang_repo = keranjang_repo

    def execute(self, item_id: int):
        self.keranjang_repo.delete_item(item_id)
