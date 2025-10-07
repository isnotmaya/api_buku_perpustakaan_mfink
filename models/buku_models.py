from sqlalchemy import Column, Integer, String
from config.database import Base

class Buku(Base):
    __tablename__ = "buku"

    id_buku = Column(Integer, primary_key=True, index=True)
    judul_buku = Column(String(150))
    pengarang = Column(String(100))
    penerbit = Column(String(100))
    tahun = Column(Integer)
    isbn = Column(String(20), unique=True)
    cover = Column(String(255))  # URL gambar cover buku
