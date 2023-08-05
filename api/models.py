from database import Base
from typing import List
from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_table"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    mail = Column("mail", String)
    age = Column("age", Integer)
    bucket: Mapped[List["Bucket"]] = relationship(back_populates="user")


class Bucket(Base):
    __tablename__ = "bucket_table"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("first_name", String)
    is_private = Column("is_private", Boolean)
    created_at = Column("created_at", DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="bucket")
    chat_history: Mapped[List["ChatHistory"]] = relationship(back_populates="bucket")


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    created_at = Column("created_at", DateTime)
    query = Column("query", String)
    text = Column("text", Float)
    bucket_id: Mapped[int] = mapped_column(ForeignKey("bucket_table.id"))
    bucket: Mapped["Bucket"] = relationship(back_populates="chat_history")
