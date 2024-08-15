from datetime import datetime, timezone
from sqlmodel import create_engine, SQLModel, text

DATABASE_URL = "sqlite:///./db/chat.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Mở phiên kết nối và thực hiện ALTER TABLE
# with engine.connect() as connection:
#     connection.execute(text("ALTER TABLE user ADD COLUMN created_at DATETIME"))

# Sau đó, bạn có thể cập nhật giá trị cho các bản ghi hiện có
# with engine.connect() as connection:
#     now = datetime.now(timezone.utc)
#     connection.execute(text("UPDATE user SET created_at = '{now}' WHERE created_at IS NULL"))