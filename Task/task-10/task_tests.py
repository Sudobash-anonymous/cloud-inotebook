import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
API = os.path.join(BASE, "app", "api")
UTIL = os.path.join(BASE, "utils")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def test_v1_directory_exists():
    v1 = os.path.join(API, "v1")
    assert os.path.exists(v1)

def test_version_guard_exists():
    path = os.path.join(UTIL, "apiVersionGuard.js")
    assert os.path.exists(path)

def test_old_api_has_deprecation_header():
    login = os.path.join(API, "Login", "route.js")
    c = read(login)
    assert "X-API-DEPRECATED" in c

def test_v1_api_sets_version_header():
    login = os.path.join(API, "v1", "Login", "route.js")
    c = read(login)
    assert "X-API-Version" in c

def test_unknown_versions_blocked():
    guard = read(os.path.join(UTIL, "apiVersionGuard.js"))
    assert "410" in guard
    assert "API version no longer supported" in guard

def test_old_api_proxies_to_v1():
    login = read(os.path.join(API, "Login", "route.js"))
    assert "/api/v1/Login" in login