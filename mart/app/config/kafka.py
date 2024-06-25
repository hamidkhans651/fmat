from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlmodel import Session, select
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app import mart_pb2
from app.schema import OrderPlace, Product, UpdateProduct
from app import setting

connection_str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)


async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def kafka_consumer(topic:str, bootstrap_server:str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_server, group_id="mart_group" ,auto_offset_reset="earliest")
    await consumer.start()
    try:  
        
        if topic=="mart-product-topic":
            async for message in consumer:
                new_product = mart_pb2.Product()
                new_product.ParseFromString(message.value)
                product_data = {
                "id": UUID(new_product.id),
                "name": new_product.name,
                "category": new_product.category,
                "price": new_product.price,
                "quantity": new_product.quantity
                }
                product_instance = Product(**product_data)
                with Session(engine) as session:               
                    session.add(product_instance)
                    session.commit()

        elif topic=="mart-order-topic":
            async for message in consumer:
                new_order = mart_pb2.Order()
                new_order.ParseFromString(message.value)
                order_data = { 
                    "product_id":UUID(new_order.product_id), 
                    "order_id":UUID(new_order.order_id), 
                    "product_name": new_order.product_name, 
                    "product_category": new_order.product_category, 
                    "quantity":new_order.quantity, 
                    "product_price": new_order.product_price, 
                    "totle_price": new_order.totle_price}    

                # Initialize the Product instance using the extracted id
                Order_instance = OrderPlace(**order_data) 
                with Session(engine) as session:   
                    session.add(Order_instance)
                    session.commit()

        elif topic=="mart-product-decrease-topic":
            async for message in consumer:
                new_order = mart_pb2.Order()
                new_order.ParseFromString(message.value)
                order_data = { 
                    "product_id":UUID(new_order.product_id), 
                    "order_id":UUID(new_order.order_id), 
                    "product_name": new_order.product_name, 
                    "product_category": new_order.product_category, 
                    "quantity":new_order.quantity, 
                    "product_price": new_order.product_price, 
                    "totle_price": new_order.totle_price}
                product_instance = OrderPlace(**order_data) 
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==product_instance.product_id)).first() #get(Product, product_instance.product_id)
                    product.quantity -= product_instance.quantity 
                    session.add(product)
                    session.commit()

        elif topic=="mart-update-product-topic":
            async for message in consumer:
                new_product = mart_pb2.UpdateProduct()
                new_product.ParseFromString(message.value)
                id=UUID(new_product.id)

                updated_product = {
                "name": new_product.name ,
                "category": new_product.category ,
                "price": new_product.price ,
                "quantity": new_product.quantity }

                product_instance = UpdateProduct(**updated_product)  # change datatype dict to SQLModel 
                with Session(engine) as session:
                    product = session.get(Product, id) #exec(select(Product).where(Product.id==id)).first()
                    product.name = product_instance.name if product_instance.name else product.name
                    product.price = product_instance.price if product_instance.price else product.price
                    product.quantity = product_instance.quantity if product_instance.quantity else product.quantity
                    product.category = product_instance.category if product_instance.category else product.category
                    session.add(product)
                    session.commit()
                #     # final_updated_product = product_instance.model_dump(exclude_unset=True)   # filter the data, removing None value
                #     # product.sqlmodel_update(final_updated_product)

        elif topic=="mart-product-increase-topic":
            async for message in consumer:
                new_inc_product = mart_pb2.IncrementProductItem()
                new_inc_product.ParseFromString(message.value)
                id = UUID(new_inc_product.id)
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==id)).first()
                    product.quantity += new_inc_product.add_product
                    session.add(product)
                    session.commit()
        
        else:
            raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found ",)

    finally:
        await consumer.stop()

