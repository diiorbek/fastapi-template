from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str

class UserOut(UserCreate):
    id: int

    class Config:
        model_config = {
    "from_attributes": True
}
