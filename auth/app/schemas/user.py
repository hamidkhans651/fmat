from pydantic import EmailStr, BaseModel

class CreateUser(BaseModel):
    first_name : str
    last_name : str
    password : str
    email : EmailStr

class SendUserToken(BaseModel):
    token_type: str = "Bearer"
    token: str
    expire_in: str
    def to_dict(self) -> dict:
        return {
            "token_type": self.token_type,
            "token": self.token,
            "expire_in": self.expire_in,
            }
