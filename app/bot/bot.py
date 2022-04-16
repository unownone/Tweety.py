import traceback
import tweepy
from decouple import config
from random import choice
from datetime import datetime,timedelta
from fastapi import BackgroundTasks
from app.send_email import send_email_background, send_email_async
from app.db import User



async def tweepyOauth(user_obj):
    if user_obj.request_token and (user_obj.access_token and user_obj.access_secret):
        raise ValueError('Already Authenticated')
    auth = tweepy.OAuthHandler(config("CONSUMER_KEY"),config("CONSUMER_SECRET"))
    url = auth.get_authorization_url()
    user_obj.request_token = auth.request_token
    user_obj.save()
    return url

async def tweepyOauthVerify(user_obj,verifier):
    if user_obj.request_token is None:
        raise ValueError('No Request Token Provided')
    auth = tweepy.OAuthHandler(config("CONSUMER_KEY"),config("CONSUMER_SECRET"))
    auth.request_token = user_obj.request_token
    user_obj.access_token,user_obj.access_secret = auth.get_access_token(verifier)
    user_obj.save()
    return True

async def tweetify(user_obj,scripts=[],tags='',tweetnums=''):
    try:
        auth = tweepy.OAuthHandler(config("CONSUMER_KEY"),config("CONSUMER_SECRET"))
        auth.set_access_token(user_obj.access_token,user_obj.access_secret)
        api = tweepy.API(auth)
        try:
            api.verify_credentials()
        except:
            print("hi")
            datas = {
                'header':'Your Task was Terminated due to Authentication Failer!',
                'body':'We failed to authenticate with your credentials and hence the job was terminated!'
            }
            # send_email_background(BackgroundTasks,'TweetyPy Alert!',user_obj.email,datas,type=1)
            return -1


        limit = user_obj.quota
        if user_obj.reset is None:
            user_obj.reset = datetime.now() + timedelta(days=1)
        time = user_obj.reset

        if limit <= tweetnums:
            datas = {
                'header':'Your Task was Terminated due to Lack of Balance!',
                'body':f'Sorry You do not have enough balance to execute this order. Current balance :{limit},job size:{tweetnums}'
            }
            # send_email_background(BackgroundTasks,'TweetyPy Alert!',user_obj.email,datas,type=1)
            return 2
        
        datas = {
            'header':'Your Task was succesfully started!',
            'body':'Your task has been started Successfully!'
        }
        # await send_email_async('TweetyPy Alert!',user_obj.email,datas,type=1)
        MAX_TWEETS = 100 #Maximum tweetnumbers
        for tweet in tweepy.Cursor(api.search_tweets, q=tags).items(min(tweetnums,MAX_TWEETS)):
            try:
                api.update_status(status = choice(scripts),in_reply_to_status_id = tweet.id,auto_populate_reply_metadata = True)
            except:
                pass
        flag = False
        if time > datetime.now():
            limit = 100
            flag = True
            user_obj.quota = limit
            user_obj.reset = datetime.now() + timedelta(days=1)
        else:
            limit = limit - tweetnums
            user_obj.quota = limit
            if flag:
                data = 'Your quota has been refilled!'
            else:
                data =""
            datas = {
                'header':'Your task was successfully Completed!',
                'body':f'Good news! Your task has been successfully completed.{data} Your Current quota balance is : {limit}.'
            }
            # send_email_background(BackgroundTasks,'TweetyPy Alert!',user_obj.email,datas,type=1)
            user_obj.save()
        return 1
    except Exception as e:
        raise e
        datas = {
                'header':'Your Task was terminated due to internal Error',
                'body':'Due to some error your task was terminated. We are looking into it! Be sure , your balance has not been deducted!'
            }
        # send_email_background(BackgroundTasks,'TweetyPy Alert!',user_obj.email,datas,type=1)
        return -2