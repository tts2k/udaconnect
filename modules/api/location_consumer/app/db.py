from flask_sqlalchemy import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_NAME, DB_PORT, DB_HOST, DB_USERNAME, DB_PASSWORD

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

db_url = SQLALCHEMY_DATABASE_URI
db_engine = create_engine(db_url)
metadata = MetaData()
Base = declarative_base(bind=db_engine, metadata=metadata)
Session = sessionmaker(bind=db_engine)
Session.configure(bind=db_engine)
db_session = Session()
