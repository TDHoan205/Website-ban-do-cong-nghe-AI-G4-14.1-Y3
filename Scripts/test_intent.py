"""Test intent detection sau cac fix"""
import sys, re
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()

HAS_PRICE_RE = r'\d+\s*(?:triệu|trieu|tr\b|củ|cu\b|lít|lit\b|nghìn|ngàn|k\b)'
greet_kws = ['xin chào', 'hello', 'helo', 'hela', 'hola', 'hi ', 'hi!', 'chào', 'hey', 'alo']
price_strict = ['giá', 'bao nhiêu', 'rẻ', 'đắt', 'tầm giá', 'khoảng giá', 'budget', 'tầm tiền', 'muốn mua', 'cần mua']

tests = [
    ('helo',                       'greeting'),
    ('hello',                      'greeting'),
    ('alo',                        'greeting'),
    ('hi',                         'greeting'),
    ('tôi muốn mua máy 20 tr',     'price_query'),
    ('mua điện thoại 10-20 triệu', 'price_query'),
    ('tầm 15 củ',                  'price_query'),
    ('dưới 30 tr',                 'price_query'),
    ('laptop khoảng 20k',          'price_query'),
    ('giúp tôi tìm laptop',        'product_query'),
]

print("=== Intent detection tests ===")
ok = err = 0
for msg, expected in tests:
    m = msg.lower()
    if re.search(HAS_PRICE_RE, m) or any(kw in m for kw in price_strict):
        intent = 'price_query'
    elif any(kw in m for kw in greet_kws) or m.strip() in ['hi','helo','hello','alo','hey']:
        intent = 'greeting'
    else:
        intent = 'product_query'

    status = 'OK  ' if intent == expected else 'FAIL'
    if intent == expected:
        ok += 1
    else:
        err += 1
    print(f"  {status} '{msg}' => {intent} (expected: {expected})")

print(f"\nKet qua: {ok} OK / {err} FAIL")
