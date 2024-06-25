from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks
from pydantic import EmailStr
 
config = ConnectionConfig(
    MAIL_USERNAME="username", 
    MAIL_PASSWORD="12345", 
    MAIL_FROM="noreply@raiboot.com", 
    MAIL_FROM_NAME="RaiBoot", 
    MAIL_PORT=1025,
    MAIL_SERVER="smtpCount",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=True,
    # MAIL_DEBUG=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent/"templates",
    )

fm = FastMail(config)
async def send_mail(email:list, subject:str, template_name:str, context:dict):
    message = MessageSchema(subject=subject, recipients=email, template_body=context, subtype=MessageType.html,  )
    # background_tasks.add_task(func=fm.send_message, message=message, template_name=template_name)
    await fm.send_message(message=message, template_name=template_name)