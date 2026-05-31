-- =====================================================
-- TechShopWebsite2 - Sample data aligned to Models
-- Run after schema.sql
-- =====================================================
USE TechShopWebsite2;
GO

-- Xóa dữ liệu cũ nếu có
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

-- =====================================================
-- ROLES & ACCOUNTS
-- =====================================================
SET IDENTITY_INSERT Roles ON;
INSERT INTO Roles (role_id, role_name, description) VALUES
(1, N'Admin', N'Quản trị viên hệ thống cao nhất'),
(2, N'Customer', N'Khách hàng mua sắm'),
(3, N'Staff', N'Nhân viên cửa hàng');
SET IDENTITY_INSERT Roles OFF;

SET IDENTITY_INSERT Accounts ON;
INSERT INTO Accounts (account_id, username, password_hash, email, full_name, phone, address, is_active, role_id)
VALUES
(1, N'admin', N'123456', N'admin@techstore.vn', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, 1),
(2, N'customer01', N'$2b$12$r5fU5Qb9eU1rQhsx0bQwcuIbWYzInjEuu0crmFJMzJyc1UNdIFQM6', N'customer01@techstore.vn', N'Nguyễn Văn Khách', N'0901234001', N'Q.Bình Thạnh, TP.HCM', 1, 2),
(3, N'staff01', N'$2b$12$RrufLkeBvFeTIN5zhjkWGuy.8qRPjtvIDsljhczp7ft0P8rwe9Q0G', N'staff01@techstore.vn', N'Trần Thị Nhân Viên', N'0901234002', N'Q.3, TP.HCM', 1, 3);
SET IDENTITY_INSERT Accounts OFF;

SET IDENTITY_INSERT Employees ON;
INSERT INTO Employees (employee_id, account_id, department, position, hire_date, salary, is_active)
VALUES
(1, 1, N'Ban Giám Đốc', N'Giám đốc', SYSUTCDATETIME(), 50000000, 1),
(2, 3, N'Kinh doanh', N'Nhân viên bán hàng', SYSUTCDATETIME(), 12000000, 1);
SET IDENTITY_INSERT Employees OFF;

SET IDENTITY_INSERT Users ON;
INSERT INTO Users (user_id, username, email, password_hash, full_name, phone, address, is_active, role, avatar_url)
VALUES
(1, N'admin', N'admin@techstore.vn', N'$2b$12$mUqpjMM0J1jQifI7j5fFnehx6DZu1nMRConvoXiN20yTSifyaFpES', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', 1, N'Admin', N'/images/products/iPhone_15_Pro_Max.png'),
(2, N'customer01', N'customer01@techstore.vn', N'$2b$12$r5fU5Qb9eU1rQhsx0bQwcuIbWYzInjEuu0crmFJMzJyc1UNdIFQM6', N'Nguyễn Văn Khách', N'0901234001', N'Q.Bình Thạnh, TP.HCM', 1, N'Customer', NULL),
(3, N'staff01', N'staff01@techstore.vn', N'$2b$12$RrufLkeBvFeTIN5zhjkWGuy.8qRPjtvIDsljhczp7ft0P8rwe9Q0G', N'Trần Thị Nhân Viên', N'0901234002', N'Q.3, TP.HCM', 1, N'Staff', NULL);
SET IDENTITY_INSERT Users OFF;
GO

-- =====================================================
-- CATEGORIES
-- =====================================================
SET IDENTITY_INSERT Categories ON;
INSERT INTO Categories (category_id, name, description, image_url, display_order, is_active)
VALUES
(1, N'Điện thoại di động', N'Smartphone các hãng Apple, Samsung, Xiaomi, OPPO, Vivo...', N'/images/products/iPhone_15_Pro_Max.png', 1, 1),
(2, N'Laptop & Macbook', N'Máy tính xách tay phục vụ làm việc, học tập và gaming', N'/images/products/MacBook_Pro_14_M3_Pro.png', 2, 1),
(3, N'Máy tính bảng', N'Tablet iPad, Galaxy Tab...', N'/images/products/iPad_Air_M2.png', 3, 1),
(4, N'Phụ kiện', N'Tai nghe, đồng hồ, ốp lưng, bàn phím, chuột, sạc...', N'/images/products/AirPods_Pro_2.png', 4, 1);
SET IDENTITY_INSERT Categories OFF;
GO

-- =====================================================
-- SUPPLIERS
-- =====================================================
SET IDENTITY_INSERT Suppliers ON;
INSERT INTO Suppliers (supplier_id, name, contact_person, phone, email, address, is_active)
VALUES
(1, N'Apple Vietnam', N'Nguyễn Văn A', N'0901234567', N'contact@apple.vn', N'Q1, TP.HCM', 1),
(2, N'Samsung Electronics', N'Trần Thị B', N'0901234568', N'b2b@samsung.vn', N'Q9, TP.HCM', 1),
(3, N'Dell Technologies', N'Lê Văn C', N'0901234569', N'sales@dell.vn', N'Cầu Giấy, Hà Nội', 1),
(4, N'ASUS Vietnam', N'Phạm Thị D', N'0901234570', N'support@asus.vn', N'Q3, TP.HCM', 1),
(5, N'Xiaomi Vietnam', N'Hoàng Minh E', N'0901234571', N'vn@xiaomi.com', N'Q7, TP.HCM', 1),
(6, N'OPPO Vietnam', N'Vũ Thị F', N'0901234572', N'contact@oppo.vn', N'Q.Bình Thạnh, TP.HCM', 1),
(7, N'HP Vietnam', N'Đặng Văn G', N'0901234573', N'vn@hp.com', N'Q.3, TP.HCM', 1),
(8, N'Lenovo Vietnam', N'Bùi Thị H', N'0901234574', N'vn@lenovo.com', N'Q.Tân Bình, TP.HCM', 1);
SET IDENTITY_INSERT Suppliers OFF;
GO

-- =====================================================
-- PRODUCTS - ĐIỆN THOẠI (Category 1)
-- =====================================================
SET IDENTITY_INSERT Products ON;
INSERT INTO Products (product_id, name, description, image_url, price, original_price, stock_quantity, is_available, rating, is_new, is_hot, discount_percent, specifications, category_id, supplier_id)
VALUES
-- Điện thoại
(1, N'iPhone 15 Pro Max 256GB', N'Điện thoại flagship cao cấp nhất của Apple với chip A17 Pro, camera 48MP, khung titanium.', N'/images/products/iPhone_15_Pro_Max.png', 29990000, 34990000, 50, 1, 4.9, 1, 1, 14, N'{"chip":"A17 Pro","ram":"8GB","screen":"6.7 inch OLED","battery":"4422mAh","camera":"48MP"}', 1, 1),
(2, N'iPhone 15 Pro 256GB', N'Chip A17 Pro, camera 48MP, khung titanium nhẹ bền.', N'/images/products/iPhone_15_Pro_Max.png', 27990000, 31990000, 40, 1, 4.9, 1, 1, 12, N'{"chip":"A17 Pro","ram":"8GB","screen":"6.1 inch OLED","battery":"3274mAh","camera":"48MP"}', 1, 1),
(3, N'iPhone 15 128GB', N'iPhone 15 với Dynamic Island, camera 48MP, chip A16 Bionic.', N'/images/products/iPhone_15.png', 22990000, 26990000, 60, 1, 4.8, 1, 0, 14, N'{"chip":"A16 Bionic","ram":"6GB","screen":"6.1 inch OLED","battery":"3349mAh","camera":"48MP"}', 1, 1),
(4, N'iPhone 14 Pro Max 256GB', N'Flagship thế hệ trước với Dynamic Island và camera 48MP.', N'/images/products/iPhone_15_Pro_Max.png', 24990000, 29990000, 30, 1, 4.8, 0, 1, 16, N'{"chip":"A16 Bionic","ram":"6GB","screen":"6.7 inch OLED","battery":"4323mAh","camera":"48MP"}', 1, 1),
(5, N'iPhone 14 128GB', N'iPhone 14 với chip A15 Bionic, camera 12MP kép.', N'/images/products/iPhone_14.png', 19990000, 22990000, 45, 1, 4.7, 0, 0, 13, N'{"chip":"A15 Bionic","ram":"6GB","screen":"6.1 inch OLED","battery":"3279mAh","camera":"12MP"}', 1, 1),
(6, N'iPhone SE 2022', N'iPhone giá rẻ với chip A15 Bionic mạnh mẽ, màn hình 4.7 inch.', N'/images/products/iPhone_SE.png', 12990000, 14990000, 35, 1, 4.5, 0, 0, 13, N'{"chip":"A15 Bionic","ram":"4GB","screen":"4.7 inch LCD","battery":"2018mAh","camera":"12MP"}', 1, 1),
(7, N'Samsung Galaxy S24 Ultra', N'Điện thoại AI đầu tiên với S Pen, camera 200MP, Galaxy AI tích hợp.', N'/images/products/Galaxy_S24_Ultra.png', 32990000, 34990000, 40, 1, 4.8, 1, 1, 5, N'{"chip":"Snapdragon 8 Gen 3","ram":"12GB","screen":"6.8 inch AMOLED","battery":"5000mAh","camera":"200MP"}', 1, 2),
(8, N'Samsung Galaxy S24+', N'Galaxy AI, màn hình 6.7 inch, chip Snapdragon 8 Gen 3.', N'/images/products/samsung-s24-plus.png', 24990000, 27990000, 30, 1, 4.7, 1, 0, 10, N'{"chip":"Snapdragon 8 Gen 3","ram":"12GB","screen":"6.7 inch AMOLED","battery":"4900mAh","camera":"50MP"}', 1, 2),
(9, N'Samsung Galaxy S24', N'Flagship nhỏ gọn với Galaxy AI, màn hình 6.2 inch.', N'/images/products/samsung-s24-plus.png', 19990000, 22990000, 35, 1, 4.7, 1, 0, 13, N'{"chip":"Snapdragon 8 Gen 3","ram":"8GB","screen":"6.2 inch AMOLED","battery":"4000mAh","camera":"50MP"}', 1, 2),
(10, N'Samsung Galaxy Z Fold5', N'Điện thoại gập đa năng với màn hình 7.6 inch, S Pen.', N'/images/products/Tab_S9_Ultra__01.jpg', 40990000, 44990000, 20, 1, 4.6, 0, 1, 8, N'{"chip":"Snapdragon 8 Gen 2","ram":"12GB","screen":"7.6 inch AMOLED (gập)","battery":"4400mAh","camera":"50MP"}', 1, 2),
(11, N'Samsung Galaxy Z Flip5', N'Điện thoại gập nhỏ gọn với màn hình ngoài 3.4 inch.', N'/images/products/Z_Flip5.png', 22990000, 25990000, 25, 1, 4.6, 0, 1, 11, N'{"chip":"Snapdragon 8 Gen 2","ram":"8GB","screen":"6.7 inch AMOLED (gập)","battery":"3700mAh","camera":"12MP"}', 1, 2),
(12, N'Xiaomi 14 Ultra', N'Flagship Xiaomi với Leica, camera 1 inch, chip Snapdragon 8 Gen 3.', N'/images/products/Xiaomi_13T_Pro.png', 27990000, 29990000, 20, 1, 4.7, 1, 1, 6, N'{"chip":"Snapdragon 8 Gen 3","ram":"16GB","screen":"6.73 inch LTPO AMOLED","battery":"5300mAh","camera":"50MP Leica"}', 1, 5),
(13, N'Xiaomi 14', N'Flagship compact với Leica, chip Snapdragon 8 Gen 3.', N'/images/products/xiaomi-14.png', 18990000, 21990000, 25, 1, 4.6, 1, 0, 13, N'{"chip":"Snapdragon 8 Gen 3","ram":"12GB","screen":"6.36 inch LTPO AMOLED","battery":"4610mAh","camera":"50MP Leica"}', 1, 5),
(14, N'OPPO Find X7 Ultra', N'Flagship OPPO với camera zoom quang học 6x, Hasselblad.', N'/images/products/Xiaomi_13T_Pro__01.jpg', 24990000, 27990000, 15, 1, 4.6, 1, 1, 10, N'{"chip":"Snapdragon 8 Gen 3","ram":"16GB","screen":"6.82 inch LTPO AMOLED","battery":"5000mAh","camera":"50MP Hasselblad"}', 1, 6),
(15, N'Vivo X100 Pro', N'Flagship Vivo với Zeiss, camera 1 inch, chip Dimensity 9300.', N'/images/products/Reno11_F_5G.png', 22990000, 25990000, 15, 1, 4.7, 1, 1, 11, N'{"chip":"Dimensity 9300","ram":"16GB","screen":"6.78 inch LTPO AMOLED","battery":"5400mAh","camera":"50MP Zeiss"}', 1, 6),
-- LAPTOP
(16, N'MacBook Pro 14 M3', N'MacBook Pro 14 inch với chip M3, màn hình Liquid Retina XDR.', N'/images/products/MacBook_Pro_14_M3_Pro.png', 44990000, 49990000, 20, 1, 4.9, 1, 1, 10, N'{"chip":"Apple M3","ram":"18GB","screen":"14.2 inch Liquid Retina XDR","storage":"512GB SSD","battery":"70Wh"}', 2, 1),
(17, N'MacBook Pro 16 M3 Max', N'MacBook Pro 16 inch với chip M3 Max, hiệu năng workstation.', N'/images/products/MacBook_Pro_14_M3_Pro.png', 89990000, 99990000, 10, 1, 4.9, 1, 0, 10, N'{"chip":"Apple M3 Max","ram":"36GB","screen":"16.2 inch Liquid Retina XDR","storage":"1TB SSD","battery":"100Wh"}', 2, 1),
(18, N'MacBook Air 15 M3', N'MacBook Air màn hình lớn 15 inch, chip M3 tiết kiệm pin.', N'/images/products/MacBook_Air_M3.png', 34990000, 37990000, 25, 1, 4.8, 1, 0, 7, N'{"chip":"Apple M3","ram":"16GB","screen":"15.3 inch Liquid Retina","storage":"256GB SSD","battery":"66Wh"}', 2, 1),
(19, N'MacBook Air 13 M3', N'MacBook Air 13 inch nhẹ nhất, chip M3, silent fanless.', N'/images/products/macbook-air-13-m3.png', 28990000, 31990000, 30, 1, 4.8, 1, 0, 9, N'{"chip":"Apple M3","ram":"16GB","screen":"13.6 inch Liquid Retina","storage":"256GB SSD","battery":"52.6Wh"}', 2, 1),
(20, N'Dell XPS 15 9530', N'Laptop Windows cao cấp viền màn hình siêu mỏng, OLED.', N'/images/products/Dell_XPS_15.png', 49990000, 54990000, 15, 1, 4.7, 0, 0, 9, N'{"chip":"Intel Core i9-13900H","ram":"32GB","screen":"15.6 inch OLED 3.5K","storage":"1TB SSD","battery":"86Wh"}', 2, 3),
(21, N'Dell XPS 13 Plus', N'Laptop siêu mỏng 13 inch với bàn phím edge-to-edge.', N'/images/products/dell-xps-13.png', 32990000, 35990000, 20, 1, 4.6, 0, 0, 8, N'{"chip":"Intel Core i7-1360P","ram":"16GB","screen":"13.4 inch FHD+","storage":"512GB SSD","battery":"55Wh"}', 2, 3),
(22, N'Dell G15 Gaming', N'Laptop gaming tầm trung với RTX 4060, chip Intel Gen 13.', N'/images/products/dell-g15.png', 32990000, 36990000, 25, 1, 4.5, 0, 1, 10, N'{"chip":"Intel Core i7-13700H","ram":"16GB","screen":"15.6 inch FHD 165Hz","storage":"512GB SSD","gpu":"RTX 4060"}', 2, 3),
(23, N'ASUS ROG Zephyrus G14', N'Laptop gaming nhỏ gọn 14 inch với RTX 4070, AMD Ryzen 9.', N'/images/products/ROG_Zephyrus_G14.png', 44990000, 49990000, 15, 1, 4.7, 0, 1, 10, N'{"chip":"AMD Ryzen 9 7940HS","ram":"32GB","screen":"14 inch QHD+ 165Hz","storage":"1TB SSD","gpu":"RTX 4070"}', 2, 4),
(24, N'ASUS ZenBook 14', N'Laptop văn phòng mỏng nhẹ với OLED, chip Intel Gen 13.', N'/images/products/ZenBook_14_OLED.png', 24990000, 27990000, 30, 1, 4.6, 0, 0, 10, N'{"chip":"Intel Core i7-1360P","ram":"16GB","screen":"14 inch OLED 2.8K","storage":"512GB SSD","battery":"75Wh"}', 2, 4),
(25, N'ASUS VivoBook 15', N'Laptop văn phòng giá rẻ, màn hình 15.6 inch, chip AMD Ryzen 5.', N'/images/products/VivoBook_15.png', 14990000, 16990000, 40, 1, 4.4, 0, 0, 11, N'{"chip":"AMD Ryzen 5 7520U","ram":"8GB","screen":"15.6 inch FHD","storage":"512GB SSD","battery":"42Wh"}', 2, 4),
(26, N'HP Spectre x360', N'Laptop 2-trong-1 cao cấp với màn hình OLED cảm ứng.', N'/images/products/hp-spectre.png', 39990000, 44990000, 15, 1, 4.7, 0, 0, 11, N'{"chip":"Intel Core i7-1355U","ram":"16GB","screen":"13.5 inch OLED 3K2K cảm ứng","storage":"1TB SSD","battery":"66Wh"}', 2, 7),
(27, N'HP Pavilion 15', N'Laptop văn phòng đa năng, chip Intel Gen 12, màn hình IPS.', N'/images/products/HP_Pavilion_Plus_14.png', 19990000, 22990000, 35, 1, 4.5, 0, 0, 13, N'{"chip":"Intel Core i5-1235U","ram":"16GB","screen":"15.6 inch FHD IPS","storage":"512GB SSD","battery":"41Wh"}', 2, 7),
(28, N'Lenovo ThinkPad X1 Carbon', N'Laptop doanh nhân siêu nhẹ với carbon fiber, bảo mật cao.', N'/images/products/ThinkPad_X1_Carbon.png', 49990000, 55990000, 10, 1, 4.8, 0, 0, 10, N'{"chip":"Intel Core i7-1365U","ram":"32GB","screen":"14 inch 2.8K OLED","storage":"1TB SSD","battery":"57Wh"}', 2, 8),
(29, N'Lenovo Yoga 9i', N'Laptop 2-trong-1 cao cấp với màn hình OLED 4K.', N'/images/products/lenovo-yoga.png', 42990000, 47990000, 12, 1, 4.7, 0, 1, 10, N'{"chip":"Intel Core i7-1360P","ram":"16GB","screen":"14 inch 4K OLED cảm ứng","storage":"512GB SSD","battery":"75Wh"}', 2, 8),
(30, N'MSI Stealth 16', N'Laptop gaming cao cấp 16 inch với RTX 4080, màn hình 4K 144Hz.', N'/images/products/MSI_Modern_15_H.png', 69990000, 79990000, 8, 1, 4.6, 0, 1, 12, N'{"chip":"Intel Core i9-13900H","ram":"32GB","screen":"16 inch 4K 144Hz","storage":"2TB SSD","gpu":"RTX 4080"}', 2, 4),
-- TABLET
(31, N'iPad Pro 13 M4', N'Máy tính bảng cao cấp nhất với chip M4, màn hình Ultra Retina XDR.', N'/images/products/iPad_Pro_12.9.png', 39990000, 44990000, 20, 1, 4.9, 1, 1, 11, N'{"chip":"Apple M4","ram":"8GB","screen":"13 inch Ultra Retina XDR OLED","storage":"256GB","battery":"38.99Wh"}', 3, 1),
(32, N'iPad Pro 11 M4', N'Máy tính bảng 11 inch với chip M4, hỗ trợ Apple Pencil Pro.', N'/images/products/iPad_Air_M2.png', 28990000, 32990000, 25, 1, 4.9, 1, 0, 12, N'{"chip":"Apple M4","ram":"8GB","screen":"11 inch Ultra Retina XDR OLED","storage":"256GB","battery":"31.29Wh"}', 3, 1),
(33, N'iPad Air 11 M2', N'Máy tính bảng 11 inch với chip M2, hỗ trợ Apple Pencil.', N'/images/products/iPad_Air_M2.png', 19990000, 22990000, 30, 1, 4.8, 0, 1, 13, N'{"chip":"Apple M2","ram":"8GB","screen":"11 inch Liquid Retina","storage":"128GB","battery":"28.93Wh"}', 3, 1),
(34, N'iPad 10.9 inch', N'Máy tính bảng giá rẻ với màn hình 10.9 inch, chip A14.', N'/images/products/iPad_Air_M2.png', 13990000, 15990000, 40, 1, 4.6, 0, 0, 12, N'{"chip":"A14 Bionic","ram":"4GB","screen":"10.9 inch Liquid Retina","storage":"64GB","battery":"28.6Wh"}', 3, 1),
(35, N'iPad mini', N'Máy tính bảng nhỏ gọn 8.3 inch, chip A15, dễ cầm một tay.', N'/images/products/iPad_mini_6.png', 14990000, 16990000, 25, 1, 4.7, 0, 0, 11, N'{"chip":"A15 Bionic","ram":"4GB","screen":"8.3 inch Liquid Retina","storage":"64GB","battery":"19.3Wh"}', 3, 1),
(36, N'Samsung Galaxy Tab S9 Ultra', N'Tablet Android cao cấp 14.6 inch với S Pen, IP68.', N'/images/products/Tab_S9_Ultra.png', 32990000, 36990000, 15, 1, 4.7, 0, 1, 10, N'{"chip":"Snapdragon 8 Gen 2","ram":"12GB","screen":"14.6 inch AMOLED 120Hz","storage":"256GB","battery":"11200mAh"}', 3, 2),
(37, N'Samsung Galaxy Tab S9', N'Tablet Android 11 inch với S Pen, kháng nước IP68.', N'/images/products/Tab_S9_FE.png', 19990000, 22990000, 20, 1, 4.6, 0, 0, 13, N'{"chip":"Snapdragon 8 Gen 2","ram":"8GB","screen":"11 inch AMOLED 120Hz","storage":"128GB","battery":"8400mAh"}', 3, 2),
(38, N'Samsung Galaxy Tab S9 FE', N'Tablet Android giá rẻ với S Pen, màn hình LCD 10.9 inch.', N'/images/products/Tab_S9_FE.png', 10990000, 12990000, 30, 1, 4.5, 0, 0, 15, N'{"chip":"Exynos 1380","ram":"6GB","screen":"10.9 inch TFT LCD 90Hz","storage":"128GB","battery":"8000mAh"}', 3, 2),
(39, N'Xiaomi Pad 6', N'Tablet Android giá rẻ với màn hình 11 inch 144Hz.', N'/images/products/Xiaomi_Pad_6.png', 8990000, 9990000, 35, 1, 4.5, 0, 0, 10, N'{"chip":"Snapdragon 870","ram":"6GB","screen":"11 inch LCD 144Hz","storage":"128GB","battery":"8840mAh"}', 3, 5),
-- PHỤ KIỆN
(40, N'AirPods Pro 2', N'Tai nghe true wireless chống ồn chủ động ANC tốt nhất, USB-C.', N'/images/products/AirPods_Pro_2.png', 5990000, 6990000, 100, 1, 4.9, 0, 1, 14, N'{"type":"In-ear True Wireless","noise_cancelling":"ANC","battery":"6h (30h case)","charging":"USB-C"}', 4, 1),
(41, N'AirPods 3', N'Tai nghe true wireless với Spatial Audio, không chống ồn.', N'/images/products/airpods-3.png', 3990000, 4490000, 80, 1, 4.8, 0, 0, 11, N'{"type":"In-ear True Wireless","spatial_audio":true,"battery":"6h (30h case)","charging":"Lightning"}', 4, 1),
(42, N'AirPods 2', N'Tai nghe true wireless phổ thông, thiết kế classic.', N'/images/products/airpods-3.png', 2490000, 2990000, 60, 1, 4.6, 0, 0, 16, N'{"type":"In-ear True Wireless","battery":"5h (24h case)","charging":"Lightning"}', 4, 1),
(43, N'AirPods Max', N'Tai nghe over-ear cao cấp với Spatial Audio, chống ồn ANC.', N'/images/products/AirPods_Pro_2.png', 13990000, 14990000, 30, 1, 4.8, 0, 1, 6, N'{"type":"Over-ear","noise_cancelling":"ANC","battery":"20h","charging":"Lightning"}', 4, 1),
(44, N'Apple Watch Ultra 2', N'Đồng hồ Apple cao cấp nhất với titanium grade 5, GPS + Cellular.', N'/images/products/Apple_Watch_S9.png', 19990000, 22990000, 25, 1, 4.9, 1, 1, 13, N'{"screen":"49mm OLED","material":"Titanium","gps":"GPS + Cellular","battery":"36h","water":"100m"}', 4, 1),
(45, N'Apple Watch Series 9 45mm', N'Đồng hồ Apple với chip S9, màn hình Always-On Retina.', N'/images/products/Apple_Watch_S9.png', 11990000, 13990000, 40, 1, 4.8, 0, 1, 14, N'{"screen":"45mm OLED","chip":"S9","gps":"GPS + Cellular","battery":"18h","water":"50m"}', 4, 1),
(46, N'Apple Watch SE 2023', N'Đồng hồ Apple giá rẻ với tính năng cơ bản, GPS.', N'/images/products/Apple_Watch_S9.png', 6990000, 7990000, 50, 1, 4.7, 0, 0, 12, N'{"screen":"40mm OLED","chip":"S8","gps":"GPS","battery":"18h","water":"50m"}', 4, 1),
(47, N'Samsung Galaxy Watch 6', N'Đồng hồ thông minh Samsung với Wear OS, đo sức khỏe.', N'/images/products/Galaxy_Watch_6_Classic.png', 7990000, 8990000, 30, 1, 4.6, 0, 0, 11, N'{"screen":"44mm AMOLED","os":"Wear OS","battery":"40h","water":"50m","health":"ECG, SpO2"}', 4, 2),
(48, N'Samsung Galaxy Watch 6 Classic', N'Đồng hồ Samsung cao cấp với vòng xoay bezel, Wear OS.', N'/images/products/Galaxy_Watch_6_Classic.png', 11990000, 13990000, 20, 1, 4.7, 0, 1, 14, N'{"screen":"47mm AMOLED","os":"Wear OS","battery":"40h","water":"50m","bezel":"Xoay"}', 4, 2),
(49, N'Samsung Galaxy Buds 2 Pro', N'Tai nghe true wireless Samsung với 360 Audio, ANC.', N'/images/products/Galaxy_Buds2_Pro.png', 4990000, 5990000, 50, 1, 4.7, 0, 0, 16, N'{"type":"In-ear True Wireless","noise_cancelling":"ANC","battery":"5h (18h case)","charging":"USB-C"}', 4, 2),
(50, N'Samsung Galaxy Buds FE', N'Tai nghe true wireless giá rẻ của Samsung, ANC.', N'/images/products/Galaxy_Buds2_Pro.png', 1990000, 2490000, 60, 1, 4.5, 0, 0, 20, N'{"type":"In-ear True Wireless","noise_cancelling":"ANC","battery":"6h (21h case)","charging":"USB-C"}', 4, 2),
(51, N'OPPO Enco X3', N'Tai nghe true wireless OPPO với driver 11mm, ANC, pin 44h.', N'/images/products/Galaxy_Buds2_Pro.png', 3990000, 4490000, 40, 1, 4.6, 0, 0, 11, N'{"type":"In-ear True Wireless","noise_cancelling":"ANC","battery":"6h (44h case)","charging":"USB-C"}', 4, 6),
(52, N'OPPO Watch 4 Pro', N'Đồng hồ thông minh OPPO với Snapdragon W5, pin 5 ngày.', N'/images/products/Xiaomi_Watch_S3.png', 9990000, 11990000, 15, 1, 4.6, 0, 1, 16, N'{"screen":"1.9 inch LTPO AMOLED","chip":"Snapdragon W5","battery":"5 ngày","water":"5ATM"}', 4, 6),
(53, N'Sạc MagSafe Apple 15W', N'Sạc không dây MagSafe cho iPhone, công suất 15W.', N'/images/products/sac-magsafe.png', 1490000, 1790000, 150, 1, 4.7, 0, 0, 16, N'{"type":"Wireless","power":"15W","compatible":"iPhone 12+","plug":"USB-C"}', 4, 1),
(54, N'Sạc Apple 20W USB-C', N'Sạc nhanh USB-C 20W cho iPhone, iPad.', N'/images/products/sac-20w-apple.png', 690000, 890000, 200, 1, 4.8, 0, 0, 22, N'{"type":"Sạc nhanh","power":"20W","plug":"USB-C","compatible":"iPhone, iPad"}', 4, 1),
(55, N'Sạc Samsung 45W', N'Sạc nhanh Samsung 45W USB-C với PPS, cho laptop.', N'/images/products/sac-samsung-45w.png', 1490000, 1790000, 100, 1, 4.6, 0, 0, 16, N'{"type":"Sạc nhanh","power":"45W","plug":"USB-C","pps":true}', 4, 2),
(56, N'Ốp lưng iPhone 15 Pro Max', N'Ốp lưng silicon cao cấp Apple với MagSafe.', N'/images/products/op-lung-iphone-15-pro.png', 990000, 1190000, 200, 1, 4.7, 0, 0, 16, N'{"material":"Silicone","magsafe":true,"compatible":"iPhone 15 Pro Max"}', 4, 1),
(57, N'Ốp lưng iPhone 15', N'Ốp lưng trong suốt Apple với MagSafe, bảo vệ tối đa.', N'/images/products/op-lung-iphone-15-pro.png', 990000, 1190000, 180, 1, 4.6, 0, 0, 16, N'{"material":"Trong suốt","magsafe":true,"compatible":"iPhone 15"}', 4, 1),
(58, N'Kính Mac Studio/Pro Display XDR', N'Thiết bị đánh bóng màn hình Apple Pro Display XDR.', N'/images/products/kinh-mac-mini.png', 6990000, 7990000, 10, 1, 4.8, 0, 0, 12, N'{"compatible":"Pro Display XDR, Mac Studio","material":"Nano-texture","size":"32 inch"}', 4, 1),
(59, N'Bàn phím Apple Magic Keyboard', N'Bàn phím không dây Apple với Touch ID.', N'/images/products/ban-phim-apple.png', 4990000, 5990000, 50, 1, 4.8, 0, 0, 16, N'{"type":"Bluetooth","touch_id":true,"layout":"US/INT","battery":"1 tháng"}', 4, 1),
(60, N'Chuột Apple Magic Mouse', N'Chuột không dây Apple với Surface Multi-Touch.', N'/images/products/Apple_Watch_S9.png', 2990000, 3490000, 60, 1, 4.6, 0, 0, 14, N'{"type":"Bluetooth","touch":true,"battery":"1 tháng","charging":"Lightning"}', 4, 1),
(61, N'Sạc dự phòng 20000mAh', N'Pin dự phòng sạc nhanh 65W PD, QC 3.0, sạc laptop.', N'/images/products/Anker_PowerCore.jpg', 14990000, 16990000, 40, 1, 4.7, 0, 0, 11, N'{"capacity":"20000mAh","power":"65W PD","output":"USB-C PD, USB-A QC","input":"USB-C PD"}', 4, 5),
(62, N'Cáp USB-C to Lightning', N'Cáp sạc Lightning dài 1m, sạc nhanh PD 20W cho iPhone.', N'/images/products/cap-usbc.png', 490000, 590000, 300, 1, 4.7, 0, 0, 16, N'{"type":"USB-C to Lightning","length":"1m","fast_charge":"PD 20W","durability":"Bện dệp"}', 4, 1),
(63, N'Hub USB-C 7 in 1', N'Hub mở rộng USB-C với HDMI 4K, USB-A, SD, microSD, PD.', N'/images/products/HyperDrive_Gen2.png', 1490000, 1790000, 80, 1, 4.5, 0, 0, 16, N'{"ports":"HDMI 4K, 2xUSB-A, SD, microSD, USB-C PD","resolution":"HDMI 4K@60Hz","power":"PD 100W","plug":"USB-C"}', 4, 4),
(64, N'Loa JBL Flip 6', N'Loa Bluetooth di động chống nước IP67, 12h pin.', N'/images/products/JBL_Flip_6.png', 2990000, 3490000, 50, 1, 4.7, 0, 0, 14, N'{"type":"Bluetooth di động","battery":"12h","water":"IP67","power":"20W","bluetooth":"5.1"}', 4, 5),
(65, N'Loa Sonos Roam', N'Loa thông minh Bluetooth/WiFi nhỏ gọn, chống nước IP67.', N'/images/products/JBL_Flip_6.png', 4990000, 5990000, 30, 1, 4.6, 0, 0, 16, N'{"type":"Bluetooth + WiFi","battery":"10h","water":"IP67","assistant":"Alexa, Google","bluetooth":"5.0"}', 4, 3);
SET IDENTITY_INSERT Products OFF;
GO

-- =====================================================
-- PRODUCT VARIANTS
-- =====================================================
SET IDENTITY_INSERT ProductVariants ON;
INSERT INTO ProductVariants (variant_id, product_id, color, color_hex, storage, ram, variant_name, sku, price, original_price, stock_quantity, display_order, is_active)
VALUES
-- iPhone 15 Pro Max (1)
(1, 1, N'Titan Tự nhiên', N'#C9B8A8', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', N'IP15PM-NT-256', 29990000, 34990000, 15, 1, 1),
(2, 1, N'Titan Đen', N'#2B2B2D', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Đen 256GB', N'IP15PM-BK-256', 29990000, 34990000, 15, 2, 1),
(3, 1, N'Titan Trắng', N'#E8E8E8', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Trắng 256GB', N'IP15PM-WH-256', 29990000, 34990000, 10, 3, 1),
(4, 1, N'Titan Xanh', N'#3B4F6B', N'256GB', N'8GB', N'iPhone 15 Pro Max Titan Xanh 256GB', N'IP15PM-BL-256', 29990000, 34990000, 10, 4, 1),
(5, 1, N'Titan Tự nhiên', N'#C9B8A8', N'512GB', N'8GB', N'iPhone 15 Pro Max Titan Tự nhiên 512GB', N'IP15PM-NT-512', 33990000, 38990000, 8, 5, 1),
(6, 1, N'Titan Đen', N'#2B2B2D', N'512GB', N'8GB', N'iPhone 15 Pro Max Titan Đen 512GB', N'IP15PM-BK-512', 33990000, 38990000, 8, 6, 1),

-- iPhone 15 Pro (2)
(7, 2, N'Titan Tự nhiên', N'#C9B8A8', N'256GB', N'8GB', N'iPhone 15 Pro Titan Tự nhiên 256GB', N'IP15P-NT-256', 27990000, 31990000, 12, 1, 1),
(8, 2, N'Titan Đen', N'#2B2B2D', N'256GB', N'8GB', N'iPhone 15 Pro Titan Đen 256GB', N'IP15P-BK-256', 27990000, 31990000, 12, 2, 1),
(9, 2, N'Titan Trắng', N'#E8E8E8', N'256GB', N'8GB', N'iPhone 15 Pro Titan Trắng 256GB', N'IP15P-WH-256', 27990000, 31990000, 8, 3, 1),
(10, 2, N'Titan Xanh', N'#3B4F6B', N'256GB', N'8GB', N'iPhone 15 Pro Titan Xanh 256GB', N'IP15P-BL-256', 27990000, 31990000, 8, 4, 1),

-- iPhone 15 (3)
(11, 3, N'Đen', N'#1D1D1F', N'128GB', N'6GB', N'iPhone 15 Đen 128GB', N'IP15-BK-128', 22990000, 26990000, 20, 1, 1),
(12, 3, N'Trắng', N'#F5F5F7', N'128GB', N'6GB', N'iPhone 15 Trắng 128GB', N'IP15-WH-128', 22990000, 26990000, 15, 2, 1),
(13, 3, N'Hồng', N'#FACBD0', N'128GB', N'6GB', N'iPhone 15 Hồng 128GB', N'IP15-PK-128', 22990000, 26990000, 15, 3, 1),
(14, 3, N'Xanh lá', N'#64B496', N'128GB', N'6GB', N'iPhone 15 Xanh lá 128GB', N'IP15-GN-128', 22990000, 26990000, 10, 4, 1),
(15, 3, N'Xanh dương', N'#5B9BD5', N'128GB', N'6GB', N'iPhone 15 Xanh dương 128GB', N'IP15-BL-128', 22990000, 26990000, 10, 5, 1),

-- Samsung Galaxy S24 Ultra (7)
(16, 7, N'Titan Đen', N'#1D1D1F', N'256GB', N'12GB', N'Galaxy S24 Ultra Titan Đen 256GB', N'S24U-BK-256', 32990000, 34990000, 15, 1, 1),
(17, 7, N'Titan Xám', N'#8A8D91', N'256GB', N'12GB', N'Galaxy S24 Ultra Titan Xám 256GB', N'S24U-GY-256', 32990000, 34990000, 10, 2, 1),
(18, 7, N'Titan Tím', N'#6B5B95', N'256GB', N'12GB', N'Galaxy S24 Ultra Titan Tím 256GB', N'S24U-PL-256', 32990000, 34990000, 8, 3, 1),
(19, 7, N'Titan Vàng', N'#C9A96E', N'256GB', N'12GB', N'Galaxy S24 Ultra Titan Vàng 256GB', N'S24U-YL-256', 32990000, 34990000, 7, 4, 1),

-- MacBook Pro 14 M3 (16)
(20, 16, N'Silver', N'#D8D8D8', N'512GB', N'18GB', N'MacBook Pro 14 M3 Silver 512GB', N'MBP14-SL-512', 44990000, 49990000, 8, 1, 1),
(21, 16, N'Space Black', N'#2B2B2D', N'512GB', N'18GB', N'MacBook Pro 14 M3 Space Black 512GB', N'MBP14-SB-512', 46990000, 51990000, 12, 2, 1),

-- MacBook Air 15 M3 (18)
(22, 18, N'Silver', N'#D8D8D8', N'256GB', N'16GB', N'MacBook Air 15 M3 Silver', N'MBA15-SL-256', 34990000, 37990000, 12, 1, 1),
(23, 18, N'Space Black', N'#2B2B2D', N'256GB', N'16GB', N'MacBook Air 15 M3 Space Black', N'MBA15-SB-256', 34990000, 37990000, 13, 2, 1),

-- AirPods Pro 2 (40)
(24, 40, N'Trắng', N'#F5F5F0', N'N/A', N'N/A', N'AirPods Pro 2', N'APP2-WH', 5990000, 6990000, 100, 1, 1),

-- Apple Watch Ultra 2 (44)
(25, 44, N'Titan tự nhiên', N'#C9B8A8', N'64GB', N'N/A', N'Apple Watch Ultra 2 49mm', N'AWU2-NT', 19990000, 22990000, 25, 1, 1),

-- Apple Watch Series 9 (45)
(26, 45, N'Midnight', N'#1D1D1F', N'64GB', N'N/A', N'Apple Watch Series 9 45mm Midnight', N'AWS9-45-MD', 11990000, 13990000, 15, 1, 1),
(27, 45, N'Silver', N'#D8D8D8', N'64GB', N'N/A', N'Apple Watch Series 9 45mm Silver', N'AWS9-45-SL', 11990000, 13990000, 13, 2, 1),
(28, 45, N'Starlight', N'#F0E5D4', N'64GB', N'N/A', N'Apple Watch Series 9 45mm Starlight', N'AWS9-45-ST', 11990000, 13990000, 12, 3, 1),

-- Samsung Galaxy Watch 6 (47)
(29, 47, N'Đen', N'#1D1D1F', N'16GB', N'1.5GB', N'Samsung Galaxy Watch 6 44mm Đen', N'GW6-44-BK', 7990000, 8990000, 15, 1, 1),
(30, 47, N'Bạc', N'#D8D8D8', N'16GB', N'1.5GB', N'Samsung Galaxy Watch 6 44mm Bạc', N'GW6-44-SL', 7990000, 8990000, 15, 2, 1),

-- iPad Pro 11 M4 (32)
(31, 32, N'Space Black', N'#2B2B2D', N'256GB', N'8GB', N'iPad Pro 11 M4 Space Black 256GB', N'IPP11-SB-256', 28990000, 32990000, 10, 1, 1),
(32, 32, N'Silver', N'#D8D8D8', N'256GB', N'8GB', N'iPad Pro 11 M4 Silver 256GB', N'IPP11-SL-256', 28990000, 32990000, 15, 2, 1),

-- iPad Air (33)
(33, 33, N'Space Gray', N'#6E6E73', N'128GB', N'8GB', N'iPad Air 11 Space Gray 128GB', N'IPA11-SG-128', 19990000, 22990000, 12, 1, 1),
(34, 33, N'Silver', N'#D8D8D8', N'128GB', N'8GB', N'iPad Air 11 Silver 128GB', N'IPA11-SL-128', 19990000, 22990000, 10, 2, 1),
(35, 33, N'Blue', N'#5B9BD5', N'128GB', N'8GB', N'iPad Air 11 Blue 128GB', N'IPA11-BL-128', 19990000, 22990000, 8, 3, 1);
SET IDENTITY_INSERT ProductVariants OFF;
GO

-- =====================================================
-- PRODUCT IMAGES
-- =====================================================
SET IDENTITY_INSERT ProductImages ON;
INSERT INTO ProductImages (image_id, product_id, image_url, display_order, is_primary)
VALUES
(1, 1, N'/images/products/iPhone_15_Pro_Max.png', 1, 1),
(2, 2, N'/images/products/iPhone_15_Pro_Max.png', 1, 1),
(3, 3, N'/images/products/iPhone_15.png', 1, 1),
(4, 4, N'/images/products/iPhone_15_Pro_Max.png', 1, 1),
(5, 5, N'/images/products/iPhone_14.png', 1, 1),
(6, 6, N'/images/products/iPhone_SE.png', 1, 1),
(7, 7, N'/images/products/Galaxy_S24_Ultra.png', 1, 1),
(8, 8, N'/images/products/samsung-s24-plus.png', 1, 1),
(9, 9, N'/images/products/samsung-s24-plus.png', 1, 1),
(10, 10, N'/images/products/Tab_S9_Ultra__01.jpg', 1, 1),
(11, 11, N'/images/products/Z_Flip5.png', 1, 1),
(12, 12, N'/images/products/Xiaomi_13T_Pro.png', 1, 1),
(13, 13, N'/images/products/xiaomi-14.png', 1, 1),
(14, 14, N'/images/products/Xiaomi_13T_Pro__01.jpg', 1, 1),
(15, 15, N'/images/products/Reno11_F_5G.png', 1, 1),
(16, 16, N'/images/products/MacBook_Pro_14_M3_Pro.png', 1, 1),
(17, 17, N'/images/products/MacBook_Pro_14_M3_Pro.png', 1, 1),
(18, 18, N'/images/products/MacBook_Air_M3.png', 1, 1),
(19, 19, N'/images/products/macbook-air-13-m3.png', 1, 1),
(20, 20, N'/images/products/Dell_XPS_15.png', 1, 1),
(21, 21, N'/images/products/dell-xps-13.png', 1, 1),
(22, 22, N'/images/products/dell-g15.png', 1, 1),
(23, 23, N'/images/products/ROG_Zephyrus_G14.png', 1, 1),
(24, 24, N'/images/products/ZenBook_14_OLED.png', 1, 1),
(25, 25, N'/images/products/VivoBook_15.png', 1, 1),
(26, 26, N'/images/products/hp-spectre.png', 1, 1),
(27, 27, N'/images/products/HP_Pavilion_Plus_14.png', 1, 1),
(28, 28, N'/images/products/ThinkPad_X1_Carbon.png', 1, 1),
(29, 29, N'/images/products/lenovo-yoga.png', 1, 1),
(30, 30, N'/images/products/MSI_Modern_15_H.png', 1, 1),
(31, 31, N'/images/products/iPad_Pro_12.9.png', 1, 1),
(32, 32, N'/images/products/iPad_Air_M2.png', 1, 1),
(33, 33, N'/images/products/iPad_Air_M2.png', 1, 1),
(34, 34, N'/images/products/iPad_Air_M2.png', 1, 1),
(35, 35, N'/images/products/iPad_mini_6.png', 1, 1),
(36, 36, N'/images/products/Tab_S9_Ultra.png', 1, 1),
(37, 37, N'/images/products/Tab_S9_FE.png', 1, 1),
(38, 38, N'/images/products/Tab_S9_FE.png', 1, 1),
(39, 39, N'/images/products/Xiaomi_Pad_6.png', 1, 1),
(40, 40, N'/images/products/AirPods_Pro_2.png', 1, 1),
(41, 41, N'/images/products/airpods-3.png', 1, 1),
(42, 42, N'/images/products/airpods-3.png', 1, 1),
(43, 43, N'/images/products/AirPods_Pro_2.png', 1, 1),
(44, 44, N'/images/products/Apple_Watch_S9.png', 1, 1),
(45, 45, N'/images/products/Apple_Watch_S9.png', 1, 1),
(46, 46, N'/images/products/Apple_Watch_S9.png', 1, 1),
(47, 47, N'/images/products/Galaxy_Watch_6_Classic.png', 1, 1),
(48, 48, N'/images/products/Galaxy_Watch_6_Classic.png', 1, 1),
(49, 49, N'/images/products/Galaxy_Buds2_Pro.png', 1, 1),
(50, 50, N'/images/products/Galaxy_Buds2_Pro.png', 1, 1),
(51, 51, N'/images/products/Galaxy_Buds2_Pro.png', 1, 1),
(52, 52, N'/images/products/Xiaomi_Watch_S3.png', 1, 1),
(53, 53, N'/images/products/sac-magsafe.png', 1, 1),
(54, 54, N'/images/products/sac-20w-apple.png', 1, 1),
(55, 55, N'/images/products/sac-samsung-45w.png', 1, 1),
(56, 56, N'/images/products/op-lung-iphone-15-pro.png', 1, 1),
(57, 57, N'/images/products/op-lung-iphone-15-pro.png', 1, 1),
(58, 58, N'/images/products/kinh-mac-mini.png', 1, 1),
(59, 59, N'/images/products/ban-phim-apple.png', 1, 1),
(60, 60, N'/images/products/Apple_Watch_S9.png', 1, 1),
(61, 61, N'/images/products/Anker_PowerCore.jpg', 1, 1),
(62, 62, N'/images/products/cap-usbc.png', 1, 1),
(63, 63, N'/images/products/HyperDrive_Gen2.png', 1, 1),
(64, 64, N'/images/products/JBL_Flip_6.png', 1, 1),
(65, 65, N'/images/products/JBL_Flip_6.png', 1, 1);
SET IDENTITY_INSERT ProductImages OFF;
GO

-- =====================================================
-- INVENTORY
-- =====================================================
SET IDENTITY_INSERT Inventory ON;
INSERT INTO Inventory (inventory_id, product_id, quantity_in_stock, min_stock_level, max_stock_level, last_restock_date)
VALUES
(1, 1, 50, 10, 100, SYSUTCDATETIME()), (2, 2, 40, 8, 80, SYSUTCDATETIME()), (3, 3, 60, 10, 120, SYSUTCDATETIME()),
(4, 4, 30, 5, 60, SYSUTCDATETIME()), (5, 5, 45, 8, 90, SYSUTCDATETIME()), (6, 6, 35, 5, 70, SYSUTCDATETIME()),
(7, 7, 40, 8, 80, SYSUTCDATETIME()), (8, 8, 30, 5, 60, SYSUTCDATETIME()), (9, 9, 35, 5, 70, SYSUTCDATETIME()),
(10, 10, 20, 3, 40, SYSUTCDATETIME()), (11, 11, 25, 4, 50, SYSUTCDATETIME()), (12, 12, 20, 3, 40, SYSUTCDATETIME()),
(13, 13, 25, 4, 50, SYSUTCDATETIME()), (14, 14, 15, 2, 30, SYSUTCDATETIME()), (15, 15, 15, 2, 30, SYSUTCDATETIME()),
(16, 20, 20, 3, 40, SYSUTCDATETIME()), (17, 17, 10, 2, 20, SYSUTCDATETIME()), (18, 18, 25, 4, 50, SYSUTCDATETIME()),
(19, 19, 30, 5, 60, SYSUTCDATETIME()), (20, 20, 15, 2, 30, SYSUTCDATETIME()), (21, 21, 20, 3, 40, SYSUTCDATETIME()),
(22, 22, 25, 4, 50, SYSUTCDATETIME()), (23, 23, 15, 2, 30, SYSUTCDATETIME()), (24, 24, 30, 5, 60, SYSUTCDATETIME()),
(25, 25, 40, 8, 80, SYSUTCDATETIME()), (26, 26, 15, 2, 30, SYSUTCDATETIME()), (27, 27, 35, 5, 70, SYSUTCDATETIME()),
(28, 28, 10, 2, 20, SYSUTCDATETIME()), (29, 29, 12, 2, 25, SYSUTCDATETIME()), (30, 30, 8, 1, 15, SYSUTCDATETIME()),
(31, 31, 20, 3, 40, SYSUTCDATETIME()), (32, 32, 25, 4, 50, SYSUTCDATETIME()), (33, 33, 30, 5, 60, SYSUTCDATETIME()),
(34, 34, 40, 8, 80, SYSUTCDATETIME()), (35, 35, 25, 4, 50, SYSUTCDATETIME()), (36, 36, 15, 2, 30, SYSUTCDATETIME()),
(37, 37, 20, 3, 40, SYSUTCDATETIME()), (38, 38, 30, 5, 60, SYSUTCDATETIME()), (39, 39, 35, 5, 70, SYSUTCDATETIME()),
(40, 40, 100, 20, 200, SYSUTCDATETIME()), (41, 41, 80, 15, 160, SYSUTCDATETIME()), (42, 42, 60, 10, 120, SYSUTCDATETIME()),
(43, 43, 30, 5, 60, SYSUTCDATETIME()), (44, 44, 25, 4, 50, SYSUTCDATETIME()), (45, 45, 40, 8, 80, SYSUTCDATETIME()),
(46, 46, 50, 10, 100, SYSUTCDATETIME()), (47, 47, 30, 5, 60, SYSUTCDATETIME()), (48, 48, 20, 3, 40, SYSUTCDATETIME()),
(49, 49, 50, 10, 100, SYSUTCDATETIME()), (50, 50, 60, 10, 120, SYSUTCDATETIME()), (51, 51, 40, 8, 80, SYSUTCDATETIME()),
(52, 52, 15, 2, 30, SYSUTCDATETIME()), (53, 53, 150, 30, 300, SYSUTCDATETIME()), (54, 54, 200, 40, 400, SYSUTCDATETIME()),
(55, 55, 100, 20, 200, SYSUTCDATETIME()), (56, 56, 200, 40, 400, SYSUTCDATETIME()), (57, 57, 180, 36, 360, SYSUTCDATETIME()),
(58, 58, 10, 2, 20, SYSUTCDATETIME()), (59, 59, 50, 10, 100, SYSUTCDATETIME()), (60, 60, 60, 12, 120, SYSUTCDATETIME()),
(61, 61, 40, 8, 80, SYSUTCDATETIME()), (62, 62, 300, 60, 600, SYSUTCDATETIME()), (63, 63, 80, 16, 160, SYSUTCDATETIME()),
(64, 64, 50, 10, 100, SYSUTCDATETIME()), (65, 65, 30, 5, 60, SYSUTCDATETIME());
SET IDENTITY_INSERT Inventory OFF;
GO

-- =====================================================
-- CARTS & SAMPLE CART ITEMS
-- =====================================================
SET IDENTITY_INSERT Carts ON;
INSERT INTO Carts (cart_id, account_id) VALUES (1, 1);
SET IDENTITY_INSERT Carts OFF;

SET IDENTITY_INSERT CartItems ON;
INSERT INTO CartItems (cart_item_id, cart_id, product_id, variant_id, quantity)
VALUES
(1, 1, 1, 1, 1),
(2, 1, 16, 20, 1),
(3, 1, 40, 24, 2);
SET IDENTITY_INSERT CartItems OFF;
GO

-- =====================================================
-- ORDERS & ORDER ITEMS (sample orders)
-- =====================================================
SET IDENTITY_INSERT Orders ON;
INSERT INTO Orders (order_id, account_id, order_date, total_amount, status, customer_name, customer_phone, customer_address, notes)
VALUES
(1, 1, SYSUTCDATETIME(), 29990000, N'Delivered', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'Đơn hàng mẫu test'),
(2, 1, DATEADD(day, -3, SYSUTCDATETIME()), 44990000, N'Shipped', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'MacBook Pro'),
(3, 1, DATEADD(day, -7, SYSUTCDATETIME()), 11990000, N'Delivered', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'Apple Watch'),
(4, 1, DATEADD(day, -10, SYSUTCDATETIME()), 64990000, N'Delivered', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'iPhone + AirPods'),
(5, 1, DATEADD(day, -14, SYSUTCDATETIME()), 32990000, N'Cancelled', N'Quản Trị Viên', N'0999999999', N'Trụ sở Tech Store', N'Đơn hàng đã hủy');
SET IDENTITY_INSERT Orders OFF;

SET IDENTITY_INSERT OrderItems ON;
INSERT INTO OrderItems (order_item_id, order_id, product_id, variant_id, product_name, variant_name, quantity, unit_price, subtotal)
VALUES
(1, 1, 1, 1, N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', 1, 29990000, 29990000),
(2, 2, 16, 20, N'MacBook Pro 14 M3', N'MacBook Pro 14 M3 Silver 512GB', 1, 44990000, 44990000),
(3, 3, 45, 26, N'Apple Watch Series 9 45mm', N'Apple Watch Series 9 45mm Midnight', 1, 11990000, 11990000),
(4, 4, 1, 1, N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max Titan Tự nhiên 256GB', 1, 29990000, 29990000),
(5, 4, 40, 24, N'AirPods Pro 2', N'AirPods Pro 2', 2, 5990000, 11980000),
(6, 5, 7, 16, N'Samsung Galaxy S24 Ultra', N'Galaxy S24 Ultra Titan Đen 256GB', 1, 32990000, 32990000);
SET IDENTITY_INSERT OrderItems OFF;
GO

-- =====================================================
-- FAQs
-- =====================================================
INSERT INTO FAQs (question, answer, display_order, is_active) VALUES
(N'Làm sao để đặt hàng?', N'Bạn có thể đặt hàng trực tiếp trên website hoặc gọi hotline 1800.6601. Thêm sản phẩm vào giỏ hàng và tiến hành thanh toán.', 1, 1),
(N'Chính sách đổi trả như thế nào?', N'Chúng tôi hỗ trợ đổi trả trong 7 ngày đầu tiên nếu sản phẩm bị lỗi từ nhà sản xuất. Sản phẩm còn nguyên seal và phụ kiện đi kèm.', 2, 1),
(N'Thời gian giao hàng bao lâu?', N'Đơn hàng nội thành TP.HCM và Hà Nội sẽ được giao trong 2-4 giờ. Các tỉnh thành khác: 2-4 ngày làm việc.', 3, 1),
(N'Có hỗ trợ trả góp không?', N'Có, chúng tôi hỗ trợ trả góp 0% qua thẻ tín dụng và trả góp có lãi suất qua các đối tác tài chính.', 4, 1),
(N'Sản phẩm có bảo hành chính hãng không?', N'Tất cả sản phẩm đều được bảo hành chính hãng theo chính sách của nhà sản xuất. iPhone 1 năm, MacBook 1 năm, Samsung 1 năm.', 5, 1);
GO

PRINT N'Đã seed 65 sản phẩm mẫu thành công!';
GO
