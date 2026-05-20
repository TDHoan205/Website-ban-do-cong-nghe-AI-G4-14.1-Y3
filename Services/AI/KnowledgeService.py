"""
Knowledge Service - Truy vấn dữ liệu từ DB cho RAG Pipeline
Tối ưu: eager loading tránh N+1, filter stop words, giới hạn description length
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import List, Optional, Dict
from Models.Product import Product, ProductVariant
from Models.Category import Category
from Models.Order import Order, OrderItem
import json


class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db

    def search_products(self, query: str, limit: int = 5) -> List[Dict]:
        """Tìm sản phẩm — eager load category, tránh N+1"""
        keywords = [kw for kw in query.lower().split() if len(kw) > 1]
        if not keywords:
            return []

        conditions = []
        for kw in keywords:
            pat = f"%{kw}%"
            conditions.append(or_(func.lower(Product.name).like(pat), func.lower(Product.description).like(pat)))

        products = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(*conditions)
            .filter(Product.is_available == True)
            .order_by(Product.is_hot.desc(), Product.rating.desc())
            .limit(limit)
            .all()
        )
        return [self._fmt(p) for p in products]

    def get_products_by_category(self, category_name: str, limit: int = 5) -> List[Dict]:
        cat = self.db.query(Category).filter(func.lower(Category.name).like(f"%{category_name.lower()}%")).first()
        if not cat:
            return []
        products = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == cat.category_id, Product.is_available == True)
            .order_by(Product.is_hot.desc())
            .limit(limit)
            .all()
        )
        return [self._fmt(p) for p in products]

    def get_hot_products(self, limit: int = 5) -> List[Dict]:
        products = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_available == True)
            .filter(or_(Product.is_hot == True, Product.is_new == True))
            .order_by(Product.rating.desc())
            .limit(limit)
            .all()
        )
        return [self._fmt(p) for p in products]

    def get_deal_products(self, limit: int = 5) -> List[Dict]:
        products = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_available == True, Product.discount_percent > 0)
            .order_by(Product.discount_percent.desc())
            .limit(limit)
            .all()
        )
        return [self._fmt(p) for p in products]

    def get_product_by_name(self, name: str) -> Optional[Dict]:
        product = (
            self.db.query(Product)
            .options(joinedload(Product.category), joinedload(Product.variants))
            .filter(func.lower(Product.name).like(f"%{name.lower()}%"))
            .first()
        )
        return self._fmt_detail(product) if product else None

    def compare_products(self, names: List[str]) -> List[Dict]:
        results = []
        for name in names[:3]:
            p = (
                self.db.query(Product)
                .options(joinedload(Product.category), joinedload(Product.variants))
                .filter(func.lower(Product.name).like(f"%{name.lower()}%"))
                .first()
            )
            if p:
                results.append(self._fmt_detail(p))
        return results

    def get_all_categories(self) -> List[Dict]:
        cats = self.db.query(Category).filter(Category.is_active == True).order_by(Category.display_order).all()
        return [{"name": c.name, "description": c.description or ""} for c in cats]

    def get_price_range(self, min_price: float = None, max_price: float = None, limit: int = 5) -> List[Dict]:
        """Tìm sản phẩm theo khoảng giá"""
        query = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_available == True)
        )
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        products = query.order_by(Product.price).limit(limit).all()
        return [self._fmt(p) for p in products]

    def lookup_order(self, order_id: int) -> Optional[Dict]:
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None
        items = self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        return {
            "order_id": order.order_id, "status": order.status,
            "total_amount": float(order.total_amount) if order.total_amount else 0,
            "order_date": order.order_date.strftime("%d/%m/%Y %H:%M") if order.order_date else "",
            "customer_name": order.customer_name or "",
            "items": [{"product_name": i.product_name, "quantity": i.quantity, "unit_price": float(i.unit_price) if i.unit_price else 0, "subtotal": float(i.subtotal) if i.subtotal else 0} for i in items],
        }

    def lookup_orders_by_account(self, account_id: int, limit: int = 5) -> List[Dict]:
        orders = self.db.query(Order).filter(Order.account_id == account_id).order_by(Order.order_date.desc()).limit(limit).all()
        return [{"order_id": o.order_id, "status": o.status, "total_amount": float(o.total_amount) if o.total_amount else 0, "order_date": o.order_date.strftime("%d/%m/%Y %H:%M") if o.order_date else ""} for o in orders]

    def _fmt(self, p: Product) -> Dict:
        """Format cơ bản — dùng eager-loaded category"""
        cat_name = p.category.name if p.category else ""
        return {
            "id": p.product_id, "name": p.name,
            "price": float(p.price) if p.price else 0,
            "original_price": float(p.original_price) if p.original_price else None,
            "discount_percent": p.discount_percent or 0,
            "rating": float(p.rating) if p.rating else 0,
            "category": cat_name,
            "is_hot": p.is_hot, "is_new": p.is_new,
            "stock": p.stock_quantity or 0,
        }

    def _fmt_detail(self, p: Product) -> Dict:
        """Format chi tiết — bao gồm mô tả (cắt ngắn), specs, variants"""
        base = self._fmt(p)
        # Cắt description tối đa 150 ký tự để tiết kiệm tokens
        desc = p.description or ""
        base["description"] = desc[:150] + "..." if len(desc) > 150 else desc

        specs = {}
        if p.specifications:
            try:
                specs = json.loads(p.specifications)
            except (json.JSONDecodeError, TypeError):
                specs = {}
        base["specifications"] = specs

        variants = []
        if p.variants:
            for v in p.variants:
                if v.is_active:
                    variants.append({
                        "name": v.variant_name or "",
                        "color": v.color or "",
                        "storage": v.storage or "",
                        "ram": v.ram or "",
                        "price": float(v.price) if v.price else None,
                    })
        base["variants"] = variants
        return base

    def build_product_context(self, products: List[Dict]) -> str:
        """Chuyển sản phẩm → text context cho LLM — ngắn gọn, tiết kiệm tokens"""
        if not products:
            return ""
        lines = [f"=== CỬA HÀNG CÓ {len(products)} SẢN PHẨM LIÊN QUAN ===\n"]
        for i, p in enumerate(products, 1):
            line = f"{i}. {p['name']} — {p['price']:,.0f}₫"
            if p.get("original_price") and p["original_price"] > p["price"]:
                line += f" (Gốc: {p['original_price']:,.0f}₫)"
            if p.get("discount_percent", 0) > 0:
                line += f" [-{p['discount_percent']}%]"
            if p.get("category"):
                line += f" | {p['category']}"
            if p.get("rating"):
                line += f" | ⭐{p['rating']}"
            if p.get("is_hot"):
                line += " 🔥"
            lines.append(line)

            # Description ngắn
            if p.get("description"):
                lines.append(f"   {p['description'][:120]}")
            # Specs tóm tắt
            if p.get("specifications") and isinstance(p["specifications"], dict):
                s = ", ".join(f"{k}: {v}" for k, v in list(p["specifications"].items())[:4] if k != "raw")
                if s:
                    lines.append(f"   Thông số: {s}")
            # Variants
            if p.get("variants"):
                vs = []
                for v in p["variants"][:3]:
                    parts = [v.get("name", "")]
                    if v.get("color"):
                        parts.append(v["color"])
                    if v.get("storage"):
                        parts.append(v["storage"])
                    if v.get("price"):
                        parts.append(f"{v['price']:,.0f}₫")
                    vs.append(" ".join(filter(None, parts)))
                lines.append(f"   Phiên bản: {' | '.join(vs)}")
            # Stock
            if p.get("stock", 0) == 0:
                lines.append("   ⚠️ Hết hàng")
            lines.append("")
        return "\n".join(lines)

    def build_order_context(self, order_data: Dict) -> str:
        if not order_data:
            return ""
        status_map = {
            "Pending": "⏳ Chờ xử lý", "Processing": "🔄 Đang xử lý",
            "Confirmed": "✅ Đã xác nhận", "Shipping": "🚚 Đang giao",
            "Delivered": "📦 Đã giao", "Completed": "✅ Hoàn thành",
            "Cancelled": "❌ Đã hủy",
        }
        lines = [
            "=== THÔNG TIN ĐƠN HÀNG ===\n",
            f"Mã đơn: #{order_data['order_id']}",
            f"Trạng thái: {status_map.get(order_data['status'], order_data['status'])}",
            f"Ngày đặt: {order_data['order_date']}",
            f"Tổng tiền: {order_data['total_amount']:,.0f}₫",
        ]
        if order_data.get("items"):
            lines.append("\nSản phẩm:")
            for item in order_data["items"]:
                lines.append(f"  - {item['product_name']} x{item['quantity']} = {item['subtotal']:,.0f}₫")
        return "\n".join(lines)
