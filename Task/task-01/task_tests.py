# import os
# import subprocess
# import glob
# import re


# def run(cmd, env=None):
#     # """Run shell command and capture output."""
#     return subprocess.run(
#         cmd,
#         shell=True,
#         capture_output=True,
#         text=True,
#         env=env
#     )

# def test_dev_mode_runs():
#     # """Dev mode must start without crashing."""
#     out = run("npm run dev -- --help")
#     assert out.returncode == 0


# def test_build_does_not_crash():
#     # """Production build must succeed without DB access."""
#     out = run("npm run build")
#     assert out.returncode == 0


# def test_start_runs():
#     # """Production start must be callable."""
#     out = run("npm start -- --help")
#     assert out.returncode == 0


# def test_docker_build_succeeds():
#     # """Docker build must succeed without DB access."""
#     out = run("docker build -t test-task01 .")
#     assert out.returncode == 0


# def test_missing_env_fails_cleanly():
#     # """Missing MONGODB_URI must cause a clean hard failure."""
#     env = os.environ.copy()
#     env.pop("MONGODB_URI", None)

#     result = subprocess.run(
#         ["node", "-e", "require('./app/testConnect/page.js')"],
#         env=env,
#         capture_output=True,
#         text=True
#     )

#     assert result.returncode != 0
#     assert "missing" in result.stderr.lower() or "error" in result.stderr.lower()


# def test_runtime_db_failure_throws_hard_error():
#     # """Invalid MongoDB URI must cause runtime failure immediately."""
#     env = os.environ.copy()
#     env["MONGODB_URI"] = "mongodb://127.0.0.1:1/invalid"

#     result = subprocess.run(
#         ["node", "-e", "require('./app/testConnect/page.js')"],
#         env=env,
#         capture_output=True,
#         text=True,
#         timeout=10
#     )

#     assert result.returncode != 0
#     assert (
#         "econnrefused" in result.stderr.lower()
#         or "failed" in result.stderr.lower()
#         or "error" in result.stderr.lower()
#     )


# def test_all_api_routes_use_shared_connector():
#     # """
#     # Every API route must import the unified DB connector.
#     # Prevents duplicated or legacy connectors.
#     # """
#     api_files = glob.glob("app/api//route.js", recursive=True)
#     assert api_files, "No API route files found"

#     for file in api_files:
#         with open(file, "r", encoding="utf-8") as f:
#             content = f.read()

#         assert (
#             "testConnect" in content or "dbConnect" in content
#         ), f"API route does not use shared connector: {file}"


# def test_no_middleware_style_db_wrappers_exist():
#     """
#     Middleware-style DB wrappers must not exist anymore.
#     """
#     bad_patterns = [
#         "connectDB(",
#         "dbMiddleware(",
#         "withDB("
#     ]

#     js_files = glob.glob("app//*.js", recursive=True)

#     for file in js_files:
#         with open(file, "r", encoding="utf-8") as f:
#             content = f.read()

#         for pattern in bad_patterns:
#             assert pattern not in content, f"Deprecated DB middleware found in {file}"


# def test_buffering_timeout_error_not_present():
#     # """
#     # Ensure no Mongoose buffering timeout errors are present in logs.
#     # """
#     out = run("npm start")
#     assert "buffering timed out" not in out.stderr.lower()


# def test_api_routes_handle_db_failure_consistently():
#     #
#     # All API routes must return clean error responses when DB fails.
#     #
#     env = os.environ.copy()
#     env["MONGODB_URI"] = "mongodb://127.0.0.1:1/invalid"

#     api_files = glob.glob("app/api//route.js", recursive=True)

#     for file in api_files:
#         route_test = subprocess.run(
#             ["node", file],
#             env=env,
#             capture_output=True,
#             text=True
#         )

#         assert (
#             route_test.returncode != 0
#             or "error" in route_test.stderr.lower()
#             or "failed" in route_test.stderr.lower()
#         ), f"API route {file} does not handle DB failure properly"



import os
import subprocess
import glob
import re


def run(cmd, env=None):
    # Small helper to run shell commands and grab the output.
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        env=env
    )


def test_dev_mode_runs():
    # Make sure dev mode doesn’t immediately blow up.
    out = run("npm run dev -- --help")
    assert out.returncode == 0


def test_build_does_not_crash():
    # A production build should work even if Mongo isn’t reachable.
    out = run("npm run build")
    assert out.returncode == 0


def test_start_runs():
    # The production start script should at least be callable.
    out = run("npm start -- --help")
    assert out.returncode == 0


def test_docker_build_succeeds():
    # Docker should be able to build the image without depending on Mongo.
    out = run("docker build -t test-task01 .")
    assert out.returncode == 0


def test_missing_env_fails_cleanly():
    # If MONGODB_URI is missing, the app should fail fast and clearly.
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)

    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "missing" in result.stderr.lower() or "error" in result.stderr.lower()


def test_runtime_db_failure_throws_hard_error():
    # Invalid URI should break immediately instead of silently hanging.
    env = os.environ.copy()
    env["MONGODB_URI"] = "mongodb://127.0.0.1:1/invalid"

    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode != 0
    assert (
        "econnrefused" in result.stderr.lower()
        or "failed" in result.stderr.lower()
        or "error" in result.stderr.lower()
    )


def test_all_api_routes_use_shared_connector():
    # Every API route should be using the unified DB connector.
    api_files = glob.glob("app/api/**/route.js", recursive=True)
    assert api_files, "No API route files found"

    for file in api_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        assert (
            "testConnect" in content or "dbConnect" in content
        ), f"API route does not use shared connector: {file}"


def test_no_middleware_style_db_wrappers_exist():
    # Old middleware-based DB wrappers shouldn’t exist anymore.
    bad_patterns = [
        "connectDB(",
        "dbMiddleware(",
        "withDB("
    ]

    js_files = glob.glob("app/**/*.js", recursive=True)

    for file in js_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        for pattern in bad_patterns:
            assert pattern not in content, f"Deprecated DB middleware found in {file}"


def test_buffering_timeout_error_not_present():
    # Check that the classic Mongoose “buffering timed out” error isn’t showing up.
    out = run("npm start")
    assert "buffering timed out" not in out.stderr.lower()


def test_api_routes_handle_db_failure_consistently():
    # Routes should respond cleanly when Mongo is down.
    env = os.environ.copy()
    env["MONGODB_URI"] = "mongodb://127.0.0.1:1/invalid"

    api_files = glob.glob("app/api/**/route.js", recursive=True)

    for file in api_files:
        route_test = subprocess.run(
            ["node", file],
            env=env,
            capture_output=True,
            text=True
        )

        assert (
            route_test.returncode != 0
            or "error" in route_test.stderr.lower()
            or "failed" in route_test.stderr.lower()
        ), f"API route {file} does not handle DB failure properly"

