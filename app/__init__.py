import uvicorn
from ctypes import Union
from typing import Optional
from fastapi import FastAPI, Request,responses
from datetime import timedelta
from pydantic import BaseModel
from decouple import config
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = config("JWT_SECRET")
    authjwt_access_token_expires = timedelta(minutes=45)
    
   
@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
    

templates = Jinja2Templates(directory='templates')


from app.main import *