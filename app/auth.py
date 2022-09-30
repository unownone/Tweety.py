from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi import  Depends, HTTPException, Request, APIRouter
from pydantic import BaseModel
from decouple import config
from app.db import User
from app.utils import Hasher
from app.models import (
    dictResponseModel,ListResponseModel,
    ErrorResponseModel,User_dict,
    User_signup_dict,
)


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    )


    

@router.post('/login')
def login(user: User_dict, Authorize: AuthJWT = Depends()):
    hash:Hasher = Hasher()
    try:
        user_obj:User = User.objects.get(email=user.email)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not hash.verify_password(user.password, user_obj.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if user_obj.suspended:
        raise HTTPException(status_code=400, detail="Account has been Suspended!Contact Support!")
    # subject identifier for who this token is for example id or username from database
    user_claims = {
        'access_level':'user'
    }
    if user_obj.email == 'royimonroy@gmail.com':
        user_claims['access_level'] = 'admin'
    access_token = Authorize.create_access_token(subject=user_obj.email,
                                                 user_claims=user_claims)
    refresh_token = Authorize.create_refresh_token(subject=user_obj.email,
                                                   user_claims=user_claims)
    headers = {"Authorization":f"Bearer {access_token}"}
    return JSONResponse(content={
            "access_token": access_token,
            "refresh_token":refresh_token,
            'user_type':user_claims['access_level']
        },headers=headers,status_code=200)


@router.post('/signup')
def signup(user: User_signup_dict):
    hash:Hasher = Hasher()
    try:
        user_obj:User = User.objects.get(email=user.email)
        return ErrorResponseModel(error='Email Already Exists!')
    except User.DoesNotExist:
        print('Proper Let us Create an user')
    user_obj:User = User.objects.create(
        email=user.email,
        password=hash.get_password_hash(user.password),
        name=user.name,
        active=True,
    )
    return dictResponseModel(data={
            "message": "User Created Successfully"
    })


@router.get('/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return dictResponseModel(data={
            "user": current_user
    })