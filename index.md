# Tweety.py 

## [<font color=red align=center>deployed on Heroku</font>](https://tweetypy1.herokuapp.com/)
## A End to End no-code Twitter Bot Api

Ever wanted to automate marketing with twitter? Well, now you can!

Using Tweety.py's Fast API Now you can do that and much more !

## <font size=6 color=skyblue>Demo</font> 
  <p align="center">
    <img width="40%" src="https://1000logos.net/wp-content/uploads/2021/04/Twitter-logo.png" alt="Tweety.Py"/>
  </p>

## Features Currently:
- comment on tweets with a specific hashtag/ keyword
- comment on tweets for free!
- comment on tweets that match a certain sentiment [Coming soon]
- comment on tweets that match a certain location [Coming soon]
- comment on tweets that match a certain language [Coming soon]
- Run campaigns on twitter that are scheduled! [Coming soon]

# API ENDPOINTS:

Want Better Documentation ?  
 [<font size=5 color=green> Use FastAPI's Swagger UI </font>](https://tweetypy1.herokuapp.com/docs)
## <font color=orange>/auth</font> : Signup/Login to the tweety.py
    /signup : [POST]
        body: {
            "name":"",
            "email": "",
            "password": ""
        }
    /login : [POST]
        body: {
            "email": "",
            "password": ""
        }
        returns : {
            "access_token":"",
            "refresh_token":""
        }
    /user : [GET] Get current user
## <font color=orange>/bot</font> : Use the Bot
    /twitter: [GET] Connect twitter account to tweetypy account.

    returns : Twitter URL to connect to
    /twitter-callback-url: [GET] Twitter Callback url to finish Oauth `DANCE`.

    /commentbot: [POST] Comment Bot to comment on posts
    body: {
        {
        "tags": [
            "string"  // stores hashtags and keywords
        ],
        "scripts": [
            "string" // stores list of strings to
                    //be sent as comment randomly
        ],
        "nums": 0   // count of comments to be sent in total.
        }
    }

# Running on Local / forking.

- clone the repo
- cd into the folder
- first create a virtualenv and activate it.
    example : 
    
        virtualenv venv
    then activate it
        
        ./venv/bin/activate

- Install requirements.
    
        pip install -r requirements.txt

- run server using:

        uvicorn app:app --reload --port 8000

Your App will be running on LocalHost.

## ENV DETAILS :
have a .env file in root that will contain these values:
- ```CONSUMER_KEY``` : twitter Consumer Key
- ```CONSUMER_SECRET``` : twitter Consumer Secret
- ```JWT_SECRET``` : For jwt token generation
- ```MONGO_DB``` : Mongo database name
- ```MONGO_HOST``` : Mongo host name 
- ```MONGO_PORT``` : Mongo port number
- ```MONGO_USER``` : Mongo user name
- ```MONGO_PASS``` : Mongo password
- ```EMAIL_HOST``` : Email host
- ```EMAIL_HOST_USER``` : Email of user
- ```EMAIL_HOST_PASSWORD``` : Email password


# Built using [FastAPI](https://fastapi.tiangolo.com) , [MongoDB](https://mongodb.org) , [Heroku](https://www.heroku.com)

