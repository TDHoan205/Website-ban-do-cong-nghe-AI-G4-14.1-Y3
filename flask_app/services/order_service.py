"""
Order service - handles checkout, order creation, and order management.
Creates Orders + OrderItems from the current cart.
"""
from decimal import Decimal
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from .cart_service import CartService
from ..models import Order, OrderItem


class OrderService:
    """Handles order-related database operations."""

    def __init__(self, db: Session):
        self.db = db
        self.cart_service = CartService(db)

    def get_all_orders(self) -> List[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .order_by(Order.order_date.desc())
            .all()
        )

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.order_id == order_id)
            .first()
        )

    def get_orders_by_account(self, account_id: int) -> List[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.account_id == account_id)
            .order_by(Order.order_date.desc())
            .all()
        )

    def checkout(
        self,
        account_id: int,
        customer_name: str,
        customer_phone: str,
        customer_address: str,
        notes: Optional[str] = None,
    ) -> tuple[bool, str, Optional[Order]]:
        """
        Convert the user's cart into an order.
        Returns (success, message, order_or_None).
        """
        # Get cart items
        cart_items = self.cart_service.get_cart(account_id)
        if not cart_items:
            return False, "Giỏ hàng trống. Không thể thanh toán.", None

        # Calculate total
        total = Decimal("0.00")
        order_items = []
        for item in cart_items:
            if item.variant and item.variant.price:
                unit_price = item.variant.price
            elif item.product:
                unit_price = item.product.price
            else:
                unit_price = Decimal("0.00")

            subtotal = unit_price * item.quantity
            total += subtotal

            # Build snapshot of product name at time of purchase
            product_name = item.product.name if item.product else "Sản phẩm không xác định"
            variant_name = None
            if item.variant:
                parts = [item.variant.color or ""]
                if item.variant.storage:
                    parts.append(item.variant.storage)
                if item.variant.ram:
                    parts.append(item.variant.ram)
                variant_name = " / ".join(p for p in parts if p) or None

            order_items.append({
                "product_id": item.product_id,
                "variant_id": item.variant_id,
                "product_name": product_name,
                "variant_name": variant_name,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
            })

        # Create order
        order = Order(
            account_id=account_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            total_amount=total,
            status="Pending",
            notes=notes,
        )
        self.db.add(order)
        self.db.flush()  # Get order_id before adding items

        # Create order items
        for item_data in order_items:
            order_item = OrderItem(order_id=order.order_id, **item_data)
            self.db.add(order_item)

        # Clear the cart
        self.cart_service.clear_cart(account_id)

        self.db.commit()
        self.db.refresh(order)

        return True, "Đặt hàng thành công!", order
