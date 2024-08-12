import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import logging
import uuid
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, status
from sqlmodel import Session, select, delete
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
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):
        if room_id in self.active_connections:
            self.active_connections[room_id].pop(user_id, None)
            if not self.active_connections[room_id]:  # Remove the room if empty
                self.active_connections.pop(room_id)

    async def broadcast(self, response: dict, room_id: int):
        if room_id in self.active_connections:
            for websocket in self.active_connections[room_id].values():
                try:
                    await websocket.send_json(response)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    # Handle disconnection during send
                    user_id = next(key for key, value in self.active_connections[room_id].items() if value == websocket)
                    self.disconnect(room_id, user_id)


manager = ConnectionManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

connected_clients = []
connected_rooms = {}  # Dictionary to manage connections per room

async def heavy_data_processing(data: dict):
    """Some (fake) heavy data processing logic."""
    await asyncio.sleep(0.5)
    message_processed = data.get("message", "")
    return message_processed

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, session: Session = Depends(get_session)):
    user_id = str(uuid.uuid4())
    await manager.connect(websocket, room_id, user_id)
    logger.info(f"New connection: {websocket.client}, ID: {user_id}")

    try:
        while True:
            data = await websocket.receive_json()
            message_processed = await heavy_data_processing(data)
            response = {
                "content": message_processed,
                "time": round(datetime.now().timestamp()),
                "room_id": room_id,
                "user_id": user_id
            }

            # Save the message to the database
            message = Message(content=response["content"], time=response["time"], room_id=room_id, user_id=user_id)
            session.add(message)
            session.commit()
            session.refresh(message)

            # Broadcast the message to all clients in the room
            await manager.broadcast(response, room_id)

    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        print(f"User {user_id} disconnected from room {room_id}")
        
    except Exception as e:
        print(f"Error in websocket_endpoint: {e}")


@app.get("/chatrooms", response_model=List[ChatRoom])
def read_chatrooms(session: Session = Depends(get_session)):
    chatrooms = session.exec(select(ChatRoom)).all()
    return chatrooms

@app.get("/chatrooms/{room_id}/messages", response_model=List[Message])
def read_messages(room_id: int, session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.room_id == room_id)).all()
    # sort
    # messages = session.exec(select(Message).where(Message.room_id == room_id).order_by(Message.time.desc())).all()
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


@app.delete("/chatrooms/{room_id}")
def delete_chatroom(room_id: int, session: Session = Depends(get_session)):
    # Kiểm tra xem phòng chat có tồn tại hay không
    existing_room = session.exec(select(ChatRoom).where(ChatRoom.id == room_id)).first()
    if not existing_room:
        raise HTTPException(status_code=404, detail="Room not found.")
    
    session.execute(delete(Message).where(Message.room_id == room_id))

    session.delete(existing_room)
    session.commit()
    
    return {"message": f"Chat room with ID {room_id} deleted successfully"}

