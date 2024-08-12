from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from sqlmodel import Session, select, delete
from typing import List
from backend.models.chatroom import ChatRoom, Message
from backend.utils.session import get_session

router = APIRouter()

@router.get("/chatrooms", response_model=List[ChatRoom])
def read_chatrooms(session: Session = Depends(get_session)):
    chatrooms = session.exec(select(ChatRoom)).all()
    return chatrooms

@router.get("/chatrooms/{room_id}/messages", response_model=List[Message])
def read_messages(room_id: int, session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.room_id == room_id)).all()
    # sort
    # messages = session.exec(select(Message).where(Message.room_id == room_id).order_by(Message.time.desc())).all()
    return messages

# Endpoint để tạo room mới
@router.post("/chatrooms", response_model=ChatRoom, status_code=status.HTTP_201_CREATED)
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


@router.delete("/chatrooms/{room_id}")
def delete_chatroom(room_id: int, session: Session = Depends(get_session)):
    # Kiểm tra xem phòng chat có tồn tại hay không
    existing_room = session.exec(select(ChatRoom).where(ChatRoom.id == room_id)).first()
    if not existing_room:
        raise HTTPException(status_code=404, detail="Room not found.")
    
    session.execute(delete(Message).where(Message.room_id == room_id))

    session.delete(existing_room)
    session.commit()
    
    return {"message": f"Chat room with ID {room_id} deleted successfully"}

