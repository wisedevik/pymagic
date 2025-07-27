from sqlalchemy import Column, Integer, String
from . import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pass_token = Column(String, unique=True, nullable=False)
