from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# 用户商品收藏关联表
user_favorites = Table(
    'user_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(50))
    avatar = Column(String(255))
    level = Column(String(20), default="普通会员")
    points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    favorite_products = relationship("Product", secondary=user_favorites, back_populates="favorite_users")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_name = Column(String(50), nullable=False)
    receiver_phone = Column(String(20), nullable=False)
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    detail = Column(String(255), nullable=False)
    tag = Column(String(20))  # 家、公司等标签
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(50))  # emoji图标
    parent_id = Column(Integer, ForeignKey('categories.id'))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # 关系
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    stock = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    image = Column(String(255))
    images = Column(Text)  # JSON字符串存储多图
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand = Column(String(50))
    unit = Column(String(20), default="件")
    specs = Column(Text)  # JSON字符串存储规格
    detail = Column(Text)  # 商品详情HTML
    is_active = Column(Boolean, default=True)
    is_hot = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    favorite_users = relationship("User", secondary=user_favorites, back_populates="favorite_products")
    reviews = relationship("Review", back_populates="product")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    specs = Column(Text)  # JSON字符串存储选择的规格
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    freight_amount = Column(Float, default=0)
    pay_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, paid, shipped, completed, cancelled
    payment_method = Column(String(20))
    remark = Column(Text)
    paid_at = Column(DateTime(timezone=True))
    shipped_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_name = Column(String(200))
    product_image = Column(String(255))
    product_spec = Column(String(255))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    rating = Column(Integer, default=5)
    content = Column(Text)
    images = Column(Text)  # JSON字符串存储图片
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    product = relationship("Product", back_populates="reviews")


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20))  # discount, cash
    value = Column(Float, nullable=False)
    min_amount = Column(Float, default=0)
    total_count = Column(Integer)
    received_count = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
