from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, status
from sqlmodel import Session, select, create_engine, SQLModel
from typing import List, Dict
from models.models import ChatRoom, Message
from utils.middleware import setup_cors
from utils.database import engine, create_db_and_tables

def get_session():
    with Session(engine) as session:
        yield session

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
    lifespan=lifespan
)

# Gọi hàm setup_cors để cấu hình CORS
setup_cors(app)

# Manage active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: int):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, session: Session = Depends(get_session)):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Save the message to the database
            message = Message(content=data, room_id=room_id, user_id=1)  # Assume user_id=1 for simplicity
            session.add(message)
            session.commit()
            session.refresh(message)
            # Broadcast the message to all clients in the room
            await manager.broadcast(f"{message.user_id}: {message.content}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

@app.get("/chatrooms", response_model=List[ChatRoom])
def read_chatrooms(session: Session = Depends(get_session)):
    chatrooms = session.exec(select(ChatRoom)).all()
    return chatrooms

@app.get("/chatrooms/{room_id}/messages", response_model=List[Message])
def read_messages(room_id: int, session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.room_id == room_id)).all()
    return messages

# Endpoint để tạo room mới
@app.post("/chatrooms", response_model=ChatRoom, status_code=status.HTTP_201_CREATED)
def create_chatroom(room: ChatRoom, session: Session = Depends(get_session)):
    # Kiểm tra xem phòng chat có tồn tại hay không
    existing_room = session.exec(select(ChatRoom).where(ChatRoom.name == room.name)).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Room with this name already exists.")
    
    # Tạo phòng chat mới
    new_room = ChatRoom(name=room.name)
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    
    return new_room