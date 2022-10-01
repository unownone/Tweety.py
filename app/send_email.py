from jinja2 import Template
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config

conf:ConnectionConfig = ConnectionConfig(
    MAIL_USERNAME=config("EMAIL_HOST_USER"),
    MAIL_PASSWORD=config("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=config("EMAIL_HOST_USER"),
    MAIL_PORT=587,
    MAIL_SERVER=config("EMAIL_HOST"),
    MAIL_FROM_NAME='Tweety.Py Admin',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./templates/email'
)


async def send_email_async(subject: str, email_to: str, body: dict,type:int=0):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body='',
        template_body=body,
        subtype='html',
    )
    
    fm:FastMail = FastMail(conf)
    if type == 0:
        await fm.send_message(message, template_name='email.html')
    elif type == 1:
        await fm.send_message(message, template_name='alert.html')



#type 1 for alert , 0 for otp
def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict,type:int=0):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body='',
        template_body=body,
        subtype='html',
    )
    fm:FastMail = FastMail(conf)
    if type==0:
        background_tasks.add_task(fm.send_message, message, template_name='email.html')
    elif type==1:
        background_tasks.add_task(fm.send_message, message, template_name='alert.html') 