from flask import jsonify, request
from config.database import SessionLocal
from models.buku_models import Buku
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# --- GET: Semua buku ---
def get_all_buku():
    db: Session = SessionLocal()
    try:
        data = db.query(Buku).all()

        return jsonify([
            {
                "id_buku": b.id_buku,
                "judul_buku": b.judul_buku,
                "pengarang": b.pengarang,
                "penerbit": b.penerbit,
                "tahun": b.tahun,
                "isbn": b.isbn,
                "cover": b.cover
            } for b in data
        ])
    finally:
        db.close()


# --- GET: Buku berdasarkan ID ---
def get_buku_by_id(id_buku):
    db: Session = SessionLocal()
    try:
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

        if not buku:
            return jsonify({"message": "Buku tidak ditemukan"}), 404

        return jsonify({
            "id_buku": buku.id_buku,
            "judul_buku": buku.judul_buku,
            "pengarang": buku.pengarang,
            "penerbit": buku.penerbit,
            "tahun": buku.tahun,
            "isbn": buku.isbn,
            "cover": buku.cover
        })
    finally:
        db.close()


# --- POST: Tambah buku baru ---
def add_buku():
    if not request.is_json:
        return jsonify({"message": "Gunakan format JSON"}), 400

    body = request.json
    required_fields = ["judul_buku", "pengarang", "penerbit", "tahun", "isbn"]

    # Validasi data wajib
    if not all(field in body and body[field] for field in required_fields):
        return jsonify({"message": "Data tidak lengkap"}), 400

    db: Session = SessionLocal()
    try:
        # Cek ISBN unik
        if db.query(Buku).filter(Buku.isbn == body["isbn"]).first():
            return jsonify({"message": "ISBN sudah terdaftar"}), 400

        # Cek judul unik (case-insensitive)
        if db.query(Buku).filter(Buku.judul_buku.ilike(body["judul_buku"])).first():
            return jsonify({"message": "Judul buku sudah terdaftar"}), 400

        # Buat objek buku baru
        new_buku = Buku(
            judul_buku=body["judul_buku"],
            pengarang=body["pengarang"],
            penerbit=body["penerbit"],
            tahun=body["tahun"],
            isbn=body["isbn"],
            cover=body.get("cover")
        )

        db.add(new_buku)
        db.commit()
        db.refresh(new_buku)

        return jsonify({
            "message": "Buku berhasil ditambahkan",
            "id_buku": new_buku.id_buku,
            "cover": new_buku.cover
        }), 201

    except IntegrityError:
        db.rollback()
        return jsonify({"message": "Terjadi kesalahan database"}), 500
    finally:
        db.close()


# --- PUT: Update buku ---
def update_buku(id_buku):
    if not request.is_json:
        return jsonify({"message": "Gunakan format JSON"}), 400

    body = request.json
    db: Session = SessionLocal()
    try:
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

        if not buku:
            return jsonify({"message": "Buku tidak ditemukan"}), 404

        # Cek duplikasi ISBN (kalau diubah)
        if "isbn" in body and body["isbn"] != buku.isbn:
            if db.query(Buku).filter(Buku.isbn == body["isbn"]).first():
                return jsonify({"message": "ISBN sudah terdaftar"}), 400

        # Cek duplikasi judul (kalau diubah)
        if "judul_buku" in body and body["judul_buku"].lower() != buku.judul_buku.lower():
            if db.query(Buku).filter(Buku.judul_buku.ilike(body["judul_buku"])).first():
                return jsonify({"message": "Judul buku sudah terdaftar"}), 400

        # Update data
        buku.judul_buku = body.get("judul_buku", buku.judul_buku)
        buku.pengarang = body.get("pengarang", buku.pengarang)
        buku.penerbit = body.get("penerbit", buku.penerbit)
        buku.tahun = body.get("tahun", buku.tahun)
        buku.isbn = body.get("isbn", buku.isbn)
        buku.cover = body.get("cover", buku.cover)

        db.commit()
        db.refresh(buku)

        return jsonify({
            "message": "Buku berhasil diperbarui",
            "id_buku": buku.id_buku
        })
    except IntegrityError:
        db.rollback()
        return jsonify({"message": "Terjadi kesalahan database"}), 500
    finally:
        db.close()


# --- DELETE: Hapus buku ---
def delete_buku(id_buku):
    db: Session = SessionLocal()
    try:
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()

        if not buku:
            return jsonify({"message": "Buku tidak ditemukan"}), 404

        db.delete(buku)
        db.commit()

        return jsonify({"message": "Buku berhasil dihapus"})
    finally:
        db.close()
