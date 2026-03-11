from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.core.config import settings

# quote_plus handles special characters in password like @ # etc
password = quote_plus(settings.DB_PASSWORD)

# MySQL connection URL
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:"
    f"{password}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

# SSL configuration for Aiven
connect_args = {}
if settings.DB_SSL_REQUIRED:
    connect_args = {
        "ssl": {
            "ca": settings.SSL_CA_PATH
        }
    }

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()