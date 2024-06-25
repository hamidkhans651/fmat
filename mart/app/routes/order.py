from uuid import UUID
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from app import mart_pb2
from app.config.kafka import get_producer
from app.schema import OrderPlace, Product, Order
from app.config.database import get_session

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")

router : APIRouter = APIRouter(prefix="/order", tags=["Order"], responses={404:{"description": "Not found"}})


@router.post("/order-place/")
async def order_place(order:Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[Session, Depends(get_producer) ], token: Annotated[dict, Depends(oauth2_scheme)]):
    product: Product | None = session.exec(select(Product).where(Product.id==order.product_id)).first()
    if not product:
        raise HTTPException(status_code=402, detail="product does not exist")
    if product.quantity < int(order.quantity):
        raise HTTPException(status_code=402, detail=f"Sorry, we have only {product.quantity} item of {product.name}")
    new_order = OrderPlace(product_id=order.product_id, quantity=order.quantity, product_price=product.price, product_name=product.name, product_category=product.category, totle_price=(product.price * order.quantity) )
    
    # SQLModel to protobuf
    order_protobuf = mart_pb2.Order(product_id=str(new_order.product_id), order_id=str(new_order.order_id), product_name= new_order.product_name, product_category= new_order.product_category, quantity=new_order.quantity, product_price= new_order.product_price, totle_price= new_order.totle_price)
    serialized_order = order_protobuf.SerializeToString()
    

    # Kafka
    await producer.send_and_wait("mart-order-topic", serialized_order) 
    await producer.send_and_wait("mart-product-decrease-topic", serialized_order)
    return new_order

@router.get("/get_orders", response_model=list[OrderPlace])
def get_orders( session: Annotated[Session, Depends(get_session)]):
    orders = session.exec(select(OrderPlace)).all()
    return orders

