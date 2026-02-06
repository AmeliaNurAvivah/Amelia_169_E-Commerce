from flask import Blueprint, render_template, request, redirect, url_for
from ecommerce.application.use_cases import (
    ProdukUseCase,
    KategoriUseCase,
    LokasiUseCase,
    KeranjangUseCase,
    PesananUseCase
)
import os
from werkzeug.utils import secure_filename
from ecommerce.infrastructure.sqlite_db.repositories.pesanan_repository import SQLitePesananRepository





# =========================
# INIT
# =========================
main_bp = Blueprint("main", __name__)

produk_uc = ProdukUseCase()
kategori_uc = KategoriUseCase()
lokasi_uc = LokasiUseCase()
keranjang_uc = KeranjangUseCase()
pesanan_uc = PesananUseCase(keranjang_uc)

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

    return render_template("pages/detail_produk.html", produk=produk)


# =========================
# KERANJANG
# =========================
@main_bp.route("/keranjang/tambah/<int:produk_id>", methods=["POST"])
def tambah_ke_keranjang(produk_id):
    jumlah = int(request.form.get("jumlah", 1))
    keranjang_uc.tambah_ke_keranjang(produk_id, jumlah)
    return redirect(url_for("main.view_keranjang"))


@main_bp.route("/keranjang")
def view_keranjang():
    keranjang_list = keranjang_uc.list_keranjang()
    total = keranjang_uc.total_keranjang()
    return render_template("pages/keranjang.html", keranjang_list=keranjang_list, total=total)


@main_bp.route("/keranjang/hapus/<int:keranjang_id>")
def hapus_dari_keranjang(keranjang_id):
    keranjang_uc.hapus_dari_keranjang(keranjang_id)
    return redirect(url_for("main.view_keranjang"))


@main_bp.route("/keranjang/kosongkan")
def kosongkan_keranjang():
    keranjang_uc.kosongkan_keranjang()
    return redirect(url_for("main.view_keranjang"))


@main_bp.route("/keranjang/update/<int:keranjang_id>", methods=["POST"])
def update_jumlah_keranjang(keranjang_id):
    aksi = request.form.get("aksi")
    if aksi == "tambah":
        keranjang_uc.tambah_jumlah(keranjang_id)
    elif aksi == "kurang":
        keranjang_uc.kurangi_jumlah(keranjang_id)
    return redirect(url_for("main.view_keranjang"))


# =========================
# CHECKOUT & PESANAN
# =========================
@main_bp.route("/checkout")
def checkout():
    keranjang_list = keranjang_uc.list_keranjang()
    total = keranjang_uc.total_keranjang()

    if not keranjang_list:
        return redirect(url_for("main.view_keranjang"))

    return render_template("pages/checkout.html", keranjang_list=keranjang_list, total=total)


@main_bp.route("/buat-pesanan", methods=["POST"])
def buat_pesanan():
    metode = request.form.get("metode", "COD")
    pesanan_uc.buat_pesanan(metode)
    return redirect(url_for("main.riwayat_pesanan"))


@main_bp.route("/riwayat-pesanan")
def riwayat_pesanan():
    data = pesanan_uc.list_pesanan()
    return render_template("pages/riwayat_pesanan.html", pesanan_list=data)


@main_bp.route("/riwayat-pesanan/<int:pesanan_id>")
def detail_pesanan(pesanan_id):
    items = pesanan_uc.detail_pesanan(pesanan_id)
    return render_template("pages/detail_pesanan.html", items=items)


@main_bp.route("/pesanan/<int:pesanan_id>/hapus", methods=["POST"])
def hapus_pesanan(pesanan_id):
    repo = SQLitePesananRepository()
    repo.hapus_pesanan(pesanan_id)
    return redirect(url_for("main.riwayat_pesanan"))


@main_bp.route("/riwayat-pesanan/<int:pesanan_id>/selesai")
def selesai_pesanan(pesanan_id):
    repo = SQLitePesananRepository()
    repo.ubah_status(pesanan_id, "Selesai")
    return redirect(url_for("main.riwayat_pesanan"))

@main_bp.route("/riwayat-pesanan/<int:pesanan_id>/status/<status>")
def ubah_status_pesanan(pesanan_id, status):
    repo = SQLitePesananRepository()
    repo.ubah_status(pesanan_id, status)
    return redirect(url_for("main.riwayat_pesanan"))
