-- 购物中心MySQL数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS shopping_mall DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE shopping_mall;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    level VARCHAR(20) DEFAULT '普通会员' COMMENT '会员等级',
    points INT DEFAULT 0 COMMENT '积分',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_phone (phone),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 分类表
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    icon VARCHAR(100) DEFAULT NULL COMMENT '图标',
    parent_id INT DEFAULT NULL COMMENT '父分类ID',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- 商品表
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '商品名称',
    description TEXT COMMENT '商品描述',
    price DECIMAL(10, 2) NOT NULL COMMENT '价格',
    original_price DECIMAL(10, 2) DEFAULT NULL COMMENT '原价',
    brand VARCHAR(50) DEFAULT NULL COMMENT '品牌',
    stock INT DEFAULT 0 COMMENT '库存',
    sales INT DEFAULT 0 COMMENT '销量',
    image VARCHAR(255) DEFAULT NULL COMMENT '主图',
    images JSON DEFAULT NULL COMMENT '图片列表',
    category_id INT NOT NULL COMMENT '分类ID',
    is_hot BOOLEAN DEFAULT FALSE COMMENT '是否热销',
    is_new BOOLEAN DEFAULT FALSE COMMENT '是否新品',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_brand (brand),
    INDEX idx_is_hot (is_hot),
    INDEX idx_is_new (is_new),
    FULLTEXT idx_name_description (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- 商品SKU表
CREATE TABLE IF NOT EXISTS product_skus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL COMMENT '商品ID',
    sku_name VARCHAR(100) NOT NULL COMMENT 'SKU名称',
    price DECIMAL(10, 2) NOT NULL COMMENT 'SKU价格',
    stock INT DEFAULT 0 COMMENT 'SKU库存',
    specs JSON DEFAULT NULL COMMENT '规格属性',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品SKU表';

-- 收藏表（用户-商品多对多）
CREATE TABLE IF NOT EXISTS user_favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    product_id INT NOT NULL COMMENT '商品ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- 购物车表
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    product_id INT NOT NULL COMMENT '商品ID',
    quantity INT NOT NULL DEFAULT 1 COMMENT '数量',
    specs VARCHAR(255) DEFAULT NULL COMMENT '规格',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='购物车表';

-- 收货地址表
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    receiver_name VARCHAR(50) NOT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) NOT NULL COMMENT '手机号',
    province VARCHAR(50) NOT NULL COMMENT '省份',
    city VARCHAR(50) NOT NULL COMMENT '城市',
    district VARCHAR(50) NOT NULL COMMENT '区县',
    detail VARCHAR(255) NOT NULL COMMENT '详细地址',
    tag VARCHAR(10) DEFAULT NULL COMMENT '标签(家/公司/学校)',
    is_default BOOLEAN DEFAULT FALSE COMMENT '是否默认',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收货地址表';

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号',
    user_id INT NOT NULL COMMENT '用户ID',
    address_id INT NOT NULL COMMENT '地址ID',
    total_amount DECIMAL(10, 2) NOT NULL COMMENT '总金额',
    discount_amount DECIMAL(10, 2) DEFAULT 0 COMMENT '优惠金额',
    pay_amount DECIMAL(10, 2) NOT NULL COMMENT '实付金额',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '订单状态',
    payment_method VARCHAR(20) DEFAULT NULL COMMENT '支付方式',
    payment_time TIMESTAMP DEFAULT NULL COMMENT '支付时间',
    shipment_time TIMESTAMP DEFAULT NULL COMMENT '发货时间',
    receipt_time TIMESTAMP DEFAULT NULL COMMENT '收货时间',
    remark VARCHAR(255) DEFAULT NULL COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (address_id) REFERENCES addresses(id),
    INDEX idx_user_id (user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- 订单商品表
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL COMMENT '订单ID',
    product_id INT NOT NULL COMMENT '商品ID',
    product_name VARCHAR(200) NOT NULL COMMENT '商品名称',
    product_image VARCHAR(255) DEFAULT NULL COMMENT '商品图片',
    price DECIMAL(10, 2) NOT NULL COMMENT '单价',
    quantity INT NOT NULL COMMENT '数量',
    subtotal DECIMAL(10, 2) NOT NULL COMMENT '小计',
    specs VARCHAR(255) DEFAULT NULL COMMENT '规格',
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单商品表';

-- 评价表
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL COMMENT '商品ID',
    user_id INT NOT NULL COMMENT '用户ID',
    order_id INT DEFAULT NULL COMMENT '订单ID',
    rating INT NOT NULL COMMENT '评分1-5',
    content TEXT COMMENT '评价内容',
    images JSON DEFAULT NULL COMMENT '评价图片',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评价表';

-- 插入初始分类数据
INSERT INTO categories (name, icon, sort_order) VALUES
('手机', '📱', 1),
('电脑', '💻', 2),
('电视', '📺', 3),
('耳机', '🎧', 4),
('相机', '📷', 5),
('智能手表', '⌚', 6),
('平板', '📱', 7),
('配件', '🔌', 8);

-- 插入测试用户
INSERT INTO users (phone, password_hash, username, level, points) VALUES
('13800138000', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aqxkO8tLYGuK', '张三', '黄金会员', 1280),
('13800138001', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aqxkO8tLYGuK', '李四', '普通会员', 500);

-- 插入测试商品
INSERT INTO products (name, description, price, original_price, brand, stock, sales, image, category_id, is_hot, is_new) VALUES
('iPhone 15 Pro Max 256GB', '苹果最新旗舰手机，搭载A17 Pro芯片', 9999.00, 10999.00, 'Apple', 100, 520, '📱', 1, TRUE, TRUE),
('小米14 Pro', '徕卡光学镜头，骁龙8 Gen3', 4999.00, 5499.00, '小米', 200, 320, '📱', 1, TRUE, FALSE),
('MacBook Pro 14英寸', 'M3 Pro芯片，专业级性能', 14999.00, 16999.00, 'Apple', 50, 180, '💻', 2, TRUE, FALSE),
('ThinkPad X1 Carbon', '轻薄商务本，i7处理器', 12999.00, 14999.00, '联想', 80, 120, '💻', 2, FALSE, FALSE),
('索尼75英寸4K电视', 'XR认知芯片，HDR', 8999.00, 9999.00, '索尼', 30, 85, '📺', 3, FALSE, TRUE),
('AirPods Pro 2', '主动降噪，空间音频', 1899.00, 2199.00, 'Apple', 300, 890, '🎧', 4, TRUE, FALSE),
('Sony WH-1000XM5', '头戴式降噪耳机', 2499.00, 2699.00, '索尼', 150, 420, '🎧', 4, TRUE, FALSE),
('Apple Watch Series 9', '健康监测，运动追踪', 3199.00, 3499.00, 'Apple', 120, 350, '⌚', 6, TRUE, FALSE);

COMMIT;
