from backend.utils.session import get_session
from sqlmodel import Session,select
from fastapi import APIRouter, Depends, HTTPException, status
from backend.models.user import User
from backend.schemas.user import LoginRequest, UserCreate, UserRead
from backend.utils.auth import get_current_user, hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Kiểm tra xem người dùng đã tồn tại chưa
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Tạo người dùng mới với mật khẩu đã được hash
    new_user = User(username=user.username, password=hash_password(user.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    # Tìm người dùng theo username
    statement = select(User).where(User.username == login_data.username)
    user = session.exec(statement).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"message": "Login successful"}


# @router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, session: Session = Depends(get_session)):
#     # Tìm người dùng theo ID
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     # Xoá người dùng
#     session.delete(user)
#     session.commit()
#     return {"message": "User and related data deleted successfully"}


@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user