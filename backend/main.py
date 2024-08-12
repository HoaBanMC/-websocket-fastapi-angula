from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.utils.database import create_db_and_tables
from backend.utils.middleware import setup_cors
from backend.routes import chatrooms, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Example: use `app` to access configuration or perform setup
    print(f"Configuring app: {app.title}")
    create_db_and_tables()
    yield


app = FastAPI(
    title="My Chatroom",
    description="This is a description of my chatroom API.",
    version="1.0.0",
    lifespan=lifespan,
)

# Gọi hàm setup_cors để cấu hình CORS
setup_cors(app)

# Gọi các router
app.include_router(chatrooms.router)
app.include_router(websocket.router)
