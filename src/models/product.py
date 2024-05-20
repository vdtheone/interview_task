from datetime import datetime
from sqlalchemy import Boolean, Column, Float, ForeignKey, String, DateTime
from src.models.user import User
from src.database import db
from src.utils.get_uuid import generate_uuid


class Product(db.Model):
    __table_name__ = 'products'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey(User.id))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    