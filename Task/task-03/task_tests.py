import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
APP_DIR = os.path.join(BASE_DIR, "app")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def test_auth_helper_exists():
    path = os.path.join(BASE_DIR, "lib", "auth.js")
    assert os.path.exists(path), "lib/auth.js must exist"
    content = read(path)
    assert "export async function requireAuth" in content
    assert "export function verifyToken" in content

def test_auth_helper_uses_jwt_secret():
    path = os.path.join(BASE_DIR, "lib", "auth.js")
    content = read(path)
    assert "process.env.JWT_SECRET_" in content

def test_useremail_route_uses_requireAuth():
    path = os.path.join(APP_DIR, "api", "useremail", "route.js")
    content = read(path)
    assert "requireAuth" in content, "useremail route must use requireAuth"
    assert "verifyToken(" not in content, "low-level verifyToken should not be called directly here"

def test_textcloud_route_no_raw_email_from_body():
    path = os.path.join(APP_DIR, "api", "textcloud", "route.js")
    content = read(path)
    # Should not trust body.email
    assert "body.email" not in content
    assert "requireAuth" in content

def test_addimage_route_no_raw_email_from_formdata():
    path = os.path.join(APP_DIR, "api", "addimage", "route.js")
    content = read(path)
    assert "formData.get(\"email\")" not in content
    assert "requireAuth" in content

def test_auth_error_message_consistent():
    files = [
        os.path.join(APP_DIR, "api", "useremail", "route.js"),
        os.path.join(APP_DIR, "api", "textcloud", "route.js"),
        os.path.join(APP_DIR, "api", "addimage", "route.js"),
    ]
    for path in files:
        content = read(path)
        assert "Invalid or expired token" in content, f"{path} must use standard auth error message"

def test_no_raw_token_logging():
    path = os.path.join(BASE_DIR, "lib", "auth.js")
    content = read(path)
    # Should not log token
    forbidden_patterns = [
        "console.log(token)",
        "console.log(decoded)",
        "console.log(payload)"
    ]
    for p in forbidden_patterns:
        assert p not in content, f"auth.js must not log sensitive token/payload: {p}"