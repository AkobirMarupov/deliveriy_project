from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.table.schemas import SignUpModel, UserResponse, LoginModel
from app.table.models import User
from app.table.database import engine, get_db
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter(
    prefix='/auth'
)



@auth_router.get('/', response_model=list[UserResponse])
async def signup_page(session: Session = Depends(get_db)):
    db_all = session.query(User).all()

    return db_all

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def signup(user: SignUpModel, session: Session = Depends(get_db)):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bunday email orqali allaqachon ro‘yxatdan o‘tgan.'
        )

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bunday username allaqachon bazada mavjud.'
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@auth_router.post('/login', status_code=200, response_model=LoginModel)
async def login(user: LoginModel, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Parol yoki username xato.')
