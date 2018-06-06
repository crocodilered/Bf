import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean
from sqlalchemy import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(36))
    enabled = Column(Boolean)

    def __init__(self, email="", password="", enabled=True):
        Base.__init__(self)
        self.email = email
        self.password = password
        self.enabled = enabled

    @staticmethod
    def list(session):
        r = session.query(User).order_by(User.title).all()
        return r

    @staticmethod
    def get_by_email(session, email):
        r = None
        if email:
            try:
                r = session.query(User)\
                    .filter(func.lower(User.email) == func.lower(email))\
                    .one()
            except sqlalchemy.orm.exc.NoResultFound or sqlalchemy.orm.exc.MultipleResultsFound:
                pass
        return r

    @staticmethod
    def get_by_token(session, token):
        r = None
        if token:
            try:
                r = session.query(User)\
                    .filter(User.token == token)\
                    .one()
            except sqlalchemy.orm.exc.NoResultFound or sqlalchemy.orm.exc.MultipleResultsFound:
                pass
        return r
