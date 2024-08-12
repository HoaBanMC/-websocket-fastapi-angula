from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./db/chat.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
