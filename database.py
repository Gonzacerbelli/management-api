from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey
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
    client_id = Column(ForeignKey("clients.id"), nullable=False)
    date = Column(DateTime, nullable=False)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) #tipo facial, corporal
    category = Column(String, nullable=False) #categoria locion, crema, serum, mascara
    laboratory = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    unit = Column(String, nullable=False) #unidad de medida gramos, cm3
    price = Column(Float, nullable=False)
    stock = Column(Boolean, nullable=False)
    image_url = Column(String, nullable=False)


Base.metadata.create_all(
    engine, Base.metadata.tables.values(), checkfirst=True)
