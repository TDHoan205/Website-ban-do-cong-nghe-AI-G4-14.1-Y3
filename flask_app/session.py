"""
Session management for FastAPI.
- Authenticated users: stored in DB (Accounts table)
- Guests: tracked by UUID cookie, mapped to a "guest" account in session

Usage:
  1. On every request, call `get_or_create_session(request, db)` to get (account_id, is_authenticated).
  2. Use account_id for all cart/order operations.
  3. For guests, use `get_guest_account_id(session_id)` which returns 0.
"""
import secrets
import time
from typing import Optional, Dict

from fastapi import Request, Response
from sqlalchemy.orm import Session

from .models import Account

# ── In-memory session store ────────────────────────────────────────────────
# Maps session_token → {account_id: int, created_at: float}
_auth_sessions: Dict[str, dict] = {}

# Maps session_token → guest_uuid (for linking guest carts to accounts on login)
_token_to_uuid: Dict[str, str] = {}

# Guest account ID sentinel (no DB row)
GUEST_ACCOUNT_ID = 0


def generate_session_token() -> str:
    return secrets.token_hex(24)


def create_session(response: Response, account_id: int, guest_uuid: Optional[str] = None) -> str:
    """Create a new session, set cookie, return token."""
    token = generate_session_token()
    _auth_sessions[token] = {
        "account_id": account_id,
        "created_at": time.time(),
        "guest_uuid": guest_uuid,
    }
    if guest_uuid:
        _token_to_uuid[token] = guest_uuid
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400 * 30,  # 30 days
    )
    return token


def get_session(token: str) -> Optional[dict]:
    """Return session data for a token, or None if expired/invalid."""
    data = _auth_sessions.get(token)
    if data and (time.time() - data["created_at"]) < 86400 * 30:
        return data
    # Expired — clean up
    if token in _auth_sessions:
        del _auth_sessions[token]
    if token in _token_to_uuid:
        del _token_to_uuid[token]
    return None


def delete_session(response: Response, token: Optional[str]):
    """Clear session from memory and delete cookie."""
    if token:
        _auth_sessions.pop(token, None)
        _token_to_uuid.pop(token, None)
    response.delete_cookie(key="session_token")


def get_session_token(request: Request) -> Optional[str]:
    return request.cookies.get("session_token")


# ── Authenticated session helpers ─────────────────────────────────────────

def get_account_id(request: Request, response: Response, db: Session) -> int:
    """
    Main entry point: returns the current account_id.
    Creates a guest session if none exists.
    """
    token = get_session_token(request)
    if token:
        session = get_session(token)
        if session:
            return session["account_id"]

    # No valid session — create a guest session
    token = create_session(response, account_id=GUEST_ACCOUNT_ID)
    return GUEST_ACCOUNT_ID


def login(response: Response, account: Account, guest_uuid: Optional[str] = None) -> str:
    """Log in a user, create a session."""
    return create_session(response, account.account_id, guest_uuid)


def logout(response: Response, request: Request):
    """Log out current user."""
    token = get_session_token(request)
    delete_session(response, token)


def is_authenticated(request: Request) -> bool:
    """Check if current session belongs to a logged-in user."""
    token = get_session_token(request)
    if not token:
        return False
    session = get_session(token)
    return session is not None and session["account_id"] != GUEST_ACCOUNT_ID
