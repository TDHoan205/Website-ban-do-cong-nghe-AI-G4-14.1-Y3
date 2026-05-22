"""
Product Service - Xử lý logic sản phẩm
Tương đương Services/ProductService.cs trong C#
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func, and_
from typing import Optional, List, Tuple
from decimal import Decimal

from Models.Product import Product, ProductVariant, ProductImage
from Models.Category import Category
from Utilities import PagedList


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}

    def invalidate_cache(self):
        """Xóa cache"""
        self._cache = {}

    # ============ Products CRUD ============
    def get_products(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        sort_order: str = "name",
        page_number: int = 1,
        page_size: int = 10
    ) -> PagedList:
        """Lấy danh sách sản phẩm có phân trang"""

        query = self.db.query(Product).filter(Product.is_available == True)

        # Filter by category
        if category_id:
            query = query.filter(Product.category_id == category_id)

        # Search
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )

        # Sort
        if sort_order == "name":
            query = query.order_by(Product.name)
        elif sort_order == "name_desc":
            query = query.order_by(desc(Product.name))
        elif sort_order == "price":
            query = query.order_by(Product.price)
        elif sort_order == "price_desc":
            query = query.order_by(desc(Product.price))
        elif sort_order == "category":
            query = query.join(Category).order_by(Category.name)
        elif sort_order == "category_desc":
            query = query.join(Category).order_by(desc(Category.name))
        elif sort_order == "created":
            query = query.order_by(desc(Product.created_at))
        else:
            query = query.order_by(Product.name)

        return PagedList.create(query, page_number, page_size)

    def get_all_products(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 12,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        discount: bool = False,
        is_new: bool = False,
        is_hot: bool = False,
    ) -> Tuple[List[Product], int]:
        """Lay tat ca san pham co loc nang cao - tra ve list va total"""
        query = self.db.query(Product).filter(Product.is_available == True)

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if search:
            term = f"%{search}%"
            query = query.filter(
                or_(Product.name.ilike(term), Product.description.ilike(term))
            )

        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if discount:
            query = query.filter(Product.discount_percent > 0)
        if is_new:
            query = query.filter(Product.is_new == True)
        if is_hot:
            query = query.filter(Product.is_hot == True)

        total = query.count()

        if sort_by == "name":
            query = query.order_by(Product.name if sort_order == "asc" else desc(Product.name))
        elif sort_by == "price":
            query = query.order_by(Product.price if sort_order == "asc" else desc(Product.price))
        elif sort_by == "rating":
            query = query.order_by(desc(Product.rating))
        elif sort_by == "created_at":
            query = query.order_by(desc(Product.created_at))
        else:
            query = query.order_by(desc(Product.created_at))

        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()
        return products, total

    def get_all_products_admin(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        sort_order: str = "name",
        page_number: int = 1,
        page_size: int = 10
    ) -> PagedList:
        """Lấy tất cả sản phẩm (kể cả unavailable) cho admin"""
        query = self.db.query(Product)

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )

        # Sort
        if sort_order == "name":
            query = query.order_by(Product.name)
        elif sort_order == "name_desc":
            query = query.order_by(desc(Product.name))
        elif sort_order == "price":
            query = query.order_by(Product.price)
        elif sort_order == "price_desc":
            query = query.order_by(desc(Product.price))
        else:
            query = query.order_by(Product.name)

        return PagedList.create(query, page_number, page_size)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Lấy sản phẩm theo ID"""
        return self.db.query(Product).filter(Product.product_id == product_id).first()

    def create_product(self, product_data: dict) -> Product:
        """Tạo sản phẩm mới"""
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        self.invalidate_cache()
        return product

    def update_product(self, product_id: int, product_data: dict) -> Optional[Product]:
        """Cập nhật sản phẩm"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        for key, value in product_data.items():
            if hasattr(product, key):
                setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        self.invalidate_cache()
        return product

    def delete_product(self, product_id: int) -> bool:
        """Xóa sản phẩm"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        self.invalidate_cache()
        return True

    # ============ Featured Products ============
    def get_featured_products(self, limit: int = 8) -> List[Product]:
        """Lấy sản phẩm nổi bật"""
        cache_key = f"featured_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        products = self.db.query(Product).filter(
            Product.is_hot == True,
            Product.is_available == True
        ).limit(limit).all()

        self._cache[cache_key] = products
        return products

    def get_new_products(self, limit: int = 8) -> List[Product]:
        """Lấy sản phẩm mới"""
        cache_key = f"new_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        products = self.db.query(Product).filter(
            Product.is_new == True,
            Product.is_available == True
        ).limit(limit).all()

        self._cache[cache_key] = products
        return products

    def get_deal_products(self, limit: int = 8) -> List[Product]:
        """Lấy sản phẩm giảm giá"""
        return self.db.query(Product).filter(
            Product.discount_percent > 0,
            Product.is_available == True
        ).order_by(desc(Product.discount_percent)).limit(limit).all()

    def get_related_products(self, product_id: int, category_id: int, limit: int = 4) -> List[Product]:
        """Lấy sản phẩm liên quan"""
        return self.db.query(Product).filter(
            Product.category_id == category_id,
            Product.product_id != product_id,
            Product.is_available == True
        ).limit(limit).all()

    # ============ Category ============
    def get_all_categories(self) -> List[Category]:
        """Lấy tất cả danh mục"""
        return self.db.query(Category).filter(
            Category.is_active == True
        ).order_by(Category.display_order, Category.name).all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Lấy danh mục theo ID"""
        return self.db.query(Category).filter(Category.category_id == category_id).first()

    def get_products_by_category(self, category_id: int, page: int = 1, page_size: int = 12) -> Tuple[List[Product], int]:
        """Lấy sản phẩm theo danh mục"""
        query = self.db.query(Product).filter(
            Product.category_id == category_id,
            Product.is_available == True
        )

        total = query.count()
        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()

        return products, total

    # ============ Search ============
    def search_products(self, query: str, limit: int = 10) -> List[Product]:
        """Tìm kiếm sản phẩm"""
        search_term = f"%{query}%"
        return self.db.query(Product).filter(
            Product.is_available == True,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        ).limit(limit).all()

    # ============ Variants ============
    def get_product_variants(self, product_id: int) -> List[ProductVariant]:
        """Lấy biến thể của sản phẩm"""
        return self.db.query(ProductVariant).filter(
            ProductVariant.product_id == product_id,
            ProductVariant.is_active == True
        ).order_by(ProductVariant.display_order).all()

    def get_variant_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        """Lấy biến thể theo ID"""
        return self.db.query(ProductVariant).filter(
            ProductVariant.variant_id == variant_id
        ).first()

    def create_variant(self, variant_data: dict) -> ProductVariant:
        """Tạo biến thể mới"""
        variant = ProductVariant(**variant_data)
        self.db.add(variant)
        self.db.commit()
        self.db.refresh(variant)
        return variant

    def update_variant(self, variant_id: int, variant_data: dict) -> Optional[ProductVariant]:
        """Cập nhật biến thể"""
        variant = self.get_variant_by_id(variant_id)
        if not variant:
            return None

        for key, value in variant_data.items():
            if hasattr(variant, key):
                setattr(variant, key, value)

        self.db.commit()
        self.db.refresh(variant)
        return variant

    def delete_variant(self, variant_id: int) -> bool:
        """Xóa biến thể"""
        variant = self.get_variant_by_id(variant_id)
        if not variant:
            return False
        self.db.delete(variant)
        self.db.commit()
        return True

    # ============ Images ============
    def get_product_images(self, product_id: int) -> List[ProductImage]:
        """Lấy hình ảnh của sản phẩm"""
        return self.db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).order_by(ProductImage.display_order).all()

    def add_product_image(self, product_id: int, image_url: str, is_primary: bool = False) -> ProductImage:
        """Thêm hình ảnh cho sản phẩm"""
        # Nếu là primary, unset others
        if is_primary:
            self.db.query(ProductImage).filter(
                ProductImage.product_id == product_id
            ).update({"is_primary": False})

        image = ProductImage(
            product_id=product_id,
            image_url=image_url,
            is_primary=is_primary
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def delete_product_image(self, image_id: int) -> bool:
        """Xóa hình ảnh"""
        image = self.db.query(ProductImage).filter(ProductImage.image_id == image_id).first()
        if not image:
            return False
        self.db.delete(image)
        self.db.commit()
        return True
