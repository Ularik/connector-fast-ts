from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
# from pydantic import Field, BaseModel, EmailStr, ConfigDict
# from typing import Optional
# from authx import AuthX, AuthXConfig
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from src.api.ts_api import router as ts_router
from src.api.vs_api import router as vs_router

app = FastAPI()

app.include_router(ts_router, tags=["cars"])
app.include_router(vs_router, tags=["Права"])

@app.exception_handler(TimeoutError)
async def db_operational_error_handler(request: Request, exc: TimeoutError):
    return JSONResponse(
        status_code=503,
        content={"message": "База данных временно недоступна. Попробуйте позже."},
    )



#
# class UserSchema(BaseModel):
#     name: str
#     bio: str | None = Field(max_length=10)
#     age: int = Field(ge=0, le=130)
#
#     model_config = ConfigDict(extra='forbid')   # запрет на ввод доп параметров
#
#
# class UserAuth(BaseModel):
#     username: str
#     password: str
#
#     model_config = ConfigDict(extra='forbid')

# config = AuthXConfig()
# config.JWT_SECRET_KEY = 'SECRET_KEY'
# config.JWT_ACCESS_COOKIE_NAME = 'ulars_token'
# config.JWT_TOKEN_LOCATION = ['cookies']
#
# security = AuthX(config=config)
#
#
# @app.get("/", summary="Hellow world", tags=["Start"])
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.post('/login', tags=["login"])
# async def login(cred: UserAuth):
#     if cred.username == 'test' and cred.password == 'test':
#         token = security.create_access_token(uid='12345')
#         return {'access_token': '...'}
#     raise HTTPException(status_code=401, detail='Auth error')
#
#
# @app.post("/users/", summary="Create User", tags=["User"])
# async def create_user(data: UserSchema) -> UserSchema:
#     print(data)
#     return data

