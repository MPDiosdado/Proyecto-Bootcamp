import json
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 1. Configuración de la conexión (Ajusta con tus credenciales de Docker/Local)
# Formato: postgresql://usuario:password@localhost:5432/nombre_db
DATABASE_URL = "postgresql://TU-USUARIO:TU-CONTRASEÑA@localhost:5432/ciudadai_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definición del Modelo de Datos (Requisito: Punto 6.2 de la normativa)
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    body_raw = Column(Text)           # Cuerpo original (con PII para anonimizar luego)
    body_anon = Column(Text, nullable=True) # Aquí guardaremos el resultado de Presidio
    citizen_name = Column(String(100))
    email = Column(String(100))
    categoria_sugerida = Column(String(50))
    prioridad = Column(Integer)
    is_validated = Column(Boolean, default=False) # Para el Active Learning
    created_at = Column(DateTime, default=datetime.utcnow)

# 3. Creación de las tablas en la base de datos
Base.metadata.create_all(bind=engine)

def load_initial_data(file_path: str):
    db = SessionLocal()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
       
        for item in data:
            nuevo_ticket = Ticket(
                subject=item["subject"],
                body_raw=item["body"],
                citizen_name=item["citizen_name"],
                email=item["email"],
                categoria_sugerida=item["categoria"],
                prioridad=item["prioridad"],
                created_at=datetime.fromisoformat(item["created_at"])
            )
            db.add(nuevo_ticket)
       
        db.commit()
        print(f"✓ Éxito: {len(data)} registros cargados en PostgreSQL.")
    except Exception as e:
        print(f"Error cargando datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Asegúrate de que la ruta coincida con donde generaste el archivo
    load_initial_data("synthetic/solicitudes_train.json")
