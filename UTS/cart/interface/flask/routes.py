from flask import Blueprint, render_template, request, redirect, url_for

from application.use_cases import (
    TampilkanProdukUseCase,
    TambahKeranjangUseCase,
    LihatKeranjangUseCase,
    HapusItemKeranjangUseCase
)

from infrastructure.services.repositories_impl import (
    ProdukRepositoryImpl,
    KeranjangRepositoryImpl
)

web = Blueprint("web", __name__)

produk_repo = ProdukRepositoryImpl()
keranjang_repo = KeranjangRepositoryImpl()


@web.route("/")
def daftar_produk():
    uc = TampilkanProdukUseCase(produk_repo)
    produk = uc.execute()
    return render_template("pages/daftar_produk.html", produk=produk)


@web.route("/tambah", methods=["POST"])
def tambah():
    produk_id = int(request.form["produk_id"])
    jumlah = int(request.form["jumlah"])

    uc = TambahKeranjangUseCase(keranjang_repo)
    uc.execute(produk_id, jumlah)

    return redirect(url_for("web.keranjang"))


@web.route("/keranjang")
def keranjang():
    uc = LihatKeranjangUseCase(keranjang_repo)
    data = uc.execute()
    return render_template("pages/keranjang.html", **data)


@web.route("/hapus/<int:item_id>")
def hapus(item_id):
    uc = HapusItemKeranjangUseCase(keranjang_repo)
    uc.execute(item_id)
    return redirect(url_for("web.keranjang"))

@web.route("/debug-produk")
def debug_produk():
    from infrastructure.services.repositories_impl import ProdukRepositoryImpl
    repo = ProdukRepositoryImpl()
    data = repo.get_all()
    return str(data)
