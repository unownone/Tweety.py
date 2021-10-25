import tweepy
from decouple import config
from random import choice
from pymongo import MongoClient
import traceback
from datetime import datetime,timedelta
from fastapi import BackgroundTasks
from send_email import send_email_background, send_email_async
###BOMBIFY BOT FOR GAINING TRACTION

mongo = MongoClient(config["MONGO_HOST"])
user = mongo.tweetypy.tokens

async def tweetify(authToken,scripts=[],tags='',tweetnums=''):
    try:
        mainToken = user.find_one({'auth_token':authToken})
        if authToken == '' or authToken is None or mainToken is None:
            data = {
                'header':'Your Task was terminated!',
                'body':'Your task was terminated because of a wrong/invalid auth token! Please check your auth token and try again!'
            }
            send_email_background(BackgroundTasks,'TweetyPy Alert!',mainToken['email'],data,type=1)
            return 0
        auth = tweepy.OAuthHandler(mainToken['keyval']['cons_key'],mainToken['keyval']['cons_sec'])
        auth.set_access_token(mainToken['keyval']['access_key'],mainToken['keyval']['access_sec'])

        api = tweepy.API(auth)
        try:
            api.verify_credentials()
        except:
            datas = {
                'header':'Your Task was Terminated due to Authentication Failer!',
                'body':'We failed to authenticate with your credentials and hence the job was terminated!'
            }
            send_email_background(BackgroundTasks,'TweetyPy Alert!',mainToken['email'],datas,type=1)
            return -1


        limit = mainToken['quota']
        time = mainToken['reset']

        if limit <= tweetnums:
            datas = {
                'header':'Your Task was Terminated due to Lack of Balance!',
                'body':f'Sorry You do not have enough balance to execute this order. Current balance :{limit},job size:{tweetnums}'
            }
            send_email_background(BackgroundTasks,'TweetyPy Alert!',mainToken['email'],datas,type=1)
            return 2
        
        datas = {
            'header':'Your Task was succesfully started!',
            'body':'Your task has been started Successfully!'
        }
        send_email_async('TweetyPy Alert!',mainToken['email'],datas,type=1)
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
            user.update_one({'auth_token':authToken},{"$set":{'quota':limit,'reset':datetime.now()+timedelta(days=1)}})
        else:
            limit = limit - tweetnums
            user.update_one({'auth_token':authToken},{'$set':{'quota':limit}})
            if flag:
                data = 'Your quota has been refilled!'
            else:
                data =""
            datas = {
                'header':'Your task was successfully Completed!',
                'body':f'Good news! Your task has been successfully completed.{data} Your Current quota balance is : {limit}.'
            }
            send_email_background(BackgroundTasks,'TweetyPy Alert!',mainToken['email'],datas,type=1)
        return 1
    except Exception as e:
        print(traceback.format_exc(e))
        datas = {
                'header':'Your Task was terminated due to internal Error',
                'body':'Due to some error your task was terminated. We are looking into it! Be sure , your balance has not been deducted!'
            }
        send_email_background(BackgroundTasks,'TweetyPy Alert!',mainToken['email'],datas,type=1)
        return -2