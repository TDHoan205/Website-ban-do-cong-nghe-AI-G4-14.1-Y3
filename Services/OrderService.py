"""
Order Service - Xử lý logic đơn hàng
Tương đương Services/OrderService.cs trong C#
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import uuid

from Models.Order import Order, OrderItem, OrderStatus
from Models.Cart import Cart, CartItem
from Models.Product import Product, ProductVariant
from Utilities import PagedList


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def get_orders(
        self,
        account_id: Optional[int] = None,
        search: Optional[str] = None,
        status: Optional[str] = None,
        sort_order: str = "date",
        page_number: int = 1,
        page_size: int = 10
    ) -> PagedList:
        """Lấy danh sách đơn hàng có phân trang"""

        query = self.db.query(Order)

        if account_id:
            query = query.filter(Order.account_id == account_id)

        if status:
            query = query.filter(Order.status == status)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Order.customer_name.ilike(search_term) |
                Order.customer_phone.ilike(search_term) |
                Order.order_id == int(search) if search.isdigit() else False
            )

        # Sort
        if sort_order == "date":
            query = query.order_by(desc(Order.order_date))
        elif sort_order == "date_asc":
            query = query.order_by(Order.order_date)
        elif sort_order == "total":
            query = query.order_by(Order.total_amount)
        elif sort_order == "total_desc":
            query = query.order_by(desc(Order.total_amount))
        elif sort_order == "status":
            query = query.order_by(Order.status)
        else:
            query = query.order_by(desc(Order.order_date))

        return PagedList.create(query, page_number, page_size)

    def get_all_orders_admin(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        sort_order: str = "date",
        page_number: int = 1,
        page_size: int = 10
    ) -> PagedList:
        """Lấy tất cả đơn hàng cho admin"""

        query = self.db.query(Order)

        if status:
            query = query.filter(Order.status == status)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Order.customer_name.ilike(search_term) |
                Order.customer_phone.ilike(search_term)
            )

        if sort_order == "date":
            query = query.order_by(desc(Order.order_date))
        elif sort_order == "date_asc":
            query = query.order_by(Order.order_date)
        elif sort_order == "total":
            query = query.order_by(Order.total_amount)
        elif sort_order == "total_desc":
            query = query.order_by(desc(Order.total_amount))
        else:
            query = query.order_by(desc(Order.order_date))

        return PagedList.create(query, page_number, page_size)

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Lấy đơn hàng theo ID"""
        return self.db.query(Order).filter(Order.order_id == order_id).first()

    def get_order_items(self, order_id: int) -> List[OrderItem]:
        """Lấy items của đơn hàng"""
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    def get_orders_by_account(self, account_id: int) -> List[Order]:
        """Lấy đơn hàng của account"""
        return self.db.query(Order).filter(
            Order.account_id == account_id
        ).order_by(desc(Order.order_date)).all()

    def create_order(
        self,
        account_id: int,
        customer_name: str,
        customer_phone: str,
        customer_address: str,
        notes: str = None
    ) -> Order:
        """Tạo đơn hàng từ giỏ hàng"""

        # Lấy giỏ hàng
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart or not cart.cart_items:
            raise ValueError("Giỏ hàng trống")

        # Tính tổng tiền
        subtotal = cart.total_amount
        shipping_fee = 0  # Miễn phí ship
        tax_amount = subtotal * 0.1  # 10% VAT
        total_amount = subtotal + shipping_fee + tax_amount

        # Tạo đơn hàng
        order = Order(
            account_id=account_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            notes=notes,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            order_date=datetime.now()
        )
        self.db.add(order)
        self.db.flush()  # Lấy order_id

        # Thêm các sản phẩm vào đơn hàng
        for cart_item in cart.cart_items:
            product = self.db.query(Product).filter(
                Product.product_id == cart_item.product_id
            ).first()

            product_name = product.name if product else "Unknown"
            unit_price = float(cart_item.unit_price)
            subtotal_item = unit_price * cart_item.quantity

            order_item = OrderItem(
                order_id=order.order_id,
                product_id=cart_item.product_id,
                variant_id=cart_item.variant_id,
                product_name=product_name,
                variant_name=cart_item.variant.variant_name if cart_item.variant else None,
                quantity=cart_item.quantity,
                unit_price=unit_price,
                subtotal=subtotal_item
            )
            self.db.add(order_item)

            # Cập nhật stock
            if product:
                product.stock_quantity = max(0, product.stock_quantity - cart_item.quantity)

        # Xóa giỏ hàng
        self.db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()

        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        """Cập nhật trạng thái đơn hàng"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None

        order.status = status
        order.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(order)
        return order

    def confirm_order(self, order_id: int) -> Optional[Order]:
        """Xác nhận đơn hàng"""
        return self.update_order_status(order_id, OrderStatus.CONFIRMED)

    def process_order(self, order_id: int) -> Optional[Order]:
        """Bắt đầu xử lý đơn hàng"""
        return self.update_order_status(order_id, OrderStatus.PROCESSING)

    def ship_order(self, order_id: int) -> Optional[Order]:
        """Gửi hàng"""
        return self.update_order_status(order_id, OrderStatus.SHIPPED)

    def deliver_order(self, order_id: int) -> Optional[Order]:
        """Giao hàng thành công"""
        return self.update_order_status(order_id, OrderStatus.DELIVERED)

    def cancel_order(self, order_id: int, reason: str = None) -> Optional[Order]:
        """Hủy đơn hàng"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None

        order.status = OrderStatus.CANCELLED
        order.notes = f"{order.notes or ''}\nHủy: {reason}" if reason else order.notes
        order.updated_at = datetime.now()

        # Hoàn kho
        for item in order.order_items:
            product = self.db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()
            if product:
                product.stock_quantity += item.quantity

        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_stats(self) -> dict:
        """Lấy thống kê đơn hàng"""
        total = self.db.query(Order).count()
        pending = self.db.query(Order).filter(Order.status == OrderStatus.PENDING).count()
        confirmed = self.db.query(Order).filter(Order.status == OrderStatus.CONFIRMED).count()
        processing = self.db.query(Order).filter(Order.status == OrderStatus.PROCESSING).count()
        shipped = self.db.query(Order).filter(Order.status == OrderStatus.SHIPPED).count()
        delivered = self.db.query(Order).filter(Order.status == OrderStatus.DELIVERED).count()
        cancelled = self.db.query(Order).filter(Order.status == OrderStatus.CANCELLED).count()

        return {
            "total": total,
            "pending": pending,
            "confirmed": confirmed,
            "processing": processing,
            "shipped": shipped,
            "delivered": delivered,
            "cancelled": cancelled
        }

    def get_revenue_stats(self, days: int = 30) -> dict:
        """Lấy thống kê doanh thu"""
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=days)

        orders = self.db.query(Order).filter(
            Order.order_date >= start_date,
            Order.status == OrderStatus.DELIVERED
        ).all()

        total_revenue = sum(float(o.total_amount) for o in orders)
        total_orders = len(orders)

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
        }
