from pydantic import BaseModel
from datetime import date


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class CreateReview(BaseModel):
    comment: str
    comment_date: date


class CreateRating(BaseModel):
    grade: float
