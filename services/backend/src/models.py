import uuid

import sqlalchemy
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
metadata = sqlalchemy.MetaData()


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    count_likes = Column(Integer, nullable=False)
    user = relationship('User')



class Like(Base):
    __tablename__ = 'likes'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    post = relationship('Post')