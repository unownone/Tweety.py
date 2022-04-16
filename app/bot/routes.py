import traceback
from fastapi import BackgroundTasks,Depends,APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from app.db import User
from app.models import (
     dictResponseModel,
     ErrorResponseModel,
)
from .bot import (
    tweepyOauth,tweepyOauthVerify,
    tweetify
)
from .models import StartComment


router = APIRouter(
    prefix='/bot',
    tags=['bot'],
    )


@router.get('/twitter')
async def get_twitter(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    
    user_obj = User.objects.get(email=Authorize.get_jwt_subject())
    try:
        url = await tweepyOauth(user_obj)    
    except Exception as e:
        return ErrorResponseModel(error=str(e))
    return dictResponseModel(
        data={
            'url':url
        }
    )
    

@router.get('/twitter-callback-url')
async def get_twitter_callback(
    oauth_verifier: str,oauth_token: str,
    Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    
    
    user_obj = User.objects.get(email=Authorize.get_jwt_subject())
    try:
        await tweepyOauthVerify(user_obj,oauth_verifier)
        return dictResponseModel(
            data={"message":"Authorized Successfully"}
        )
    except Exception as e:
        return ErrorResponseModel(
            error=str(e)
        )
    

@router.post('/commentbot')
async def botify(data:StartComment,background_tasks: BackgroundTasks,Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    
    user_obj = User.objects.get(email=Authorize.get_jwt_subject())
    finalTags = (" OR ").join(data.tags)
    background_tasks.add_task(tweetify,user_obj,scripts=data.scripts,tags=finalTags,tweetnums=data.nums)
    return JSONResponse(content=jsonable_encoder({"response":"Successfully Sent!"}))
