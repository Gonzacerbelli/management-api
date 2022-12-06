from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    document = Column(Integer, nullable=False)
    phone = Column(Integer, nullable=False)
    address = Column(String)
    city = Column(String)
    birthday = Column(Date, nullable=False)
    sex = Column(String, nullable=False)


class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(
    engine, Base.metadata.tables.values(), checkfirst=True)
