from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '3aecb40fd4211af1725f4f5e36d785dc7f68b5780c638c4c9a528fe937144e69'


class LoginModel(BaseModel):
    username: str
    password: str


class ItemModel(BaseModel):
    id: Optional[int]
    quantity: int
    item_name: str
    item_type: Optional[str] = "RAW_MATERIAL"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 1,
                "item_name": "pen",
                "item_type": "FINISHED_GOODS"
            }
        }
