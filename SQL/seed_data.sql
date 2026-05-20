-- =====================================================
-- TechShopWebsite2 - Sample data aligned to Models
-- Run after schema.sql
-- =====================================================
USE TechShopWebsite2;
GO

-- Xóa dữ liệu cũ nếu có (Tuỳ chọn, nhưng để đảm bảo sạch)
DELETE FROM OrderItems;
DELETE FROM Orders;
DELETE FROM CartItems;
DELETE FROM Carts;
DELETE FROM Inventory;
DELETE FROM ProductImages;
DELETE FROM ProductVariants;
DELETE FROM Products;
DELETE FROM Suppliers;
DELETE FROM Categories;
DELETE FROM Users;
DELETE FROM Employees;
DELETE FROM Accounts;
DELETE FROM Roles;

-- Đặt lại Identity
DBCC CHECKIDENT ('Roles', RESEED, 0);
DBCC CHECKIDENT ('Accounts', RESEED, 0);
DBCC CHECKIDENT ('Employees', RESEED, 0);
DBCC CHECKIDENT ('Users', RESEED, 0);
DBCC CHECKIDENT ('Categories', RESEED, 0);
DBCC CHECKIDENT ('Suppliers', RESEED, 0);
DBCC CHECKIDENT ('Products', RESEED, 0);
DBCC CHECKIDENT ('ProductVariants', RESEED, 0);
DBCC CHECKIDENT ('ProductImages', RESEED, 0);
DBCC CHECKIDENT ('Inventory', RESEED, 0);
DBCC CHECKIDENT ('Carts', RESEED, 0);
DBCC CHECKIDENT ('CartItems', RESEED, 0);
DBCC CHECKIDENT ('Orders', RESEED, 0);
DBCC CHECKIDENT ('OrderItems', RESEED, 0);

-- Roles
INSERT INTO Roles (role_name, description) VALUES
(N'Admin', N'Quản trị viên hệ thống cao nhất'),
(N'Customer', N'Khách hàng mua sắm'),
(N'Staff', N'Nhân viên cửa hàng');

-- Accounts (Chỉ 1 tài khoản Admin duy nhất theo yêu cầu)
-- Password '123456' has bcrypt hash: $2b$12$V2Z3K3ERgRxP4ZeqmYq7fef4xDpDGV8L/jfbJ7MSGVP1qpWUEdC3m
INSERT INTO Accounts (username, password_hash, email, full_name, phone, address, is_active, role_id)
VALUES
(N'admin', N'$2b$12$V2Z3K3ERgRxP4ZeqmYq7fef4xDpDGV8L/jfbJ7MSGVP1qpWUEdC3m', N'admin@techstore.vn', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, 1);

-- Employees
INSERT INTO Employees (account_id, department, position, hire_date, salary, is_active)
VALUES
(1, N'Ban Giám Đốc', N'Giám đốc', SYSUTCDATETIME(), 50000000, 1);

-- Users (Dự phòng cho bảng Users nếu có sử dụng)
INSERT INTO Users (username, email, password_hash, full_name, phone, address, is_active, role, avatar_url)
VALUES
(N'admin', N'admin@techstore.vn', N'$2b$12$V2Z3K3ERgRxP4ZeqmYq7fef4xDpDGV8L/jfbJ7MSGVP1qpWUEdC3m', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, N'Admin', N'/avatars/admin.png');

-- Categories
INSERT INTO Categories (name, description, image_url, display_order, is_active)
VALUES
(N'Điện thoại di động', N'Smartphone các hãng Apple, Samsung...', '/images/cat_phone.png', 1, 1),
(N'Laptop & Macbook', N'Máy tính xách tay phục vụ làm việc, gaming', '/images/cat_laptop.png', 2, 1),
(N'Máy tính bảng', N'Tablet iPad, Galaxy Tab...', '/images/cat_tablet.png', 3, 1),
(N'Phụ kiện', N'Tai nghe, củ sạc, ốp lưng, bàn phím...', '/images/cat_accessories.png', 4, 1);

-- Suppliers
INSERT INTO Suppliers (name, contact_person, phone, email, address, is_active)
VALUES
(N'Apple Vietnam', N'Nguyễn Văn A', N'0901234567', N'contact@apple.vn', N'Q1, TP.HCM', 1),
(N'Samsung Electronics', N'Trần Thị B', N'0901234568', N'b2b@samsung.vn', N'Q9, TP.HCM', 1),
(N'Dell Technologies', N'Lê Văn C', N'0901234569', N'sales@dell.vn', N'Cầu Giấy, Hà Nội', 1),
(N'ASUS Vietnam', N'Phạm Thị D', N'0901234570', N'support@asus.vn', N'Q3, TP.HCM', 1);

-- Products
INSERT INTO Products (
    name, description, image_url, price, original_price, stock_quantity, is_available,
    rating, is_new, is_hot, discount_percent, specifications, category_id, supplier_id
)
VALUES
(N'iPhone 15 Pro Max 256GB', N'Điện thoại flagship cao cấp nhất của Apple.', '/images/iphone15promax.png', 29990000, 34990000, 50, 1, 4.9, 1, 1, 14, '{}', 1, 1),
(N'Samsung Galaxy S24 Ultra', N'Smartphone tích hợp Galaxy AI mạnh mẽ.', '/images/s24ultra.png', 31990000, 33990000, 30, 1, 4.8, 1, 1, 5, '{}', 1, 2),
(N'MacBook Pro 14 M3', N'Laptop chuyên nghiệp dành cho dân đồ họa, lập trình.', '/images/macbookpro14.png', 39990000, 42990000, 20, 1, 4.9, 1, 0, 6, '{}', 2, 1),
(N'Dell XPS 15 9530', N'Laptop Windows cao cấp viền màn hình siêu mỏng.', '/images/dellxps15.png', 45990000, 49990000, 15, 1, 4.7, 0, 0, 8, '{}', 2, 3),
(N'iPad Pro 11 inch M2', N'Máy tính bảng hiệu năng ngang ngửa laptop.', '/images/ipadpro11.png', 20990000, 22990000, 25, 1, 4.8, 0, 1, 8, '{}', 3, 1),
(N'Tai nghe AirPods Pro 2', N'Tai nghe true wireless chống ồn chủ động tốt nhất.', '/images/airpodspro2.png', 5990000, 6990000, 100, 1, 4.9, 0, 1, 14, '{}', 4, 1);

-- ProductVariants
INSERT INTO ProductVariants (product_id, color, storage, ram, variant_name, sku, price, original_price, stock_quantity, display_order, is_active)
VALUES
(1, N'Titan Tự nhiên', '256GB', '8GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', 'IP15PM-NT-256', 29990000, 34990000, 20, 1, 1),
(1, N'Titan Đen', '256GB', '8GB', N'iPhone 15 Pro Max Titan Đen 256GB', 'IP15PM-BK-256', 29990000, 34990000, 30, 2, 1),
(2, N'Xám Titan', '256GB', '12GB', N'Galaxy S24 Ultra Xám 256GB', 'S24U-GY-256', 31990000, 33990000, 15, 1, 1),
(3, 'Silver', '512GB', '18GB', N'MacBook Pro 14 M3 Silver', 'MBP14-SL-512', 39990000, 42990000, 10, 1, 1),
(4, 'Platinum Silver', '1TB', '32GB', N'Dell XPS 15 9530 1TB', 'XPS15-SL-1TB', 45990000, 49990000, 15, 1, 1),
(5, 'Space Grey', '256GB', '8GB', N'iPad Pro 11 M2 Space Grey', 'IPP11-SG-256', 20990000, 22990000, 25, 1, 1),
(6, N'Trắng', 'N/A', 'N/A', N'AirPods Pro 2', 'AP-PRO2-WH', 5990000, 6990000, 100, 1, 1);

-- ProductImages
INSERT INTO ProductImages (product_id, image_url, display_order, is_primary)
VALUES
(1, '/images/iphone15promax_1.png', 1, 1),
(2, '/images/s24ultra_1.png', 1, 1),
(3, '/images/macbookpro14_1.png', 1, 1),
(4, '/images/dellxps15_1.png', 1, 1),
(5, '/images/ipadpro11_1.png', 1, 1),
(6, '/images/airpodspro2_1.png', 1, 1);

-- Inventory
INSERT INTO Inventory (product_id, quantity_in_stock, min_stock_level, max_stock_level, last_restock_date)
VALUES
(1, 50, 10, 100, SYSUTCDATETIME()),
(2, 30, 5, 50, SYSUTCDATETIME()),
(3, 20, 3, 30, SYSUTCDATETIME()),
(4, 15, 2, 20, SYSUTCDATETIME()),
(5, 25, 5, 50, SYSUTCDATETIME()),
(6, 100, 20, 200, SYSUTCDATETIME());

-- Carts
INSERT INTO Carts (account_id)
VALUES
(1);

-- CartItems
INSERT INTO CartItems (cart_id, product_id, variant_id, quantity)
VALUES
(1, 1, 1, 1);

-- Orders
INSERT INTO Orders (account_id, order_date, total_amount, status, customer_name, customer_phone, customer_address, notes)
VALUES
(1, SYSUTCDATETIME(), 29990000, 'Pending', N'Quản Trị Viên', '0999999999', N'Trụ sở Tech Store', N'Đơn hàng test của admin');

-- OrderItems
INSERT INTO OrderItems (order_id, product_id, variant_id, product_name, variant_name, quantity, unit_price, subtotal)
VALUES
(1, 1, 1, N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', 1, 29990000, 29990000);

PRINT N'Đã seed dữ liệu thành công';
GO

-- =====================================================
-- FIX: Cập nhật dữ liệu bị lưu sai encoding
-- Chạy lệnh này để fix dữ liệu cũ trong database
-- =====================================================
USE TechShopWebsite2;
GO

-- Fix Roles (thêm N prefix cho chuỗi đang bị encoding sai)
UPDATE Roles SET description = N'Quản trị viên hệ thống cao nhất' WHERE role_name = N'Admin';
UPDATE Roles SET description = N'Khách hàng mua sắm' WHERE role_name = N'Customer';
UPDATE Roles SET description = N'Nhân viên cửa hàng' WHERE role_name = N'Staff';

-- Fix Accounts full_name
UPDATE Accounts SET full_name = N'Quản Trị Viên' WHERE username = N'admin';
UPDATE Accounts SET address = N'Trụ sở Tech Store' WHERE username = N'admin';
UPDATE Accounts SET phone = N'0999999999' WHERE username = N'admin';
UPDATE Accounts SET email = N'admin@techstore.vn' WHERE username = N'admin';

-- Fix Employees department/position
UPDATE Employees SET department = N'Ban Giám Đốc', position = N'Giám đốc' WHERE employee_id = 1;

-- Fix Users full_name
UPDATE Users SET full_name = N'Quản Trị Viên' WHERE username = N'admin';
UPDATE Users SET address = N'Trụ sở Tech Store' WHERE username = N'admin';
UPDATE Users SET phone = N'0999999999' WHERE username = N'admin';

-- Fix Orders customer_name/address/notes
UPDATE Orders SET customer_name = N'Quản Trị Viên' WHERE customer_name LIKE N'%Quản%';
UPDATE Orders SET customer_address = N'Trụ sở Tech Store' WHERE customer_address LIKE N'%Trụ sở%';
UPDATE Orders SET notes = N'Đơn hàng test của admin' WHERE notes LIKE N'%test%';

PRINT N'Đã fix dữ liệu bị encoding sai thành công';
GO
