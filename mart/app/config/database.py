from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.config.kafka import kafka_consumer
from app import setting
import asyncio

connection_str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating table")
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("mart-order-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-decrease-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-increase-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-update-product-topic", "broker:19092"))
    print("table created")
    yield

