"""
Service lay hinh anh san pham tu cac nguon free online.
Uu tien: Static images cua san pham -> Picsum Photos fallback.
Neu co anh local trong static/images/products thi se su dung truoc.
"""
import re
import random
import hashlib
from typing import List, Dict, Optional
from urllib.parse import quote


# =====================
# PICSUM - Pure free, no API key needed
# =====================

def get_picsum_image(product_id: int, width: int = 800, height: int = 800, category: str = '') -> str:
    """
    Lay anh tu Picsum Photos (hoan toan mien phi).
    Dung seed theo product_id de dam bao cung san pham -> cung anh moi lan seed.
    """
    seed = product_id * 17 + 31
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"


# =====================
# CATEGORY-BASED IMAGES
# Su dung Picsum voi category keywords de lay anh lien quan
# =====================

CATEGORY_IMAGES = {
    'iphone': [
        'https://picsum.photos/seed/iphone15/800/800',
        'https://picsum.photos/seed/applephone/800/800',
    ],
    'samsung': [
        'https://picsum.photos/seed/galaxyphone/800/800',
        'https://picsum.photos/seed/samsungmobile/800/800',
    ],
    'macbook': [
        'https://picsum.photos/seed/macbookpro/800/800',
        'https://picsum.photos/seed/aplelaptop/800/800',
    ],
    'laptop': [
        'https://picsum.photos/seed/laptop/800/800',
        'https://picsum.photos/seed/notebook/800/800',
    ],
    'ipad': [
        'https://picsum.photos/seed/ipad/800/800',
        'https://picsum.photos/seed/appletablet/800/800',
    ],
    'tablet': [
        'https://picsum.photos/seed/tablet/800/800',
        'https://picsum.photos/seed/androidtablet/800/800',
    ],
    'airpods': [
        'https://picsum.photos/seed/airpods/800/800',
        'https://picsum.photos/seed/wirelessbuds/800/800',
    ],
    'headphones': [
        'https://picsum.photos/seed/headphones/800/800',
        'https://picsum.photos/seed/headset/800/800',
    ],
    'applewatch': [
        'https://picsum.photos/seed/applewatch/800/800',
        'https://picsum.photos/seed/smartwatch/800/800',
    ],
    'smartwatch': [
        'https://picsum.photos/seed/smartwatch/800/800',
        'https://picsum.photos/seed/wearable/800/800',
    ],
    'keyboard': [
        'https://picsum.photos/seed/keyboard/800/800',
        'https://picsum.photos/seed/mechanicalkb/800/800',
    ],
    'mouse': [
        'https://picsum.photos/seed/computermouse/800/800',
        'https://picsum.photos/seed/mouse/800/800',
    ],
    'speaker': [
        'https://picsum.photos/seed/speaker/800/800',
        'https://picsum.photos/seed/bluetoothspeaker/800/800',
    ],
    'camera': [
        'https://picsum.photos/seed/camera/800/800',
        'https://picsum.photos/seed/dslr/800/800',
    ],
    'gaming': [
        'https://picsum.photos/seed/gaming/800/800',
        'https://picsum.photos/seed/gamer/800/800',
    ],
    'charger': [
        'https://picsum.photos/seed/charger/800/800',
        'https://picsum.photos/seed/usbcharger/800/800',
    ],
    'cable': [
        'https://picsum.photos/seed/usbcable/800/800',
        'https://picsum.photos/seed/chargingcable/800/800',
    ],
    'ssd': [
        'https://picsum.photos/seed/ssd/800/800',
        'https://picsum.photos/seed/storagedrive/800/800',
    ],
    'monitor': [
        'https://picsum.photos/seed/monitor/800/800',
        'https://picsum.photos/seed/displayscreen/800/800',
    ],
    'router': [
        'https://picsum.photos/seed/wifirouter/800/800',
        'https://picsum.photos/seed/internetrouter/800/800',
    ],
    'default': [
        'https://picsum.photos/seed/techproduct/800/800',
        'https://picsum.photos/seed/electronic/800/800',
        'https://picsum.photos/seed/gadget/800/800',
    ],
}

# =====================
# LOCAL IMAGES - Uu tien cao nhat, chi dung khi co san pham tuong ung
# Chi su dung file thuc te co trong static/images/products/
LOCAL_IMAGES = {
    # iPhone
    'iphone 15 pro max': '/static/images/products/iphone-15-pro-max.jpg',
    'iphone 15 pro': '/static/images/products/iphone-15-pro-max.jpg',
    'iphone 15': '/static/images/products/iphone-15-pro-max.jpg',
    'iphone 14': '/static/images/products/iphone-14.jpg',
    'iphone 13': '/static/images/products/iphone-15-pro-max.jpg',

    # Samsung Galaxy
    'galaxy s24 ultra': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy s24+': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy s24': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy a55': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy a35': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy z flip': '/static/images/products/galaxy-s24-ultra.jpg',
    'galaxy tab s9': '/static/images/products/samsung-tab-s9.jpg',
    'galaxy tab s9 fe': '/static/images/products/samsung-tab-s9.jpg',
    'galaxy buds': '/static/images/products/airpods-pro.jpg',
    'galaxy watch': '/static/images/products/apple-watch-ultra.jpg',

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

    # Laptop khac - su dung anh gan giong
    'asus rog': '/static/images/products/dell-xps15.jpg',
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
    'xiaomi watch': '/static/images/products/apple-watch-ultra.jpg',
    'xiaomi pad': '/static/images/products/samsung-tab-s9.jpg',
    'xiaomi': '/static/images/products/xiaomi-14-pro.jpg',

    # OPPO
    'oppo reno': '/static/images/products/xiaomi-14-pro.jpg',
    'oppo pad': '/static/images/products/samsung-tab-s9.jpg',
    'oppo': '/static/images/products/xiaomi-14-pro.jpg',

    # Realme
    'realme c': '/static/images/products/xiaomi-14-pro.jpg',
    'realme pad': '/static/images/products/samsung-tab-s9.jpg',
    'realme': '/static/images/products/xiaomi-14-pro.jpg',

    # Nokia
    'nokia': '/static/images/products/galaxy-s24-ultra.jpg',

    # Vivo
    'vivo': '/static/images/products/dell-xps15.jpg',

    # AirPods
    'airpods': '/static/images/products/airpods-pro.jpg',

    # Sony
    'sony wh-1000xm': '/static/images/products/sony-headphones.jpg',
    'sony': '/static/images/products/sony-headphones.jpg',

    # JBL
    'jbl tune': '/static/images/products/sony-headphones.jpg',
    'jbl flip': '/static/images/products/sony-headphones.jpg',
    'jbl': '/static/images/products/sony-headphones.jpg',

    # Apple Watch
    'apple watch': '/static/images/products/apple-watch-ultra.jpg',

    # Keyboard/Mouse
    'mx master': '/static/images/products/airpods-pro.jpg',
    'logitech g pro': '/static/images/products/airpods-pro.jpg',
    'logitech g502': '/static/images/products/airpods-pro.jpg',
    'logitech': '/static/images/products/airpods-pro.jpg',
    'keychron': '/static/images/products/airpods-pro.jpg',
    'corsair k70': '/static/images/products/airpods-pro.jpg',
    'corsair': '/static/images/products/airpods-pro.jpg',

    # Accessories
    'anker 735': '/static/images/products/airpods-pro.jpg',
    'anker powercore': '/static/images/products/airpods-pro.jpg',
    'anker': '/static/images/products/airpods-pro.jpg',
    'hyperdrive': '/static/images/products/airpods-pro.jpg',
    'targus': '/static/images/products/airpods-pro.jpg',
    'samsung t7': '/static/images/products/airpods-pro.jpg',
}


def get_product_image(product_name: str, product_id: int, category: str = '') -> str:
    """
    Lay hinh anh phu hop cho san pham dua tren ten va danh muc.
    Uu tien: local images -> category images -> keyword matching -> Picsum fallback.
    """
    name_lower = product_name.lower()
    category_lower = category.lower() if category else ''

    # Tim local image truoc - uu tien cao nhat
    for keyword, url in LOCAL_IMAGES.items():
        if keyword in name_lower:
            return url

    # Tim category trong ten san pham
    for cat_key, urls in CATEGORY_IMAGES.items():
        if cat_key in name_lower or cat_key in category_lower:
            idx = (product_id - 1) % len(urls)
            return urls[idx]

    # Keyword matching
    keywords = {
        'iphone': CATEGORY_IMAGES['iphone'],
        'ipad': CATEGORY_IMAGES['ipad'],
        'macbook': CATEGORY_IMAGES['macbook'],
        'airpod': CATEGORY_IMAGES['airpods'],
        'watch': CATEGORY_IMAGES['smartwatch'],
        'galaxy': CATEGORY_IMAGES['samsung'],
        'buds': CATEGORY_IMAGES['airpods'],
        'buds2': CATEGORY_IMAGES['airpods'],
        'loa': CATEGORY_IMAGES['speaker'],
        'camera': CATEGORY_IMAGES['camera'],
        'may anh': CATEGORY_IMAGES['camera'],
        'loa bluetooth': CATEGORY_IMAGES['speaker'],
        'ban phim': CATEGORY_IMAGES['keyboard'],
        'chuot': CATEGORY_IMAGES['mouse'],
        'man hinh': CATEGORY_IMAGES['monitor'],
        'monitor': CATEGORY_IMAGES['monitor'],
        'laptop': CATEGORY_IMAGES['laptop'],
        'tablet': CATEGORY_IMAGES['tablet'],
        'sac': CATEGORY_IMAGES['charger'],
        'cap': CATEGORY_IMAGES['cable'],
        'ssd': CATEGORY_IMAGES['ssd'],
        'router': CATEGORY_IMAGES['router'],
        'gaming': CATEGORY_IMAGES['gaming'],
        'ghe': CATEGORY_IMAGES['gaming'],
        'tai nghe': CATEGORY_IMAGES['headphones'],
    }

    for keyword, urls in keywords.items():
        if keyword in name_lower:
            idx = (product_id - 1) % len(urls)
            return urls[idx]

    # Default
    defaults = CATEGORY_IMAGES['default']
    idx = (product_id - 1) % len(defaults)
    return defaults[idx]


def get_product_gallery(product_name: str, product_id: int, count: int = 3) -> List[str]:
    """
    Lay nhieu hinh anh cho gallery cua san pham.
    Tra ve list cac URL anh.
    """
    primary = get_product_image(product_name, product_id)
    images = [primary]

    # Lay them anh phu voi seed khac nhau
    for i in range(1, count):
        secondary_seed = product_id * 31 + i * 17
        images.append(f"https://picsum.photos/seed/{secondary_seed}/800/800")

    return images


def get_variant_color_image(product_name: str, product_id: int, variant_id: int, color: str = '') -> str:
    """
    Lay hinh anh cho bien the theo mau sac.
    """
    base_seed = product_id * 23 + variant_id * 7
    if color:
        color_seed = base_seed + hash(color.lower()) % 100
    else:
        color_seed = base_seed
    return f"https://picsum.photos/seed/{color_seed}/800/800"
