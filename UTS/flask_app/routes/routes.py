from flask import Blueprint, render_template, request, redirect, url_for
from ecommerce.application.use_cases import (
    ProdukUseCase,
    KategoriUseCase,
    LokasiUseCase,
    KeranjangUseCase
)
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint("main", __name__)

produk_uc = ProdukUseCase()
kategori_uc = KategoriUseCase()
lokasi_uc = LokasiUseCase()
keranjang_uc = KeranjangUseCase()

UPLOAD_FOLDER = "flask_app/static/uploads"


# =========================
# HOME / LIST PRODUK
# =========================
@main_bp.route("/")
def home():
    kategori = request.args.get("kategori")
    lokasi = request.args.get("lokasi")
    min_harga = request.args.get("min_harga")
    max_harga = request.args.get("max_harga")
    q = request.args.get("q")

    produk_list = produk_uc.list_produk(
        kategori_id=kategori,
        lokasi_id=lokasi,
        min_harga=min_harga,
        max_harga=max_harga,
        q=q
    )

    return render_template(
        "pages/home.html",
        produk_list=produk_list,
        kategori_list=kategori_uc.list_kategori(),
        lokasi_list=lokasi_uc.list_lokasi()
    )



# =========================
# FORM TAMBAH PRODUK
# =========================
@main_bp.route("/produk/tambah")
def form_tambah_produk():
    return render_template("pages/tambah_produk.html")


# =========================
# SIMPAN PRODUK
# =========================
@main_bp.route("/produk/simpan", methods=["POST"])
def simpan_produk():
    nama = request.form["nama"]
    kategori = request.form["kategori"]
    lokasi = request.form["lokasi"]
    harga = float(request.form["harga"])
    keterangan = request.form["keterangan"]

    file = request.files["gambar"]
    filename = secure_filename(file.filename)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    produk_uc.tambah_produk(
        nama=nama,
        kategori_nama=kategori,
        lokasi_nama=lokasi,
        harga=harga,
        keterangan=keterangan,
        gambar=f"uploads/{filename}"
    )

    return redirect(url_for("main.home"))


# =========================
# DETAIL PRODUK
# =========================
@main_bp.route("/produk/<int:produk_id>")
def detail_produk(produk_id):
    produk_list = produk_uc.list_produk()
    produk = next((p for p in produk_list if p.id == produk_id), None)

    return render_template(
        "pages/detail_produk.html",
        produk=produk
    )


# =========================
# TAMBAH KE KERANJANG
# =========================
@main_bp.route("/keranjang/tambah/<int:produk_id>", methods=["POST"])
def tambah_ke_keranjang(produk_id):
    jumlah = int(request.form.get("jumlah", 1))
    keranjang_uc.tambah_ke_keranjang(produk_id, jumlah)
    return redirect(url_for("main.view_keranjang"))


# =========================
# LIHAT KERANJANG
# =========================
@main_bp.route("/keranjang")
def view_keranjang():
    keranjang_list = keranjang_uc.list_keranjang()
    total = keranjang_uc.total_keranjang()

    return render_template(
        "pages/keranjang.html",
        keranjang_list=keranjang_list,
        total=total
    )


# =========================
# HAPUS ITEM KERANJANG
# =========================
@main_bp.route("/keranjang/hapus/<int:keranjang_id>")
def hapus_dari_keranjang(keranjang_id):
    keranjang_uc.hapus_dari_keranjang(keranjang_id)
    return redirect(url_for("main.view_keranjang"))


# =========================
# KOSONGKAN KERANJANG
# =========================
@main_bp.route("/keranjang/kosongkan")
def kosongkan_keranjang():
    keranjang_uc.kosongkan_keranjang()
    return redirect(url_for("main.view_keranjang"))

@main_bp.route("/produk/<int:produk_id>/update", methods=["POST"])
def update_produk(produk_id):
    data = request.form
    file = request.files.get("gambar")
    produk_uc.update_produk(produk_id, data, file)
    return redirect(url_for("main.home"))

@main_bp.route("/produk/<int:produk_id>/hapus")
def hapus_produk(produk_id):
    produk_uc.hapus_produk(produk_id)
    return redirect(url_for("main.home"))
