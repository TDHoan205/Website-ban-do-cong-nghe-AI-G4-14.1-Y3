-- =====================================================
-- TechShopWebsite2 - Sample data aligned to Models
-- Run after schema.sql
-- =====================================================
USE TechShopWebsite2;
GO

-- Xóa dữ liệu cũ nếu có (Tuỳ chọn, nhưng để đảm bảo sạch)
DELETE FROM KnowledgeChunks;
DELETE FROM Notifications;
DELETE FROM FAQs;
DELETE FROM AIConversationLogs;
DELETE FROM ChatMessages;
DELETE FROM ChatSessions;
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
GO

-- Dùng SET IDENTITY_INSERT để ép chính xác ID cho mọi bảng
-- Không dùng DBCC CHECKIDENT vì dễ gây lỗi ID = 0 trên bảng mới

-- Roles
SET IDENTITY_INSERT Roles ON;
INSERT INTO Roles (role_id, role_name, description) VALUES
(1, N'Admin', N'Quản trị viên hệ thống cao nhất'),
(2, N'Customer', N'Khách hàng mua sắm'),
(3, N'Staff', N'Nhân viên cửa hàng');
SET IDENTITY_INSERT Roles OFF;

-- Accounts
SET IDENTITY_INSERT Accounts ON;
INSERT INTO Accounts (account_id, username, password_hash, email, full_name, phone, address, is_active, role_id)
VALUES
(1, N'admin', N'$2b$12$V2Z3K3ERgRxP4ZeqmYq7fef4xDpDGV8L/jfbJ7MSGVP1qpWUEdC3m', N'admin@techstore.vn', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, 1);
SET IDENTITY_INSERT Accounts OFF;

-- Employees
SET IDENTITY_INSERT Employees ON;
INSERT INTO Employees (employee_id, account_id, department, position, hire_date, salary, is_active)
VALUES
(1, 1, N'Ban Giám Đốc', N'Giám đốc', SYSUTCDATETIME(), 50000000, 1);
SET IDENTITY_INSERT Employees OFF;

-- Users
SET IDENTITY_INSERT Users ON;
INSERT INTO Users (user_id, username, email, password_hash, full_name, phone, address, is_active, role, avatar_url)
VALUES
(1, N'admin', N'admin@techstore.vn', N'$2b$12$V2Z3K3ERgRxP4ZeqmYq7fef4xDpDGV8L/jfbJ7MSGVP1qpWUEdC3m', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, N'Admin', N'/avatars/admin.png');
SET IDENTITY_INSERT Users OFF;

-- Categories
SET IDENTITY_INSERT Categories ON;
INSERT INTO Categories (category_id, name, description, image_url, display_order, is_active)
VALUES
(1, N'Điện thoại di động', N'Smartphone các hãng Apple, Samsung...', N'/images/cat_phone.png', 1, 1),
(2, N'Laptop & Macbook', N'Máy tính xách tay phục vụ làm việc, gaming', N'/images/cat_laptop.png', 2, 1),
(3, N'Máy tính bảng', N'Tablet iPad, Galaxy Tab...', N'/images/cat_tablet.png', 3, 1),
(4, N'Phụ kiện', N'Tai nghe, củ sạc, ốp lưng, bàn phím...', N'/images/cat_accessories.png', 4, 1);
SET IDENTITY_INSERT Categories OFF;

-- Suppliers
SET IDENTITY_INSERT Suppliers ON;
INSERT INTO Suppliers (supplier_id, name, contact_person, phone, email, address, is_active)
VALUES
(1, N'Apple Vietnam', N'Nguyễn Văn A', N'0901234567', N'contact@apple.vn', N'Q1, TP.HCM', 1),
(2, N'Samsung Electronics', N'Trần Thị B', N'0901234568', N'b2b@samsung.vn', N'Q9, TP.HCM', 1),
(3, N'Dell Technologies', N'Lê Văn C', N'0901234569', N'sales@dell.vn', N'Cầu Giấy, Hà Nội', 1),
(4, N'ASUS Vietnam', N'Phạm Thị D', N'0901234570', N'support@asus.vn', N'Q3, TP.HCM', 1);
SET IDENTITY_INSERT Suppliers OFF;

-- Products
SET IDENTITY_INSERT Products ON;
INSERT INTO Products (
    product_id, name, description, image_url, price, original_price, stock_quantity, is_available,
    rating, is_new, is_hot, discount_percent, specifications, category_id, supplier_id
)
VALUES
(1, N'iPhone 15 Pro Max 256GB', N'Điện thoại flagship cao cấp nhất của Apple.', N'/images/iphone15promax.png', 29990000, 34990000, 50, 1, 4.9, 1, 1, 14, N'{}', 1, 1),
(2, N'Samsung Galaxy S24 Ultra', N'Smartphone tích hợp Galaxy AI mạnh mẽ.', N'/images/s24ultra.png', 31990000, 33990000, 30, 1, 4.8, 1, 1, 5, N'{}', 1, 2),
(3, N'MacBook Pro 14 M3', N'Laptop chuyên nghiệp dành cho dân đồ họa, lập trình.', N'/images/macbookpro14.png', 39990000, 42990000, 20, 1, 4.9, 1, 0, 6, N'{}', 2, 1),
(4, N'Dell XPS 15 9530', N'Laptop Windows cao cấp viền màn hình siêu mỏng.', N'/images/dellxps15.png', 45990000, 49990000, 15, 1, 4.7, 0, 0, 8, N'{}', 2, 3),
(5, N'iPad Pro 11 inch M2', N'Máy tính bảng hiệu năng ngang ngửa laptop.', N'/images/ipadpro11.png', 20990000, 22990000, 25, 1, 4.8, 0, 1, 8, N'{}', 3, 1),
(6, N'Tai nghe AirPods Pro 2', N'Tai nghe true wireless chống ồn chủ động tốt nhất.', N'/images/airpodspro2.png', 5990000, 6990000, 100, 1, 4.9, 0, 1, 14, N'{}', 4, 1);
SET IDENTITY_INSERT Products OFF;

-- ProductVariants
SET IDENTITY_INSERT ProductVariants ON;
INSERT INTO ProductVariants (variant_id, product_id, color, color_hex, storage, ram, variant_name, sku, price, original_price, stock_quantity, display_order, is_active)
VALUES
(1, 1, N'Titan Tự nhiên', N'#C9B8A8', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', N'IP15PM-NT-256', 29990000, 34990000, 20, 1, 1),
(2, 1, N'Titan Đen', N'#2B2B2D', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Đen 256GB', N'IP15PM-BK-256', 29990000, 34990000, 30, 2, 1),
(3, 2, N'Xám Titan', N'#8A8D91', N'256GB', N'12GB', N'Galaxy S24 Ultra Xám 256GB', N'S24U-GY-256', 31990000, 33990000, 15, 1, 1),
(4, 3, N'Silver', N'#D8D8D8', N'512GB', N'18GB', N'MacBook Pro 14 M3 Silver', N'MBP14-SL-512', 39990000, 42990000, 10, 1, 1),
(5, 4, N'Platinum Silver', N'#C7C9CC', N'1TB', N'32GB', N'Dell XPS 15 9530 1TB', N'XPS15-SL-1TB', 45990000, 49990000, 15, 1, 1),
(6, 5, N'Space Grey', N'#6E6E73', N'256GB', N'8GB', N'iPad Pro 11 M2 Space Grey', N'IPP11-SG-256', 20990000, 22990000, 25, 1, 1),
(7, 6, N'Trắng', N'#F5F5F0', N'N/A', N'N/A', N'AirPods Pro 2', N'AP-PRO2-WH', 5990000, 6990000, 100, 1, 1);
SET IDENTITY_INSERT ProductVariants OFF;

-- ProductImages
SET IDENTITY_INSERT ProductImages ON;
INSERT INTO ProductImages (image_id, product_id, image_url, display_order, is_primary)
VALUES
(1, 1, N'/images/iphone15promax_1.png', 1, 1),
(2, 2, N'/images/s24ultra_1.png', 1, 1),
(3, 3, N'/images/macbookpro14_1.png', 1, 1),
(4, 4, N'/images/dellxps15_1.png', 1, 1),
(5, 5, N'/images/ipadpro11_1.png', 1, 1),
(6, 6, N'/images/airpodspro2_1.png', 1, 1);
SET IDENTITY_INSERT ProductImages OFF;

-- Inventory
SET IDENTITY_INSERT Inventory ON;
INSERT INTO Inventory (inventory_id, product_id, quantity_in_stock, min_stock_level, max_stock_level, last_restock_date)
VALUES
(1, 1, 50, 10, 100, SYSUTCDATETIME()),
(2, 2, 30, 5, 50, SYSUTCDATETIME()),
(3, 3, 20, 3, 30, SYSUTCDATETIME()),
(4, 4, 15, 2, 20, SYSUTCDATETIME()),
(5, 5, 25, 5, 50, SYSUTCDATETIME()),
(6, 6, 100, 20, 200, SYSUTCDATETIME());
SET IDENTITY_INSERT Inventory OFF;

-- Carts
SET IDENTITY_INSERT Carts ON;
INSERT INTO Carts (cart_id, account_id)
VALUES
(1, 1);
SET IDENTITY_INSERT Carts OFF;

-- CartItems
SET IDENTITY_INSERT CartItems ON;
INSERT INTO CartItems (cart_item_id, cart_id, product_id, variant_id, quantity)
VALUES
(1, 1, 1, 1, 1);
SET IDENTITY_INSERT CartItems OFF;

-- Orders
SET IDENTITY_INSERT Orders ON;
INSERT INTO Orders (order_id, account_id, order_date, total_amount, status, customer_name, customer_phone, customer_address, notes)
VALUES
(1, 1, SYSUTCDATETIME(), 29990000, N'Pending', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'Đơn hàng test của admin');
SET IDENTITY_INSERT Orders OFF;

-- OrderItems
SET IDENTITY_INSERT OrderItems ON;
INSERT INTO OrderItems (order_item_id, order_id, product_id, variant_id, product_name, variant_name, quantity, unit_price, subtotal)
VALUES
(1, 1, 1, 1, N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', 1, 29990000, 29990000);
SET IDENTITY_INSERT OrderItems OFF;

PRINT N'Đã seed dữ liệu thành công';
GO

-- =====================================================
-- MIGRATION: Cập nhật database cho chức năng phân loại sản phẩm
-- Chạy lệnh này nếu database đã tồn tại (không cần tạo lại schema)
-- =====================================================
USE TechShopWebsite2;
GO

-- Thêm variant_id vào ProductImages (liên kết ảnh với từng phiên bản)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('ProductImages') AND name = 'variant_id')
BEGIN
    ALTER TABLE ProductImages ADD variant_id INT NULL;
    ALTER TABLE ProductImages
        ADD CONSTRAINT FK_ProductImages_Variants
        FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE SET NULL;
END

-- Thêm color_hex vào ProductVariants (mã màu hex cho swatch)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('ProductVariants') AND name = 'color_hex')
BEGIN
    ALTER TABLE ProductVariants ADD color_hex NVARCHAR(7) NULL;
END

PRINT N'Đã migrate database cho chức năng phân loại sản phẩm';
GO

-- =====================================================
-- MIGRATION: Cập nhật bảng cho chức năng phân loại sản phẩm (Variant + Image per Variant)
-- Chạy lệnh này nếu database đã tồn tại (không cần tạo lại schema)
-- =====================================================
USE TechShopWebsite2;
GO

-- Thêm cột variant_id vào ProductImages (cho ảnh theo variant)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('ProductImages') AND name = 'variant_id')
BEGIN
    ALTER TABLE ProductImages ADD variant_id INT NULL;
    ALTER TABLE ProductImages
        ADD CONSTRAINT FK_ProductImages_Variants
        FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE SET NULL;
END

-- Thêm cột color_hex vào ProductVariants (cho swatch màu)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('ProductVariants') AND name = 'color_hex')
BEGIN
    ALTER TABLE ProductVariants ADD color_hex NVARCHAR(7) NULL;
END

PRINT N'Đã migrate database cho chức năng phân loại sản phẩm';
GO
