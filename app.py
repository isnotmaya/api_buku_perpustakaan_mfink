from flask import Flask
from routes.web import web
from config.database import Base, engine

# Inisialisasi Flask
app = Flask(__name__)

# Buat tabel di database (jika belum ada)
Base.metadata.create_all(bind=engine)

# Daftarkan Blueprint
app.register_blueprint(web)

if __name__ == "__main__":
    app.run(debug=True)
