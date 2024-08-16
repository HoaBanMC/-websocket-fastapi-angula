from pydantic import BaseModel

# Pydantic model để nhận thông tin đăng ký
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

class TokenData(BaseModel):
    username: str

# Model cho request body của /login
class LoginRequest(BaseModel):
    username: str
    password: str