-- =====================================================
-- Tech Store - Database Schema
-- SQL Server - Tương thích với ASP.NET Core EF Core
-- =====================================================

-- Tạo Database nếu chưa có
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'TechShopWebsite1')
BEGIN
    CREATE DATABASE TechShopWebsite1;
END
GO

USE TechShopWebsite1;
GO

-- =====================================================
-- Categories Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categories')
BEGIN
    CREATE TABLE Categories (
        category_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL UNIQUE,
        description NVARCHAR(MAX),
        image_url NVARCHAR(500),
        display_order INT DEFAULT 0,
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- =====================================================
-- Suppliers Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Suppliers')
BEGIN
    CREATE TABLE Suppliers (
        supplier_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL,
        contact_person NVARCHAR(100),
        phone NVARCHAR(20),
        email NVARCHAR(100),
        address NVARCHAR(255),
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- =====================================================
-- Users Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) NOT NULL UNIQUE,
        email NVARCHAR(100) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        full_name NVARCHAR(100),
        phone NVARCHAR(20),
        address NVARCHAR(255),
        is_active BIT DEFAULT 1,
        role NVARCHAR(20) DEFAULT 'Customer',
        avatar_url NVARCHAR(500),
        reset_token NVARCHAR(64),
        reset_token_expiry DATETIME,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME
    );
END
GO

-- =====================================================
-- Products Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    CREATE TABLE Products (
        product_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL,
        description NVARCHAR(MAX),
        image_url NVARCHAR(500),
        price DECIMAL(10, 2) NOT NULL,
        original_price DECIMAL(10, 2),
        stock_quantity INT DEFAULT 50,
        rating DECIMAL(2, 1) DEFAULT 4.5,
        is_new BIT DEFAULT 0,
        is_hot BIT DEFAULT 0,
        discount_percent INT DEFAULT 0,
        specifications NVARCHAR(MAX),
        category_id INT,
        supplier_id INT,
        is_available BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    );
END
GO

-- =====================================================
-- ProductVariants Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProductVariants')
BEGIN
    CREATE TABLE ProductVariants (
        variant_id INT IDENTITY(1,1) PRIMARY KEY,
        product_id INT NOT NULL,
        color NVARCHAR(50),
        storage NVARCHAR(20),
        ram NVARCHAR(20),
        variant_name NVARCHAR(100),
        sku NVARCHAR(50),
        price DECIMAL(10, 2),
        original_price DECIMAL(10, 2),
        stock_quantity INT DEFAULT 0,
        display_order INT DEFAULT 0,
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
    );
END
GO

-- =====================================================
-- ProductImages Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProductImages')
BEGIN
    CREATE TABLE ProductImages (
        image_id INT IDENTITY(1,1) PRIMARY KEY,
        product_id INT NOT NULL,
        image_url NVARCHAR(500) NOT NULL,
        display_order INT DEFAULT 0,
        is_primary BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
    );
END
GO

-- =====================================================
-- Inventory Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Inventory')
BEGIN
    CREATE TABLE Inventory (
        inventory_id INT IDENTITY(1,1) PRIMARY KEY,
        product_id INT NOT NULL UNIQUE,
        quantity_in_stock INT DEFAULT 0,
        min_stock_level INT DEFAULT 5,
        max_stock_level INT DEFAULT 100,
        last_restock_date DATETIME,
        updated_at DATETIME,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
END
GO

-- =====================================================
-- Carts Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Carts')
BEGIN
    CREATE TABLE Carts (
        cart_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL UNIQUE,
        session_id NVARCHAR(100),
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
END
GO

-- =====================================================
-- CartItems Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CartItems')
BEGIN
    CREATE TABLE CartItems (
        cart_item_id INT IDENTITY(1,1) PRIMARY KEY,
        cart_id INT NOT NULL,
        product_id INT NOT NULL,
        variant_id INT,
        quantity INT NOT NULL DEFAULT 1,
        added_date DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id)
    );
END
GO

-- =====================================================
-- Orders Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
BEGIN
    CREATE TABLE Orders (
        order_id INT IDENTITY(1,1) PRIMARY KEY,
        order_number NVARCHAR(50) NOT NULL UNIQUE,
        user_id INT NOT NULL,
        status NVARCHAR(20) DEFAULT 'Pending',
        subtotal DECIMAL(10, 2) NOT NULL,
        shipping_fee DECIMAL(10, 2) DEFAULT 0,
        tax_amount DECIMAL(10, 2) DEFAULT 0,
        total_amount DECIMAL(10, 2) NOT NULL,
        shipping_address NVARCHAR(500),
        shipping_phone NVARCHAR(20),
        shipping_name NVARCHAR(100),
        notes NVARCHAR(MAX),
        order_date DATETIME DEFAULT GETDATE(),
        confirmed_date DATETIME,
        shipped_date DATETIME,
        delivered_date DATETIME,
        cancelled_date DATETIME,
        cancellation_reason NVARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
END
GO

-- =====================================================
-- OrderItems Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'OrderItems')
BEGIN
    CREATE TABLE OrderItems (
        order_item_id INT IDENTITY(1,1) PRIMARY KEY,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        variant_id INT,
        product_name NVARCHAR(255) NOT NULL,
        variant_name NVARCHAR(100),
        quantity INT NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        subtotal DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id)
    );
END
GO

-- =====================================================
-- Payments Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Payments')
BEGIN
    CREATE TABLE Payments (
        payment_id INT IDENTITY(1,1) PRIMARY KEY,
        order_id INT NOT NULL UNIQUE,
        payment_method NVARCHAR(50),
        payment_status NVARCHAR(20) DEFAULT 'Pending',
        transaction_id NVARCHAR(100),
        amount DECIMAL(10, 2) NOT NULL,
        payment_date DATETIME,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    );
END
GO

-- =====================================================
-- Shipments Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Shipments')
BEGIN
    CREATE TABLE Shipments (
        shipment_id INT IDENTITY(1,1) PRIMARY KEY,
        order_id INT NOT NULL UNIQUE,
        shipping_method NVARCHAR(50),
        tracking_number NVARCHAR(100),
        shipping_status NVARCHAR(20) DEFAULT 'Pending',
        estimated_delivery DATETIME,
        actual_delivery DATETIME,
        shipping_note NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    );
END
GO

-- =====================================================
-- ChatSessions Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ChatSessions')
BEGIN
    CREATE TABLE ChatSessions (
        session_id INT IDENTITY(1,1) PRIMARY KEY,
        session_uuid NVARCHAR(36) NOT NULL UNIQUE,
        user_id INT,
        device_info NVARCHAR(255),
        started_at DATETIME DEFAULT GETDATE(),
        ended_at DATETIME,
        is_active BIT DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
END
GO

-- =====================================================
-- ChatMessages Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ChatMessages')
BEGIN
    CREATE TABLE ChatMessages (
        message_id INT IDENTITY(1,1) PRIMARY KEY,
        session_id INT NOT NULL,
        sender_type NVARCHAR(20) NOT NULL,
        message_content NVARCHAR(MAX) NOT NULL,
        intent NVARCHAR(50),
        confidence_score NVARCHAR(10),
        is_product_recommendation BIT DEFAULT 0,
        recommended_product_ids NVARCHAR(255),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (session_id) REFERENCES ChatSessions(session_id) ON DELETE CASCADE
    );
END
GO

PRINT 'Database schema created successfully!';
