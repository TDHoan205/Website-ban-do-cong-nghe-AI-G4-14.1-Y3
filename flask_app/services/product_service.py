"""
Product service – CRUD operations for products, categories, variants, images.
All queries run against the real SQL Server database.
"""
from typing import Optional, List, Tuple
from decimal import Decimal

from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session, joinedload

from ..models import (
    Product, ProductVariant, ProductImage,
    Category, Supplier,
)


class ProductService:
    """Handles all product-related database queries."""

    def __init__(self, db: Session):
        self.db = db

    # ── Categories ────────────────────────────────────────────────────

    def get_all_categories(self) -> List[Category]:
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.display_order, Category.name)
            .all()
        )

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return (
            self.db.query(Category)
            .filter(Category.category_id == category_id)
            .first()
        )

    def get_category_by_name(self, name: str) -> Optional[Category]:
        return (
            self.db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    # ── Products ──────────────────────────────────────────────────────

    def get_all_products(self) -> List[Product]:
        """Return all available products with eager-loaded relationships."""
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.supplier),
                joinedload(Product.variants),
                joinedload(Product.images),
            )
            .filter(Product.is_available == True)
            .order_by(Product.created_at.desc())
            .all()
        )

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Return a single product with all relationships eagerly loaded."""
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.supplier),
                joinedload(Product.variants),
                joinedload(Product.images),
            )
            .filter(Product.product_id == product_id)
            .first()
        )

    def get_products_by_category(
        self,
        category_id: int,
        limit: int = 50,
    ) -> List[Product]:
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.variants),
                joinedload(Product.images),
            )
            .filter(
                Product.category_id == category_id,
                Product.is_available == True,
            )
            .limit(limit)
            .all()
        )

    def get_new_products(self, limit: int = 12) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category), joinedload(Product.variants))
            .filter(Product.is_new == True, Product.is_available == True)
            .order_by(Product.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_hot_products(self, limit: int = 12) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category), joinedload(Product.variants))
            .filter(Product.is_hot == True, Product.is_available == True)
            .order_by(Product.rating.desc())
            .limit(limit)
            .all()
        )

    def search_products(
        self,
        query: str,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "newest",
        page: int = 1,
        page_size: int = 12,
    ) -> Tuple[List[Product], int]:
        """
        Full-featured product search with filtering and pagination.
        Returns (products, total_count).
        """
        q = (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.variants),
                joinedload(Product.images),
            )
            .filter(Product.is_available == True)
        )

        # Text search
        if query:
            q = q.filter(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                )
            )

        # Category filter
        if category_id:
            q = q.filter(Product.category_id == category_id)

        # Price range filter
        if min_price is not None:
            q = q.filter(Product.price >= Decimal(str(min_price)))
        if max_price is not None:
            q = q.filter(Product.price <= Decimal(str(max_price)))

        # Total count before pagination
        total = q.count()

        # Sorting
        if sort_by == "price_asc":
            q = q.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            q = q.order_by(Product.price.desc())
        elif sort_by == "name_asc":
            q = q.order_by(Product.name.asc())
        elif sort_by == "rating":
            q = q.order_by(Product.rating.desc())
        elif sort_by == "newest":
            q = q.order_by(Product.is_new.desc(), Product.created_at.desc())
        else:
            q = q.order_by(Product.created_at.desc())

        # Pagination
        offset = (page - 1) * page_size
        products = q.offset(offset).limit(page_size).all()

        return products, total

    def get_related_products(self, product_id: int, category_id: int, limit: int = 4) -> List[Product]:
        """Products in the same category, excluding the current product."""
        return (
            self.db.query(Product)
            .options(joinedload(Product.variants), joinedload(Product.images))
            .filter(
                Product.category_id == category_id,
                Product.product_id != product_id,
                Product.is_available == True,
            )
            .limit(limit)
            .all()
        )

    # ── Suppliers ──────────────────────────────────────────────────────

    def get_all_suppliers(self) -> List[Supplier]:
        return (
            self.db.query(Supplier)
            .filter(Supplier.is_active == True)
            .all()
        )

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()

    # ── Variants ──────────────────────────────────────────────────────

    def get_variant_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        return (
            self.db.query(ProductVariant)
            .filter(ProductVariant.variant_id == variant_id)
            .first()
        )
