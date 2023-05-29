from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Postgres Unique URL
# 'postgresql://<user>:<password>@<host>/<database>'

SQL_ALCHEMY_CONNECTION= 'postgresql://parthasarathichakraborty:@localhost/fastapi'

engine = create_engine(SQL_ALCHEMY_CONNECTION)

# This makes the session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
# Create a session request for every specific API endpoint.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()