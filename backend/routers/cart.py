from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import CartItem, Product
from schemas import CartItemResponse, CartItemCreate
from routers.auth import get_current_user, User

router = APIRouter()


@router.get("/", response_model=List[CartItemResponse])
async def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取购物车列表"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return cart_items


@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加商品到购物车"""
    # 检查商品是否存在
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    if product.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="库存不足")

    # 检查购物车中是否已存在该商品
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return CartItemResponse.from_orm(existing_item)
    else:
        new_item = CartItem(
            user_id=current_user.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            specs=str(item_data.specs) if item_data.specs else None
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return CartItemResponse.from_orm(new_item)


@router.put("/{item_id}")
async def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新购物车商品数量"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车商品不存在")

    if quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return {"message": "商品已从购物车移除"}
    else:
        # 检查库存
        if cart_item.product.stock < quantity:
            raise HTTPException(status_code=400, detail="库存不足")
        cart_item.quantity = quantity
        db.commit()
        return {"message": "数量更新成功"}


@router.delete("/{item_id}")
async def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除购物车商品"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车商品不存在")

    db.delete(cart_item)
    db.commit()
    return {"message": "商品已从购物车移除"}


@router.delete("/")
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """清空购物车"""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "购物车已清空"}
