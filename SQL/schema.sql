-- =====================================================
-- TechShopWebsite1 - Schema aligned to Models
-- =====================================================

IF DB_ID(N'TechShopWebsite2') IS NULL
BEGIN
    CREATE DATABASE TechShopWebsite2;
END
GO

USE TechShopWebsite2;
GO
-- Roles
CREATE TABLE Roles (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(255) NULL
);
-- Accounts
CREATE TABLE Accounts (
    account_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    email NVARCHAR(100) NULL UNIQUE,
    full_name NVARCHAR(100) NULL,
    phone NVARCHAR(20) NULL,
    address NVARCHAR(255) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    role_id INT NOT NULL,
    reset_token NVARCHAR(64) NULL,
    reset_token_expiry DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL,
    CONSTRAINT FK_Accounts_Roles FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- Employees
CREATE TABLE Employees (
    employee_id INT IDENTITY(1,1) PRIMARY KEY,
    account_id INT NOT NULL UNIQUE,
    department NVARCHAR(50) NULL,
    position NVARCHAR(50) NULL,
    hire_date DATETIME2 NULL,
    salary INT NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Employees_Accounts FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Users (separate from Accounts; present in Models)
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(100) NULL,
    phone NVARCHAR(20) NULL,
    address NVARCHAR(255) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    role NVARCHAR(20) NOT NULL DEFAULT 'Customer',
    avatar_url NVARCHAR(500) NULL,
    reset_token NVARCHAR(64) NULL,
    reset_token_expiry DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL
);

-- Categories
CREATE TABLE Categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX) NULL,
    image_url NVARCHAR(500) NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL
);

-- Suppliers
CREATE TABLE Suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    contact_person NVARCHAR(100) NULL,
    phone NVARCHAR(20) NULL,
    email NVARCHAR(100) NULL,
    address NVARCHAR(255) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL
);

-- Products
CREATE TABLE Products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NULL,
    image_url NVARCHAR(500) NULL,
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2) NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    is_available BIT NOT NULL DEFAULT 1,
    rating DECIMAL(2, 1) NOT NULL DEFAULT 4.5,
    is_new BIT NOT NULL DEFAULT 0,
    is_hot BIT NOT NULL DEFAULT 0,
    discount_percent INT NOT NULL DEFAULT 0,
    specifications NVARCHAR(MAX) NULL,
    category_id INT NULL,
    supplier_id INT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL,
    CONSTRAINT FK_Products_Categories FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    CONSTRAINT FK_Products_Suppliers FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- ProductVariants
CREATE TABLE ProductVariants (
    variant_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    color NVARCHAR(50) NULL,
    storage NVARCHAR(20) NULL,
    ram NVARCHAR(20) NULL,
    variant_name NVARCHAR(100) NULL,
    sku NVARCHAR(50) NULL,
    price DECIMAL(10, 2) NULL,
    original_price DECIMAL(10, 2) NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    display_order INT NOT NULL DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_ProductVariants_Products FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- ProductImages
CREATE TABLE ProductImages (
    image_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    image_url NVARCHAR(500) NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_primary BIT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_ProductImages_Products FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- Inventory
CREATE TABLE Inventory (
    inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    quantity_in_stock INT NOT NULL DEFAULT 0,
    min_stock_level INT NOT NULL DEFAULT 5,
    max_stock_level INT NOT NULL DEFAULT 100,
    last_restock_date DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL,
    CONSTRAINT FK_Inventory_Products FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Carts
CREATE TABLE Carts (
    cart_id INT IDENTITY(1,1) PRIMARY KEY,
    account_id INT NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL,
    CONSTRAINT FK_Carts_Accounts FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- CartItems
CREATE TABLE CartItems (
    cart_item_id INT IDENTITY(1,1) PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    variant_id INT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_CartItems_Carts FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
    CONSTRAINT FK_CartItems_Products FOREIGN KEY (product_id) REFERENCES Products(product_id),
    CONSTRAINT FK_CartItems_ProductVariants FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id)
);

-- Orders
CREATE TABLE Orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    account_id INT NULL,
    order_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    total_amount DECIMAL(10, 2) NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'Pending',
    customer_name NVARCHAR(100) NULL,
    customer_phone NVARCHAR(20) NULL,
    customer_address NVARCHAR(255) NULL,
    notes NVARCHAR(500) NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NULL,
    CONSTRAINT FK_Orders_Accounts FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- OrderItems
CREATE TABLE OrderItems (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    variant_id INT NULL,
    product_name NVARCHAR(255) NOT NULL,
    variant_name NVARCHAR(100) NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    CONSTRAINT FK_OrderItems_Products FOREIGN KEY (product_id) REFERENCES Products(product_id),
    CONSTRAINT FK_OrderItems_ProductVariants FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id)
);





