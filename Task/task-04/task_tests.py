import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
APP_DIR = os.path.join(BASE_DIR, "app", "api")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def test_fetchtextcloud_has_pagination():
    path = os.path.join(APP_DIR, "fetchtextcloud", "route.js")
    assert os.path.exists(path), "fetchtextcloud route.js must exist"
    content = read(path)
    # Basic signals of pagination logic
    assert "page" in content
    assert "limit" in content
    assert ".skip(" in content
    assert ".limit(" in content
    assert "pagination" in content
    assert "total" in content

def test_fetchemail_is_lightweight_listing():
    path = os.path.join(APP_DIR, "fetchemail", "route.js")
    assert os.path.exists(path), "fetchemail route.js must exist"
    content = read(path)
    # Should not build base64 payload here anymore
    assert "base64" not in content
    assert ".toString(\"base64\")" not in content
    # Should support pagination + total
    assert "pagination" in content
    assert "total" in content

def test_fetchemail_detail_route_exists_and_uses_base64():
    path = os.path.join(APP_DIR, "fetchemailDetail", "route.js")
    assert os.path.exists(path), "fetchemailDetail route.js must exist"
    content = read(path)
    assert "base64" in content or ".toString(\"base64\")" in content
    assert "Image id is required" in content
    assert "Image not found" in content

def test_fetchimg_uses_lean_or_projection():
    path = os.path.join(APP_DIR, "fetchimg", "route.js")
    assert os.path.exists(path), "fetchimg route.js must exist"
    content = read(path)
    # Must be optimized using lean or projection
    assert ".lean(" in content or ".select(" in content

def test_fetchimg_does_not_build_base64():
    path = os.path.join(APP_DIR, "fetchimg", "route.js")
    content = read(path)
    assert "base64" not in content
    assert ".toString(\"base64\")" not in content

def test_error_messages_standardized_for_fetchemailDetail():
    path = os.path.join(APP_DIR, "fetchemailDetail", "route.js")
    content = read(path)
    assert "Image id is required" in content
    assert "Image not found" in content
    assert "Internal server error" in content