import logging
import uuid
import sqlalchemy
from datetime import datetime
from utils  import haevy_data_precessing

from fastapi import WebSocket, WebSocketDisconnect


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

connected_clients = []
connected_rooms = {}  # Dictionary to manage connections per room

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    global connected_clients

    client_id = str(uuid.uuid4())
    connected_clients.append({"id": client_id, "websocket": websocket})
    logger.info(f"New connection: {websocket.client}, ID: {client_id}")

    while True:
        try:
            data = await websocket.receive_json()
            message_processed = await haevy_data_precessing(data)
            response = {
                "message": message_processed,
                "time": datetime.now().strftime("%H:%M:%S"),
                "id": client_id
            }
            # Send the processed message to all connected clients
            for client in connected_clients:
                 await client["websocket"].send_json(response)

        except WebSocketDisconnect:
            connected_clients = [client for client in connected_clients if client["id"] != client_id]
            logger.info(f"Connection closed: {websocket.client}, ID: {client_id}")
            break

        except Exception as e:
            logger.error(f"Error: {e}")
            connected_clients = [client for client in connected_clients if client["id"] != client_id]
            await websocket.close()
            break