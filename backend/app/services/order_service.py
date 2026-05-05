from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional, Tuple
from app.models.order import Order, OrderItem
from app.models.product import Product, ProductVariant


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def get_orders(
        self,
        user_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> Tuple[List[Order], int]:
        query = self.db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product),
            joinedload(Order.user),
        )

        if user_id:
            query = query.filter(Order.user_id == user_id)

        if status:
            query = query.filter(Order.status == status)

        query = query.order_by(Order.order_date.desc())
        total = query.count()
        orders = query.offset((page - 1) * page_size).limit(page_size).all()

        return orders, total

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product),
            joinedload(Order.order_items).joinedload(OrderItem.variant),
        ).filter(Order.order_id == order_id).first()

    def create_order(
        self,
        user_id: Optional[int],
        items: List[dict],
        customer_name: Optional[str] = None,
        customer_phone: Optional[str] = None,
        customer_address: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Tuple[Optional[Order], str]:
        if not items:
            return None, "Cart is empty"

        total_amount = 0
        order_items_data = []

        for item in items:
            product = self.db.query(Product).filter(
                Product.product_id == item["product_id"]
            ).first()

            if not product:
                return None, f"Product {item['product_id']} not found"

            if product.stock_quantity < item["quantity"]:
                return None, f"Insufficient stock for {product.name}"

            price = product.price
            if item.get("variant_id"):
                variant = self.db.query(ProductVariant).filter(
                    ProductVariant.variant_id == item["variant_id"]
                ).first()
                if variant:
                    price = variant.price

            total_amount += price * item["quantity"]
            order_items_data.append({
                "product_id": item["product_id"],
                "variant_id": item.get("variant_id"),
                "quantity": item["quantity"],
                "unit_price": price,
            })

        new_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="Pending",
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            notes=notes,
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)

        for item_data in order_items_data:
            order_item = OrderItem(order_id=new_order.order_id, **item_data)
            self.db.add(order_item)

            product = self.db.query(Product).filter(
                Product.product_id == item_data["product_id"]
            ).first()
            if product:
                product.stock_quantity = max(0, product.stock_quantity - item_data["quantity"])

            if item_data.get("variant_id"):
                variant = self.db.query(ProductVariant).filter(
                    ProductVariant.variant_id == item_data["variant_id"]
                ).first()
                if variant:
                    variant.stock_quantity = max(0, variant.stock_quantity - item_data["quantity"])

        self.db.commit()
        self.db.refresh(new_order)

        return new_order, ""

    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None

        valid_statuses = ["Pending", "Confirmed", "Processing", "Shipped", "Delivered", "Cancelled"]
        if status not in valid_statuses:
            return None

        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order

    def cancel_order(self, order_id: int) -> Tuple[bool, str]:
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return False, "Order not found"

        if order.status in ["Shipped", "Delivered", "Cancelled"]:
            return False, f"Cannot cancel order with status: {order.status}"

        for item in order.order_items:
            product = self.db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()
            if product:
                product.stock_quantity += item.quantity

            if item.variant_id:
                variant = self.db.query(ProductVariant).filter(
                    ProductVariant.variant_id == item.variant_id
                ).first()
                if variant:
                    variant.stock_quantity += item.quantity

        order.status = "Cancelled"
        self.db.commit()
        return True, ""

    def get_order_stats(self) -> dict:
        total_orders = self.db.query(func.count(Order.order_id)).scalar()
        total_revenue = self.db.query(func.sum(Order.total_amount)).filter(
            Order.status.in_(["Delivered", "Shipped", "Processing"])
        ).scalar() or 0

        pending_orders = self.db.query(func.count(Order.order_id)).filter(
            Order.status == "Pending"
        ).scalar()

        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "pending_orders": pending_orders,
        }
