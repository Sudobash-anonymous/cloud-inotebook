import os
import time
import subprocess
import requests
import pytest

BASE_URL = "http://localhost:3000"


def start_server():
    """
    Starts the Next.js server in production mode if not already running.
    """
    subprocess.Popen("npm start", shell=True)
    time.sleep(6)


def api_post(path, headers=None, json=None):
    """
    Helper to send POST requests to the running API.
    """
    return requests.post(
        f"{BASE_URL}{path}",
        headers=headers or {},
        json=json or {}
    )


def test_missing_authorization_returns_401():
    """
    Missing Authorization header must return:
    { success:false, message:'Unauthorized' } with HTTP 401.
    """
    start_server()

    res = api_post("/api/useremail")

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Unauthorized"


def test_malformed_token_rejected():
    """
    Malformed JWT must return:
    { success:false, message:'Invalid token' } with HTTP 401.
    """
    headers = {"Authorization": "Bearer abc.def.xyz"}

    res = api_post("/api/useremail", headers=headers)

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Invalid token"


def test_expired_token_rejected_separately():
    """
    Expired JWT token must return:
    { success:false, message:'Token expired' } with HTTP 401.
    """
    expired_token = os.getenv("EXPIRED_TEST_JWT")

    if not expired_token:
        pytest.skip("EXPIRED_TEST_JWT not provided in environment")

    headers = {"Authorization": f"Bearer {expired_token}"}

    res = api_post("/api/useremail", headers=headers)

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Token expired"


def test_valid_token_allows_access():
    """
    Valid JWT token must allow access and return success:true.
    """
    valid_token = os.getenv("VALID_TEST_JWT")

    if not valid_token:
        pytest.skip("VALID_TEST_JWT not provided in environment")

    headers = {"Authorization": f"Bearer {valid_token}"}

    res = api_post("/api/useremail", headers=headers)

    assert res.status_code == 200
    data = res.json()

    assert data["success"] is True
    assert "email" in data


def test_protected_routes_use_standard_error_format():
    """
    All protected routes must return:
    { success:false, message:string } on auth failure.
    """
    protected_routes = [
        "/api/useremail",
        "/api/textcloud"
    ]

    for route in protected_routes:
        res = api_post(route)
        data = res.json()

        assert res.status_code == 401
        assert data.get("success") is False
        assert isinstance(data.get("message"), str)


def test_token_not_passed_as_query_param():
    """
    Tokens passed via query params MUST be rejected.
    """
    res = api_post("/api/useremail?token=abc")

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Unauthorized"


def test_token_in_request_body_is_ignored():
    """
    Tokens provided inside the request BODY must be ignored.
    Only Authorization header is allowed.
    """
    valid_token = os.getenv("VALID_TEST_JWT")

    if not valid_token:
        pytest.skip("VALID_TEST_JWT not provided in environment")

    res = api_post(
        "/api/useremail",
        json={"token": valid_token}
    )

    assert res.status_code == 401
    data = res.json()

    assert data.get("success") is False
    assert data.get("message") == "Unauthorized"


def test_auth_failure_has_minimal_response_shape():
    """
    Auth failures must return ONLY:
    { success:false, message:string }
    No extra fields are allowed.
    """
    res = api_post("/api/useremail")

    assert res.status_code == 401
    data = res.json()

    assert "success" in data
    assert "message" in data
    assert len(data.keys()) == 2