from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from database import get_db
from models import Product, Category, Review
from schemas import ProductResponse, ProductDetailResponse, CategoryResponse, ReviewResponse
from routers.auth import get_current_user, User

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取分类列表"""
    query = db.query(Category).filter(Category.is_active == True)
    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)
    else:
        query = query.filter(Category.parent_id.is_(None))
    return query.order_by(Category.sort_order).all()


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    category_id: Optional[int] = None,
    keyword: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "default",  # default, price_asc, price_desc, sales
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(Product).filter(Product.is_active == True)

    # 筛选条件
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if keyword:
        query = query.filter(Product.name.contains(keyword))
    if brand:
        query = query.filter(Product.brand == brand)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # 排序
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "sales":
        query = query.order_by(Product.sales.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    # 分页
    total = query.count()
    products = query.offset((page - 1) * page_size).limit(page_size).all()

    return products


@router.get("/products/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user) if False else None
):
    """获取商品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    return ProductDetailResponse.from_orm(product)


@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取商品评价列表"""
    reviews = db.query(Review).filter(Review.product_id == product_id)\
        .order_by(Review.created_at.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    return reviews


@router.get("/hot", response_model=List[ProductResponse])
async def get_hot_products(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取热门商品"""
    products = db.query(Product)\
        .filter(Product.is_active == True, Product.is_hot == True)\
        .order_by(Product.sales.desc())\
        .limit(limit)\
        .all()
    return products


@router.get("/new", response_model=List[ProductResponse])
async def get_new_products(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取新品"""
    products = db.query(Product)\
        .filter(Product.is_active == True, Product.is_new == True)\
        .order_by(Product.created_at.desc())\
        .limit(limit)\
        .all()
    return products


@router.post("/products/{product_id}/favorite")
async def toggle_favorite(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """收藏/取消收藏商品"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    if product in current_user.favorite_products:
        current_user.favorite_products.remove(product)
        db.commit()
        return {"message": "已取消收藏", "is_favorite": False}
    else:
        current_user.favorite_products.append(product)
        db.commit()
        return {"message": "收藏成功", "is_favorite": True}


@router.get("/search/suggestions")
async def get_search_suggestions(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """获取搜索建议"""
    products = db.query(Product.name)\
        .filter(Product.name.contains(keyword), Product.is_active == True)\
        .limit(10)\
        .all()
    return {"suggestions": [p[0] for p in products]}
