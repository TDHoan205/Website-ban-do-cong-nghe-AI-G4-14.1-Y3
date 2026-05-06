-- =====================================================
-- Tech Store - Database Schema (Updated to match Python MVC Models)
-- SQL Server - TechShopWebsite2
-- =====================================================

-- Tạo Database nếu chưa có
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'TechShopWebsite2')
BEGIN
    CREATE DATABASE TechShopWebsite2;
END
GO

USE TechShopWebsite2;
GO

-- XÓA BẢNG CŨ NẾU CẦN (Để làm mới hoàn toàn cấu trúc)
-- DROP TABLE IF EXISTS KnowledgeChunks;
-- DROP TABLE IF EXISTS ChatMessages;
-- DROP TABLE IF EXISTS ChatSessions;
-- DROP TABLE IF EXISTS Notifications;
-- DROP TABLE IF EXISTS FAQs;
-- DROP TABLE IF EXISTS AIConversationLogs;
-- DROP TABLE IF EXISTS ReceiptShipments;
-- DROP TABLE IF EXISTS OrderItems;
-- DROP TABLE IF EXISTS Orders;
-- DROP TABLE IF EXISTS CartItems;
-- DROP TABLE IF EXISTS Carts;
-- DROP TABLE IF EXISTS Inventory;
-- DROP TABLE IF EXISTS ProductImages;
-- DROP TABLE IF EXISTS ProductVariants;
-- DROP TABLE IF EXISTS Products;
-- DROP TABLE IF EXISTS Employees;
-- DROP TABLE IF EXISTS Accounts;
-- DROP TABLE IF EXISTS Roles;
-- DROP TABLE IF EXISTS Suppliers;
-- DROP TABLE IF EXISTS Categories;
-- GO

-- =====================================================
-- Roles Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Roles')
BEGIN
    CREATE TABLE Roles (
        role_id INT IDENTITY(1,1) PRIMARY KEY,
        role_name NVARCHAR(50) NOT NULL UNIQUE,
        description NVARCHAR(255),
        permissions NVARCHAR(1000), -- JSON string
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- =====================================================
-- Accounts Table (Thay thế Users)
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Accounts')
BEGIN
    CREATE TABLE Accounts (
        account_id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        email NVARCHAR(100) UNIQUE,
        full_name NVARCHAR(100),
        phone NVARCHAR(20),
        address NVARCHAR(255),
        is_active BIT DEFAULT 1,
        role_id INT NOT NULL,
        reset_token NVARCHAR(64),
        reset_token_expiry DATETIME,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id)
    );
END
GO

-- =====================================================
-- Employees Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    CREATE TABLE Employees (
        employee_id INT IDENTITY(1,1) PRIMARY KEY,
        account_id INT NOT NULL UNIQUE,
        department NVARCHAR(50),
        position NVARCHAR(50),
        hire_date DATETIME,
        salary INT,
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    );
END
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
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME
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
        stock_quantity INT DEFAULT 0,
        is_available BIT DEFAULT 1,
        rating DECIMAL(2, 1) DEFAULT 4.5,
        is_new BIT DEFAULT 0,
        is_hot BIT DEFAULT 0,
        discount_percent INT DEFAULT 0,
        specifications NVARCHAR(MAX),
        category_id INT,
        supplier_id INT,
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
        created_at DATETIME DEFAULT GETDATE(),
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
        account_id INT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME,
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
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
        account_id INT,
        order_date DATETIME DEFAULT GETDATE(),
        total_amount DECIMAL(10, 2) NOT NULL,
        status NVARCHAR(20) DEFAULT 'Pending',
        customer_name NVARCHAR(100),
        customer_phone NVARCHAR(20),
        customer_address NVARCHAR(255),
        notes NVARCHAR(500),
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME,
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
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
-- ReceiptShipments Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ReceiptShipments')
BEGIN
    CREATE TABLE ReceiptShipments (
        receipt_id INT IDENTITY(1,1) PRIMARY KEY,
        product_id INT NOT NULL,
        supplier_id INT,
        order_id INT,
        quantity INT NOT NULL,
        type NVARCHAR(20) NOT NULL, -- IN, OUT
        reason NVARCHAR(100),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
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
        account_id INT,
        device_info NVARCHAR(255),
        started_at DATETIME DEFAULT GETDATE(),
        ended_at DATETIME,
        is_active BIT DEFAULT 1,
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
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
        sender_type NVARCHAR(20) NOT NULL, -- user, bot, staff
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

-- =====================================================
-- AIConversationLogs Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AIConversationLogs')
BEGIN
    CREATE TABLE AIConversationLogs (
        log_id INT IDENTITY(1,1) PRIMARY KEY,
        session_id INT NOT NULL,
        account_id INT,
        user_message NVARCHAR(MAX),
        bot_response NVARCHAR(MAX),
        intent_detected NVARCHAR(50),
        confidence_score NVARCHAR(10),
        response_time_ms INT,
        is_escalated_to_staff BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (session_id) REFERENCES ChatSessions(session_id),
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    );
END
GO

-- =====================================================
-- FAQs Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'FAQs')
BEGIN
    CREATE TABLE FAQs (
        faq_id INT IDENTITY(1,1) PRIMARY KEY,
        question NVARCHAR(500) NOT NULL,
        answer NVARCHAR(MAX) NOT NULL,
        category NVARCHAR(50),
        display_order INT DEFAULT 0,
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME
    );
END
GO

-- =====================================================
-- Notifications Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Notifications')
BEGIN
    CREATE TABLE Notifications (
        notification_id INT IDENTITY(1,1) PRIMARY KEY,
        account_id INT,
        title NVARCHAR(200) NOT NULL,
        content NVARCHAR(MAX) NOT NULL,
        notification_type NVARCHAR(50),
        is_read BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    );
END
GO

-- =====================================================
-- KnowledgeChunks Table
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'KnowledgeChunks')
BEGIN
    CREATE TABLE KnowledgeChunks (
        chunk_id INT IDENTITY(1,1) PRIMARY KEY,
        content NVARCHAR(MAX) NOT NULL,
        content_type NVARCHAR(50),
        source_id INT,
        source_table NVARCHAR(50),
        embedding_vector NVARCHAR(MAX), -- Vector embedding lưu dạng string
        chunk_metadata NVARCHAR(MAX), -- JSON metadata
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

PRINT 'Database schema updated successfully to match Python Models!';
