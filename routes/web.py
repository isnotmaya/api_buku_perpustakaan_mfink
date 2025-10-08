from flask import Blueprint
from controllers.Buku_Controllers import (
    get_all_buku,
    get_buku_by_id,
    add_buku,
    update_buku,
    delete_buku
)

# Definisikan blueprint dulu
web = Blueprint("web", __name__)

# Route untuk homepage / tes API
@web.route('/')
def index():
    return "API Buku - Flask berjalan!"

# Endpoint API CRUD Buku
web.route("/buku", methods=["GET"])(get_all_buku)           # GET semua buku
web.route("/buku/<int:id_buku>", methods=["GET"])(get_buku_by_id)  # GET berdasarkan ID
web.route("/buku", methods=["POST"])(add_buku)              # Tambah buku
web.route("/buku/<int:id_buku>", methods=["PUT"])(update_buku)     # Update buku
web.route("/buku/<int:id_buku>", methods=["DELETE"])(delete_buku)  # Hapus buku
