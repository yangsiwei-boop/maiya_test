from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# 用户相关Schema
class UserBase(BaseModel):
    phone: str
    username: Optional[str] = None


class UserCreate(UserBase):
    password: str
    code: Optional[str] = None


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    level: str
    points: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# 地址相关Schema
class AddressBase(BaseModel):
    receiver_name: str
    receiver_phone: str
    province: str
    city: str
    district: str
    detail: str
    tag: Optional[str] = None
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# 商品相关Schema
class CategoryBase(BaseModel):
    name: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    stock: int = 0
    image: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    sales: int
    is_hot: bool
    is_new: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    images: Optional[List[str]] = []
    specs: Optional[dict] = {}
    detail: Optional[str] = None
    category: Optional[CategoryResponse] = None


# 购物车相关Schema
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    specs: Optional[dict] = None


class CartItemCreate(CartItemBase):
    pass


class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True


# 订单相关Schema
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    specs: Optional[dict] = None


class OrderCreate(BaseModel):
    address_id: int
    items: List[OrderItemBase]
    payment_method: str
    remark: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    product_image: Optional[str] = None
    product_spec: Optional[str] = None
    price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    order_number: str
    total_amount: float
    discount_amount: float
    freight_amount: float
    pay_amount: float
    status: str
    payment_method: str
    items: List[OrderItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


# 评价相关Schema
class ReviewBase(BaseModel):
    product_id: int
    rating: int = 5
    content: str


class ReviewCreate(ReviewBase):
    order_id: Optional[int] = None


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# 分页响应Schema
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int
