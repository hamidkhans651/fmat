from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks, FastAPI
# Basic email related code
config = ConnectionConfig(
    MAIL_USERNAME="username", 
    MAIL_PASSWORD="12345", 
    MAIL_FROM="iamshoaib@test.com", 
    MAIL_FROM_NAME="Full Stack Auth App", 
    MAIL_PORT=1025,
    MAIL_SERVER="smtp",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=True
    )

# app = FastAPI()

html = """
<p> Thanks for using fastapi-mail </p>
"""
fm = FastMail(config)
async def send_mail(email:str):
    message = MessageSchema(subject="Fastapi Mail Module", recipients=[email], body=html, subtype=MessageType.html,  )

    await fm.send_message(message)
    return {"email": "email has been sent!"}