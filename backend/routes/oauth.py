from backend.utils.session import get_session
from sqlmodel import Session,select
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.models.user import User
from backend.schemas.user import UserCreate, UserRead
from backend.utils.auth import authenticate_user, create_access_token, get_current_user, get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user