-- =====================================================
-- SQL Server Sample Data: 0002_sample_data.sql
-- Inserts sample data for the AI Tech Store Django project
-- Database: SQL Server
-- =====================================================

-- Suppress row count messages for cleaner output
SET NOCOUNT ON;

PRINT '=====================================================';
PRINT ' Starting Sample Data: 0002_sample_data.sql        ';
PRINT '=====================================================';
PRINT '';

-- =====================================================
-- NOTE: Password hashes
-- ----------------------------------------
-- Password fields are left as NULL for security.
-- To set passwords, use the Django shell:
--   python manage.py shell
--   >>> from apps.users.models import Account
--   >>> u = Account.objects.get(username="admin")
--   >>> u.set_password("your_password_here")
--   >>> u.save()
-- =====================================================

-- =====================================================
-- 1. INSERT ACCOUNTS (Users)
-- =====================================================
PRINT 'Inserting Accounts...';

INSERT INTO Accounts (username, password_hash, email, full_name, phone, address, is_active, role, created_at, updated_at)
VALUES
    -- 1 Admin
    (N'admin', NULL, N'admin@aitestore.vn', N'Nguyễn Văn Admin', N'0901234567', N'123 Đường Lê Lợi, Quận 1, TP.HCM', 1, N'Admin', GETDATE(), GETDATE()),

    -- 2 Employee
    (N'employee01', NULL, N'employee01@aitestore.vn', N'Trần Thị Nhân Viên', N'0902345678', N'456 Đường Nguyễn Huệ, Quận 1, TP.HCM', 1, N'Employee', GETDATE(), GETDATE()),

    -- 3 Customers
    (N'khachhang01', NULL, N'nguyenhue@email.com', N'Lê Minh Hoàng', N'0912345678', N'789 Đường Điện Biên Phủ, Quận 3, TP.HCM', 1, N'Customer', GETDATE(), GETDATE()),
    (N'khachhang02', NULL, N'thanhlong@email.com', N'Phạm Thanh Long', N'0923456789', N'101 Đường Lý Thường Kiệt, Quận 10, TP.HCM', 1, N'Customer', GETDATE(), GETDATE()),
    (N'khachhang03', NULL, N'hoaiphuong@email.com', N'Đặng Hoài Phương', N'0934567890', N'202 Đường Pasteur, Quận 3, TP.HCM', 1, N'Customer', GETDATE(), GETDATE());

PRINT '  -> 5 accounts inserted.';
PRINT '';

-- =====================================================
-- 2. INSERT EMPLOYEES
-- =====================================================
PRINT 'Inserting Employees...';

INSERT INTO Employees (account_id, employee_code, department, position, hire_date, salary, is_active, created_at, updated_at)
VALUES
    (2, N'NV001', N'Kinh doanh', N'Nhân viên bán hàng', '2023-06-15', 12000000, 1, GETDATE(), GETDATE());

PRINT '  -> 1 employee inserted.';
PRINT '';

-- =====================================================
-- 3. INSERT CATEGORIES
-- =====================================================
PRINT 'Inserting Categories...';

INSERT INTO Categories (name, description, image_url, display_order, is_active, created_at, updated_at)
VALUES
    (N'Điện thoại', N'Các dòng điện thoại thông minh từ các thương hiệu nổi tiếng: iPhone, Samsung, Xiaomi, OPPO...', N'https://placehold.co/400x300/3498db/FFFFFF?text=Dien+Thoai', 1, 1, GETDATE(), GETDATE()),
    (N'Laptop', N'Máy tính xách tay cho học tập, làm việc và giải trí: MacBook, Dell, HP, ASUS...', N'https://placehold.co/400x300/2ecc71/FFFFFF?text=Laptop', 2, 1, GETDATE(), GETDATE()),
    (N'Tablet', N'Máy tính bảng đa năng: iPad, Samsung Galaxy Tab, Xiaomi Pad...', N'https://placehold.co/400x300/9b59b6/FFFFFF?text=Tablet', 3, 1, GETDATE(), GETDATE()),
    (N'Phụ kiện', N'Phụ kiện công nghệ: tai nghe, sạc dự phòng, ốp lưng, cáp sạc...', N'https://placehold.co/400x300/f39c12/FFFFFF?text=Phu+Kien', 4, 1, GETDATE(), GETDATE()),
    (N'Smartwatch', N'Đồng hồ thông minh: Apple Watch, Samsung Watch, Xiaomi Band...', N'https://placehold.co/400x300/e74c3c/FFFFFF?text=Smartwatch', 5, 1, GETDATE(), GETDATE());

PRINT '  -> 5 categories inserted.';
PRINT '';

-- =====================================================
-- 4. INSERT SUPPLIERS
-- =====================================================
PRINT 'Inserting Suppliers...';

INSERT INTO Suppliers (name, contact_person, phone, email, address, is_active, created_at, updated_at)
VALUES
    (N'Apple Việt Nam', N'Mr. John Smith', N'02812345678', N'contact@apple.vn', N'Tầng 20, Tòa nhà Bitexco, Quận 1, TP.HCM', 1, GETDATE(), GETDATE()),
    (N'Samsung Electronics Việt Nam', N'Ms. Nguyễn Thị Lan', N'02823456789', N'vn@samsung.com', N'Khu CNC, Quận 9, TP.HCM', 1, GETDATE(), GETDATE()),
    (N'Xiaomi Việt Nam', N'Mr. Trần Văn Minh', N'02834567890', N'mi@vietnam.xiaomi.com', N'Quận 7, TP.HCM', 1, GETDATE(), GETDATE()),
    (N'OPPO Việt Nam', N'Ms. Lê Thu Hà', N'02845678901', N'oppo@oppo.vn', N'Quận Bình Thạnh, TP.HCM', 1, GETDATE(), GETDATE()),
    (N'VinSmart Việt Nam', N'Mr. Phạm Quốc Bảo', N'02456789012', N'contact@vinSmart.vn', N'Khu CNC Hòa Lạc, Hà Nội', 1, GETDATE(), GETDATE());

PRINT '  -> 5 suppliers inserted.';
PRINT '';

-- =====================================================
-- 5. INSERT BRANDS
-- =====================================================
PRINT 'Inserting Brands...';

INSERT INTO Brands (name, slug, description, logo_url, website, is_active, created_at, updated_at)
VALUES
    (N'Apple', N'apple', N'Thương hiệu công nghệ hàng đầu thế giới đến từ Mỹ. Nổi tiếng với iPhone, MacBook, iPad, Apple Watch.', N'https://placehold.co/200x80/333333/FFFFFF?text=Apple', N'https://www.apple.com', 1, GETDATE(), GETDATE()),
    (N'Samsung', N'samsung', N'Thương hiệu điện tử lớn nhất Hàn Quốc, chuyên sản xuất smartphone, TV, và thiết bị gia dụng.', N'https://placehold.co/200x80/1428A0/FFFFFF?text=Samsung', N'https://www.samsung.com', 1, GETDATE(), GETDATE()),
    (N'Xiaomi', N'xiaomi', N'Thương hiệu Trung Quốc nổi tiếng với các sản phẩm công nghệ giá rẻ nhưng chất lượng tốt.', N'https://placehold.co/200x80/FF6900/FFFFFF?text=Xiaomi', N'https://www.xiaomi.com', 1, GETDATE(), GETDATE()),
    (N'OPPO', N'oppo', N'Thương hiệu smartphone Trung Quốc, nổi tiếng với camera selfie và công nghệ sạc nhanh VOOC.', N'https://placehold.co/200x80/00A950/FFFFFF?text=OPPO', N'https://www.oppo.com', 1, GETDATE(), GETDATE()),
    (N'Sony', N'sony', N'Tập đoàn điện tử khổng lồ của Nhật Bản, nổi tiếng với PlayStation, TV Bravia, và máy ảnh Alpha.', N'https://placehold.co/200x80/000000/FFFFFF?text=Sony', N'https://www.sony.com', 1, GETDATE(), GETDATE());

PRINT '  -> 5 brands inserted.';
PRINT '';

-- =====================================================
-- 6. INSERT PRODUCTS (10 products)
-- =====================================================
PRINT 'Inserting Products...';

INSERT INTO Products (name, description, image_url, price, original_price, stock_quantity, is_available, rating, is_new, is_hot, discount_percent, specifications, category_id, supplier_id, created_at, updated_at)
VALUES
    -- 1. iPhone 15 Pro Max
    (N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch. Thiết kế titanium cao cấp, khung nhôm chắc chắn.',
     N'https://placehold.co/600x600/333333/FFFFFF?text=iPhone+15+Pro+Max',
     34990000.00, 37990000.00, 50, 1, 4.8, 1, 1, 8,
     N'Màn hình: 6.7" Super Retina XDR; Chip: A17 Pro; RAM: 8GB; Bộ nhớ: 256GB; Pin: 4422mAh; Camera: 48MP + 12MP + 12MP',
     1, 1, GETDATE(), GETDATE()),

    -- 2. Samsung Galaxy S24 Ultra
    (N'Samsung Galaxy S24 Ultra 256GB', N'Samsung Galaxy S24 Ultra với camera 200MP, chip Snapdragon 8 Gen 3, bút S Pen tích hợp.',
     N'https://placehold.co/600x600/1428A0/FFFFFF?text=Galaxy+S24+Ultra',
     29990000.00, 32990000.00, 40, 1, 4.7, 1, 1, 9,
     N'Màn hình: 6.8" Dynamic AMOLED 2X; Chip: Snapdragon 8 Gen 3; RAM: 12GB; Bộ nhớ: 256GB; Pin: 5000mAh; Camera: 200MP + 12MP + 10MP + 50MP',
     1, 2, GETDATE(), GETDATE()),

    -- 3. Xiaomi 14 Pro
    (N'Xiaomi 14 Pro 512GB', N'Xiaomi 14 Pro hợp tác với Leica, chip Snapdragon 8 Gen 3, sạc nhanh 120W.',
     N'https://placehold.co/600x600/FF6900/FFFFFF?text=Xiaomi+14+Pro',
     18990000.00, 21990000.00, 60, 1, 4.6, 0, 1, 14,
     N'Màn hình: 6.73" AMOLED; Chip: Snapdragon 8 Gen 3; RAM: 12GB; Bộ nhớ: 512GB; Pin: 4880mAh; Sạc: 120W; Camera: 50MP + 50MP + 50MP',
     1, 3, GETDATE(), GETDATE()),

    -- 4. OPPO Find X7 Pro
    (N'OPPO Find X7 Pro 256GB', N'OPPO Find X7 Pro với camera Hasselblad, chip MediaTek Dimensity 9300, sạc nhanh 100W.',
     N'https://placehold.co/600x600/00A950/FFFFFF?text=OPPO+Find+X7+Pro',
     16990000.00, 18990000.00, 35, 1, 4.5, 0, 0, 10,
     N'Màn hình: 6.82" LTPO AMOLED; Chip: Dimensity 9300; RAM: 12GB; Bộ nhớ: 256GB; Pin: 5000mAh; Sạc: 100W; Camera: 50MP + 50MP + 50MP',
     1, 4, GETDATE(), GETDATE()),

    -- 5. MacBook Pro M3 14 inch
    (N'MacBook Pro 14 inch M3 2024', N'MacBook Pro 14 inch với chip M3, màn hình Liquid Retina XDR, thời lượng pin lên đến 17 giờ.',
     N'https://placehold.co/600x600/333333/FFFFFF?text=MacBook+Pro+M3',
     42990000.00, 44990000.00, 25, 1, 4.9, 1, 1, 4,
     N'Màn hình: 14.2" Liquid Retina XDR; Chip: Apple M3; RAM: 16GB; Bộ nhớ: 512GB SSD; Pin: 17h; GPU: 10-core',
     2, 1, GETDATE(), GETDATE()),

    -- 6. Samsung Galaxy Book4 Pro
    (N'Samsung Galaxy Book4 Pro 360', N'Laptop 2-trong-1 với màn hình AMOLED 14 inch, chip Intel Core Ultra 7, hỗ trợ S Pen.',
     N'https://placehold.co/600x600/1428A0/FFFFFF?text=Galaxy+Book4+Pro',
     35990000.00, 38990000.00, 20, 1, 4.5, 0, 0, 8,
     N'Màn hình: 14" AMOLED 2X Touch; CPU: Intel Core Ultra 7; RAM: 16GB; Bộ nhớ: 512GB SSD; Pin: 63Wh; Trọng lượng: 1.66kg',
     2, 2, GETDATE(), GETDATE()),

    -- 7. iPad Pro M4 12.9 inch
    (N'iPad Pro 12.9 inch M4 256GB', N'iPad Pro với chip M4, màn hình Liquid Retina XDR, hỗ trợ Apple Pencil Pro và Magic Keyboard.',
     N'https://placehold.co/600x600/333333/FFFFFF?text=iPad+Pro+M4',
     30990000.00, 32990000.00, 30, 1, 4.8, 1, 1, 6,
     N'Màn hình: 12.9" Liquid Retina XDR; Chip: Apple M4; RAM: 8GB; Bộ nhớ: 256GB; Pin: 40.88Wh; Camera: 12MP + 10MP',
     3, 1, GETDATE(), GETDATE()),

    -- 8. Samsung Galaxy Tab S9 Ultra
    (N'Samsung Galaxy Tab S9 Ultra', N'Máy tính bảng cao cấp với màn hình Dynamic AMOLED 2X 14.6 inch, S Pen đi kèm.',
     N'https://placehold.co/600x600/1428A0/FFFFFF?text=Tab+S9+Ultra',
     24990000.00, 27990000.00, 15, 1, 4.6, 0, 0, 10,
     N'Màn hình: 14.6" Dynamic AMOLED 2X; CPU: Snapdragon 8 Gen 2; RAM: 12GB; Bộ nhớ: 256GB; Pin: 11200mAh; Camera: 13MP + 8MP',
     3, 2, GETDATE(), GETDATE()),

    -- 9. Apple Watch Ultra 2
    (N'Apple Watch Ultra 2', N'Apple Watch cao cấp dành cho thể thao mạnh mẽ, màn hình OLED 49mm, GPS + Cellular.',
     N'https://placehold.co/600x600/333333/FFFFFF?text=Apple+Watch+Ultra+2',
     22990000.00, 24990000.00, 20, 1, 4.7, 0, 1, 8,
     N'Màn hình: 49mm OLED; Chip: Apple S9; RAM: 64GB; Pin: 36h; Chống nước: 100m; GPS + Cellular',
     5, 1, GETDATE(), GETDATE()),

    -- 10. AirPods Pro 2
    (N'AirPods Pro 2 (USB-C)', N'Tai nghe không dây chống ồi chủ động, chip H2, thời lượng pin 6 giờ, sạc qua USB-C.',
     N'https://placehold.co/600x600/333333/FFFFFF?text=AirPods+Pro+2',
     5990000.00, 6490000.00, 100, 1, 4.8, 0, 1, 8,
     N'Chống ồn: ANC chủ động; Chip: Apple H2; Pin: 6h (tai nghe), 30h (hộp sạc); Sạc: USB-C; Bluetooth: 5.3',
     4, 1, GETDATE(), GETDATE());

PRINT '  -> 10 products inserted.';
PRINT '';

-- =====================================================
-- 7. INSERT PRODUCT VARIANTS
-- =====================================================
PRINT 'Inserting Product Variants...';

INSERT INTO ProductVariants (product_id, color, storage, ram, variant_name, sku, price, original_price, stock_quantity, display_order, is_active, created_at)
VALUES
    -- iPhone 15 Pro Max variants (product_id=1)
    (1, N'Natural Titanium', N'256GB', N'8GB', N'iPhone 15 Pro Max 256GB Natural Titanium', N'IP15PM-256-NT', 34990000.00, 37990000.00, 20, 1, 1, GETDATE()),
    (1, N'Black Titanium', N'256GB', N'8GB', N'iPhone 15 Pro Max 256GB Black Titanium', N'IP15PM-256-BT', 34990000.00, 37990000.00, 15, 2, 1, GETDATE()),
    (1, N'White Titanium', N'256GB', N'8GB', N'iPhone 15 Pro Max 256GB White Titanium', N'IP15PM-256-WT', 34990000.00, 37990000.00, 15, 3, 1, GETDATE()),

    -- Samsung Galaxy S24 Ultra variants (product_id=2)
    (2, N'Titanium Black', N'256GB', N'12GB', N'Galaxy S24 Ultra 256GB Titanium Black', N'S24U-256-TB', 29990000.00, 32990000.00, 20, 1, 1, GETDATE()),
    (2, N'Titanium Gray', N'256GB', N'12GB', N'Galaxy S24 Ultra 256GB Titanium Gray', N'S24U-256-TG', 29990000.00, 32990000.00, 20, 2, 1, GETDATE()),

    -- MacBook Pro M3 variants (product_id=5)
    (5, N'Space Gray', N'512GB', N'16GB', N'MacBook Pro 14" M3 512GB Space Gray', N'MBP14-M3-512-SG', 42990000.00, 44990000.00, 13, 1, 1, GETDATE()),
    (5, N'Silver', N'512GB', N'16GB', N'MacBook Pro 14" M3 512GB Silver', N'MBP14-M3-512-SL', 42990000.00, 44990000.00, 12, 2, 1, GETDATE()),

    -- iPad Pro M4 variants (product_id=7)
    (7, N'Space Black', N'256GB', N'8GB', N'iPad Pro 12.9" M4 256GB Space Black', N'IPDP12-M4-256-SB', 30990000.00, 32990000.00, 15, 1, 1, GETDATE()),
    (7, N'Silver', N'256GB', N'8GB', N'iPad Pro 12.9" M4 256GB Silver', N'IPDP12-M4-256-SL', 30990000.00, 32990000.00, 15, 2, 1, GETDATE()),

    -- AirPods Pro 2 variants (product_id=10)
    (10, N'White', N'NULL', N'NULL', N'AirPods Pro 2 (USB-C) White', N'APP2-WHT', 5990000.00, 6490000.00, 50, 1, 1, GETDATE()),
    (10, N'White with MagSafe', N'NULL', N'NULL', N'AirPods Pro 2 (USB-C) MagSafe', N'APP2-MAG', 5990000.00, 6490000.00, 50, 2, 1, GETDATE());

PRINT '  -> 11 product variants inserted.';
PRINT '';

-- =====================================================
-- 8. INSERT SLIDES (5 slides)
-- =====================================================
PRINT 'Inserting Slides...';

INSERT INTO Slides (title, subtitle, image_url, link, button_text, display_order, is_active, created_at, updated_at)
VALUES
    (N'🎉 SIÊU SALE MÙA HÈ 2026', N'Giảm đến 30% cho tất cả sản phẩm iPhone, MacBook và Apple Watch. Quà tặng kèm hấp dẫn!',
     N'https://placehold.co/1200x400/112D4E/FFFFFF?text=Slide+1', N'/products/?category=dien-thoai', N'Mua ngay', 1, 1, GETDATE(), GETDATE()),

    (N'📱 iPhone 15 Series - Trải nghiệm tương lai', N'Chip A17 Pro mạnh mẽ, camera 48MP, thiết kế titanium cao cấp.',
     N'https://placehold.co/1200x400/3498db/FFFFFF?text=Slide+2', N'/products/iphone-15-pro-max/', N'Khám phá ngay', 2, 1, GETDATE(), GETDATE()),

    (N'💻 MacBook Pro M3 - Sức mạnh vượt trội', N'Thiết kế siêu mỏng, chip M3 thế hệ mới, thời lượng pin lên đến 17 giờ.',
     N'https://placehold.co/1200x400/2ecc71/FFFFFF?text=Slide+3', N'/products/macbook-pro-m3/', N'Đặt hàng ngay', 3, 1, GETDATE(), GETDATE()),

    (N'⌚ Apple Watch Ultra 2 - Cho ngày dài năng động', N'Chống nước 100m, GPS + Cellular, pin 36 giờ. Đồng hành cùng bạn mọi lúc.',
     N'https://placehold.co/1200x400/9b59b6/FFFFFF?text=Slide+4', N'/products/apple-watch-ultra-2/', N'Xem chi tiết', 4, 1, GETDATE(), GETDATE()),

    (N'🎧 AirPods Pro 2 - Âm thanh đỉnh cao', N'Chống ồn chủ động, chip H2, sạc USB-C. Đắm chìm trong thế giới âm nhạc.',
     N'https://placehold.co/1200x400/f39c12/FFFFFF?text=Slide+5', N'/products/airpods-pro-2/', N'Thêm vào giỏ', 5, 1, GETDATE(), GETDATE());

PRINT '  -> 5 slides inserted.';
PRINT '';

-- =====================================================
-- 9. INSERT REVIEWS (5 reviews)
-- =====================================================
PRINT 'Inserting Reviews...';

INSERT INTO Reviews (product_id, account_id, rating, title, comment, is_approved, created_at, updated_at)
VALUES
    -- Review 1: iPhone 15 Pro Max - Approved
    (1, 3, 5, N'👍 Điện thoại tốt nhất mình từng dùng!',
     N'Mình đã dùng iPhone 15 Pro Max được 1 tháng và rất hài lòng. Camera chụp ảnh cực kỳ đẹp, pin trâu, màn hình mượt. Khuyên everyone nên mua!',
     1, GETDATE(), GETDATE()),

    -- Review 2: MacBook Pro M3 - Approved
    (5, 4, 5, N'💻 MacBook Pro M3 - Worth every penny',
     N'Mình là designer nên cần máy mạnh. MacBook Pro M3 xử lý Photoshop, Figma cực nhanh, pin dùng cả ngày không lo hết. Quá tuyệt vời!',
     1, DATEADD(DAY, -3, GETDATE()), GETDATE()),

    -- Review 3: Samsung Galaxy S24 Ultra - Pending
    (2, 5, 4, N'📱 Samsung S24 Ultra - Gần như hoàn hảo',
     N'Điện thoại đẹp, camera 200MP chụp ảnh cực kỳ nét. Mình thích bút S Pen. Điểm trừ là giá hơi cao và máy hơi nặng.',
     0, DATEADD(DAY, -5, GETDATE()), GETDATE()),

    -- Review 4: AirPods Pro 2 - Approved
    (10, 3, 5, N'🎧 AirPods Pro 2 - Âm thanh đỉnh cao!',
     N'Tai nghe chống ồn cực tốt, nghe nhạc như đang ở phòng thu. Fit vừa tai, không rơi khi chạy bộ. Pin trâu. Mua ngay đi các bạn!',
     1, DATEADD(DAY, -7, GETDATE()), GETDATE()),

    -- Review 5: iPad Pro M4 - Pending
    (7, 4, 4, N'📱 iPad Pro M4 - Máy tính bảng tốt nhất hiện nay',
     N'Mình mua để thay thế laptop, dùng cho việc học và giải trí. M4 quá nhanh, màn hình đẹp. Trừ điểm vì giá Apple Pencil Pro quá mắc.',
     0, DATEADD(DAY, -2, GETDATE()), GETDATE());

PRINT '  -> 5 reviews inserted.';
PRINT '';

-- =====================================================
-- 10. INSERT ORDERS (5 orders)
-- =====================================================
PRINT 'Inserting Orders...';

INSERT INTO Orders (account_id, order_code, order_date, total_amount, status, customer_name, customer_phone, customer_address, notes, created_at, updated_at)
VALUES
    -- Order 1: Delivered
    (3, N'ORD-20260501-0001', DATEADD(DAY, -10, GETDATE()), 40980000.00, N'Delivered',
     N'Lê Minh Hoàng', N'0912345678', N'789 Điện Biên Phủ, Quận 3, TP.HCM',
     N'Giao giờ hành chính, không giao thứ 7 CN.',
     DATEADD(DAY, -10, GETDATE()), GETDATE()),

    -- Order 2: Shipped
    (4, N'ORD-20260503-0002', DATEADD(DAY, -5, GETDATE()), 42990000.00, N'Shipped',
     N'Phạm Thanh Long', N'0923456789', N'101 Lý Thường Kiệt, Quận 10, TP.HCM',
     N'Giao nhanh trong 24h.',
     DATEADD(DAY, -5, GETDATE()), GETDATE()),

    -- Order 3: Processing
    (5, N'ORD-20260505-0003', DATEADD(DAY, -3, GETDATE()), 19990000.00, N'Processing',
     N'Đặng Hoài Phương', N'0934567890', N'202 Pasteur, Quận 3, TP.HCM',
     N'Gọi xác nhận trước khi giao.',
     DATEADD(DAY, -3, GETDATE()), GETDATE()),

    -- Order 4: Confirmed
    (3, N'ORD-20260506-0004', DATEADD(DAY, -1, GETDATE()), 11980000.00, N'Confirmed',
     N'Lê Minh Hoàng', N'0912345678', N'789 Điện Biên Phủ, Quận 3, TP.HCM',
     NULL,
     DATEADD(DAY, -1, GETDATE()), GETDATE()),

    -- Order 5: Pending
    (NULL, N'ORD-20260507-0005', GETDATE(), 16990000.00, N'Pending',
     N'Nguyễn Văn Khách', N'0945678901', N'555 Nguyễn Trãi, Quận 5, TP.HCM',
     N'Khách hàng mới, cần xác minh thông tin.',
     GETDATE(), GETDATE());

PRINT '  -> 5 orders inserted.';
PRINT '';

-- =====================================================
-- 11. INSERT ORDER ITEMS
-- =====================================================
PRINT 'Inserting Order Items...';

INSERT INTO OrderItems (order_id, product_id, variant_id, product_name, variant_name, quantity, unit_price, subtotal)
VALUES
    -- Order 1 items: iPhone 15 Pro Max + AirPods Pro 2
    (1, 1, 1, N'iPhone 15 Pro Max 256GB', N'iPhone 15 Pro Max 256GB Natural Titanium', 1, 34990000.00, 34990000.00),
    (1, 10, 10, N'AirPods Pro 2 (USB-C)', N'AirPods Pro 2 (USB-C) White', 1, 5990000.00, 5990000.00),

    -- Order 2 items: MacBook Pro M3
    (2, 5, 6, N'MacBook Pro 14 inch M3 2024', N'MacBook Pro 14" M3 512GB Space Gray', 1, 42990000.00, 42990000.00),

    -- Order 3 items: Xiaomi 14 Pro
    (3, 3, NULL, N'Xiaomi 14 Pro 512GB', NULL, 1, 18990000.00, 18990000.00),

    -- Order 4 items: AirPods Pro 2 (2 cái)
    (4, 10, 11, N'AirPods Pro 2 (USB-C)', N'AirPods Pro 2 (USB-C) MagSafe', 2, 5990000.00, 11980000.00),

    -- Order 5 items: OPPO Find X7 Pro
    (5, 4, NULL, N'OPPO Find X7 Pro 256GB', NULL, 1, 16990000.00, 16990000.00);

PRINT '  -> 7 order items inserted.';
PRINT '';

-- =====================================================
-- 12. INSERT CART ITEMS
-- =====================================================
PRINT 'Inserting Cart Items...';

INSERT INTO CartItems (account_id, product_id, variant_id, quantity, added_at)
VALUES
    -- Customer 3 (khachhang01) cart
    (3, 2, 4, 1, GETDATE()),
    (3, 7, 8, 1, DATEADD(DAY, -2, GETDATE())),

    -- Customer 4 (khachhang02) cart
    (4, 8, NULL, 1, GETDATE()),
    (4, 9, NULL, 1, DATEADD(DAY, -1, GETDATE())),

    -- Customer 5 (khachhang03) cart
    (5, 3, NULL, 1, GETDATE()),
    (5, 10, 10, 2, GETDATE());

PRINT '  -> 6 cart items inserted.';
PRINT '';

-- =====================================================
-- 13. INSERT NOTIFICATIONS (10 notifications)
-- =====================================================
PRINT 'Inserting Notifications...';

INSERT INTO Notifications (account_id, type, title, message, is_read, link, created_at)
VALUES
    -- Notifications for Admin
    (1, N'System', N'Chào mừng Admin trở lại!', N'Bạn có 5 đơn hàng mới cần xử lý hôm nay.', 0, N'/admin/orders/', GETDATE()),

    -- Notifications for Employee
    (2, N'Order', N'Đơn hàng mới #ORD-20260507-0005', N'Có đơn hàng mới từ khách hàng Nguyễn Văn Khách trị giá 16,990,000 VNĐ.', 0, N'/employee/orders/', GETDATE()),

    -- Notifications for Customer 3
    (3, N'Order', N'Đơn hàng đã giao thành công!', N'Đơn hàng ORD-20260501-0001 của bạn đã được giao thành công. Cảm ơn bạn đã mua sắm!', 1, N'/orders/ORD-20260501-0001/', DATEADD(DAY, -8, GETDATE())),
    (3, N'Promotion', N'🎉 Khuyến mãi mùa hè 2026!', N'Giảm đến 30% cho tất cả sản phẩm Apple. Hãy nhanh tay mua ngay!', 0, N'/promotions/summer-2026/', DATEADD(DAY, -1, GETDATE())),

    -- Notifications for Customer 4
    (4, N'Order', N'Đơn hàng đang được vận chuyển!', N'Đơn hàng ORD-20260503-0002 của bạn đang được giao đến. Dự kiến 2 ngày nữa sẽ nhận được.', 0, N'/orders/ORD-20260503-0002/', DATEADD(DAY, -3, GETDATE())),
    (4, N'System', N'Giao hàng thành công', N'Cảm ơn bạn đã mua sắm tại AITeStore. Hãy để lại đánh giá sản phẩm nhé!', 1, N'/orders/ORD-20260503-0002/', DATEADD(DAY, -1, GETDATE())),

    -- Notifications for Customer 5
    (5, N'Order', N'Xác nhận đơn hàng ORD-20260505-0003', N'Đơn hàng của bạn đang được xử lý. Chúng tôi sẽ sớm giao đến bạn.', 1, N'/orders/ORD-20260505-0003/', DATEADD(DAY, -2, GETDATE())),

    -- General notifications (NULL account_id - broadcast)
    (NULL, N'Promotion', N'🔔 iPhone 15 Series - Giảm 8%', N'iPhone 15 Pro Max và iPhone 15 Pro đang được giảm giá đặc biệt. Chỉ còn vài ngày!', 0, N'/products/?category=dien-thoai', DATEADD(DAY, -5, GETDATE())),
    (NULL, N'System', N'Mở cửa hàng mới tại Quận 7', N'AITeStore hân hạnh thông báo khai trương chi nhánh mới tại Quận 7, TP.HCM!', 0, N'/stores/', DATEADD(DAY, -7, GETDATE()));

PRINT '  -> 10 notifications inserted.';
PRINT '';

PRINT '=====================================================';
PRINT ' Sample data inserted successfully!                ';
PRINT '  - 5 Accounts (1 Admin, 1 Employee, 3 Customers)   ';
PRINT '  - 1 Employee record                                ';
PRINT '  - 5 Categories                                    ';
PRINT '  - 5 Suppliers                                     ';
PRINT '  - 5 Brands                                        ';
PRINT '  - 10 Products                                     ';
PRINT '  - 11 Product Variants                             ';
PRINT '  - 5 Slides                                        ';
PRINT '  - 5 Reviews                                       ';
PRINT '  - 5 Orders                                        ';
PRINT '  - 7 Order Items                                   ';
PRINT '  - 6 Cart Items                                    ';
PRINT '  - 10 Notifications                                ';
PRINT '=====================================================';
PRINT '';
PRINT 'IMPORTANT: Passwords are NULL. To set passwords:';
PRINT '  1. Run: python manage.py shell';
PRINT '  2. Execute:';
PRINT '     >>> from apps.users.models import Account';
PRINT '     >>> u = Account.objects.get(username="admin")';
PRINT '     >>> u.set_password("your_password_here")';
PRINT '     >>> u.save()';
PRINT '=====================================================';
