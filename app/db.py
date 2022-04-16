import mongoengine as db

from datetime import datetime, timedelta
from decouple import config
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

#Connect to MongoDB
db.connect(
    db=config('MONGO_DB'), 
    host = config('MONGO_HOST'),
    port = int(config('MONGO_PORT',27017)),
    username=config('MONGO_USER'), 
    password=config('MONGO_PASS'), 
)


class User(db.Document):
    """User Model 
    """
    email = db.EmailField(primary_key=True)
    password = db.StringField(max_length=64)
    
    name = db.StringField(max_length=100)
    date_joined = db.DateTimeField(default=datetime.now())
    
    quota = db.IntField(default=100)
    curr_quota = db.IntField(default=100)
    
    active = db.BooleanField(default=True)
    suspended = db.BooleanField(default=False)
    
    request_token = db.DictField()
    access_token = db.StringField(max_length=200)
    access_secret = db.StringField(max_length=200)

    reset = db.DateTimeField()