from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    email: str
    is_staff: bool
    is_active: bool



class LoginModel(BaseModel):
    username: str
    password: str


class Settings(BaseSettings):
    authjwt_secret_key: str = 'cb8a53e3b3eabb3b186ed24b11b50b4c750c8c30cdd2b40eba9f32a74c70f837'