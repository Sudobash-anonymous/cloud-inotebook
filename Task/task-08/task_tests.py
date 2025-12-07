import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
MODEL = os.path.join(BASE, "model")
API = os.path.join(BASE, "app", "api")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def test_text_model_has_audit_fields():
    c = read(os.path.join(MODEL, "text", "page.js"))
    assert "createdAt" in c
    assert "updatedAt" in c
    assert "deletedAt" in c

def test_image_model_has_audit_fields():
    c = read(os.path.join(MODEL, "image", "page.js"))
    assert "createdAt" in c
    assert "updatedAt" in c
    assert "deletedAt" in c

def test_deleteimage_uses_soft_delete():
    c = read(os.path.join(API, "deleteimage", "route.js"))
    assert "deletedAt" in c
    assert "findByIdAndDelete" not in c

def test_deletetextcloud_uses_soft_delete():
    c = read(os.path.join(API, "deletetextcloud", "route.js"))
    assert "deletedAt" in c
    assert "deleteOne" not in c

def test_fetchtextcloud_ignores_deleted():
    c = read(os.path.join(API, "fetchtextcloud", "route.js"))
    assert "deletedAt: null" in c

def test_fetchimg_ignores_deleted():
    c = read(os.path.join(API, "fetchimg", "route.js"))
    assert "deletedAt: null" in c