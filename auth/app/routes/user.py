from aiokafka import AIOKafkaProducer
from app.models.user import UserModel, UserTokenModel
from fastapi import APIRouter, Depends, status
from app.schemas.user import CreateUser, SendUserToken
from app.config.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from app.services.user import create_user, verify_user_account as verify_account, user_login
from app.config.security import oauth2_scheme
from app.services.user_kafka import get_producer

router : APIRouter = APIRouter(prefix="/auth",tags=["User Auth"], responses={404:{"description": "Not found"}})

@router.post("/signup")
async def create_user_account(data: CreateUser, session:Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_producer) ]):
    user = await create_user(data, session, producer)
    return user

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=SendUserToken)
async def user_login_req(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], session:Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_producer) ] ):
    user = await user_login(form_data, session, producer)
    return user

@router.post("/account-verify")
async def verify_user_account(token: str, email: str, session:Annotated[Session, Depends(get_session)] ):
    user = await verify_account(token, email, session)
    return user

@router.get("/users")
async def get_user_accounts(token: Annotated[str, Depends(oauth2_scheme)], session:Annotated[Session, Depends(get_session)],  ):
    users = session.exec(select(UserModel)).all()
    return users

@router.get("/tokens")
async def get_user_tokens(token: Annotated[str, Depends(oauth2_scheme)], session:Annotated[Session, Depends(get_session)],  ):
    tokens = session.exec(select(UserTokenModel)).all()
    return tokens
