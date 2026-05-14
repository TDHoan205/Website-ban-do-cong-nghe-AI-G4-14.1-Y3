-- =====================================================
-- TechShopWebsite1 - Sample data aligned to Models
-- Run after schema.sql
-- =====================================================
USE TechShopWebsite1;
GO

-- Roles (10)
INSERT INTO Roles (role_name, description, permissions) VALUES
('Customer', 'Default customer role', '{}'),
('Staff', 'Staff role', '{}'),
('Admin', 'Admin role', '{}'),
('Role 04', 'Role 04', '{}'),
('Role 05', 'Role 05', '{}'),
('Role 06', 'Role 06', '{}'),
('Role 07', 'Role 07', '{}'),
('Role 08', 'Role 08', '{}'),
('Role 09', 'Role 09', '{}'),
('Role 10', 'Role 10', '{}');

-- Accounts (10)
INSERT INTO Accounts (username, password_hash, email, full_name, phone, address, is_active, role_id, reset_token, reset_token_expiry)
VALUES
('user01', 'hash01', 'user01@example.com', 'User 01', '0910000001', 'Addr 01', 1, 1, NULL, NULL),
('user02', 'hash02', 'user02@example.com', 'User 02', '0910000002', 'Addr 02', 1, 1, NULL, NULL),
('user03', 'hash03', 'user03@example.com', 'User 03', '0910000003', 'Addr 03', 1, 1, NULL, NULL),
('user04', 'hash04', 'user04@example.com', 'User 04', '0910000004', 'Addr 04', 1, 2, NULL, NULL),
('user05', 'hash05', 'user05@example.com', 'User 05', '0910000005', 'Addr 05', 1, 2, NULL, NULL),
('user06', 'hash06', 'user06@example.com', 'User 06', '0910000006', 'Addr 06', 1, 2, NULL, NULL),
('user07', 'hash07', 'user07@example.com', 'User 07', '0910000007', 'Addr 07', 1, 3, NULL, NULL),
('user08', 'hash08', 'user08@example.com', 'User 08', '0910000008', 'Addr 08', 1, 3, NULL, NULL),
('user09', 'hash09', 'user09@example.com', 'User 09', '0910000009', 'Addr 09', 1, 3, NULL, NULL),
('user10', 'hash10', 'user10@example.com', 'User 10', '0910000010', 'Addr 10', 1, 1, NULL, NULL);

-- Employees (10)
INSERT INTO Employees (account_id, department, position, hire_date, salary, is_active)
VALUES
(1, 'Dept A', 'Staff', SYSUTCDATETIME(), 500, 1),
(2, 'Dept B', 'Staff', SYSUTCDATETIME(), 510, 1),
(3, 'Dept C', 'Staff', SYSUTCDATETIME(), 520, 1),
(4, 'Dept D', 'Staff', SYSUTCDATETIME(), 530, 1),
(5, 'Dept E', 'Staff', SYSUTCDATETIME(), 540, 1),
(6, 'Dept F', 'Manager', SYSUTCDATETIME(), 600, 1),
(7, 'Dept G', 'Manager', SYSUTCDATETIME(), 620, 1),
(8, 'Dept H', 'Manager', SYSUTCDATETIME(), 640, 1),
(9, 'Dept I', 'Admin', SYSUTCDATETIME(), 700, 1),
(10, 'Dept J', 'Admin', SYSUTCDATETIME(), 720, 1);

-- Users (10)
INSERT INTO Users (username, email, password_hash, full_name, phone, address, is_active, role, avatar_url, reset_token, reset_token_expiry)
VALUES
('u01', 'u01@example.com', 'hashu01', 'User A01', '0920000001', 'Addr U01', 1, 'Customer', '/avatars/u01.png', NULL, NULL),
('u02', 'u02@example.com', 'hashu02', 'User A02', '0920000002', 'Addr U02', 1, 'Customer', '/avatars/u02.png', NULL, NULL),
('u03', 'u03@example.com', 'hashu03', 'User A03', '0920000003', 'Addr U03', 1, 'Customer', '/avatars/u03.png', NULL, NULL),
('u04', 'u04@example.com', 'hashu04', 'User A04', '0920000004', 'Addr U04', 1, 'Employee', '/avatars/u04.png', NULL, NULL),
('u05', 'u05@example.com', 'hashu05', 'User A05', '0920000005', 'Addr U05', 1, 'Employee', '/avatars/u05.png', NULL, NULL),
('u06', 'u06@example.com', 'hashu06', 'User A06', '0920000006', 'Addr U06', 1, 'Employee', '/avatars/u06.png', NULL, NULL),
('u07', 'u07@example.com', 'hashu07', 'User A07', '0920000007', 'Addr U07', 1, 'Admin', '/avatars/u07.png', NULL, NULL),
('u08', 'u08@example.com', 'hashu08', 'User A08', '0920000008', 'Addr U08', 1, 'Admin', '/avatars/u08.png', NULL, NULL),
('u09', 'u09@example.com', 'hashu09', 'User A09', '0920000009', 'Addr U09', 1, 'Admin', '/avatars/u09.png', NULL, NULL),
('u10', 'u10@example.com', 'hashu10', 'User A10', '0920000010', 'Addr U10', 1, 'Customer', '/avatars/u10.png', NULL, NULL);

-- Categories (10)
INSERT INTO Categories (name, description, image_url, display_order, is_active)
VALUES
('Category 01', 'Desc 01', '/images/c01.png', 1, 1),
('Category 02', 'Desc 02', '/images/c02.png', 2, 1),
('Category 03', 'Desc 03', '/images/c03.png', 3, 1),
('Category 04', 'Desc 04', '/images/c04.png', 4, 1),
('Category 05', 'Desc 05', '/images/c05.png', 5, 1),
('Category 06', 'Desc 06', '/images/c06.png', 6, 1),
('Category 07', 'Desc 07', '/images/c07.png', 7, 1),
('Category 08', 'Desc 08', '/images/c08.png', 8, 1),
('Category 09', 'Desc 09', '/images/c09.png', 9, 1),
('Category 10', 'Desc 10', '/images/c10.png', 10, 1);

-- Suppliers (10)
INSERT INTO Suppliers (name, contact_person, phone, email, address, is_active)
VALUES
('Supplier 01', 'Contact 01', '0900000001', 'supplier01@example.com', 'Address 01', 1),
('Supplier 02', 'Contact 02', '0900000002', 'supplier02@example.com', 'Address 02', 1),
('Supplier 03', 'Contact 03', '0900000003', 'supplier03@example.com', 'Address 03', 1),
('Supplier 04', 'Contact 04', '0900000004', 'supplier04@example.com', 'Address 04', 1),
('Supplier 05', 'Contact 05', '0900000005', 'supplier05@example.com', 'Address 05', 1),
('Supplier 06', 'Contact 06', '0900000006', 'supplier06@example.com', 'Address 06', 1),
('Supplier 07', 'Contact 07', '0900000007', 'supplier07@example.com', 'Address 07', 1),
('Supplier 08', 'Contact 08', '0900000008', 'supplier08@example.com', 'Address 08', 1),
('Supplier 09', 'Contact 09', '0900000009', 'supplier09@example.com', 'Address 09', 1),
('Supplier 10', 'Contact 10', '0900000010', 'supplier10@example.com', 'Address 10', 1);

-- Products (10)
INSERT INTO Products (
    name, description, image_url, price, original_price, stock_quantity, is_available,
    rating, is_new, is_hot, discount_percent, specifications, category_id, supplier_id
)
VALUES
('Product 01', 'Description 01', '/images/p01.png', 100.00, 120.00, 50, 1, 4.5, 1, 1, 10, '{}', 1, 1),
('Product 02', 'Description 02', '/images/p02.png', 110.00, 130.00, 40, 1, 4.2, 1, 0, 5, '{}', 2, 2),
('Product 03', 'Description 03', '/images/p03.png', 120.00, 140.00, 30, 1, 4.6, 0, 1, 0, '{}', 3, 3),
('Product 04', 'Description 04', '/images/p04.png', 130.00, 150.00, 20, 1, 4.1, 0, 0, 0, '{}', 4, 4),
('Product 05', 'Description 05', '/images/p05.png', 140.00, 160.00, 25, 1, 4.7, 1, 1, 8, '{}', 5, 5),
('Product 06', 'Description 06', '/images/p06.png', 150.00, 170.00, 35, 1, 4.3, 0, 1, 6, '{}', 6, 6),
('Product 07', 'Description 07', '/images/p07.png', 160.00, 180.00, 45, 1, 4.0, 1, 0, 3, '{}', 7, 7),
('Product 08', 'Description 08', '/images/p08.png', 170.00, 190.00, 55, 1, 4.4, 0, 0, 0, '{}', 8, 8),
('Product 09', 'Description 09', '/images/p09.png', 180.00, 200.00, 65, 1, 4.8, 1, 1, 12, '{}', 9, 9),
('Product 10', 'Description 10', '/images/p10.png', 190.00, 210.00, 75, 1, 4.9, 1, 0, 4, '{}', 10, 10);

-- ProductVariants (10)
INSERT INTO ProductVariants (product_id, color, storage, ram, variant_name, sku, price, original_price, stock_quantity, display_order, is_active)
VALUES
(1, 'Color 01', '128GB', '8GB', 'Variant 01', 'SKU-01', 100.00, 120.00, 10, 1, 1),
(2, 'Color 02', '256GB', '8GB', 'Variant 02', 'SKU-02', 110.00, 130.00, 10, 1, 1),
(3, 'Color 03', '128GB', '16GB', 'Variant 03', 'SKU-03', 120.00, 140.00, 10, 1, 1),
(4, 'Color 04', '256GB', '16GB', 'Variant 04', 'SKU-04', 130.00, 150.00, 10, 1, 1),
(5, 'Color 05', '128GB', '8GB', 'Variant 05', 'SKU-05', 140.00, 160.00, 10, 1, 1),
(6, 'Color 06', '256GB', '8GB', 'Variant 06', 'SKU-06', 150.00, 170.00, 10, 1, 1),
(7, 'Color 07', '128GB', '16GB', 'Variant 07', 'SKU-07', 160.00, 180.00, 10, 1, 1),
(8, 'Color 08', '256GB', '16GB', 'Variant 08', 'SKU-08', 170.00, 190.00, 10, 1, 1),
(9, 'Color 09', '128GB', '8GB', 'Variant 09', 'SKU-09', 180.00, 200.00, 10, 1, 1),
(10, 'Color 10', '256GB', '8GB', 'Variant 10', 'SKU-10', 190.00, 210.00, 10, 1, 1);

-- ProductImages (10)
INSERT INTO ProductImages (product_id, image_url, display_order, is_primary)
VALUES
(1, '/images/p01_1.png', 1, 1),
(2, '/images/p02_1.png', 1, 1),
(3, '/images/p03_1.png', 1, 1),
(4, '/images/p04_1.png', 1, 1),
(5, '/images/p05_1.png', 1, 1),
(6, '/images/p06_1.png', 1, 1),
(7, '/images/p07_1.png', 1, 1),
(8, '/images/p08_1.png', 1, 1),
(9, '/images/p09_1.png', 1, 1),
(10, '/images/p10_1.png', 1, 1);

-- Inventory (10)
INSERT INTO Inventory (product_id, quantity_in_stock, min_stock_level, max_stock_level, last_restock_date)
VALUES
(1, 100, 5, 100, SYSUTCDATETIME()),
(2, 90, 5, 100, SYSUTCDATETIME()),
(3, 80, 5, 100, SYSUTCDATETIME()),
(4, 70, 5, 100, SYSUTCDATETIME()),
(5, 60, 5, 100, SYSUTCDATETIME()),
(6, 50, 5, 100, SYSUTCDATETIME()),
(7, 40, 5, 100, SYSUTCDATETIME()),
(8, 30, 5, 100, SYSUTCDATETIME()),
(9, 20, 5, 100, SYSUTCDATETIME()),
(10, 10, 5, 100, SYSUTCDATETIME());

-- Carts (10)
INSERT INTO Carts (account_id)
VALUES
(1),(2),(3),(4),(5),(6),(7),(8),(9),(10);

-- CartItems (10)
INSERT INTO CartItems (cart_id, product_id, variant_id, quantity)
VALUES
(1, 1, 1, 1),
(2, 2, 2, 1),
(3, 3, 3, 1),
(4, 4, 4, 1),
(5, 5, 5, 1),
(6, 6, 6, 1),
(7, 7, 7, 1),
(8, 8, 8, 1),
(9, 9, 9, 1),
(10, 10, 10, 1);

-- Orders (10)
INSERT INTO Orders (account_id, order_date, total_amount, status, customer_name, customer_phone, customer_address, notes)
VALUES
(1, SYSUTCDATETIME(), 100.00, 'Pending', 'User 01', '0910000001', 'Addr 01', 'Note 01'),
(2, SYSUTCDATETIME(), 110.00, 'Pending', 'User 02', '0910000002', 'Addr 02', 'Note 02'),
(3, SYSUTCDATETIME(), 120.00, 'Pending', 'User 03', '0910000003', 'Addr 03', 'Note 03'),
(4, SYSUTCDATETIME(), 130.00, 'Pending', 'User 04', '0910000004', 'Addr 04', 'Note 04'),
(5, SYSUTCDATETIME(), 140.00, 'Pending', 'User 05', '0910000005', 'Addr 05', 'Note 05'),
(6, SYSUTCDATETIME(), 150.00, 'Pending', 'User 06', '0910000006', 'Addr 06', 'Note 06'),
(7, SYSUTCDATETIME(), 160.00, 'Pending', 'User 07', '0910000007', 'Addr 07', 'Note 07'),
(8, SYSUTCDATETIME(), 170.00, 'Pending', 'User 08', '0910000008', 'Addr 08', 'Note 08'),
(9, SYSUTCDATETIME(), 180.00, 'Pending', 'User 09', '0910000009', 'Addr 09', 'Note 09'),
(10, SYSUTCDATETIME(), 190.00, 'Pending', 'User 10', '0910000010', 'Addr 10', 'Note 10');

-- OrderItems (10)
INSERT INTO OrderItems (order_id, product_id, variant_id, product_name, variant_name, quantity, unit_price, subtotal)
VALUES
(1, 1, 1, 'Product 01', 'Variant 01', 1, 100.00, 100.00),
(2, 2, 2, 'Product 02', 'Variant 02', 1, 110.00, 110.00),
(3, 3, 3, 'Product 03', 'Variant 03', 1, 120.00, 120.00),
(4, 4, 4, 'Product 04', 'Variant 04', 1, 130.00, 130.00),
(5, 5, 5, 'Product 05', 'Variant 05', 1, 140.00, 140.00),
(6, 6, 6, 'Product 06', 'Variant 06', 1, 150.00, 150.00),
(7, 7, 7, 'Product 07', 'Variant 07', 1, 160.00, 160.00),
(8, 8, 8, 'Product 08', 'Variant 08', 1, 170.00, 170.00),
(9, 9, 9, 'Product 09', 'Variant 09', 1, 180.00, 180.00),
(10, 10, 10, 'Product 10', 'Variant 10', 1, 190.00, 190.00);

-- ReceiptShipments (10)
INSERT INTO ReceiptShipments (product_id, supplier_id, order_id, receipt_type, quantity, unit_price, total_amount, notes, created_by)
VALUES
(1, 1, 1, 'Import', 10, 80, 800, 'Note 01', 1),
(2, 2, 2, 'Import', 10, 85, 850, 'Note 02', 2),
(3, 3, 3, 'Import', 10, 90, 900, 'Note 03', 3),
(4, 4, 4, 'Import', 10, 95, 950, 'Note 04', 4),
(5, 5, 5, 'Import', 10, 100, 1000, 'Note 05', 5),
(6, 6, 6, 'Export', 5, 110, 550, 'Note 06', 6),
(7, 7, 7, 'Export', 5, 115, 575, 'Note 07', 7),
(8, 8, 8, 'Export', 5, 120, 600, 'Note 08', 8),
(9, 9, 9, 'Export', 5, 125, 625, 'Note 09', 9),
(10, 10, 10, 'Export', 5, 130, 650, 'Note 10', 10);

