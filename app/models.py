from pydantic import BaseModel
from fastapi.responses import JSONResponse

BaseError = 'Something Went Wrong Please try again later'

    
class User_signup_dict(BaseModel):
    name: str
    email: str
    password: str
    
class User_dict(BaseModel):
    email: str
    password: str


def dictResponseModel(data: dict={},message: str='Okay'):
    return  JSONResponse(content={
            "data": data,
            "message": message,
        },status_code=200
    )

def ListResponseModel(data=dict(), message: str='Okay'):
    return  JSONResponse(content={
            "data": [data],
            "message": message,
        },status_code=200
    )


def ErrorResponseModel(error, code: int=400, message: str=BaseError):
    return JSONResponse(
        content={
            "error": error,
            "message": message
            },
            status_code=code
        )
