from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
from app.config.setting import USER_CONTEXT

class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    first_name : str
    last_name : str
    password : str
    email : str = Field(unique=True, index=True)
    is_verified : bool = Field(False, nullable=True )
    verified_at : Optional[datetime] = Field(None, nullable=True, )
    updated_at : Optional[datetime] = Field(None, nullable=True )
    created_at : datetime = Field(default_factory=datetime.utcnow, nullable=False )
    tokens: Optional[List["UserTokenModel"]] = Relationship(back_populates="user")
    
    def get_context_str(self):
        return f"{USER_CONTEXT}{self.password[-6:]}{self.updated_at.strftime("%Y%m%d%H%M%S")}"

class UserTokenModel(SQLModel, table=True):
    __tablename__ = "user_token"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: Optional[UUID] = Field(None, foreign_key="users.id")
    token: str
    created_at : datetime = Field(default_factory=datetime.utcnow, nullable=False )
    expired_at : datetime = Field(nullable=False) 
    user: "UserModel" = Relationship(back_populates="tokens")