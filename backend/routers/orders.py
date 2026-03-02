from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import random
from database import get_db
from models import Order, OrderItem, CartItem, Product
from schemas import OrderCreate, OrderResponse, OrderItemResponse
from routers.auth import get_current_user, User

router = APIRouter()


def generate_order_number():
    """生成订单号"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"{timestamp}{random_num}"


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建订单"""
    # 计算订单金额
    total_amount = 0
    order_items_data = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品ID {item.product_id} 不存在")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"商品 {product.name} 库存不足")

        item_total = product.price * item.quantity
        total_amount += item_total

        order_items_data.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price,
            "subtotal": item_total,
            "specs": item.specs
        })

    # 运费计算（简单示例：满99包邮）
    freight_amount = 0 if total_amount >= 99 else 10
    discount_amount = 0  # 可以根据优惠券等计算

    # 创建订单
    order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        address_id=order_data.address_id,
        total_amount=total_amount,
        discount_amount=discount_amount,
        freight_amount=freight_amount,
        pay_amount=total_amount + freight_amount - discount_amount,
        payment_method=order_data.payment_method,
        remark=order_data.remark,
        status="pending"
    )

    db.add(order)
    db.flush()  # 获取订单ID

    # 创建订单明细
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product"].id,
            product_name=item_data["product"].name,
            product_image=item_data["product"].image,
            product_spec=str(item_data["specs"]) if item_data["specs"] else "",
            price=item_data["price"],
            quantity=item_data["quantity"],
            subtotal=item_data["subtotal"]
        )
        db.add(order_item)

        # 减少库存
        item_data["product"].stock -= item_data["quantity"]
        item_data["product"].sales += item_data["quantity"]

    # 清除购物车中已购买的商品
    db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id.in_([item.product_id for item in order_data.items])
    ).delete(synchronize_session=False)

    db.commit()
    db.refresh(order)

    return OrderResponse.from_orm(order)


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status: str = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取订单列表"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取订单详情"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    return OrderResponse.from_orm(order)


@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消订单"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="该订单状态不允许取消")

    # 恢复库存
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
            product.sales -= item.quantity

    order.status = "cancelled"
    db.commit()

    return {"message": "订单已取消"}


@router.put("/{order_id}/pay")
async def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """支付订单"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="该订单状态不允许支付")

    order.status = "paid"
    order.paid_at = datetime.now()
    db.commit()

    return {"message": "订单支付成功"}


@router.put("/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """确认收货"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "shipped":
        raise HTTPException(status_code=400, detail="该订单状态不允许确认收货")

    order.status = "completed"
    order.completed_at = datetime.now()

    # 增加用户积分（简单规则：订单金额的1%）
    current_user.points += int(order.pay_amount)

    db.commit()

    return {"message": "确认收货成功"}
