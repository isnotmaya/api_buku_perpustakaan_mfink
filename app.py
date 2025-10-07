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
    host = "0.0.0.0" if os.environ.get("RAILWAY_ENVIRONMENT") else "127.0.0.1"

    # Mode lokal akan tampil di browser, Railway tidak
    debug_mode = not os.environ.get("RAILWAY_ENVIRONMENT")

    app.run(host=host, port=port, debug=debug_mode)
