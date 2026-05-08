"""
Product Recommender - Gợi ý sản phẩm dựa trên query.
"""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Lazy import để tránh lỗi khi chưa có products app
_product_model = None

def get_product_model():
    global _product_model
    if _product_model is None:
        try:
            from apps.products.models import Product
            _product_model = Product
        except ImportError:
            _product_model = None
    return _product_model


def get_category_model():
    try:
        from apps.categories.models import Category
        return Category
    except ImportError:
        return None


class ProductRecommender:
    """Gợi ý sản phẩm cho chatbot."""

    CATEGORY_KEYWORDS = {
        'laptop': ['laptop', 'máy tính xách tay', 'notebook', 'macbook', 'asus', 'dell', 'hp', 'lenovo', 'acer'],
        'dienthoai': ['điện thoại', 'smartphone', 'phone', 'iphone', 'samsung', 'xiaomi', 'oppo', 'vivo'],
        'tablet': ['tablet', 'ipad', 'máy tính bảng', 'samsung tab'],
        'amthanh': ['tai nghe', 'tai nghe không dây', 'loa', 'loa bluetooth', 'loa nghe nhạc', 'tai nghe bluetooth'],
        'dongho': ['đồng hồ', 'smartwatch', 'apple watch', 'galaxy watch', 'band'],
        'phukien': ['ốp lưng', 'sạc', 'cáp sạc', 'pin dự phòng', 'bàn phím', 'chuột', 'miếng dán'],
        'camera': ['camera', 'máy ảnh', 'webcam', 'action cam'],
    }

    def __init__(self):
        self.Product = get_product_model()
        self.Category = get_category_model()

    def _get_products_from_db(self, query: str, category_hint: str = None, top_k: int = 3) -> List[Dict]:
        """Lấy sản phẩm từ database."""
        if not self.Product:
            return []

        try:
            from django.db.models import Q

            qs = self.Product.objects.filter(is_available=True)

            if category_hint:
                qs = qs.filter(category__slug__icontains=category_hint)

            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            ).select_related('category')[:top_k]

            results = []
            for p in qs:
                img_url = ''
                if hasattr(p, 'product_images') and p.product_images.exists():
                    img_url = p.product_images.first().image.url
                results.append({
                    'product_id': p.id,
                    'name': p.name,
                    'price': float(p.price),
                    'original_price': float(p.original_price) if p.original_price else None,
                    'image_url': img_url,
                    'category': p.category.name if p.category else '',
                    'slug': getattr(p, 'slug', str(p.id)),
                })

            return results
        except Exception as e:
            logger.error(f"Product recommender error: {e}")
            return []

    def _search_by_keywords(self, keywords: List[str], top_k: int = 3) -> List[Dict]:
        """Tìm sản phẩm theo keywords."""
        if not self.Product:
            return []

        try:
            from django.db.models import Q

            qs = self.Product.objects.filter(is_available=True)
            q_filter = Q()
            for kw in keywords:
                q_filter |= Q(name__icontains=kw) | Q(category__name__icontains=kw)

            qs = qs.filter(q_filter).select_related('category')[:top_k]

            results = []
            for p in qs:
                img_url = ''
                if hasattr(p, 'product_images') and p.product_images.exists():
                    img_url = p.product_images.first().image.url
                results.append({
                    'product_id': p.id,
                    'name': p.name,
                    'price': float(p.price),
                    'original_price': float(p.original_price) if p.original_price else None,
                    'image_url': img_url,
                    'category': p.category.name if p.category else '',
                    'slug': getattr(p, 'slug', str(p.id)),
                })
            return results
        except Exception as e:
            logger.error(f"Product search error: {e}")
            return []

    def _detect_category_from_query(self, query: str) -> Optional[str]:
        """Phát hiện category từ query."""
        query_lower = query.lower()
        for cat_key, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in query_lower:
                    return cat_key
        return None

    def _get_featured_products(self, top_k: int = 3) -> List[Dict]:
        """Lấy sản phẩm nổi bật làm fallback."""
        if not self.Product:
            return []

        try:
            from django.db.models import Q, F

            qs = self.Product.objects.filter(
                is_available=True
            ).exclude(
                original_price__isnull=True
            ).exclude(
                original_price=0
            ).filter(
                original_price__gt=F('price')
            ).select_related('category')[:top_k]

            results = []
            for p in qs:
                img_url = ''
                if hasattr(p, 'product_images') and p.product_images.exists():
                    img_url = p.product_images.first().image.url
                results.append({
                    'product_id': p.id,
                    'name': p.name,
                    'price': float(p.price),
                    'original_price': float(p.original_price) if p.original_price else None,
                    'image_url': img_url,
                    'category': p.category.name if p.category else '',
                    'slug': getattr(p, 'slug', str(p.id)),
                })
            return results
        except Exception as e:
            logger.error(f"Featured products error: {e}")
            return []

    def get_recommendations(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Lấy gợi ý sản phẩm cho query.
        Ưu tiên: DB search → keyword search → featured products.
        """
        if not query or len(query.strip()) < 2:
            return self._get_featured_products(top_k)

        # 1. Thử tìm theo category hint
        category_hint = self._detect_category_from_query(query)
        results = self._get_products_from_db(query, category_hint, top_k)
        if results:
            return results

        # 2. Thử tìm theo keywords
        keywords = [w.strip() for w in query.split() if len(w.strip()) >= 3]
        if keywords:
            results = self._search_by_keywords(keywords[:5], top_k)
            if results:
                return results

        # 3. Fallback: sản phẩm nổi bật
        return self._get_featured_products(top_k)
