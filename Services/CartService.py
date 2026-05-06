"""
Cart Service - Xử lý logic giỏ hàng
Tương đương Services/CartService.cs trong C#
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from Models.Cart import Cart, CartItem
from Models.Product import Product, ProductVariant


class CartService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_cart(self, account_id: int) -> Cart:
        """Lấy hoặc tạo giỏ hàng cho account"""
        cart = self.db.query(Cart).filter(Cart.account_id == account_id).first()
        if not cart:
            cart = Cart(account_id=account_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def get_cart_by_account(self, account_id: int) -> Optional[Cart]:
        """Lấy giỏ hàng theo account"""
        return self.db.query(Cart).filter(Cart.account_id == account_id).first()

    def get_cart_items(self, cart_id: int) -> List[CartItem]:
        """Lấy danh sách sản phẩm trong giỏ hàng"""
        return self.db.query(CartItem).filter(
            CartItem.cart_id == cart_id
        ).all()

    def get_cart_item(self, cart_item_id: int) -> Optional[CartItem]:
        """Lấy cart item theo ID"""
        return self.db.query(CartItem).filter(
            CartItem.cart_item_id == cart_item_id
        ).first()

    def add_item(
        self,
        account_id: int,
        product_id: int,
        quantity: int = 1,
        variant_id: Optional[int] = None
    ) -> CartItem:
        """Thêm sản phẩm vào giỏ hàng"""

        cart = self.get_or_create_cart(account_id)

        # Kiểm tra sản phẩm đã có trong giỏ chưa
        existing_item = self.db.query(CartItem).filter(
            CartItem.cart_id == cart.cart_id,
            CartItem.product_id == product_id,
            CartItem.variant_id == variant_id
        ).first()

        if existing_item:
            existing_item.quantity += quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item

        # Thêm mới
        item = CartItem(
            cart_id=cart.cart_id,
            product_id=product_id,
            variant_id=variant_id,
            quantity=quantity
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item_quantity(self, cart_item_id: int, quantity: int) -> Optional[CartItem]:
        """Cập nhật số lượng sản phẩm"""
        item = self.get_cart_item(cart_item_id)
        if not item:
            return None

        if quantity <= 0:
            self.db.delete(item)
        else:
            item.quantity = quantity
            self.db.commit()
            self.db.refresh(item)

        return item

    def remove_item(self, cart_item_id: int) -> bool:
        """Xóa sản phẩm khỏi giỏ hàng"""
        item = self.get_cart_item(cart_item_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True

    def clear_cart(self, account_id: int) -> bool:
        """Xóa toàn bộ giỏ hàng"""
        cart = self.get_cart_by_account(account_id)
        if not cart:
            return False
        self.db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
        self.db.commit()
        return True

    def get_cart_total(self, account_id: int) -> float:
        """Tính tổng tiền giỏ hàng"""
        cart = self.get_cart_by_account(account_id)
        if not cart:
            return 0
        return cart.total_amount

    def get_cart_item_count(self, account_id: int) -> int:
        """Đếm số item trong giỏ hàng"""
        cart = self.get_cart_by_account(account_id)
        if not cart:
            return 0
        return cart.total_items

    def validate_cart_items(self, account_id: int) -> List[CartItem]:
        """Kiểm tra và trả về các item không hợp lệ (hết hàng, ngừng bán)"""
        cart = self.get_cart_by_account(account_id)
        if not cart:
            return []

        invalid_items = []
        for item in cart.cart_items:
            product = self.db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()

            if not product or not product.is_available:
                invalid_items.append(item)
                continue

            if item.variant_id:
                variant = self.db.query(ProductVariant).filter(
                    ProductVariant.variant_id == item.variant_id
                ).first()
                if not variant or not variant.is_active:
                    invalid_items.append(item)

        return invalid_items

    def remove_invalid_items(self, account_id: int) -> int:
        """Xóa các item không hợp lệ và trả về số lượng đã xóa"""
        invalid_items = self.validate_cart_items(account_id)
        count = len(invalid_items)

        for item in invalid_items:
            self.db.delete(item)

        self.db.commit()
        return count
