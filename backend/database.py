from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# 1. Prioridad: Variable de entorno (la que pone Docker)
# 2. Segunda opción: Conexión local al puerto 5433 (para uvicorn en Windows)
# 3. Tercera opción: SQLite (como último recurso)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:admin123@localhost:5433/neuralledger"
)

# Ajuste para PostgreSQL vs SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Para PostgreSQL no necesitamos check_same_thread
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()