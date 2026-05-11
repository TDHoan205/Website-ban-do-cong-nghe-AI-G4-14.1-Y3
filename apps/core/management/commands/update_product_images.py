"""
Management command de update hinh anh san pham cho dung voi file anh co san trong static va wwwroot.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Update product image URLs to match actual available image files'

    # Mapping tu product keywords den file anh static co san
    IMAGE_MAP = {
        # iPhone
        'iphone 15 pro max': '/static/images/products/iphone-15-pro-max.jpg',
        'iphone 15 pro': '/static/images/products/iphone-15-pro-max.jpg',
        'iphone 15': '/static/images/products/iphone-15-pro-max.jpg',
        'iphone 14': '/static/images/products/iphone-14.jpg',
        'iphone 13': '/static/images/products/iphone-15-pro-max.jpg',  # fallback

        # Samsung Galaxy
        'galaxy s24 ultra': '/static/images/products/galaxy-s24-ultra.jpg',
        'galaxy s24+': '/static/images/products/galaxy-s24-ultra.jpg',
        'galaxy s24': '/static/images/products/galaxy-s24-ultra.jpg',
        'galaxy a55': '/static/images/products/galaxy-s24-ultra.jpg',  # fallback
        'galaxy a35': '/static/images/products/galaxy-s24-ultra.jpg',  # fallback
        'galaxy z flip': '/static/images/products/galaxy-s24-ultra.jpg',  # fallback
        'galaxy tab s9': '/static/images/products/samsung-tab-s9.jpg',
        'galaxy tab s9 fe': '/static/images/products/samsung-tab-s9.jpg',

        # iPad
        'ipad pro': '/static/images/products/ipad-pro.jpg',
        'ipad air': '/static/images/products/ipad-pro.jpg',
        'ipad mini': '/static/images/products/ipad-pro.jpg',
        'ipad': '/static/images/products/ipad-pro.jpg',

        # MacBook
        'macbook pro': '/static/images/products/macbook-pro-m3.jpg',
        'macbook air': '/static/images/products/macbook-pro-m3.jpg',
        'macbook': '/static/images/products/macbook-pro-m3.jpg',

        # Dell
        'dell xps': '/static/images/products/dell-xps15.jpg',
        'dell inspiron': '/static/images/products/dell-xps15.jpg',
        'dell': '/static/images/products/dell-xps15.jpg',

        # Laptop khac - fallback
        'asus rog': '/static/images/products/macbook-pro-m3.jpg',
        'asus vivobook': '/static/images/products/dell-xps15.jpg',
        'asus zenbook': '/static/images/products/dell-xps15.jpg',
        'asus': '/static/images/products/dell-xps15.jpg',
        'hp pavilion': '/static/images/products/dell-xps15.jpg',
        'hp victus': '/static/images/products/dell-xps15.jpg',
        'hp': '/static/images/products/dell-xps15.jpg',
        'lenovo thinkpad': '/static/images/products/dell-xps15.jpg',
        'lenovo ideapad': '/static/images/products/dell-xps15.jpg',
        'lenovo': '/static/images/products/dell-xps15.jpg',
        'msi': '/static/images/products/dell-xps15.jpg',
        'acer swift': '/static/images/products/dell-xps15.jpg',
        'acer': '/static/images/products/dell-xps15.jpg',
        'surface laptop': '/static/images/products/dell-xps15.jpg',
        'surface': '/static/images/products/dell-xps15.jpg',

        # Xiaomi
        'xiaomi 13t': '/static/images/products/xiaomi-14-pro.jpg',
        'xiaomi 14': '/static/images/products/xiaomi-14-pro.jpg',
        'xiaomi redmi': '/static/images/products/xiaomi-14-pro.jpg',
        'xiaomi poco': '/static/images/products/xiaomi-14-pro.jpg',
        'xiaomi': '/static/images/products/xiaomi-14-pro.jpg',
        'redmi': '/static/images/products/xiaomi-14-pro.jpg',
        'poco': '/static/images/products/xiaomi-14-pro.jpg',

        # OPPO
        'oppo reno': '/static/images/products/xiaomi-14-pro.jpg',  # fallback
        'oppo pad': '/static/images/products/samsung-tab-s9.jpg',  # fallback
        'oppo': '/static/images/products/xiaomi-14-pro.jpg',

        # Realme
        'realme': '/static/images/products/xiaomi-14-pro.jpg',  # fallback

        # Nokia
        'nokia': '/static/images/products/galaxy-s24-ultra.jpg',  # fallback

        # Vivo
        'vivo': '/static/images/products/dell-xps15.jpg',  # fallback

        # Audio - AirPods
        'airpods': '/static/images/products/airpods-pro.jpg',

        # Audio - Sony
        'sony wh-1000xm': '/static/images/products/sony-headphones.jpg',
        'sony': '/static/images/products/sony-headphones.jpg',

        # Audio - JBL
        'jbl tune': '/static/images/products/sony-headphones.jpg',
        'jbl flip': '/static/images/products/sony-headphones.jpg',
        'jbl': '/static/images/products/sony-headphones.jpg',

        # Watch - Apple
        'apple watch': '/static/images/products/apple-watch-ultra.jpg',

        # Watch - Samsung/Xiaomi
        'galaxy watch': '/static/images/products/apple-watch-ultra.jpg',
        'xiaomi watch': '/static/images/products/apple-watch-ultra.jpg',
    }

    # Gallery images (2nd, 3rd, 4th image) - dung wwwroot images
    GALLERY_IMAGES = {
        'iphone': [
            'https://picsum.photos/seed/iphone15gallery1/800/800',
            'https://picsum.photos/seed/iphone15gallery2/800/800',
            'https://picsum.photos/seed/iphone15gallery3/800/800',
        ],
        'macbook': [
            'https://picsum.photos/seed/macbookgallery1/800/800',
            'https://picsum.photos/seed/macbookgallery2/800/800',
            'https://picsum.photos/seed/macbookgallery3/800/800',
        ],
        'samsung': [
            'https://picsum.photos/seed/samsunggallery1/800/800',
            'https://picsum.photos/seed/samsunggallery2/800/800',
            'https://picsum.photos/seed/samsunggallery3/800/800',
        ],
        'ipad': [
            'https://picsum.photos/seed/ipadgallery1/800/800',
            'https://picsum.photos/seed/ipadgallery2/800/800',
            'https://picsum.photos/seed/ipadgallery3/800/800',
        ],
        'xiaomi': [
            'https://picsum.photos/seed/xiaomigallery1/800/800',
            'https://picsum.photos/seed/xiaomigallery2/800/800',
            'https://picsum.photos/seed/xiaomigallery3/800/800',
        ],
        'airpods': [
            'https://picsum.photos/seed/airpodsgallery1/800/800',
            'https://picsum.photos/seed/airpodsgallery2/800/800',
            'https://picsum.photos/seed/airpodsgallery3/800/800',
        ],
        'sony': [
            'https://picsum.photos/seed/sonygallery1/800/800',
            'https://picsum.photos/seed/sonygallery2/800/800',
            'https://picsum.photos/seed/sonygallery3/800/800',
        ],
        'apple watch': [
            'https://picsum.photos/seed/applewatchgallery1/800/800',
            'https://picsum.photos/seed/applewatchgallery2/800/800',
            'https://picsum.photos/seed/applewatchgallery3/800/800',
        ],
        'default': [
            'https://picsum.photos/seed/productgallery1/800/800',
            'https://picsum.photos/seed/productgallery2/800/800',
            'https://picsum.photos/seed/productgallery3/800/800',
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Hien thi thay doi khong thuc hien',
        )

    def get_image_for_product(self, product_name: str) -> str:
        """Tim image URL cho san pham dua tren ten."""
        name_lower = product_name.lower()

        # Tim exact match trong IMAGE_MAP
        for keyword, url in self.IMAGE_MAP.items():
            if keyword in name_lower:
                return url

        # Fallback based on category keywords
        if 'iphone' in name_lower:
            return '/static/images/products/iphone-15-pro-max.jpg'
        if 'macbook' in name_lower:
            return '/static/images/products/macbook-pro-m3.jpg'
        if 'ipad' in name_lower:
            return '/static/images/products/ipad-pro.jpg'
        if 'galaxy' in name_lower or 'samsung' in name_lower:
            if 'tab' in name_lower or 'pad' in name_lower:
                return '/static/images/products/samsung-tab-s9.jpg'
            return '/static/images/products/galaxy-s24-ultra.jpg'
        if 'dell' in name_lower:
            return '/static/images/products/dell-xps15.jpg'
        if 'asus' in name_lower or 'hp' in name_lower or 'lenovo' in name_lower or 'acer' in name_lower or 'surface' in name_lower or 'msi' in name_lower:
            return '/static/images/products/dell-xps15.jpg'
        if 'xiaomi' in name_lower or 'redmi' in name_lower or 'poco' in name_lower or 'realme' in name_lower or 'oppo' in name_lower:
            return '/static/images/products/xiaomi-14-pro.jpg'
        if 'airpods' in name_lower:
            return '/static/images/products/airpods-pro.jpg'
        if 'sony' in name_lower:
            return '/static/images/products/sony-headphones.jpg'
        if 'jbl' in name_lower:
            return '/static/images/products/sony-headphones.jpg'
        if 'apple watch' in name_lower:
            return '/static/images/products/apple-watch-ultra.jpg'
        if 'watch' in name_lower:
            return '/static/images/products/apple-watch-ultra.jpg'

        # Default fallback
        return '/static/images/products/placeholder.svg'

    def get_gallery_for_product(self, product_name: str) -> list:
        """Lay gallery images cho san pham."""
        name_lower = product_name.lower()

        for keyword, gallery in self.GALLERY_IMAGES.items():
            if keyword in name_lower:
                return gallery

        return self.GALLERY_IMAGES['default']

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)

        self.stdout.write('Bat dau update hinh anh san pham...')

        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN] Khong co thay doi nao duoc thuc hien'))

        products = Product.objects.all()
        total = products.count()
        updated = 0
        gallery_updated = 0

        for product in products:
            new_image = self.get_image_for_product(product.name)
            old_image = product.image_url or ''

            changed = False
            if old_image != new_image:
                changed = True
                if not dry_run:
                    product.image_url = new_image
                    product.save(update_fields=['image_url'])
                updated += 1

            # Update gallery images
            if changed or not product.product_images.exists():
                gallery = self.get_gallery_for_product(product.name)
                if not dry_run:
                    product.product_images.all().delete()
                    images_to_create = []
                    for idx, url in enumerate(gallery):
                        images_to_create.append(ProductImage(
                            product=product,
                            image_url=url,
                            is_primary=(idx == 0),
                            is_thumbnail=(idx == 0),
                            alt_text=f"{product.name} - Hinh {idx + 1}",
                            display_order=idx + 1,
                        ))
                    ProductImage.objects.bulk_create(images_to_create)
                gallery_updated += 1

            # Log
            status_icon = '>' if changed else '='
            self.stdout.write(f'  {status_icon} {product.name[:50]}')
            if changed:
                self.stdout.write(f'      Old: {old_image}')
                self.stdout.write(f'      New: {new_image}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Tong cong: {total} san pham'))
        self.stdout.write(self.style.SUCCESS(f'Da update image: {updated} san pham'))
        self.stdout.write(self.style.SUCCESS(f'Da update gallery: {gallery_updated} san pham'))

        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN] Chay lenh khong co --dry-run de thuc hien thay doi'))
