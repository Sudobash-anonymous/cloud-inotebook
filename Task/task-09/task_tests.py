import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
MODEL = os.path.join(BASE, "model")
API = os.path.join(BASE, "app", "api")
UTILS = os.path.join(BASE, "utils")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def test_audit_model_exists():
    path = os.path.join(MODEL, "AuditLog", "page.js")
    assert os.path.exists(path)
    c = read(path)
    assert "action" in c
    assert "userEmail" in c
    assert "ipAddress" in c
    assert "userAgent" in c
    assert "createdAt" in c

def test_audit_logger_exists():
    path = os.path.join(UTILS, "auditLogger.js")
    assert os.path.exists(path)
    c = read(path)
    assert "export async function logAudit" in c

def test_login_logs_audit():
    c = read(os.path.join(API, "Login", "route.js"))
    assert "logAudit" in c
    assert "LOGIN_SUCCESS" in c

def test_signup_logs_audit():
    c = read(os.path.join(API, "LoginNew", "route.js"))
    assert "logAudit" in c
    assert "SIGNUP" in c

def test_deleteimage_logs_audit():
    c = read(os.path.join(API, "deleteimage", "route.js"))
    assert "logAudit" in c
    assert "DELETE_IMAGE" in c

def test_auditlogs_api_exists():
    path = os.path.join(API, "auditlogs", "route.js")
    assert os.path.exists(path)