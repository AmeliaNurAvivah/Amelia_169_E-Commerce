from pydantic import BaseModel

class FilterProdukDTO(BaseModel):
    nama: str | None = None
    harga_min: int | None | str = None
    harga_max: int | None | str = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True