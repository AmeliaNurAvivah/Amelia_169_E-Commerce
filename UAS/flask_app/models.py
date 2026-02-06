from pydantic import BaseModel, Field
from typing import Optional, Any

class Produk(BaseModel):
    nama: str
    deskripsi: str
    harga: int
    kode_barang: str
    id: str = Field(default=None)
    
