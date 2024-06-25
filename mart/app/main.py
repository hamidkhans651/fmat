from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.config.database import lifespan
from fastapi import Depends, FastAPI
from app.routes.order import router as order_router
from app.routes.product import router as product_router

app: FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")


@app.get("/")
def root(token: Annotated[dict, Depends(oauth2_scheme) ]):
    return {"Message":"Mart API Sourcecode", "token":token}

app.include_router(product_router)
app.include_router(order_router)

