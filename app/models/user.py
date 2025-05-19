from sqlalchemy import Column, Integer, String
from app.database.base_class import Base
from app.utils.generate_uuid import generate_uuid


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=generate_uuid(), index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)
