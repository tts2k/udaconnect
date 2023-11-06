import os
from flask_sqlalchemy import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

db_url = SQLALCHEMY_DATABASE_URI
db_engine = create_engine(db_url)
metadata = MetaData()
Base = declarative_base(bind=db_engine, metadata=metadata)
session_factory = sessionmaker(bind=db_engine)
Session = scoped_session(session_factory)
