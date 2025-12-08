import os
import glob
import requests
import pytest

BASE_URL = os.getenv("TASK_BASE_URL", "http://localhost:3000")


def api_post(path: str, headers=None, json=None):
    """Helper to POST to the API under test."""
    return requests.post(
        BASE_URL + path,
        headers=headers or {},
        json=json,
        timeout=10,
    )


def test_missing_authorization_returns_401():
    """
    Missing Authorization header on /api/useremail must return:
    HTTP 401 with { success: false, message: 'Unauthorized' }.
    """
    res = api_post("/api/useremail")
    assert res.status_code == 401
    data = res.json()
    assert data.get("success") is False
    assert data.get("message") == "Unauthorized"


def test_malformed_token_returns_invalid_token():
    """
    Malformed JWT in Authorization header must return:
    HTTP 401 with { success: false, message: 'Invalid token' }.
    """
    headers = {"Authorization": "Bearer this.is.not.a.jwt"}
    res = api_post("/api/useremail", headers=headers)
    assert res.status_code == 401
    data = res.json()
    assert data.get("success") is False
    assert data.get("message") == "Invalid token"


def test_expired_token_returns_token_expired():
    """
    Expired JWT must return:
    HTTP 401 with { success: false, message: 'Token expired' }.
    """
    expired_token = os.getenv("EXPIRED_TEST_JWT")
    if not expired_token:
        pytest.skip("EXPIRED_TEST_JWT not provided in environment")

    headers = {"Authorization": f"Bearer {expired_token}"}
    res = api_post("/api/useremail", headers=headers)
    assert res.status_code == 401
    data = res.json()
    assert data.get("success") is False
    assert data.get("message") == "Token expired"


def test_valid_token_allows_access_and_returns_email():
    """
    Valid JWT must allow access to /api/useremail and return success:true
    with an 'email' field in the JSON body.
    """
    valid_token = os.getenv("VALID_TEST_JWT")
    if not valid_token:
        pytest.skip("VALID_TEST_JWT not provided in environment")

    headers = {"Authorization": f"Bearer {valid_token}"}
    res = api_post("/api/useremail", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    assert isinstance(data.get("email"), str)


def test_useremail_ignores_body_email_and_uses_token_identity():
    """
    /api/useremail must ignore client-supplied 'email' in body and derive
    identity solely from the token payload.

    We send an obviously fake email in the body and assert that the response
    'email' is not equal to that fake value.
    """
    valid_token = os.getenv("VALID_TEST_JWT")
    if not valid_token:
        pytest.skip("VALID_TEST_JWT not provided in environment")

    fake_email = "attacker@example.com"
    headers = {"Authorization": f"Bearer {valid_token}"}
    res = api_post("/api/useremail", headers=headers, json={"email": fake_email})
    assert res.status_code in (200, 201)
    data = res.json()
    assert data.get("success") is True
    assert data.get("email") != fake_email


def test_protected_routes_reject_query_param_token():
    """
    Protected routes must NOT accept tokens passed via query params.
    They must treat such requests as unauthorized.
    """
    protected_routes = ["/api/useremail", "/api/textcloud"]

    for route in protected_routes:
        res = api_post(f"{route}?token=abc.def.ghi")
        assert res.status_code == 401
        data = res.json()
        assert data.get("success") is False
        assert isinstance(data.get("message"), str)


def test_protected_routes_use_standard_error_format():
    """
    Protected routes must use the standard auth error format:
    HTTP 401 with { success:false, message:string } when unauthorized.
    """
    protected_routes = ["/api/useremail", "/api/textcloud"]

    for route in protected_routes:
        res = api_post(route)
        assert res.status_code == 401
        data = res.json()
        assert data.get("success") is False
        assert isinstance(data.get("message"), str)


def test_login_routes_use_testconnect():
    """
    /api/Login and /api/LoginNew must import and use testConnect for DB access.
    This is checked structurally by inspecting the route files.
    """
    login_files = [
        "app/api/Login/route.js",
        "app/api/LoginNew/route.js",
    ]

    for path in login_files:
        assert os.path.exists(path), f"Missing route file: {path}"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "testConnect" in content, f"testConnect not used in {path}"


def test_useremail_route_uses_testconnect_and_auth_guard():
    """
    /api/useremail must use testConnect and an Authorization-based auth guard.

    This verifies:
    - The route imports/uses testConnect
    - The string 'Authorization' appears in the implementation
    (indicating a header-based auth guard).
    """
    path = "app/api/useremail/route.js"
    assert os.path.exists(path), "Missing /api/useremail route.js file"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "testConnect" in content, "testConnect not used in /api/useremail"
    assert "Authorization" in content, "Authorization header not referenced in /api/useremail"


def test_all_protected_routes_are_covered_by_auth():
    """
    Ensure that all protected routes that should be guarded by JWT
    are actually implemented (at minimum in the file system) so they
    can be wired to the auth guard.
    """
    protected_paths = [
        "app/api/useremail/route.js",
        "app/api/textcloud/route.js",
    ]

    for path in protected_paths:
        assert os.path.exists(path), f"Protected route file missing: {path}"