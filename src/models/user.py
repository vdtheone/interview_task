from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime
from src.database import db
from src.utils.get_uuid import generate_uuid


class User(db.Model):
    __table_name__ = 'users'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())