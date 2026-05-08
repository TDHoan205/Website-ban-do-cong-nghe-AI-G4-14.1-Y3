"""
Test script cho TechStore website.
"""
import requests
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

def test_page(url, expected_status=200, description=""):
    """Test một trang."""
    try:
        resp = session.get(url, timeout=10)
        status = "OK" if resp.status_code == expected_status else f"FAIL ({resp.status_code})"
        print(f"  [{status}] {description or url}")
        if resp.status_code != expected_status:
            print(f"       Response: {resp.status_code}")
            if resp.status_code == 500:
                print(f"       Error preview: {resp.text[:200]}")
        return resp.status_code == expected_status
    except Exception as e:
        print(f"  [ERROR] {description or url}: {e}")
        return False

def get_csrf_token(url):
    """Lấy CSRF token từ trang."""
    try:
        resp = session.get(url, timeout=10)
        for line in resp.text.split('\n'):
            if 'csrfmiddlewaretoken' in line:
                import re
                match = re.search(r'value="([^"]+)"', line)
                if match:
                    return match.group(1)
    except:
        pass
    return ""

def test_api(url, data, description="", requires_csrf=True):
    """Test API endpoint."""
    try:
        post_data = data.copy()
        if requires_csrf:
            csrf = get_csrf_token(BASE_URL)
            post_data['csrfmiddlewaretoken'] = csrf

        resp = session.post(url, data=post_data, timeout=10)
        try:
            json_resp = resp.json()
            print(f"  [OK] {description}: {json_resp.get('success', json_resp)}")
            return True
        except:
            print(f"  [WARN] {description}: Non-JSON response ({resp.status_code})")
            return resp.status_code == 200
    except Exception as e:
        print(f"  [ERROR] {description}: {e}")
        return False

print("=" * 60)
print("TEST WEBSITE: TechStore")
print("=" * 60)

results = []

# Test public pages
print("\n[1] Test trang công khai:")
results.append(test_page(BASE_URL + "/", description="Trang chủ"))
results.append(test_page(BASE_URL + "/shop/products/", description="Danh sách sản phẩm"))
results.append(test_page(BASE_URL + "/accounts/login/", description="Trang đăng nhập"))

# Login
print("\n[2] Đăng nhập:")
csrf = get_csrf_token(BASE_URL + "/accounts/login/")
login_data = {
    'csrfmiddlewaretoken': csrf,
    'username': 'admin',
    'password': 'admin123',
    'next': '/dashboard/'
}
try:
    resp = session.post(BASE_URL + "/accounts/login/", data=login_data, timeout=10)
    if resp.status_code in [200, 302]:
        print(f"  [OK] Đăng nhập admin thành công")
        results.append(True)
    else:
        print(f"  [FAIL] Đăng nhập: {resp.status_code}")
        results.append(False)
except Exception as e:
    print(f"  [ERROR] Đăng nhập: {e}")
    results.append(False)

# Test authenticated pages
print("\n[3] Test trang sau khi đăng nhập:")
results.append(test_page(BASE_URL + "/dashboard/", description="Dashboard"))
results.append(test_page(BASE_URL + "/shop/cart/", description="Giỏ hàng"))
results.append(test_page(BASE_URL + "/shop/checkout/", description="Thanh toán"))
results.append(test_page(BASE_URL + "/faqs/support/", description="Hỗ trợ"))
results.append(test_page(BASE_URL + "/shop/?new_page=1", description="Sản phẩm mới (phân trang)"))
results.append(test_page(BASE_URL + "/shop/?hot_page=1", description="Sản phẩm hot (phân trang)"))

# Test API
print("\n[4] Test API:")
csrf = get_csrf_token(BASE_URL + "/shop/products/")
test_api(BASE_URL + "/shop/cart/add/", {
    'product_id': 1,
    'quantity': 1
}, "Thêm vào giỏ hàng", requires_csrf=True)

test_api(BASE_URL + "/shop/cart/count/", {}, "Lấy số lượng giỏ hàng", requires_csrf=False)

# Test search
test_api(BASE_URL + "/shop/search/suggestions/?q=iphone", {}, "Tìm kiếm gợi ý", requires_csrf=False)

# Test admin pages
print("\n[5] Test trang Admin:")
results.append(test_page(BASE_URL + "/admin/products/", description="QL Sản phẩm"))
results.append(test_page(BASE_URL + "/admin/orders/", description="QL Đơn hàng"))
results.append(test_page(BASE_URL + "/admin/categories/", description="QL Danh mục"))
results.append(test_page(BASE_URL + "/admin/cart/", description="QL Giỏ hàng"))

# Summary
print("\n" + "=" * 60)
passed = sum(results)
total = len(results)
print(f"KẾT QUẢ: {passed}/{total} tests passed")
if passed == total:
    print("✓ Tất cả test đều OK!")
else:
    print(f"✗ Có {total - passed} test thất bại")
print("=" * 60)
