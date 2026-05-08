"""
Management command để seed dữ liệu mẫu.
Mirror từ SeedData.cs của dự án C# Webstore.

Usage:
    python manage.py seed_data
    python manage.py seed_data --reset  # Xóa dữ liệu cũ trước khi seed
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.users.models import Account
from apps.categories.models import Category
from apps.suppliers.models import Supplier
from apps.products.models import Product, ProductVariant, ProductImage
from apps.orders.models import Order, OrderItem
from apps.inventory.models import Inventory
from apps.faqs.models import FAQ
from apps.chat.models import ChatSession, ChatMessage


class Command(BaseCommand):
    help = 'Seed sample data cho TechShop website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Xóa dữ liệu cũ trước khi seed',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Đang xóa dữ liệu cũ...')
            self._reset_data()

        self.stdout.write('🚀 Bắt đầu seed dữ liệu...')

        with transaction.atomic():
            self._seed_categories()
            self._seed_suppliers()
            self._seed_accounts()
            self._seed_products()
            self._seed_product_variants()
            self._seed_product_images()
            self._seed_inventory()
            self._seed_faqs()
            self._seed_orders()

        self.stdout.write(self.style.SUCCESS('✅ Seed dữ liệu hoàn tất!'))

    def _reset_data(self):
        """Xóa dữ liệu theo thứ tự để tránh lỗi foreign key."""
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        ProductImage.objects.all().delete()
        ProductVariant.objects.all().delete()
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        FAQ.objects.all().delete()
        ChatMessage.objects.all().delete()
        ChatSession.objects.all().delete()
        Supplier.objects.all().delete()
        Category.objects.all().delete()
        Account.objects.filter(role='Customer').delete()
        Account.objects.filter(role='Admin').delete()
        self.stdout.write('   Đã xóa dữ liệu cũ.')

    def _seed_categories(self):
        """Seed 20 categories."""
        self.stdout.write('📂 Đang seed Categories...')
        
        categories_data = [
            ('Điện thoại di động', 'Điện thoại thông minh các hãng', 1, 'mobile-alt'),
            ('Laptop & Máy tính', 'Máy tính xách tay và máy bàn', 2, 'laptop'),
            ('Tablet', 'Máy tính bảng', 3, 'tablet-alt'),
            ('Tai nghe & Âm thanh', 'Tai nghe, loa bluetooth', 4, 'headphones'),
            ('Phụ kiện điện tử', 'Sạc, cáp, hub USB', 5, 'plug'),
            ('Thiết bị mạng', 'Router, wifi mesh', 6, 'wifi'),
            ('Máy ảnh & Quay phim', 'Máy ảnh, action cam', 7, 'camera'),
            ('Linh kiện máy tính', 'RAM, SSD, VGA', 8, 'cpu'),
            ('Đồng hồ thông minh', 'Smartwatch, vòng tay thông minh', 9, 'smartwatch'),
            ('Bàn phím & Chuột', 'Bàn phím, chuột máy tính', 10, 'keyboard'),
            ('Màn hình máy tính', 'Màn hình LED, IPS, OLED', 11, 'display'),
            ('Ổ cứng & Lưu trữ', 'HDD, SSD, NAS', 12, 'hard-drive'),
            ('Sạc & Cáp kết nối', 'Sạc nhanh, cáp USB-C', 13, 'usb-c'),
            ('Bảo vệ & Ốp lưng', 'Ốp lưng, kính bảo vệ', 14, 'shield-check'),
            ('Máy in & Thiết bị văn phòng', 'Máy in, máy scan', 15, 'printer'),
            ('Camera giám sát', 'Camera IP, webcam', 16, 'webcam'),
            ('Loa & Dàn âm thanh', 'Loa bluetooth, loa thông minh', 17, 'speaker'),
            ('Gaming Gear', 'Tay cầm, bàn di chuột', 18, 'gamepad'),
            ('Thiết bị thông minh', 'Smart home, robot hút bụi', 19, 'house'),
            ('Phần mềm & Bản quyền', 'Phần mềm, license', 20, 'code-slash'),
        ]

        for name, description, order, icon in categories_data:
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'display_order': order,
                    'is_active': True,
                    'icon_name': icon,
                }
            )

        self.stdout.write(f'   Đã tạo {Category.objects.count()} categories')

    def _seed_suppliers(self):
        """Seed 20 suppliers."""
        self.stdout.write('🏢 Đang seed Suppliers...')

        suppliers_data = [
            ('Apple Vietnam', 'contact@apple.com.vn', '1800-1192', 'Phòng Kinh Doanh', 'Lầu 3, Sheraton Plaza, 175 Đồng Khởi, Q.1, TP.HCM'),
            ('Samsung Electronics Vietnam', 'contact@samsung.com.vn', '1800-588-889', 'Bộ phận Đối tác', 'Tòa nhà PVI, 1 Phạm Văn Bạch, Cầu Giấy, Hà Nội'),
            ('Dell Vietnam', 'dell@vietnam.com', '1800-545-455', 'Phòng Phân phối', 'Tòa nhà Empress, 128 Hồng Bàng, Q.5, TP.HCM'),
            ('Sony Vietnam', 'sony@vietnam.com', '1800-588-880', 'Phòng Kinh doanh', 'Tòa nhà VBC, Q.1, TP.HCM'),
            ('LG Electronics Vietnam', 'lg@vietnam.com', '1800-1503', 'Bộ phận Đối tác', 'Tòa nhà Lotte Center, Hà Nội'),
            ('Xiaomi Vietnam', 'xiaomi@vn.com', '1800-1234-05', 'Phòng Marketing', 'Tòa nhà Bitexco, Q.1, TP.HCM'),
            ('OPPO Vietnam', 'oppo@vn.com', '1800-5555-01', 'Bộ phận Kinh doanh', 'Tòa nhà Lotte Center, Q.1, TP.HCM'),
            ('Realme Vietnam', 'realme@vn.com', '1800-8888-01', 'Phòng Hỗ trợ', 'Quận 7, TP.HCM'),
            ('ASUS Vietnam', 'asus@vn.com', '1800-8888-09', 'Phòng Kinh doanh', 'Tòa nhà Saigon Tower, Q.1, TP.HCM'),
            ('HP Vietnam', 'hp@vn.com', '1800-5888-54', 'Bộ phận Bán lẻ', 'Tòa nhà Gemadept, Q.1, TP.HCM'),
            ('Lenovo Vietnam', 'lenovo@vn.com', '1800-1003', 'Phòng Kinh doanh', 'Quận 2, TP.HCM'),
            ('Logitech Vietnam', 'logitech@vn.com', '1800-1234-89', 'Bộ phận Phân phối', 'Quận Phú Nhuận, TP.HCM'),
            ('JBL Vietnam', 'jbl@vn.com', '1800-8888-52', 'Phòng Marketing', 'Quận 3, TP.HCM'),
            ('Anker Vietnam', 'anker@vn.com', '1800-1234-56', 'Bộ phận Hỗ trợ', 'Quận Bình Thạnh, TP.HCM'),
            ('Kingston Technology', 'kingston@vn.com', '1800-8888-44', 'Phòng Kinh doanh', 'Quận Gò Vấp, TP.HCM'),
            ('Corsair Vietnam', 'corsair@vn.com', '1800-9999-88', 'Bộ phận Gaming', 'Quận Tân Bình, TP.HCM'),
            ('Western Digital Vietnam', 'wd@vn.com', '1800-5555-44', 'Phòng Phân phối', 'Quận 10, TP.HCM'),
            ('TP-Link Vietnam', 'tplink@vn.com', '1800-8888-47', 'Bộ phận Mạng', 'Quận Tân Phú, TP.HCM'),
            ('Canon Vietnam', 'canon@vn.com', '1800-9999-26', 'Phòng Kinh doanh', 'Tòa nhà MB Center, Q.1, TP.HCM'),
            ('Nikon Vietnam', 'nikon@vn.com', '1800-1234-65', 'Bộ phận Camera', 'Quận 3, TP.HCM'),
        ]

        for name, email, phone, contact, address in suppliers_data:
            Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'email': email,
                    'phone': phone,
                    'contact_person': contact,
                    'address': address,
                    'is_active': True,
                }
            )

        self.stdout.write(f'   Đã tạo {Supplier.objects.count()} suppliers')

    def _seed_accounts(self):
        """Seed 15 accounts (1 admin, 14 customers)."""
        self.stdout.write('👤 Đang seed Accounts...')

        # Create admin account
        admin, created = Account.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@techshop.com',
                'full_name': 'Nguyễn Văn An',
                'phone': '0123456789',
                'address': '123 Đường ABC, Quận 1, TP.HCM',
                'role': 'Admin',
                'is_active': True,
                'is_staff': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()

        # Create customer accounts
        customers_data = [
            ('khachhang1', 'Lê Minh Cường', 'cuong.le@email.com', '0901234567', '789 Đường DEF, Q.3, TP.HCM'),
            ('khachhang2', 'Phạm Hoàng Duy', 'duy.pham@email.com', '0902345678', '321 Đường GHI, Q.4, TP.HCM'),
            ('khachhang3', 'Vũ Thị Em', 'em.vu@email.com', '0903456789', '654 Đường JKL, Q.5, TP.HCM'),
            ('khachhang4', 'Đặng Minh Phong', 'phong.dang@email.com', '0904567890', '987 Đường MNO, Q.6, TP.HCM'),
            ('khachhang5', 'Bùi Thị Quỳnh', 'quynh.bui@email.com', '0905678901', '147 Đường PQR, Q.7, TP.HCM'),
            ('khachhang6', 'Hoàng Văn Sơn', 'son.hoang@email.com', '0906789012', '258 Đường STU, Q.8, TP.HCM'),
            ('khachhang7', 'Ngô Thị Thanh', 'thanh.ngo@email.com', '0907890123', '369 Đường VWX, Q.9, TP.HCM'),
            ('khachhang8', 'Trịnh Văn Tùng', 'tung.trinh@email.com', '0908901234', '741 Đường YZA, Q.10, TP.HCM'),
            ('khachhang9', 'Lý Thị Vân', 'van.ly@email.com', '0909012345', '852 Đường BCD, Q.11, TP.HCM'),
            ('khachhang10', 'Đinh Minh Tuấn', 'tuan.dinh@email.com', '0910123456', '963 Đường EFG, Q.12, TP.HCM'),
            ('khachhang11', 'Võ Thị Ngọc', 'ngoc.vo@email.com', '0915678901', '159 Đường TUV, Q.Tân Phú, TP.HCM'),
            ('khachhang12', 'Đỗ Văn Hùng', 'hung.do@email.com', '0916789012', '753 Đường WXY, Q.Bình Tân, TP.HCM'),
            ('khachhang13', 'Hồ Thị Mai', 'mai.ho@email.com', '0917890123', '951 Đường ZAB, H.Hóc Môn, TP.HCM'),
            ('khachhang14', 'Nguyễn Văn Đức', 'duc.nguyen@email.com', '0918901234', '246 Đường CDE, H.Củ Chi, TP.HCM'),
        ]

        for username, full_name, email, phone, address in customers_data:
            customer, created = Account.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'full_name': full_name,
                    'phone': phone,
                    'address': address,
                    'role': 'Customer',
                    'is_active': True,
                }
            )
            if created:
                customer.set_password('password123')
                customer.save()

        self.stdout.write(f'   Đã tạo {Account.objects.count()} accounts (1 admin, {Account.objects.filter(role="Customer").count()} customers)')

    def _seed_products(self):
        """Seed 50 products."""
        self.stdout.write('📦 Đang seed Products...')

        # Get categories and suppliers
        phone_cat = Category.objects.get(name='Điện thoại di động')
        laptop_cat = Category.objects.get(name='Laptop & Máy tính')
        tablet_cat = Category.objects.get(name='Tablet')
        audio_cat = Category.objects.get(name='Tai nghe & Âm thanh')
        accessory_cat = Category.objects.get(name='Phụ kiện điện tử')
        keyboard_cat = Category.objects.get(name='Bàn phím & Chuột')
        watch_cat = Category.objects.get(name='Đồng hồ thông minh')

        apple = Supplier.objects.get(name='Apple Vietnam')
        samsung = Supplier.objects.get(name='Samsung Electronics Vietnam')
        dell = Supplier.objects.get(name='Dell Vietnam')
        sony = Supplier.objects.get(name='Sony Vietnam')
        xiaomi = Supplier.objects.get(name='Xiaomi Vietnam')
        oppo = Supplier.objects.get(name='OPPO Vietnam')
        realme = Supplier.objects.get(name='Realme Vietnam')
        asus = Supplier.objects.get(name='ASUS Vietnam')
        hp = Supplier.objects.get(name='HP Vietnam')
        lenovo = Supplier.objects.get(name='Lenovo Vietnam')
        logitech = Supplier.objects.get(name='Logitech Vietnam')
        jbl = Supplier.objects.get(name='JBL Vietnam')
        anker = Supplier.objects.get(name='Anker Vietnam')
        corsair = Supplier.objects.get(name='Corsair Vietnam')

        products_data = [
            # ĐIỆN THOẠI (10)
            ('iPhone 15 Pro Max 256GB Titan Tự Nhiên', 'Titan grade 5, A17 Pro chip, camera 48MP, Dynamic Island, pin siêu bền cả ngày.', 34990000, phone_cat, apple, True, True),
            ('iPhone 15 Pro 128GB Titan Xanh', 'Chip A17 Pro, camera 48MP, titanium grade 5, USB-C 3.0.', 27990000, phone_cat, apple, True, False),
            ('iPhone 15 128GB Xanh Dương', 'Chip A16 Bionic, camera 48MP, Dynamic Island, pin 24h.', 19990000, phone_cat, apple, True, False),
            ('iPhone 13 128GB Hồng', 'Chip A15 Bionic, camera kép 12MP, Face ID nhanh.', 15990000, phone_cat, apple, False, True),
            ('Samsung Galaxy S24 Ultra 256GB Titan Đen', 'S Pen tích hợp, màn hình Dynamic AMOLED 2X 6.8 inch, camera 200MP, pin 5000mAh.', 29990000, phone_cat, samsung, True, True),
            ('Samsung Galaxy S24+ 256GB Tím', 'Màn hình 6.7 inch AMOLED 2X, camera 50MP, pin 4900mAh.', 24990000, phone_cat, samsung, True, False),
            ('Samsung Galaxy A55 5G 128GB Xanh', 'Màn hình 6.6 inch Super AMOLED, camera 50MP, pin 5000mAh.', 9990000, phone_cat, samsung, False, True),
            ('Samsung Galaxy A35 5G 128GB Vàng', 'Màn hình 6.6 inch FHD+, camera 50MP OIS, kháng nước IP67.', 7490000, phone_cat, samsung, False, False),
            ('Samsung Galaxy Z Flip5 256GB Xanh', 'Màn hình gập nhỏ gọn 6.7 inch, Snapdragon 8 Gen 2, Flex Mode đa năng.', 22990000, phone_cat, samsung, False, True),
            ('Xiaomi 13T Pro 512GB Xanh', 'Snapdragon 8 Gen 2, Leica camera 50MP, 120W HyperCharge siêu nhanh.', 19990000, phone_cat, xiaomi, True, False),
            
            # LAPTOP (10)
            ('MacBook Pro 14 M3 Pro 512GB Bạc', 'Chip M3 Pro 12-core CPU, 18-core GPU, 18GB RAM, 512GB SSD, Liquid Retina XDR.', 49990000, laptop_cat, apple, True, True),
            ('MacBook Air 15 M3 256GB Xám', 'Chip M3, 15.3 inch Liquid Retina, 8GB RAM, 256GB SSD, pin 18h.', 32990000, laptop_cat, apple, True, True),
            ('Dell XPS 15 9530 1TB Bạc', 'Intel Core i9-13900H, RTX 4070, 32GB RAM, 1TB SSD, 15.6 inch 3.5K OLED.', 69990000, laptop_cat, dell, False, False),
            ('Dell Inspiron 15 3530 512GB Đen', 'Intel Core i5-1335U, 8GB RAM, 512GB SSD, 15.6 inch FHD IPS.', 15990000, laptop_cat, dell, False, False),
            ('ASUS ROG Zephyrus G14 1TB Trắng', 'AMD Ryzen 9 7940HS, RTX 4070, 16GB RAM, 1TB SSD, 14 inch 165Hz.', 54990000, laptop_cat, asus, False, True),
            ('ASUS VivoBook 15 512GB Bạc', 'Intel Core i5-1235U, 8GB RAM, 512GB SSD, 15.6 inch FHD.', 13990000, laptop_cat, asus, False, False),
            ('HP Pavilion Plus 14 512GB Xanh', 'Intel Core i7-13700H, 16GB RAM, 512GB SSD, 14 inch 2.8K OLED.', 29990000, laptop_cat, hp, True, False),
            ('HP Victus 15 512GB Đen', 'AMD Ryzen 5 7535HS, RTX 2050, 8GB RAM, 512GB SSD, 15.6 inch 144Hz.', 18990000, laptop_cat, hp, False, True),
            ('Lenovo ThinkPad X1 Carbon 512GB Đen', 'Intel Core i7-1365U, 16GB RAM, 512GB SSD, 14 inch 2.8K OLED.', 49990000, laptop_cat, lenovo, False, False),
            ('Lenovo IdeaPad Gaming 3 512GB Đen', 'AMD Ryzen 5 5600H, RTX 3050, 8GB RAM, 512GB SSD, 15.6 inch 120Hz.', 16990000, laptop_cat, lenovo, False, True),

            # TABLET (5)
            ('iPad Pro 12.9 inch M2 256GB Xám', 'M2 chip, 12.9-inch Liquid Retina XDR, 256GB, WiFi + 5G.', 32990000, tablet_cat, apple, True, False),
            ('iPad Air M2 256GB Tím', 'Chip M2, 11 inch Liquid Retina, 256GB, WiFi, hỗ trợ Apple Pencil Pro.', 22990000, tablet_cat, apple, True, True),
            ('iPad mini 6 64GB Hồng', 'Chip A15 Bionic, 8.3 inch Liquid Retina, hỗ trợ Apple Pencil Gen 2.', 14990000, tablet_cat, apple, False, False),
            ('Samsung Galaxy Tab S9 Ultra 256GB Đen', 'Snapdragon 8 Gen 2, 14.6 inch AMOLED 120Hz, S Pen included.', 28990000, tablet_cat, samsung, True, True),
            ('Samsung Galaxy Tab S9 FE 128GB Bạc', 'Exynos 1380, 10.9 inch LCD, S Pen included, 128GB.', 9990000, tablet_cat, samsung, False, False),

            # TAI NGHE (5)
            ('Sony WH-1000XM5 Đen', 'Tai nghe chống ồn cao cấp, 30 giờ pin, LDAC, 8 micro khử ồn AI.', 9990000, audio_cat, sony, True, True),
            ('AirPods Pro 2 Trắng', 'Chip H2, Active Noise Cancellation, Adaptive Audio, USB-C.', 6490000, audio_cat, apple, True, True),
            ('Samsung Galaxy Buds2 Pro Trắng', 'Tai nghe True Wireless, chống ồn chủ động, 360 Audio, IPX7.', 4990000, audio_cat, samsung, False, False),
            ('JBL Tune 770NC Đen', 'Tai nghe over-ear chống ồn, 70 giờ pin, JBL Pure Bass Sound.', 2990000, audio_cat, jbl, False, True),
            ('JBL Flip 6 Xanh', 'Loa bluetooth chống nước IPX7, 12 giờ pin, JBL Pro Sound.', 2490000, audio_cat, jbl, False, False),

            # BÀN PHÍM & CHUỘT (5)
            ('Logitech MX Master 3S Đen', 'Chuột không dây cao cấp, 8K DPI, kết nối 3 thiết bị.', 2490000, keyboard_cat, logitech, True, True),
            ('Keychron K3 Pro Đen', 'Bàn phím cơ low-profile, switch Gateron, kết nối đa thiết bị.', 2290000, keyboard_cat, logitech, False, False),
            ('Logitech G Pro X Superlight 2 Trắng', 'Chuột gaming siêu nhẹ 60g, HERO 25K sensor, 95h pin.', 3490000, keyboard_cat, logitech, True, True),
            ('Corsair K70 RGB Pro Đen', 'Bàn phím gaming cơ, switch Cherry MX, RGB per-key.', 3990000, keyboard_cat, corsair, False, False),
            ('Logitech G502 X Plus Trắng', 'Chuột gaming, HERO 25K sensor, 13 nút lập trình.', 1990000, keyboard_cat, logitech, False, True),

            # PHỤ KIỆN (5)
            ('Anker 735 65W GaN Đen', 'Sạc nhanh GaN 65W, 3 cổng USB-C, siêu nhỏ gọn.', 1290000, accessory_cat, anker, True, True),
            ('Anker PowerCore 20000 Đen', 'Pin dự phòng 20000mAh, sạc nhanh PowerIQ.', 1490000, accessory_cat, anker, False, False),
            ('HyperDrive Gen2 Bạc', 'Hub USB-C 10 in 1, HDMI 4K, SD/microSD, 100W PD.', 2490000, accessory_cat, anker, False, True),
            ('Targus Newport Đen', 'Túi đựng laptop 15.6 inch, chống sốc, nhiều ngăn.', 990000, accessory_cat, anker, False, False),
            ('Samsung T7 1TB Xám', 'Ổ SSD di động USB 3.2 Gen 2, tốc độ 1050MB/s.', 2490000, accessory_cat, samsung, False, True),

            # ĐỒNG HỒ THÔNG MINH (3)
            ('Apple Watch Series 9 45mm Đen', 'Chip S9, màn hình Always-On Retina, theo dõi sức khỏe.', 11990000, watch_cat, apple, True, True),
            ('Samsung Galaxy Watch 6 Classic 47mm Bạc', 'Màn hình Super AMOLED 47mm, bezel xoay, LTE.', 9990000, watch_cat, samsung, True, False),
            ('Xiaomi Watch S3 Đen', 'Màn hình AMOLED 1.43 inch, GPS tích hợp, 21 ngày pin.', 3990000, watch_cat, xiaomi, True, False),

            # THÊM SẢN PHẨM (7)
            ('MSI Modern 15 H 512GB Đen', 'Intel Core i7-13700H, RTX 2050, 16GB RAM, 512GB SSD.', 24990000, laptop_cat, dell, False, False),
            ('ASUS ZenBook 14 OLED 512GB Xanh', 'Intel Core Ultra 7, 16GB RAM, 512GB SSD, 14 inch 2.8K OLED.', 27990000, laptop_cat, asus, True, True),
            ('Acer Swift Go 14 512GB Bạc', 'Intel Core Ultra 5, 16GB RAM, 512GB SSD, 14 inch 2.8K OLED.', 21990000, laptop_cat, dell, True, True),
            ('Realme C67 128GB Xanh', 'Snapdragon 685, camera 108MP, pin 5000mAh, sạc nhanh 33W.', 4990000, phone_cat, realme, False, True),
            ('OPPO Reno11 F 5G 256GB Xanh', 'Dimensity 7050, camera 64MP OIS, sạc nhanh 67W SUPERVOOC.', 9990000, phone_cat, oppo, True, False),
            ('Xiaomi Redmi Note 13 Pro 256GB Đen', 'Snapdragon 7s Gen 2, camera 200MP OIS, sạc nhanh 120W.', 7990000, phone_cat, xiaomi, True, True),
            ('Xiaomi POCO X6 Pro 256GB Vàng', 'Dimensity 8300-Ultra, camera 64MP OIS, 120Hz AMOLED.', 9990000, phone_cat, xiaomi, True, True),
        ]

        for name, desc, price, category, supplier, is_new, is_hot in products_data:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'price': Decimal(str(price)),
                    'category': category,
                    'supplier': supplier,
                    'is_new': is_new,
                    'is_hot': is_hot,
                    'is_available': True,
                    'stock_quantity': random.randint(10, 200),
                    'rating': Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                }
            )

        self.stdout.write(f'   Đã tạo {Product.objects.count()} products')

    def _seed_product_variants(self):
        """Seed product variants cho mỗi sản phẩm."""
        self.stdout.write('🔀 Đang seed Product Variants...')

        phone_cat = Category.objects.get(name='Điện thoại di động')
        tablet_cat = Category.objects.get(name='Tablet')
        laptop_cat = Category.objects.get(name='Laptop & Máy tính')
        audio_cat = Category.objects.get(name='Tai nghe & Âm thanh')
        watch_cat = Category.objects.get(name='Đồng hồ thông minh')

        storage_options = ['128GB', '256GB', '512GB', '1TB']
        ram_options = ['8GB', '16GB', '32GB']
        color_options = ['Đen', 'Trắng', 'Xanh', 'Tím', 'Vàng']

        for product in Product.objects.all():
            # Skip if already has variants
            if product.variants.exists():
                continue

            variants = []
            base_price = product.price

            if product.category == phone_cat or product.category == tablet_cat:
                # Phone/Tablet: variants by storage
                for i, storage in enumerate(storage_options[:2]):
                    variant_price = base_price + (i * Decimal('3000000'))
                    variants.append(ProductVariant(
                        product=product,
                        color='Mặc định',
                        storage=storage,
                        variant_name=f'{product.name} {storage}',
                        price=variant_price,
                        stock_quantity=random.randint(10, 100),
                        display_order=i,
                        is_active=True,
                    ))
            elif product.category == laptop_cat:
                # Laptop: variants by RAM/SSD
                for i, (ram, storage) in enumerate([('16GB', '512GB'), ('32GB', '1TB')]):
                    variant_price = base_price + (i * Decimal('5000000'))
                    variants.append(ProductVariant(
                        product=product,
                        ram=ram,
                        storage=storage,
                        variant_name=f'{product.name} {ram}/{storage}',
                        price=variant_price,
                        stock_quantity=random.randint(5, 50),
                        display_order=i,
                        is_active=True,
                    ))
            elif product.category == audio_cat or product.category == watch_cat:
                # Audio/Watch: variants by color
                for i, color in enumerate(color_options[:2]):
                    variants.append(ProductVariant(
                        product=product,
                        color=color,
                        variant_name=f'{product.name} - {color}',
                        price=base_price,
                        stock_quantity=random.randint(20, 80),
                        display_order=i,
                        is_active=True,
                    ))
            else:
                # Default: 2 variants
                variants.append(ProductVariant(
                    product=product,
                    variant_name=f'{product.name} - Bản tiêu chuẩn',
                    price=base_price,
                    stock_quantity=random.randint(20, 100),
                    display_order=0,
                    is_active=True,
                ))
                variants.append(ProductVariant(
                    product=product,
                    variant_name=f'{product.name} - Bản cao cấp',
                    price=base_price + Decimal('1000000'),
                    stock_quantity=random.randint(10, 60),
                    display_order=1,
                    is_active=True,
                ))

            ProductVariant.objects.bulk_create(variants)

        self.stdout.write(f'   Đã tạo {ProductVariant.objects.count()} product variants')

    def _seed_product_images(self):
        """Seed product images cho mỗi sản phẩm."""
        self.stdout.write('🖼️  Đang seed Product Images...')

        for product in Product.objects.all():
            # Skip if already has images
            if product.product_images.exists():
                continue

            # Primary image
            ProductImage.objects.create(
                product=product,
                image_url=f'/images/products/{product.product_id}.png',
                is_primary=True,
                is_thumbnail=True,
                display_order=1,
            )
            # Secondary gallery image
            ProductImage.objects.create(
                product=product,
                image_url=f'/images/products/{product.product_id}_2.png',
                is_primary=False,
                is_thumbnail=False,
                display_order=2,
            )

        self.stdout.write(f'   Đã tạo {ProductImage.objects.count()} product images')

    def _seed_inventory(self):
        """Seed inventory cho mỗi sản phẩm."""
        self.stdout.write('📊 Đang seed Inventory...')

        for product in Product.objects.all():
            Inventory.objects.get_or_create(
                product=product,
                defaults={
                    'stock_quantity': product.stock_quantity,
                    'low_stock_threshold': 10,
                }
            )

        self.stdout.write(f'   Đã tạo {Inventory.objects.count()} inventory records')

    def _seed_faqs(self):
        """Seed 20 FAQs."""
        self.stdout.write('❓ Đang seed FAQs...')

        faqs_data = [
            ('Làm sao để đặt hàng?', 'Bạn có thể đặt hàng trực tiếp trên website bằng cách chọn sản phẩm, thêm vào giỏ hàng và tiến hành thanh toán.', 'Đặt hàng', 1),
            ('Các phương thức thanh toán nào được chấp nhận?', 'Chúng tôi chấp nhận thanh toán qua: COD (nhận hàng rồi trả tiền), chuyển khoản ngân hàng.', 'Thanh toán', 1),
            ('Thời gian giao hàng là bao lâu?', 'Đơn hàng nội thành TP.HCM: 1-2 ngày. Các tỉnh thành khác: 2-5 ngày tùy khu vực.', 'Vận chuyển', 1),
            ('Chính sách đổi trả như thế nào?', 'Quý khách được đổi trả trong vòng 7 ngày nếu sản phẩm bị lỗi từ nhà sản xuất.', 'Đổi trả', 1),
            ('Làm sao để liên hệ hỗ trợ?', 'Bạn có thể liên hệ qua hotline 0123-456-789, email support@techshop.com.', 'Hỗ trợ', 1),
            ('Có giao hàng COD không?', 'Có, chúng tôi hỗ trợ thanh toán khi nhận hàng (COD) cho tất cả các đơn hàng.', 'Thanh toán', 2),
            ('Làm sao để theo dõi đơn hàng?', 'Sau khi đặt hàng thành công, bạn sẽ nhận được mã đơn hàng để theo dõi.', 'Đặt hàng', 2),
            ('Sản phẩm có bảo hành không?', 'Tất cả sản phẩm đều được bảo hành chính hãng. Thời gian bảo hành tùy theo sản phẩm (12-24 tháng).', 'Bảo hành', 1),
            ('Tôi có thể hủy đơn hàng không?', 'Bạn có thể hủy đơn hàng trước khi sản phẩm được giao.', 'Đặt hàng', 2),
            ('Phí vận chuyển là bao nhiêu?', 'Miễn phí vận chuyển cho đơn hàng từ 500.000đ trở lên. Đơn hàng dưới 500.000đ phí ship 30.000đ.', 'Vận chuyển', 1),
            ('Sản phẩm có chính hãng không?', 'Tất cả sản phẩm tại TechShop đều là hàng chính hãng 100%.', 'Sản phẩm', 1),
            ('Làm sao để đăng ký tài khoản?', 'Click vào nút Đăng ký ở góc phải màn hình, điền thông tin cá nhân.', 'Tài khoản', 2),
            ('Quên mật khẩu thì làm sao?', 'Click vào Quên mật khẩu ở trang đăng nhập, nhập email đã đăng ký.', 'Tài khoản', 2),
            ('Tôi có thể cập nhật thông tin cá nhân không?', 'Có, đăng nhập vào tài khoản, vào mục Tài khoản để cập nhật.', 'Tài khoản', 3),
            ('Có chương trình khuyến mãi không?', 'Chúng tôi thường xuyên có các chương trình khuyến mãi và mã giảm giá.', 'Khuyến mãi', 2),
            ('Sản phẩm có đầy đủ phụ kiện không?', 'Tất cả sản phẩm đều có đầy đủ phụ kiện theo quy định của nhà sản xuất.', 'Sản phẩm', 3),
            ('Tôi có thể mua sỉ không?', 'Có, chúng tôi có chính sách bán sỉ cho các đơn hàng lớn.', 'Mua sỉ', 3),
            ('Sản phẩm còn hàng không?', 'Website cập nhật số lượng tồn kho theo thời gian thực.', 'Sản phẩm', 2),
            ('Làm sao để viết đánh giá sản phẩm?', 'Sau khi nhận được hàng và đăng nhập, vào trang chi tiết sản phẩm để đánh giá.', 'Đánh giá', 3),
            ('Tôi có thể đặt hàng qua điện thoại không?', 'Có, bạn có thể gọi hotline 0123-456-789 để đặt hàng qua điện thoại.', 'Đặt hàng', 2),
        ]

        for question, answer, category, priority in faqs_data:
            FAQ.objects.get_or_create(
                question=question,
                defaults={
                    'answer': answer,
                    'category': category,
                    'priority': priority,
                    'is_active': True,
                }
            )

        self.stdout.write(f'   Đã tạo {FAQ.objects.count()} FAQs')

    def _seed_orders(self):
        """Seed 20 sample orders."""
        self.stdout.write('🛒 Đang seed Orders...')

        customers = list(Account.objects.filter(role='Customer'))
        products = list(Product.objects.all())
        statuses = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Cancelled']

        for i in range(20):
            customer = random.choice(customers)
            product = random.choice(products)
            status = random.choice(statuses)
            
            # Generate order code
            order_code = f'ORD{timezone.now().strftime("%Y%m%d")}{i+1:04d}'
            
            # Calculate total
            unit_price = product.price
            quantity = 1
            total_amount = unit_price * quantity

            order, created = Order.objects.get_or_create(
                order_code=order_code,
                defaults={
                    'account': customer,
                    'total_amount': total_amount,
                    'status': status,
                    'customer_name': customer.full_name,
                    'customer_phone': customer.phone,
                    'customer_address': customer.address,
                    'notes': 'Giao giờ hành chính' if i % 3 == 0 else '',
                }
            )

            if created:
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=total_amount,
                )

        self.stdout.write(f'   Đã tạo {Order.objects.count()} orders với {OrderItem.objects.count()} order items')
