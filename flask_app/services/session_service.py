"""
Session & cart service – in-memory storage for demo.
Sessions are keyed by a simple session cookie value.
Carts are stored per-session.
"""
from typing import List, Optional
from uuid import uuid4

from ..models.schemas import CartItem, Product


# ─── In-memory stores ───────────────────────────────────
_sessions: dict[str, dict] = {}
_carts: dict[str, List[CartItem]] = {}   # session_id → list of CartItem


# ─── Session helpers ────────────────────────────────────
def get_or_create_session(session_id: Optional[str]) -> tuple[str, dict]:
    """Return (session_id, session_data) – creating a new session if needed."""
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]
    new_id = str(uuid4())[:32]
    _sessions[new_id] = {"user_id": None, "username": None, "role": None}
    _carts[new_id] = []
    return new_id, _sessions[new_id]


def set_session_user(session_id: str, user_id: int, username: str, role: str):
    _sessions[session_id]["user_id"] = user_id
    _sessions[session_id]["username"] = username
    _sessions[session_id]["role"] = role


def get_session(session_id: str) -> dict:
    return _sessions.get(session_id, {})


def logout_session(session_id: str):
    if session_id in _sessions:
        _sessions[session_id] = {"user_id": None, "username": None, "role": None}


# ─── Cart helpers ────────────────────────────────────────
def get_cart(session_id: str) -> List[CartItem]:
    return _carts.get(session_id, [])


def get_cart_count(session_id: str) -> int:
    return sum(item.quantity for item in get_cart(session_id))


def add_to_cart(session_id: str, product_id: int,
                quantity: int = 1, variant_id: Optional[int] = None) -> bool:
    if session_id not in _carts:
        _carts[session_id] = []

    cart = _carts[session_id]
    for item in cart:
        if item.product_id == product_id and item.variant_id == variant_id:
            item.quantity += quantity
            return True

    from .mock_data import get_product_by_id, PRODUCT_MAP
    product = get_product_by_id(product_id)
    if not product:
        return False

    from ..models.schemas import ProductVariant
    variant = None
    if variant_id:
        for v in product.variants:
            if v.variant_id == variant_id:
                variant = v
                break

    cart.append(CartItem(
        product_id=product_id,
        variant_id=variant_id,
        product=product,
        variant=variant,
        quantity=quantity,
    ))
    return True


def update_cart_item(session_id: str, product_id: int,
                     quantity: int, variant_id: Optional[int] = None) -> Optional[int]:
    """Update quantity. Returns corrected quantity or None if not found."""
    cart = get_cart(session_id)
    for item in cart:
        if item.product_id == product_id and item.variant_id == variant_id:
            if quantity <= 0:
                cart.remove(item)
                return None
            item.quantity = quantity
            return quantity
    return None


def remove_from_cart(session_id: str, product_id: int,
                     variant_id: Optional[int] = None) -> bool:
    cart = get_cart(session_id)
    for i, item in enumerate(cart):
        if item.product_id == product_id and item.variant_id == variant_id:
            cart.pop(i)
            return True
    return False


def clear_cart(session_id: str):
    if session_id in _carts:
        _carts[session_id] = []


def get_cart_total(session_id: str) -> float:
    total = 0.0
    for item in get_cart(session_id):
        price = item.variant.price if item.variant else (item.product.price if item.product else 0)
        total += price * item.quantity
    return total
