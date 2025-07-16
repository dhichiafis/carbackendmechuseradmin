from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

Base=declarative_base()


DB="sqlite:///firstcs.db"

engine=create_engine(DB)

SessionMaker=sessionmaker(bind=engine,autocommit=False,autoflush=False)


def connect():
    db=SessionMaker()
    try:
        yield db 
    finally:
        db.close()