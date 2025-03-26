from fastapi import FastAPI
from app.routers.order_rout import order_router
from app.routers.auth_rout import auth_router
from app.table.database import engine, Base
from app.table.schemas import Settings, LoginModel
from fastapi_jwt_auth import AuthJWT



app = FastAPI()

Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/')
async def get_root():
    return {"Dastavka": "Asosiy Sahifa"}


app.include_router(order_router, tags=["Buyurtmalar"])
app.include_router(auth_router, tags=["SignUp"])