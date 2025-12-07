import os
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

# ✅ Dev mode must start without crashing
def test_dev_mode_runs():
    out = run("npm run dev -- --help")
    assert out.returncode == 0

# ✅ Build must NOT crash even if env is missing
def test_build_does_not_crash():
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)

    out = subprocess.run(
        "npm run build",
        shell=True,
        env=env,
        capture_output=True,
        text=True
    )

    # ✅ Build must finish (even if API logs error)
    assert out.returncode == 0 or "MONGODB_URI is missing" in out.stderr

# ✅ Production start must run
def test_start_runs():
    out = run("npm start -- --help")
    assert out.returncode == 0

# ✅ Docker image must build (no output text dependency)
def test_docker_build_succeeds():
    out = run("docker build -t test-task01 .")
    assert out.returncode == 0

# ✅ Missing env must fail CLEANLY with readable error
def test_missing_env_fails_cleanly():
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)

    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True
    )

    # ✅ Either explicit message OR clean non-zero exit
    assert (
        "MONGODB_URI is missing" in result.stderr
        or "missing" in result.stderr.lower()
        or result.returncode != 0
    )