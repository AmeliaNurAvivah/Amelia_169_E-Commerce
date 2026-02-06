# flask_app/routes/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from perkuliahan.application.use_cases import DosenUseCase, MatakuliahUseCase, KelasUseCase, MahasiswaUseCase

from flask_app.decorators import login_required


main_bp = Blueprint("main", __name__)

dosen_uc = DosenUseCase()
mk_uc = MatakuliahUseCase()
kelas_uc = KelasUseCase()
mhs_uc = MahasiswaUseCase()


@main_bp.route("/")
@login_required
def dashboard():
    # simple dashboard that links to pages
    dosen = dosen_uc.list_dosen()
    mk = mk_uc.list_matakuliah()
    kelas = kelas_uc.list_kelas()
    return render_template("pages/dashboard.html", dosen=dosen, matakuliah=mk, kelas=kelas)

# --- DOSEN ---
@main_bp.route("/dosen")
def dosen_list():
    data = dosen_uc.list_dosen()
    return render_template("pages/dosen.html", data=data)


@main_bp.route("/dosen/tambah", methods=["POST"])
@login_required
def dosen_tambah():
    try:
        dosen_uc.tambah_dosen(
            request.form.get("nama"),
            request.form.get("ndn")
        )
        flash("Dosen berhasil ditambahkan", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.dosen_list"))



@main_bp.route("/dosen/edit", methods=["POST"])
@login_required
def dosen_edit():
    try:
        dosen_uc.edit_dosen(
            request.form.get("id"),
            request.form.get("nama"),
            request.form.get("ndn")
        )
        flash("Data dosen berhasil diperbarui", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.dosen_list"))


@main_bp.route("/dosen/hapus/<int:id>")
def dosen_hapus(id):
    dosen_uc.hapus_dosen(id)
    return redirect(url_for("main.dosen_list"))

@main_bp.route("/matakuliah")
def matakuliah_list():
    return render_template(
        "pages/matakuliah.html",
        data=mk_uc.list_matakuliah(),
        dosen=dosen_uc.list_dosen()
    )

@main_bp.route("/matakuliah/tambah", methods=["POST"])
def matakuliah_tambah():
    try:
        mk_uc.tambah_matakuliah(
            request.form.get("nama"),
            request.form.get("dosen_id")
        )
        flash("Mata kuliah berhasil ditambahkan", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.matakuliah_list"))

@main_bp.route("/matakuliah/edit", methods=["POST"])
def matakuliah_edit():
    try:
        mk_uc.edit_matakuliah(
            request.form.get("id"),
            request.form.get("nama"),
            request.form.get("dosen_id")
        )
        flash("Mata kuliah berhasil diperbarui", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.matakuliah_list"))

@main_bp.route("/matakuliah/hapus/<int:id>")
def matakuliah_hapus(id):
    mk_uc.hapus_matakuliah(id)
    flash("Mata kuliah berhasil dihapus", "success")
    return redirect(url_for("main.matakuliah_list"))

@main_bp.route("/kelas")
@login_required
def kelas_list():
    data = kelas_uc.list_kelas()
    mk = mk_uc.list_matakuliah()
    dosen = dosen_uc.list_dosen()
    return render_template("pages/kelas.html", data=data, matakuliah=mk, dosen=dosen)

@main_bp.route("/kelas")
def kelas():
    return render_template(
        "kelas.html",
        data=kelas_uc.list_kelas(),
        dosen=dosen_uc.list_dosen(),
        matakuliah=mk_uc.list_matakuliah()
    )


@main_bp.route("/kelas/tambah", methods=["POST"])
def kelas_tambah():
    kelas_uc.tambah_kelas(
        request.form["nama"],
        request.form["matakuliah_id"],
        request.form["dosen_id"]
    )
    return redirect(url_for("main.kelas"))


@main_bp.route("/kelas/edit/<int:kelas_id>", methods=["POST"])
def kelas_edit(kelas_id):
    kelas_uc.update_kelas(
        kelas_id,
        request.form["nama"],
        request.form["matakuliah_id"],
        request.form["dosen_id"]
    )
    return redirect(url_for("main.kelas"))


@main_bp.route("/kelas/hapus/<int:kelas_id>")
def kelas_hapus(kelas_id):
    kelas_uc.delete_kelas(kelas_id)
    return redirect(url_for("main.kelas"))

@main_bp.route("/kelas/<int:kelas_id>")
def kelas_detail(kelas_id):
    kelas = kelas_uc.get_kelas(kelas_id)
    mahasiswa = mhs_uc.list_by_kelas(kelas_id)

    return render_template(
        "pages/kelas_detail.html",
        kelas=kelas,
        mahasiswa=mahasiswa
    )


# --- MAHASISWA ---
@main_bp.route("/mahasiswa/tambah", methods=["POST"])
def mahasiswa_tambah():
    nama = request.form.get("nama")
    nim = request.form.get("nim")
    kelas_id = request.form.get("kelas_id")
    mhs_uc.tambah_mahasiswa(nama, nim, kelas_id)
    return redirect(request.referrer or url_for("main.kelas_list"))

@main_bp.route("/mahasiswa/edit", methods=["POST"])
def mahasiswa_edit():
    id = request.form.get("id")
    nama = request.form.get("nama")
    nim = request.form.get("nim")
    mhs_uc.edit_mahasiswa(id, nama, nim)
    return redirect(request.referrer or url_for("main.kelas_list"))

@main_bp.route("/mahasiswa/hapus/<int:id>")
def mahasiswa_hapus(id):
    mhs_uc.hapus_mahasiswa(id)
    return redirect(request.referrer or url_for("main.kelas_list"))
