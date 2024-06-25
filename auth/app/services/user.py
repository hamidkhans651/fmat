from app.services.email import send_activation_confirmation_mail, send_verification_mail
from fastapi import HTTPException, status, Depends
from app.schemas.user import CreateUser, SendUserToken
from app.schemas import users_pb2
from sqlmodel import Session, select
from app.models.user import UserModel, UserTokenModel
from datetime import datetime, timezone, timedelta
from app.config.security import hashed_password, verify_hashed_password, create_access_token, oauth2_scheme
from app.config.validation import validate_password
from app.config.setting import ACCESS_TOKEN_EXPIRE_MINUTES as EXP_MIN
from app.services.user_kafka import get_producer
from typing import Annotated
from aiokafka import AIOKafkaProducer

async def create_user(data:CreateUser, session:Session, producer: AIOKafkaProducer):
    user_exist = session.exec(select(UserModel).where(UserModel.email==data.email)).first()
    if user_exist:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user email '{data.email}' is already exist")
    # check password validation
    validate_password(data.password)
    user_protobuf = users_pb2.CreateUser(first_name=data.first_name, last_name=data.last_name, password=data.password, email=data.email)
    serialized_user = user_protobuf.SerializeToString()
    await producer.send_and_wait("user-create-topic", serialized_user)
    return {"Notify": f"Email has been sent to {data.email}, please check your check you email inbox or maybe inside the spam to verify account"}
    

async def verify_user_account(token: str, email: str, session: Session):
    user: UserModel = session.exec(select(UserModel).where(UserModel.email==email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"This email is not a valid")
    get_context_str = user.get_context_str()
    
    if not verify_hashed_password(get_context_str, token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Eigther this url is expired or not a valid")
    user.is_verified = True
    user.verified_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_activation_confirmation_mail(user)
    return {"Notify": f"Congratulation! you have successfully registered"}
    

async def user_login(form_data, session: Session, producer: AIOKafkaProducer):
    user = session.exec(select(UserModel).where(UserModel.email==form_data.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This email is not register")    
    if not verify_hashed_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"eigther this url is expired or not a valid")
    if not user.is_verified:
        # send mail
        await send_verification_mail(user=user)  
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"This user is not verified, we have sent you an email, please check you mail inbox or maybe inside spam and then follow the instruction")
    # send token
    token = create_access_token({"id": str(user.id), "email": user.email })
    user_token = UserTokenModel(
        created_at=datetime.now(timezone.utc),expired_at=datetime.now(timezone.utc) + timedelta(minutes=int(EXP_MIN)), token=token, user_id=user.id)
    session.add(user_token)
    session.commit()
    session.refresh(user_token)
    ready_token = SendUserToken(token=token, expire_in=str(EXP_MIN), token_type="Bearer")
    return ready_token