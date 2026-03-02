from database import SessionLocal, Base, engine
from models import User, Category, Product, Address
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_database():
    """初始化数据库数据"""
    db = SessionLocal()

    try:
        # 创建分类
        categories = [
            Category(name="手机", icon="📱", sort_order=1),
            Category(name="电脑", icon="💻", sort_order=2),
            Category(name="电视", icon="📺", sort_order=3),
            Category(name="耳机", icon="🎧", sort_order=4),
            Category(name="服装", icon="👕", sort_order=5),
            Category(name="鞋靴", icon="👟", sort_order=6),
            Category(name="美妆", icon="💄", sort_order=7),
            Category(name="食品", icon="🍎", sort_order=8),
        ]
        db.add_all(categories)
        db.flush()

        # 创建商品
        products = [
            Product(
                name="iPhone 15 Pro Max",
                description="A17 Pro芯片 | 钛金属机身 | 4800万像素相机系统",
                price=9999,
                original_price=10999,
                stock=999,
                sales=5000,
                image="📱",
                category_id=categories[0].id,
                brand="Apple",
                is_hot=True,
                specs='{"colors": ["原色钛金属", "蓝色钛金属", "白色钛金属", "黑色钛金属"], "storage": ["256GB", "512GB", "1TB"]}'
            ),
            Product(
                name="华为 Mate 60 Pro",
                description="卫星通信 鸿蒙系统",
                price=6999,
                original_price=7999,
                stock=500,
                sales=8000,
                image="📱",
                category_id=categories[0].id,
                brand="华为",
                is_hot=True,
                is_new=True
            ),
            Product(
                name="小米14 Ultra",
                description="徕卡影像 骁龙8Gen3",
                price=5999,
                stock=300,
                sales=3000,
                image="📱",
                category_id=categories[0].id,
                brand="小米",
                is_new=True
            ),
            Product(
                name="OPPO Find X7 Pro",
                description="哈苏影像 超级闪充",
                price=5499,
                stock=200,
                sales=2000,
                image="📱",
                category_id=categories[0].id,
                brand="OPPO"
            ),
            Product(
                name="vivo X100 Pro",
                description="蔡司影像 蓝海电池",
                price=4999,
                original_price=5999,
                stock=250,
                sales=2500,
                image="📱",
                category_id=categories[0].id,
                brand="vivo"
            ),
            Product(
                name="三星 Galaxy S24 Ultra",
                description="AI功能 S Pen",
                price=8999,
                stock=150,
                sales=1500,
                image="📱",
                category_id=categories[0].id,
                brand="三星"
            ),
            Product(
                name="一加 12",
                description="哈苏影像 超薄屏下",
                price=4299,
                stock=400,
                sales=4000,
                image="📱",
                category_id=categories[0].id,
                brand="一加",
                is_hot=True
            ),
            Product(
                name="realme GT5 Pro",
                description="旗舰性能 性价比之选",
                price=3299,
                stock=500,
                sales=6000,
                image="📱",
                category_id=categories[0].id,
                brand="realme"
            ),
            Product(
                name="MacBook Pro 14英寸",
                description="M3芯片 专业级性能",
                price=14999,
                stock=100,
                sales=1000,
                image="💻",
                category_id=categories[1].id,
                brand="Apple"
            ),
            Product(
                name="联想拯救者 Y9000P",
                description="电竞游戏本 RTX4060",
                price=8999,
                stock=200,
                sales=1500,
                image="💻",
                category_id=categories[1].id,
                brand="联想"
            ),
            Product(
                name="AirPods Pro 2",
                description="主动降噪 空间音频",
                price=1899,
                stock=500,
                sales=8000,
                image="🎧",
                category_id=categories[3].id,
                brand="Apple",
                is_hot=True
            ),
            Product(
                name="Sony WH-1000XM5",
                description="顶级降噪 30小时续航",
                price=2499,
                stock=150,
                sales=2000,
                image="🎧",
                category_id=categories[3].id,
                brand="Sony"
            ),
            Product(
                name="Magic Keyboard",
                description="中文输入 带数字小键盘",
                price=1299,
                stock=300,
                sales=1200,
                image="⌨️",
                category_id=categories[1].id,
                brand="Apple"
            ),
            Product(
                name="Apple Watch Series 9",
                description="健康监测 运动追踪",
                price=3199,
                stock=200,
                sales=1800,
                image="⌚",
                category_id=categories[0].id,
                brand="Apple"
            ),
            Product(
                name="Sony Bravia 65英寸",
                description="4K HDR 智能电视",
                price=6999,
                stock=80,
                sales=500,
                image="📺",
                category_id=categories[2].id,
                brand="Sony"
            ),
            Product(
                name="小米电视 75英寸",
                description="4K 超高清 智能语音",
                price=3999,
                stock=200,
                sales=3000,
                image="📺",
                category_id=categories[2].id,
                brand="小米"
            ),
        ]
        db.add_all(products)

        # 创建测试用户
        test_user = User(
            phone="13800138000",
            password_hash=pwd_context.hash("123456"),
            username="测试用户",
            level="黄金会员",
            points=1280
        )
        db.add(test_user)
        db.flush()

        # 创建测试地址
        address = Address(
            user_id=test_user.id,
            receiver_name="张三",
            receiver_phone="13800138000",
            province="北京市",
            city="朝阳区",
            district="建国路",
            detail="SOHO现代城 A座 1001室",
            tag="家",
            is_default=True
        )
        db.add(address)

        db.commit()
        print("数据库初始化成功！")
        print("测试账号: 13800138000 / 123456")

    except Exception as e:
        print(f"初始化失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    # 初始化数据
    init_database()
