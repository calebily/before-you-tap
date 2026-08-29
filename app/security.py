from urllib.parse import urlsplit

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

CONTENT_SECURITY_POLICY = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self' blob: data:",
        "media-src 'self' blob:",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "frame-ancestors 'none'",
        "form-action 'self'",
    ]
)

SECURITY_HEADERS = {
    "Content-Security-Policy": CONTENT_SECURITY_POLICY,
    "Permissions-Policy": "camera=(self), microphone=(), geolocation=(), payment=(), usb=()",
    "Referrer-Policy": "no-referrer",
    "Strict-Transport-Security": "max-age=31536000",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-Permitted-Cross-Domain-Policies": "none",
}

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
MULTIPART_OVERHEAD_BYTES = 1024 * 1024
FOLLOW_UP_BODY_LIMIT_BYTES = 64 * 1024


def is_cross_origin_api_request(request: Request) -> bool:
    if request.method not in MUTATING_METHODS or not request.url.path.startswith("/api/"):
        return False

    origin = request.headers.get("origin")
    if not origin:
        return False

    origin_url = urlsplit(origin)
    request_host = request.headers.get("host", "").lower()
    return not origin_url.netloc or origin_url.netloc.lower() != request_host


def is_oversized_api_request(request: Request, *, max_upload_bytes: int) -> bool:
    limits = {
        "/api/uploads/validate": max_upload_bytes + MULTIPART_OVERHEAD_BYTES,
        "/api/analyse/images": max_upload_bytes + MULTIPART_OVERHEAD_BYTES,
        "/api/analyse/audio": max_upload_bytes + MULTIPART_OVERHEAD_BYTES,
        "/api/follow-up": FOLLOW_UP_BODY_LIMIT_BYTES,
    }
    limit = limits.get(request.url.path)
    if limit is None or request.method not in MUTATING_METHODS:
        return False

    raw_content_length = request.headers.get("content-length")
    if not raw_content_length:
        return False
    try:
        return int(raw_content_length) > limit
    except ValueError:
        return True


def secure_response(response: Response, *, api_response: bool) -> Response:
    for name, value in SECURITY_HEADERS.items():
        response.headers[name] = value
    if api_response:
        response.headers["Cache-Control"] = "no-store"
    return response


def cross_origin_error() -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Cross-origin API requests are not allowed."},
    )
    return secure_response(response, api_response=True)


def request_too_large_error() -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
        content={"detail": "The request is too large."},
    )
    return secure_response(response, api_response=True)
