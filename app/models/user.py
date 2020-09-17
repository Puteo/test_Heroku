from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import asc
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin

from app.models.base import Base
from app.models.base import session_scope
from app.models.base import Session
from app.controllers.utils import GetHashValue

class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(Text)
    password = Column(Text)

    @classmethod
    def create(cls, user_name, password):
        user = cls(user_name=user_name,password=GetHashValue(password))
        try:
            with session_scope() as session:
                session.add(user)
            return user
        except IntegrityError:
            return False
            
    @classmethod
    def DeleteAllRecord(cls):
        with session_scope() as session:
            users = session.query(cls).all()
            for user in users:
                session.delete(user)

    @classmethod
    def get(cls, user_name):
        with session_scope() as session:
            user = session.query(cls).filter(
                cls.user_name == user_name).first()
        if user is None:
            return None
        return user

    def save(self):
        with session_scope() as session:
            session.add(self)

    @classmethod
    def get_user_one_or_none(cls, user_id):
        with session_scope() as session:
            user = session.query(cls).filter(
                cls.user_id == user_id).one_or_none()
        return user

    @classmethod
    def get_all_users(cls, limit=100):
        with session_scope() as session:
            users = session.query(cls).order_by(
                asc(cls.user_id)).limit(limit).all()

        if len(users) == 0:
            return None

        return users
    
    @property
    def value(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'password': self.password,
        }

class LoginUser(UserMixin, User):
    def get_id(self):
        return self.user_id
    
    @classmethod
    def get_user_one_by_name(cls, user_name):
        with session_scope() as session:
            user = session.query(cls).filter(
                cls.user_name == user_name).one_or_none()
        return user