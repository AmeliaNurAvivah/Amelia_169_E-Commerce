from dataclasses import dataclass

@dataclass
class Produk:
    id: int
    nama: str
    harga: float


@dataclass
class KeranjangItem:
    id: int | None
    produk_id: int
    nama_produk: str
    harga: float
    jumlah: int

    @property
    def subtotal(self) -> float:
        return self.harga * self.jumlah
