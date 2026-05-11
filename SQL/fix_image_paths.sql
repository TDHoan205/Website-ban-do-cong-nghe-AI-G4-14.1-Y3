-- =====================================================
-- SUA DUONG DAN ANH TRONG DATABASE
-- Chay script nay de sua tat ca duong dan anh bi loi
-- =====================================================
USE TechShopWebsite1;
GO

PRINT '=====================================================';
PRINT '  SUA DUONG DAN ANH TRONG DATABASE';
PRINT '=====================================================';
PRINT '';

-- 1. Sua bang Products
PRINT 'Dang sua bang Products...';
UPDATE Products SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Products';

-- 2. Sua bang ProductImages
PRINT 'Dang sua bang ProductImages...';
UPDATE ProductImages SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong ProductImages';

-- 3. Sua bang ProductColorImages
PRINT 'Dang sua bang ProductColorImages...';
UPDATE ProductColorImages SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong ProductColorImages';

-- 4. Sua bang Categories
PRINT 'Dang sua bang Categories...';
UPDATE Categories SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Categories';

-- 5. Sua bang Brands
PRINT 'Dang sua bang Brands...';
UPDATE Brands SET logo_url = REPLACE(logo_url, '/images/', '/static/images/') WHERE logo_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Brands';

-- 6. Sua bang Slides
PRINT 'Dang sua bang Slides...';
UPDATE Slides SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Slides';

-- 7. Sua bang Banners
PRINT 'Dang sua bang Banners...';
UPDATE Banners SET image_url = REPLACE(image_url, '/images/', '/static/images/') WHERE image_url LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Banners';

-- 8. Sua bang Accounts (avatar)
PRINT 'Dang sua bang Accounts (avatar)...';
UPDATE Accounts SET avatar = REPLACE(avatar, '/images/', '/static/images/') WHERE avatar LIKE '/images/%';
PRINT '  -> Da sua duong dan trong Accounts';

PRINT '';
PRINT '=====================================================';
PRINT '  HOAN THANH SUA DUONG DAN ANH!';
PRINT '=====================================================';
PRINT '';
PRINT 'Bay gio cac anh se hien thi dung tren website.';
PRINT '=====================================================';
GO
