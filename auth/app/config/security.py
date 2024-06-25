from typing_extensions import Annotated, Doc
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Form
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from app.config.setting import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES as EXP

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_password(password: str):
    return pwd_context.hash(password)

def verify_hashed_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)

class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    email: str = Form(...,  example="username@gmail.com")
    username: str = Form(None, example="username")
    password: str = Form(..., example="password")

    def __init__(self, **abc):
        super().__init__(abc)


def create_access_token(data: dict, expiry:timedelta=timedelta(minutes=int(EXP))):
    try:
        expiries = datetime.now(timezone.utc) + expiry
        to_encode = {"exp":expiries, "detail": data }
        return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM )
    except Exception as jwt_exec:
        return {"error": str(jwt_exec)}

def decode_access_token(token:str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM )
    except Exception as jwt_exec:
        return {"error": str(jwt_exec)}
