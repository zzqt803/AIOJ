-- 创建管理员用户（密码: 12345678）
INSERT IGNORE INTO users (username, email, password_hash, role, is_active)
VALUES ('admin', 'admin@test.com', '$2b$12$cx.2HmyKUhKNX6QUItHVd.A6a2HvtwA3D4EqmD/MLFEUrf77xznDC', 'admin', 1);
