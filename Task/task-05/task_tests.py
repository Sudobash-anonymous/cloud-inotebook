import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
API_DIR = os.path.join(BASE_DIR, "app", "api")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def test_useremail_requires_bearer():
    path = os.path.join(API_DIR, "useremail", "route.js")
    c = read(path)
    assert "Authorization" in c
    assert "Bearer" in c

def test_useremail_uses_testConnect():
    path = os.path.join(API_DIR, "useremail", "route.js")
    c = read(path)
    assert "testConnect" in c

def test_login_uses_testConnect():
    path = os.path.join(API_DIR, "Login", "route.js")
    c = read(path)
    assert "testConnect" in c

def test_loginnew_uses_testConnect():
    path = os.path.join(API_DIR, "LoginNew", "route.js")
    c = read(path)
    assert "testConnect" in c

def test_token_error_message_standard():
    path = os.path.join(API_DIR, "useremail", "route.js")
    c = read(path)
    assert "Invalid or expired token" in c

def test_identity_not_from_frontend():
    path = os.path.join(API_DIR, "useremail", "route.js")
    c = read(path)
    assert "decoded.email" in c