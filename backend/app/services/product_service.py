from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional, Tuple
from app.models.product import Product, ProductVariant, Category, ProductImage
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_products(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        sort_by: str = "newest",
        page: int = 1,
        page_size: int = 20,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        filter_type: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        query = self.db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.supplier),
            joinedload(Product.variants),
            joinedload(Product.images),
        )

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if min_price:
            query = query.filter(
                or_(
                    Product.price >= min_price,
                    Product.variants.any(ProductVariant.price >= min_price)
                )
            )

        if max_price:
            query = query.filter(
                or_(
                    Product.price <= max_price,
                    Product.variants.any(ProductVariant.price <= max_price)
                )
            )

        if filter_type:
            if filter_type.lower() == "new":
                query = query.filter(Product.is_new == True)
            elif filter_type.lower() == "hot":
                query = query.filter(Product.is_hot == True)
            elif filter_type.lower() == "deal":
                query = query.filter(
                    or_(Product.discount_percent > 0, Product.original_price != None)
                )

        sort_options = {
            "name": Product.name.asc(),
            "name_desc": Product.name.desc(),
            "price": Product.price.asc(),
            "price_desc": Product.price.desc(),
            "newest": Product.product_id.desc(),
            "rating": Product.rating.desc(),
        }
        query = query.order_by(sort_options.get(sort_by, Product.product_id.desc()))

        total = query.count()
        products = query.offset((page - 1) * page_size).limit(page_size).all()

        return products, total

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.supplier),
            joinedload(Product.variants),
            joinedload(Product.images),
            joinedload(Product.inventory),
        ).filter(Product.product_id == product_id).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return False

        self.db.delete(product)
        self.db.commit()
        return True

    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return False

        product.stock_quantity = max(0, product.stock_quantity + quantity_change)
        self.db.commit()
        return True

    def search_products(self, query: str, limit: int = 10) -> List[Product]:
        search_term = f"%{query}%"
        return self.db.query(Product).options(
            joinedload(Product.category)
        ).filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        ).limit(limit).all()

    def get_related_products(self, product_id: int, category_id: int, limit: int = 5) -> List[Product]:
        return self.db.query(Product).options(
            joinedload(Product.category),
        ).filter(
            Product.category_id == category_id,
            Product.product_id != product_id,
        ).limit(limit).all()

    def get_featured_products(self, feature_type: str = "new", limit: int = 10) -> List[Product]:
        query = self.db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.supplier),
        )

        if feature_type == "new":
            query = query.filter(Product.is_new == True)
        elif feature_type == "hot":
            query = query.filter(Product.is_hot == True)
        elif feature_type == "deal":
            query = query.filter(
                or_(Product.discount_percent > 0, Product.original_price != None)
            )

        return query.limit(limit).all()
