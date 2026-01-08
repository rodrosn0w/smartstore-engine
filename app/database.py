from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tu conexión centralizada
URL_DATABASE = "mysql+mysqlconnector://root:admin123@localhost:3306/smart_store"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()