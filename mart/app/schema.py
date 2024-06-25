from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional, Dict

class BaseProduct(SQLModel):
    name: str
    category: str = Field(default='food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: int
    quantity : int

class Product(BaseProduct, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "id": str(self.id)
        }

class UpdateProduct(SQLModel):
    name: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)#'food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: Optional[int] = Field(default=None)
    quantity : Optional[int] = Field(default=None)
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity
        }

class ProductReq(BaseProduct):
    pass

class Order(SQLModel):
    product_id: UUID
    quantity: int

class OrderPlace(Order, table=True):
    order_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)    
    product_price: int
    product_name: str
    product_category: str
    totle_price: int

    def to_dict(self) -> Dict:
        return {
            "product_id": str(self.product_id),
            "quantity": self.quantity,
            "product_price": self.product_price,
            "product_name": self.product_name,
            "product_category": self.product_category,
            "totle_price": self.totle_price,
            "order_id": str(self.order_id)
        }
