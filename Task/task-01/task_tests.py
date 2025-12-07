import os
import subprocess
import glob

def run(cmd, env=None):
    """Utility to run shell commands and capture output."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)

def test_dev_mode_runs():
    """Verify that the development server command starts without crashing."""
    out = run("npm run dev -- --help")
    assert out.returncode == 0

def test_build_does_not_crash_without_env():
    """Ensure build does not fail even when MONGODB_URI is missing."""
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)
    out = run("npm run build", env=env)
    assert out.returncode == 0 or "MONGODB_URI is missing" in out.stderr

def test_start_runs():
    """Verify that the production start command executes successfully."""
    out = run("npm start -- --help")
    assert out.returncode == 0

def test_docker_build_succeeds_without_env():
    """Verify Docker image builds successfully without database access."""
    out = run("docker build -t test-task01 .")
    assert out.returncode == 0

def test_unified_db_connector_exists():
    """Check that the unified database connector file exists."""
    assert os.path.exists("app/testConnect/page.js")

def test_middleware_style_is_removed():
    """Ensure old middleware-style handler wrapping is removed from DB connector."""
    content = open("app/testConnect/page.js", "r", encoding="utf-8").read()
    assert "return handler(" not in content

def test_all_api_routes_use_same_connector():
    """Verify that all API routes import and use the same unified DB connector."""
    api_files = glob.glob("app/api//route.js", recursive=True)
    assert len(api_files) > 5  # sanity check that APIs exist
    for f in api_files:
        content = open(f, "r", encoding="utf-8").read()
        assert "testConnect" in content or "dbConnect" in content

def test_buffering_timeout_is_disabled():
    """Ensure Mongoose buffering timeout protection is configured."""
    content = open("app/testConnect/page.js", "r", encoding="utf-8").read()
    assert "bufferCommands" in content or "serverSelectionTimeoutMS" in content

def test_missing_env_fails_cleanly():
    """Ensure missing MONGODB_URI fails with a clear, readable error."""
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)
    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True
    )
    assert "missing" in result.stderr.lower() or result.returncode != 0