import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
API_DIR = os.path.join(BASE_DIR, "app", "api")
UTILS_DIR = os.path.join(BASE_DIR, "utils")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def test_rate_limiter_exists():
    path = os.path.join(UTILS_DIR, "rateLimiter.js")
    assert os.path.exists(path), "utils/rateLimiter.js must exist"
    content = read(path)
    assert "export function rateLimit" in content

def test_login_uses_rate_limit():
    path = os.path.join(API_DIR, "Login", "route.js")
    content = read(path)
    assert "rateLimit" in content
    assert "login:" in content

def test_loginnew_uses_rate_limit():
    path = os.path.join(API_DIR, "LoginNew", "route.js")
    content = read(path)
    assert "rateLimit" in content
    assert "signup:" in content

def test_varificationMail_uses_rate_limit_with_email_key():
    path = os.path.join(API_DIR, "varificationMail", "route.js")
    content = read(path)
    assert "rateLimit" in content
    assert "otp:" in content
    assert ".toLowerCase()" in content

def test_userforgot_uses_rate_limit_with_email_key():
    path = os.path.join(API_DIR, "userforgot", "route.js")
    content = read(path)
    assert "rateLimit" in content
    assert "forgot:" in content
    assert ".toLowerCase()" in content

def test_standard_429_message_used_everywhere():
    files = [
        os.path.join(API_DIR, "Login", "route.js"),
        os.path.join(API_DIR, "LoginNew", "route.js"),
        os.path.join(API_DIR, "varificationMail", "route.js"),
        os.path.join(API_DIR, "userforgot", "route.js"),
    ]
    for p in files:
        c = read(p)
        assert "Too many requests, try again later" in c