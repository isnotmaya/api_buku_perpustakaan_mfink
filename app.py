import os
from flask import Flask
from routes.web import web
from config.database import Base, engine

app = Flask(__name__)

# Buat tabel otomatis jika belum ada
Base.metadata.create_all(bind=engine)

# Daftarkan blueprint
app.register_blueprint(web)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    # WAJIB pakai 0.0.0.0 agar Railway bisa mengakses aplikasi
    app.run(host="0.0.0.0", port=port)
