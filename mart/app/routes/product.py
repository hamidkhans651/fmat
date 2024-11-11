from uuid import UUID
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from app import mart_pb2
from app.config.kafka import get_producer
from app.schema import Product, ProductReq, UpdateProduct
from app.config.database import get_session

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")

router : APIRouter = APIRouter(prefix="/product",tags=["Products"], responses={404:{"description": "Not found"}})

@router.post("/add-product") 
async def add_product(product: ProductReq, producer: Annotated[Session, Depends(get_producer) ], token: Annotated[dict, Depends(oauth2_scheme) ] ):
    if product.category not in categories:""
    raise HTTPException(status_code=402, detail="Add a specific keyword")
    ready_product = Product(name=product.name, price=product.price, category=product.category, quantity=product.quantity)
    
    # SQLModel to protobuf
    product_protobuf = mart_pb2.Product(id=str(ready_product.id), name= ready_product.name, price=ready_product.price, category= ready_product.category, quantity= ready_product.quantity)
    serialized_product = product_protobuf.SerializeToString()
    
    # Kafka
    await producer.send_and_wait("mart-product-topic", serialized_product) 
    return ready_product
 

@router.get("/get-all-products", response_model=list[Product])
def all_products(session: Annotated[Session, Depends(get_session) ] ):
    products = session.exec(select(Product)).all()
    return products


@router.get("/get-products-by-cotegory/${product_category}", response_model=list[Product])
def products_by_category(product_category: str, session: Annotated[Session, Depends(get_session) ]):
    if product_category not in categories:
        raise HTTPException(status_code=402, detail="write a valiad keyword")
    products = session.exec(select(Product).where(Product.category==product_category)).all()
    return products

@router.get("/get-product/${product_id}", response_model=Product)
def get_product(product_id: UUID, session: Annotated[Session, Depends(get_session) ] ):
    product = session.exec(select(Product).where(Product.id==product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@router.patch("/update_product/${product_id}")
async def update_product(product_id: UUID, product: UpdateProduct, session: Annotated[Session, Depends(get_session) ], producer: Annotated[Session, Depends(get_producer) ] , token: Annotated[dict, Depends(oauth2_scheme) ] ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    updated_product = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(updated_product)
    if db_product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")

    # SQLModel datatype to product
    protobuf_product = mart_pb2.UpdateProduct(
        id=str(db_product.id),
        name=product.name if product.name else None,
        category=product.category if product.category else None,
        price=product.price if product.price else None,
        quantity=product.quantity if product.quantity else None
    )
    serialized_product = protobuf_product.SerializeToString()

    # kafka
    await producer.send_and_wait("mart-update-product-topic", serialized_product)
    return db_product


@router.patch("/increment_product_item/${product_id}", response_model=Product)
async def update_product_item(product_id: UUID, add_item: int, session: Annotated[Session, Depends(get_session) ], producer: Annotated[Session, Depends(get_producer) ], token: Annotated[dict, Depends(oauth2_scheme) ] ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    db_product.quantity += int(add_item)

    # SQLModel to protobuf
    add_product_protobuf = mart_pb2.IncrementProductItem(id=str(db_product.id), add_product=add_item)
    serialized_product = add_product_protobuf.SerializeToString()
    # Kafka
    await producer.send_and_wait("mart-product-increase-topic", serialized_product)
    return db_product

