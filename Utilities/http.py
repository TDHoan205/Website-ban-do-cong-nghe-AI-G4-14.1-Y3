from urllib.parse import urlparse

from fastapi import Request


def is_ajax_request(request: Request) -> bool:
    return (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("accept", "")
    )


def safe_redirect_url(request: Request, fallback: str) -> str:
    referer = request.headers.get("referer")
    if not referer:
        return fallback

    parsed_referer = urlparse(referer)
    parsed_current = urlparse(str(request.url))
    if parsed_referer.netloc == parsed_current.netloc:
        path = parsed_referer.path or fallback
        return f"{path}?{parsed_referer.query}" if parsed_referer.query else path

    return fallback
