import requests
import subprocess
import time
import os

BASE_URL = "http://localhost:3000"


def start_server():
    """Ensure the Next.js server is running before tests execute."""
    subprocess.Popen("npm start", shell=True)
    time.sleep(5)


def test_missing_authorization_returns_401():
    """
    Missing Authorization header must return:
    { success:false, message:'Unauthorized' } with HTTP 401.
    """
    start_server()

    res = requests.post(f"{BASE_URL}/api/useremail")

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Unauthorized"


def test_malformed_token_rejected():
    """
    Malformed token must return:
    { success:false, message:'Invalid token' } with HTTP 401.
    """
    headers = {"Authorization": "Bearer abc.def.xyz"}

    res = requests.post(f"{BASE_URL}/api/useremail", headers=headers)

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

    headers = {"Authorization": f"Bearer {expired_token}"}

    res = requests.post(f"{BASE_URL}/api/useremail", headers=headers)

    assert res.status_code == 401
    data = res.json()

    assert data["success"] is False
    assert data["message"] == "Token expired"


def test_valid_token_allows_access():
    """
    Valid JWT token must allow access and return success:true.
    """
    valid_token = os.getenv("VALID_TEST_JWT")

    headers = {"Authorization": f"Bearer {valid_token}"}

    res = requests.post(f"{BASE_URL}/api/useremail", headers=headers)

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
        res = requests.post(f"{BASE_URL}{route}")

        data = res.json()

        assert res.status_code == 401
        assert isinstance(data.get("message"), str)
        assert data.get("success") is False


def test_token_not_passed_as_query_param():
    """
    Security check: tokens passed as query params must be rejected.
    """
    res = requests.post(f"{BASE_URL}/api/useremail?token=abc")

    assert res.status_code == 401