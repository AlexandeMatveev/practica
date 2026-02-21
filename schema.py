from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    name: str
    age: int




class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True