from flask import jsonify, request
from config.database import get_db
from models.buku_models import Buku
from sqlalchemy.orm import Session

# --- GET: Semua buku ---
def get_all_buku():
    db: Session = next(get_db())
    data = db.query(Buku).all()

    return jsonify([
        {
            "id_buku": b.id_buku,
            "judul_buku": b.judul_buku,
            "pengarang": b.pengarang,
            "penerbit": b.penerbit,
            "tahun": b.tahun,
            "isbn": b.isbn
        } for b in data
    ])


# --- GET: Buku berdasarkan ID ---
def get_buku_by_id(id_buku):
    db: Session = next(get_db())
    buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

    if not buku:
        return jsonify({"message": "Buku tidak ditemukan"}), 404

    return jsonify({
        "id_buku": buku.id_buku,
        "judul_buku": buku.judul_buku,
        "pengarang": buku.pengarang,
        "penerbit": buku.penerbit,
        "tahun": buku.tahun,
        "isbn": buku.isbn
    })


# --- POST: Tambah buku baru ---
def add_buku():
    db: Session = next(get_db())
    body = request.json

    new_buku = Buku(
        judul_buku=body["judul_buku"],
        pengarang=body["pengarang"],
        penerbit=body["penerbit"],
        tahun=body["tahun"],
        isbn=body["isbn"]
    )

    db.add(new_buku)
    db.commit()
    db.refresh(new_buku)

    return jsonify({
        "message": "Buku berhasil ditambahkan",
        "id_buku": new_buku.id_buku
    })


# --- PUT: Update buku ---
def update_buku(id_buku):
    db: Session = next(get_db())
    body = request.json
    buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

    if not buku:
        return jsonify({"message": "Buku tidak ditemukan"}), 404

    buku.judul_buku = body.get("judul_buku", buku.judul_buku)
    buku.pengarang = body.get("pengarang", buku.pengarang)
    buku.penerbit = body.get("penerbit", buku.penerbit)
    buku.tahun = body.get("tahun", buku.tahun)
    buku.isbn = body.get("isbn", buku.isbn)

    db.commit()
    db.refresh(buku)

    return jsonify({"message": "Buku berhasil diperbarui"})


# --- DELETE: Hapus buku ---
def delete_buku(id_buku):
    db: Session = next(get_db())
    buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

    if not buku:
        return jsonify({"message": "Buku tidak ditemukan"}), 404

    db.delete(buku)
    db.commit()

    return jsonify({"message": "Buku berhasil dihapus"})
