"""
Models Package - Database Entities
"""
from Data.database import Base

# Import all models
from Models.Account import Account, Employee, Role
from Models.Category import Category
from Models.Supplier import Supplier
from Models.Inventory import Inventory
from Models.ReceiptShipment import ReceiptShipment
from Models.Product import Product, ProductVariant, ProductImage
from Models.Cart import Cart, CartItem
from Models.Order import Order, OrderItem, OrderStatus
from Models.Chat import (
    ChatSession, ChatMessage, AIConversationLog,
    FAQ, Notification, KnowledgeChunk
)
from Models.AI import AIResponse, RAGContext, ProductContext

__all__ = [
    # Base
    "Base",

    # Account
    "Account",
    "Employee",
    "Role",

    # Category
    "Category",
    "Supplier",
    "Inventory",
    "ReceiptShipment",

    # Product
    "Product",
    "ProductVariant",
    "ProductImage",

    # Cart
    "Cart",
    "CartItem",

    # Order
    "Order",
    "OrderItem",
    "OrderStatus",

    # Chat
    "ChatSession",
    "ChatMessage",
    "AIConversationLog",
    "FAQ",
    "Notification",
    "KnowledgeChunk",

    # AI
    "AIResponse",
    "RAGContext",
    "ProductContext",
]
