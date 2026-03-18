-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建产品表
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入测试数据
INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', 'admin123'),
('user', 'user@example.com', 'user123')
ON DUPLICATE KEY UPDATE username = VALUES(username);

INSERT INTO products (name, price, stock) VALUES
('产品A', 100.00, 10),
('产品B', 200.00, 5)
ON DUPLICATE KEY UPDATE name = VALUES(name);