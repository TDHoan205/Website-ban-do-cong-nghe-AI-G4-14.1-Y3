"""
Cart service – manages the shopping cart for both guests and authenticated users.
Guest carts use a session UUID stored in a cookie.
Authenticated users have a persistent cart in the database.
"""
from decimal import Decimal
from typing import Optional, List, Tuple
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from ..models import Cart, CartItem, Product, ProductVariant


class CartService:
    """
    Handles cart operations. For guests, uses a session-based approach.
    For authenticated users, persists the cart in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    # ── Internal helpers ─────────────────────────────────────────────

    def _get_or_create_db_cart(self, account_id: int) -> Cart:
        """Get or create a DB-backed cart for a logged-in user."""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            cart = Cart(account_id=account_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    # ── Cart item management ────────────────────────────────────────

    def add_item(
        self,
        account_id: int,
        product_id: int,
        quantity: int = 1,
        variant_id: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Add an item to the cart (or increase quantity if it already exists).
        Returns (success, message).
        """
        # Validate product
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return False, "Sản phẩm không tồn tại."

        # Validate variant if provided
        if variant_id:
            variant = (
                self.db.query(ProductVariant)
                .filter(ProductVariant.variant_id == variant_id, ProductVariant.product_id == product_id)
                .first()
            )
            if not variant:
                return False, "Phiên bản sản phẩm không hợp lệ."
            price = variant.price if variant.price else product.price
        else:
            price = product.price

        # Get or create cart
        cart = self._get_or_create_db_cart(account_id)

        # Check if item already in cart
        existing = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.cart_id,
                CartItem.product_id == product_id,
                CartItem.variant_id == variant_id,
            )
            .first()
        )

        if existing:
            existing.quantity += quantity
        else:
            item = CartItem(
                cart_id=cart.cart_id,
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity,
            )
            self.db.add(item)

        cart.updated_at = datetime.now()
        self.db.commit()
        return True, "Đã thêm vào giỏ hàng!"

    def update_item_quantity(
        self,
        account_id: int,
        product_id: int,
        quantity: int,
        variant_id: Optional[int] = None,
    ) -> Tuple[bool, str, int]:
        """
        Update the quantity of a cart item.
        Returns (success, message, new_quantity).
        If quantity <= 0, removes the item.
        """
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            return False, "Giỏ hàng trống.", 0

        item = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.cart_id,
                CartItem.product_id == product_id,
                CartItem.variant_id == variant_id,
            )
            .first()
        )

        if not item:
            return False, "Sản phẩm không có trong giỏ hàng.", 0

        if quantity <= 0:
            self.db.delete(item)
            self.db.commit()
            return True, "Đã xóa sản phẩm.", 0

        item.quantity = quantity
        cart.updated_at = datetime.now()
        self.db.commit()
        return True, "Đã cập nhật số lượng.", quantity

    def remove_item(
        self,
        account_id: int,
        product_id: int,
        variant_id: Optional[int] = None,
    ) -> bool:
        """Remove a specific item from the cart."""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            return False

        item = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.cart_id,
                CartItem.product_id == product_id,
                CartItem.variant_id == variant_id,
            )
            .first()
        )

        if item:
            self.db.delete(item)
            cart.updated_at = datetime.now()
            self.db.commit()
            return True
        return False

    def clear_cart(self, account_id: int) -> bool:
        """Remove all items from the user's cart."""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            return False
        self.db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
        cart.updated_at = datetime.now()
        self.db.commit()
        return True

    # ── Cart retrieval ──────────────────────────────────────────────

    def get_cart(self, account_id: int) -> List[CartItem]:
        """Return all cart items with eager-loaded product/variant."""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            return []

        return (
            self.db.query(CartItem)
            .options(
                joinedload(CartItem.product).joinedload(Product.category),
                joinedload(CartItem.variant),
            )
            .filter(CartItem.cart_id == cart.cart_id)
            .all()
        )

    def get_cart_count(self, account_id: int) -> int:
        """Return total number of items in cart."""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            return 0
        result = (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart.cart_id)
            .with_entities(func.sum(CartItem.quantity))
            .scalar()
        )
        return int(result or 0)

    def get_cart_total(self, account_id: int) -> float:
        """Calculate the total price of the cart."""
        items = self.get_cart(account_id)
        total = Decimal("0.00")
        for item in items:
            if item.variant and item.variant.price:
                price = item.variant.price
            elif item.product:
                price = item.product.price
            else:
                price = Decimal("0.00")
            total += price * item.quantity
        return float(total)
