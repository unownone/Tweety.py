import uvicorn
from fastapi import FastAPI,Request,BackgroundTasks
from pymongo import MongoClient
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import binascii,os
from send_email import send_email_background, send_email_async
from decouple import config
from pydantic import BaseModel
from datetime import datetime,timedelta
from bot import tweetify

class Token(BaseModel):
    token: str
    scripts: list
    tags:list
    nums:int



class AuthTokens(BaseModel):
    email: str
    cons_key: str
    cons_sec: str
    access_key: str
    access_sec: str

mongo = MongoClient(config("mongo_host"))
user = mongo.tweetypy.tokens


templates = Jinja2Templates(directory='templates')

app = FastAPI(docs_url=None,openapi_url=None)


def generate_key():

    token = binascii.hexlify(os.urandom(20)).decode()
    while user.find_one({'auth_token':token}) is not None:
        token = binascii.hexlify(os.urandom(20)).decode()
    return token 



@app.get('/',response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post('/authtoken',response_class=JSONResponse)
async def authorizationToken(data:AuthTokens,background_tasks: BackgroundTasks):
    auth_token = generate_key()
    if user.find_one({"email":data.email}) is None:
        datas ={'auth_token':auth_token,'email':data.email,
        'keyval':{
            'cons_key':data.cons_key,
            'cons_sec':data.cons_sec,
            'access_key':data.access_key,
            'access_sec':data.access_sec},
        'quota':100,
        'reset':datetime.now()+timedelta(days=1)}
        user.insert_one(datas)
        send_email_background(background_tasks=background_tasks,subject='TweetyPy Authentication Token',email_to=data.email,body={'apikey':auth_token})
        return JSONResponse(content=jsonable_encoder({"response":"Email Successfully Sent!"}))
    else:
        send_email_background(background_tasks=background_tasks,subject='TweetyPy Authentication Token',email_to=data.email,body={'apikey':auth_token})
        return JSONResponse(content=jsonable_encoder({"response":"Email Successfully Sent!"}))


@app.post('/commentbot',response_class=JSONResponse)
async def botify(data:Token,background_tasks: BackgroundTasks):
    if data.token == '' or len(data.scripts) == 0 or len(data.tags) == 0 or data.nums == 0 or data.nums is None:
        return JSONResponse(content=jsonable_encoder({"response":"Invalid/empty Data"}))
    finalTags = (" OR ").join(data.tags)
    background_tasks.add_task(tweetify,data.token,scripts=data.scripts,tags=finalTags,tweetnums=data.nums)
    return JSONResponse(content=jsonable_encoder({"response":"Successfully Sent!"}))
