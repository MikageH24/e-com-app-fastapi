from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Date
from sqlalchemy.orm import relationship
from app.models import *
from datetime import datetime


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    comment = Column(String)
    comment_date = Column(Date, default=datetime.now())
    is_active = Column(Boolean, default=True)