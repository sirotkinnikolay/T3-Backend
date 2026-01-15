from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TEXT, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "postgresql://postgres:postgres@db:5432/order_service"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(10, 2), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class CategoryHierarchy(Base):
    __tablename__ = "category_hierarchy"

    parent_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    child_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    depth = Column(Integer, nullable=False)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(TEXT)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    order_date = Column(TIMESTAMP, nullable=False, server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
