from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# En Docker usaremos la URL del contenedor, en local puedes usar SQLite para probar rápido
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./neuralledger.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()