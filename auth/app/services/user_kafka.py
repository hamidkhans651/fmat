from datetime import datetime, timezone
from typing import Annotated
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.config.security import hashed_password
from app.models.user import UserModel, UserTokenModel
from sqlmodel import Session, create_engine
from app.schemas import users_pb2
from app.services.email import send_verification_mail
from app.config.setting import DATABASE_URL
from google.protobuf.timestamp_pb2 import Timestamp
from uuid import UUID

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

async def kafka_consumer(topic:str, bootstrap_server:str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_server, group_id="user_group" ,auto_offset_reset="earliest")
    await consumer.start()
    try:  
        
        if topic=="user-create-topic":
            async for message in consumer:
                user_data = users_pb2.CreateUser()
                user_data.ParseFromString(message.value)
                new_user = UserModel(
                first_name=user_data.first_name, 
                last_name=user_data.last_name,
                email= user_data.email,
                password=hashed_password(user_data.password),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
                )
                with Session(engine) as session:
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)

                # Account Verification Email
                await send_verification_mail(user=new_user)
    
        if topic=="user-token-topic":
            async for message in consumer:
                user_token = users_pb2.SendUserToken()
                user_token.ParseFromString(message.value)
                
                # created_at = user_token.created_at.ToDatetime()
                new_user = UserTokenModel(
                token=user_token.token,
                user_id=UUID(user_token.user_id),
                expire_in= user_token.expire_in,
                created_at=user_token.created_at.ToDatetime(),
                expired_at=user_token.expired_at.ToDatetime()
                )
                with Session(engine) as session:
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)
                    
                # Account Verification Email
                await send_verification_mail(user=new_user)

    
    
    finally:
        await consumer.stop()

async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()