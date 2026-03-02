from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Address, Order
from schemas import AddressResponse, AddressCreate
from routers.auth import get_current_user

router = APIRouter()


@router.get("/addresses", response_model=List[AddressResponse])
async def get_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取地址列表"""
    addresses = db.query(Address).filter(Address.user_id == current_user.id)\
        .order_by(Address.is_default.desc(), Address.created_at.desc())\
        .all()
    return addresses


@router.post("/addresses", response_model=AddressResponse)
async def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加地址"""
    # 如果设置为默认地址，取消其他默认地址
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.is_default == True
        ).update({"is_default": False})

    new_address = Address(
        user_id=current_user.id,
        **address_data.dict()
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return AddressResponse.from_orm(new_address)


@router.put("/addresses/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新地址"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")

    # 如果设置为默认地址，取消其他默认地址
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.id != address_id,
            Address.is_default == True
        ).update({"is_default": False})

    for key, value in address_data.dict().items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return AddressResponse.from_orm(address)


@router.delete("/addresses/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除地址"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")

    db.delete(address)
    db.commit()

    return {"message": "地址已删除"}


@router.get("/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户统计信息"""
    # 订单统计
    total_orders = db.query(Order).filter(Order.user_id == current_user.id).count()
    pending_orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == "pending"
    ).count()
    shipped_orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == "shipped"
    ).count()
    completed_orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == "completed"
    ).count()

    # 收藏商品数量
    favorite_count = len(current_user.favorite_products)

    # 优惠券数量（可以后续添加）
    coupon_count = 0

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "completed_orders": completed_orders,
        "favorite_count": favorite_count,
        "coupon_count": coupon_count,
        "points": current_user.points,
        "level": current_user.level
    }
