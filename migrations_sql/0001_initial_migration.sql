-- =====================================================
-- SQL Server Migration: 0001_initial_migration.sql
-- Creates all tables for the AI Tech Store Django project
-- Database: SQL Server
-- =====================================================

-- Suppress row count messages for cleaner output
SET NOCOUNT ON;

PRINT '=====================================================';
PRINT ' Starting Migration: 0001_initial_migration.sql   ';
PRINT '=====================================================';
PRINT '';

-- =====================================================
-- 1. ACCOUNTS TABLE
-- =====================================================
PRINT 'Creating table: Accounts...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Accounts')
BEGIN
    CREATE TABLE Accounts (
        account_id    INT IDENTITY(1,1) PRIMARY KEY,
        username      NVARCHAR(50)  UNIQUE NOT NULL,
        password_hash NVARCHAR(255) NULL,
        email         NVARCHAR(100) UNIQUE NULL,
        full_name     NVARCHAR(100) NULL,
        phone         NVARCHAR(20)  NULL,
        address       NVARCHAR(255) NULL,
        is_active     BIT DEFAULT 1,
        role          NVARCHAR(20) DEFAULT N'Customer',
        reset_token   NVARCHAR(64) NULL,
        reset_token_expiry DATETIME NULL,
        created_at    DATETIME DEFAULT GETDATE(),
        updated_at    DATETIME DEFAULT GETDATE()
    );
    PRINT '  -> Accounts table created successfully.';
END
ELSE
    PRINT '  -> Accounts table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 2. EMPLOYEES TABLE
-- =====================================================
PRINT 'Creating table: Employees...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    CREATE TABLE Employees (
        employee_id    INT IDENTITY(1,1) PRIMARY KEY,
        account_id     INT NULL,
        employee_code  NVARCHAR(10) UNIQUE NULL,
        department     NVARCHAR(50) NULL,
        position       NVARCHAR(50) NULL,
        hire_date      DATE NULL,
        salary         INT NULL,
        is_active      BIT DEFAULT 1,
        created_at     DATETIME DEFAULT GETDATE(),
        updated_at     DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Employees_Accounts FOREIGN KEY (account_id)
            REFERENCES Accounts(account_id) ON DELETE SET NULL
    );
    PRINT '  -> Employees table created successfully.';
END
ELSE
    PRINT '  -> Employees table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 3. CATEGORIES TABLE
-- =====================================================
PRINT 'Creating table: Categories...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categories')
BEGIN
    CREATE TABLE Categories (
        category_id     INT IDENTITY(1,1) PRIMARY KEY,
        name            NVARCHAR(100) UNIQUE NOT NULL,
        description     NVARCHAR(MAX) NULL,
        image_url       NVARCHAR(500) NULL,
        display_order   INT DEFAULT 0,
        is_active       BIT DEFAULT 1,
        created_at      DATETIME DEFAULT GETDATE(),
        updated_at      DATETIME DEFAULT GETDATE()
    );
    PRINT '  -> Categories table created successfully.';
END
ELSE
    PRINT '  -> Categories table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 4. SUPPLIERS TABLE
-- =====================================================
PRINT 'Creating table: Suppliers...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Suppliers')
BEGIN
    CREATE TABLE Suppliers (
        supplier_id     INT IDENTITY(1,1) PRIMARY KEY,
        name            NVARCHAR(255) NOT NULL,
        contact_person  NVARCHAR(100) NULL,
        phone           NVARCHAR(20) NULL,
        email           NVARCHAR(100) NULL,
        address         NVARCHAR(255) NULL,
        is_active       BIT DEFAULT 1,
        created_at      DATETIME DEFAULT GETDATE(),
        updated_at      DATETIME DEFAULT GETDATE()
    );
    PRINT '  -> Suppliers table created successfully.';
END
ELSE
    PRINT '  -> Suppliers table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 5. BRANDS TABLE
-- =====================================================
PRINT 'Creating table: Brands...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Brands')
BEGIN
    CREATE TABLE Brands (
        brand_id     INT IDENTITY(1,1) PRIMARY KEY,
        name         NVARCHAR(255) UNIQUE NOT NULL,
        slug         NVARCHAR(255) UNIQUE NULL,
        description  NVARCHAR(MAX) NULL,
        logo_url     NVARCHAR(500) NULL,
        website      NVARCHAR(255) NULL,
        is_active    BIT DEFAULT 1,
        created_at   DATETIME DEFAULT GETDATE(),
        updated_at   DATETIME DEFAULT GETDATE()
    );
    PRINT '  -> Brands table created successfully.';
END
ELSE
    PRINT '  -> Brands table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 6. PRODUCTS TABLE
-- =====================================================
PRINT 'Creating table: Products...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    CREATE TABLE Products (
        product_id         INT IDENTITY(1,1) PRIMARY KEY,
        name               NVARCHAR(255) NOT NULL,
        description        NVARCHAR(MAX) NULL,
        image_url          NVARCHAR(500) NULL,
        price              DECIMAL(10,2) NOT NULL,
        original_price     DECIMAL(10,2) NULL,
        stock_quantity     INT DEFAULT 0,
        is_available      BIT DEFAULT 1,
        rating             DECIMAL(2,1) DEFAULT 4.5,
        is_new             BIT DEFAULT 0,
        is_hot             BIT DEFAULT 0,
        discount_percent   INT DEFAULT 0,
        specifications     NVARCHAR(MAX) NULL,
        category_id        INT NULL,
        supplier_id        INT NULL,
        created_at         DATETIME DEFAULT GETDATE(),
        updated_at         DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Products_Categories FOREIGN KEY (category_id)
            REFERENCES Categories(category_id) ON DELETE SET NULL,
        CONSTRAINT FK_Products_Suppliers FOREIGN KEY (supplier_id)
            REFERENCES Suppliers(supplier_id) ON DELETE SET NULL
    );
    PRINT '  -> Products table created successfully.';
END
ELSE
    PRINT '  -> Products table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 7. PRODUCT VARIANTS TABLE
-- =====================================================
PRINT 'Creating table: ProductVariants...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProductVariants')
BEGIN
    CREATE TABLE ProductVariants (
        variant_id      INT IDENTITY(1,1) PRIMARY KEY,
        product_id      INT NOT NULL,
        color           NVARCHAR(50) NULL,
        storage         NVARCHAR(20) NULL,
        ram             NVARCHAR(20) NULL,
        variant_name    NVARCHAR(100) NOT NULL,
        sku             NVARCHAR(50) UNIQUE NULL,
        price           DECIMAL(10,2) NULL,
        original_price  DECIMAL(10,2) NULL,
        stock_quantity  INT DEFAULT 0,
        display_order   INT DEFAULT 0,
        is_active       BIT DEFAULT 1,
        created_at      DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_ProductVariants_Products FOREIGN KEY (product_id)
            REFERENCES Products(product_id) ON DELETE CASCADE
    );
    PRINT '  -> ProductVariants table created successfully.';
END
ELSE
    PRINT '  -> ProductVariants table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 8. PRODUCT IMAGES TABLE
-- =====================================================
PRINT 'Creating table: ProductImages...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProductImages')
BEGIN
    CREATE TABLE ProductImages (
        image_id      INT IDENTITY(1,1) PRIMARY KEY,
        product_id    INT NOT NULL,
        image_url     NVARCHAR(500) NOT NULL,
        display_order INT DEFAULT 0,
        is_primary    BIT DEFAULT 0,
        created_at    DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_ProductImages_Products FOREIGN KEY (product_id)
            REFERENCES Products(product_id) ON DELETE CASCADE
    );
    PRINT '  -> ProductImages table created successfully.';
END
ELSE
    PRINT '  -> ProductImages table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 9. ORDERS TABLE
-- =====================================================
PRINT 'Creating table: Orders...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
BEGIN
    CREATE TABLE Orders (
        order_id          INT IDENTITY(1,1) PRIMARY KEY,
        account_id        INT NULL,
        order_code        NVARCHAR(50) UNIQUE NOT NULL,
        order_date        DATETIME DEFAULT GETDATE(),
        total_amount      DECIMAL(12,2) NOT NULL,
        status            NVARCHAR(20) DEFAULT N'Pending',
        customer_name     NVARCHAR(100) NULL,
        customer_phone    NVARCHAR(20) NULL,
        customer_address  NVARCHAR(255) NULL,
        notes             NVARCHAR(MAX) NULL,
        created_at        DATETIME DEFAULT GETDATE(),
        updated_at        DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Orders_Accounts FOREIGN KEY (account_id)
            REFERENCES Accounts(account_id) ON DELETE SET NULL
    );
    PRINT '  -> Orders table created successfully.';
END
ELSE
    PRINT '  -> Orders table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 10. ORDER ITEMS TABLE
-- =====================================================
PRINT 'Creating table: OrderItems...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'OrderItems')
BEGIN
    CREATE TABLE OrderItems (
        item_id       INT IDENTITY(1,1) PRIMARY KEY,
        order_id      INT NOT NULL,
        product_id    INT NULL,
        variant_id    INT NULL,
        product_name  NVARCHAR(255) NOT NULL,
        variant_name  NVARCHAR(100) NULL,
        quantity      INT NOT NULL,
        unit_price    DECIMAL(10,2) NOT NULL,
        subtotal      DECIMAL(12,2) NOT NULL,
        CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (order_id)
            REFERENCES Orders(order_id) ON DELETE CASCADE,
        CONSTRAINT FK_OrderItems_Products FOREIGN KEY (product_id)
            REFERENCES Products(product_id) ON DELETE SET NULL,
        CONSTRAINT FK_OrderItems_ProductVariants FOREIGN KEY (variant_id)
            REFERENCES ProductVariants(variant_id) ON DELETE SET NULL
    );
    PRINT '  -> OrderItems table created successfully.';
END
ELSE
    PRINT '  -> OrderItems table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 11. CART ITEMS TABLE
-- =====================================================
PRINT 'Creating table: CartItems...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CartItems')
BEGIN
    CREATE TABLE CartItems (
        cart_item_id  INT IDENTITY(1,1) PRIMARY KEY,
        account_id    INT NULL,
        product_id    INT NULL,
        variant_id    INT NULL,
        quantity      INT DEFAULT 1,
        added_at      DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_CartItems_Accounts FOREIGN KEY (account_id)
            REFERENCES Accounts(account_id) ON DELETE CASCADE,
        CONSTRAINT FK_CartItems_Products FOREIGN KEY (product_id)
            REFERENCES Products(product_id) ON DELETE CASCADE,
        CONSTRAINT FK_CartItems_ProductVariants FOREIGN KEY (variant_id)
            REFERENCES ProductVariants(variant_id) ON DELETE SET NULL
    );
    PRINT '  -> CartItems table created successfully.';
END
ELSE
    PRINT '  -> CartItems table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 12. REVIEWS TABLE
-- =====================================================
PRINT 'Creating table: Reviews...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reviews')
BEGIN
    CREATE TABLE Reviews (
        review_id    INT IDENTITY(1,1) PRIMARY KEY,
        product_id   INT NOT NULL,
        account_id   INT NULL,
        rating       INT NOT NULL DEFAULT 5,
        title        NVARCHAR(255) NULL,
        comment      NVARCHAR(MAX) NULL,
        is_approved  BIT DEFAULT 0,
        created_at   DATETIME DEFAULT GETDATE(),
        updated_at   DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Reviews_Products FOREIGN KEY (product_id)
            REFERENCES Products(product_id) ON DELETE CASCADE,
        CONSTRAINT FK_Reviews_Accounts FOREIGN KEY (account_id)
            REFERENCES Accounts(account_id) ON DELETE SET NULL,
        CONSTRAINT CK_Reviews_Rating CHECK (rating >= 1 AND rating <= 5)
    );
    PRINT '  -> Reviews table created successfully.';
END
ELSE
    PRINT '  -> Reviews table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 13. NOTIFICATIONS TABLE
-- =====================================================
PRINT 'Creating table: Notifications...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Notifications')
BEGIN
    CREATE TABLE Notifications (
        notification_id  INT IDENTITY(1,1) PRIMARY KEY,
        account_id       INT NULL,
        type             NVARCHAR(50) DEFAULT N'System',
        title            NVARCHAR(255) NOT NULL,
        message          NVARCHAR(MAX) NOT NULL,
        is_read          BIT DEFAULT 0,
        link             NVARCHAR(255) NULL,
        created_at       DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Notifications_Accounts FOREIGN KEY (account_id)
            REFERENCES Accounts(account_id) ON DELETE CASCADE
    );
    PRINT '  -> Notifications table created successfully.';
END
ELSE
    PRINT '  -> Notifications table already exists. Skipping.';
PRINT '';

-- =====================================================
-- 14. SLIDES TABLE
-- =====================================================
PRINT 'Creating table: Slides...';

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Slides')
BEGIN
    CREATE TABLE Slides (
        slide_id        INT IDENTITY(1,1) PRIMARY KEY,
        title           NVARCHAR(255) NOT NULL,
        subtitle        NVARCHAR(255) NULL,
        image_url       NVARCHAR(500) NOT NULL,
        link            NVARCHAR(255) NULL,
        button_text     NVARCHAR(50) NULL,
        display_order   INT DEFAULT 0,
        is_active       BIT DEFAULT 1,
        created_at      DATETIME DEFAULT GETDATE(),
        updated_at      DATETIME DEFAULT GETDATE()
    );
    PRINT '  -> Slides table created successfully.';
END
ELSE
    PRINT '  -> Slides table already exists. Skipping.';
PRINT '';

-- =====================================================
-- CREATE INDEXES for better query performance
-- =====================================================
PRINT 'Creating indexes...';

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_CategoryId' AND object_id = OBJECT_ID('Products'))
    CREATE INDEX IX_Products_CategoryId ON Products(category_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_SupplierId' AND object_id = OBJECT_ID('Products'))
    CREATE INDEX IX_Products_SupplierId ON Products(supplier_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_IsAvailable' AND object_id = OBJECT_ID('Products'))
    CREATE INDEX IX_Products_IsAvailable ON Products(is_available);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Orders_AccountId' AND object_id = OBJECT_ID('Orders'))
    CREATE INDEX IX_Orders_AccountId ON Orders(account_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Orders_Status' AND object_id = OBJECT_ID('Orders'))
    CREATE INDEX IX_Orders_Status ON Orders(status);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_OrderItems_OrderId' AND object_id = OBJECT_ID('OrderItems'))
    CREATE INDEX IX_OrderItems_OrderId ON OrderItems(order_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Reviews_ProductId' AND object_id = OBJECT_ID('Reviews'))
    CREATE INDEX IX_Reviews_ProductId ON Reviews(product_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Notifications_AccountId' AND object_id = OBJECT_ID('Notifications'))
    CREATE INDEX IX_Notifications_AccountId ON Notifications(account_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_CartItems_AccountId' AND object_id = OBJECT_ID('CartItems'))
    CREATE INDEX IX_CartItems_AccountId ON CartItems(account_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ProductVariants_ProductId' AND object_id = OBJECT_ID('ProductVariants'))
    CREATE INDEX IX_ProductVariants_ProductId ON ProductVariants(product_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ProductImages_ProductId' AND object_id = OBJECT_ID('ProductImages'))
    CREATE INDEX IX_ProductImages_ProductId ON ProductImages(product_id);

PRINT '  -> Indexes created successfully.';
PRINT '';

PRINT '=====================================================';
PRINT ' Migration completed successfully!                ';
PRINT ' All tables and indexes have been created.         ';
PRINT '=====================================================';
