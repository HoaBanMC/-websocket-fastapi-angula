import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict
from fastapi import  WebSocket, WebSocketDisconnect, Depends, APIRouter
from sqlmodel import Session
from typing import  Dict
from backend.models.chatroom import  Message
from backend.utils.session import get_session

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

connected_clients = []
connected_rooms = {}  # Dictionary to manage connections per room

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

async def heavy_data_processing(data: dict):
    """Some (fake) heavy data processing logic."""
    await asyncio.sleep(0.5)
    message_processed = data.get("message", "")
    return message_processed

@router.websocket("/ws/{room_id}")
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