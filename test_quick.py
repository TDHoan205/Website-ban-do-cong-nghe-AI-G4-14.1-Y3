import requests
import re

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# Get login page and csrf
resp = session.get('http://127.0.0.1:8000/accounts/login/')
print('Login page:', resp.status_code)
match = re.search(r'value="([^"]+)"', resp.text)
csrf = match.group(1) if match else ''

# Login
resp = session.post('http://127.0.0.1:8000/accounts/login/', data={
    'csrfmiddlewaretoken': csrf,
    'username': 'admin',
    'password': 'admin123',
}, allow_redirects=True)
print('Login:', resp.status_code, resp.url)

# Test checkout (requires login)
resp = session.get('http://127.0.0.1:8000/shop/checkout/')
print('Checkout:', resp.status_code)
if resp.status_code == 500:
    content = resp.text
    for line in content.split('\n'):
        if 'Exception' in line or 'Error' in line or 'TemplateSyntaxError' in line:
            print('  ERROR:', line.strip())

# Test dashboard
resp = session.get('http://127.0.0.1:8000/')
print('Dashboard (root):', resp.status_code)

# Test cart
resp = session.get('http://127.0.0.1:8000/shop/cart/')
print('Cart:', resp.status_code)

# Test admin pages
resp = session.get('http://127.0.0.1:8000/admin/products/')
print('Admin Products:', resp.status_code)
resp = session.get('http://127.0.0.1:8000/products/')
print('Products app:', resp.status_code)
resp = session.get('http://127.0.0.1:8000/orders/')
print('Orders app:', resp.status_code)
resp = session.get('http://127.0.0.1:8000/cart/admin/')
print('Cart admin:', resp.status_code)
