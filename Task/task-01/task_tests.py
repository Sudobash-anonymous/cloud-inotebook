import os
import subprocess


def run(cmd, env=None):
    """Helper to run shell commands and capture output."""
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        env=env
    )


def test_dev_mode_runs():
    """
    Verify that the development server command is callable
    and does not crash immediately.
    """
    out = run("npm run dev -- --help")
    assert out.returncode == 0


def test_build_does_not_crash():
    """
    Verify that the production build runs without crashing.
    This does NOT require database access.
    """
    out = run("npm run build")
    assert out.returncode == 0


def test_start_runs():
    """
    Verify that the production server start command is callable.
    """
    out = run("npm start -- --help")
    assert out.returncode == 0


def test_docker_build_succeeds():
    """
    Ensure that Docker image can be built successfully
    without accessing the database at build time.
    """
    out = run("docker build -t test-task01 .")
    assert out.returncode == 0


def test_missing_env_fails_cleanly():
    """
    Ensure that requiring the DB connector without MONGODB_URI
    results in a clear hard failure.
    """
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)

    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True
    )

    has_error_code = result.returncode != 0
    has_error_text = "missing" in result.stderr.lower() or "error" in result.stderr.lower()

    assert has_error_code or has_error_text


def test_runtime_db_failure_throws_hard_error():
    """
    Simulate a real database connection failure
    and ensure the app throws a hard runtime error.
    """
    env = os.environ.copy()
    env["MONGODB_URI"] = "mongodb://127.0.0.1:1/invalid"

    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10
    )

    has_error_code = result.returncode != 0
    has_error_text = (
        "econnrefused" in result.stderr.lower()
        or "failed" in result.stderr.lower()
        or "error" in result.stderr.lower()
    )

    assert has_error_code or has_error_text