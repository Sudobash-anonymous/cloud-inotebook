import os
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def test_env_exists():
    assert os.getenv("MONGODB_URI") is not None

def test_dev_mode_runs():
    out = run("npm run dev -- --help")
    assert out.returncode == 0

def test_build_does_not_crash():
    out = run("npm run build")
    assert "Compiled successfully" in out.stdout

def test_start_runs():
    out = run("npm start -- --help")
    assert out.returncode == 0

def test_docker_build_succeeds():
    out = run("docker build -t test-task01 .")
    assert "Successfully" in out.stdout or out.returncode == 0

def test_missing_env_fails_cleanly():
    env = os.environ.copy()
    env.pop("MONGODB_URI", None)
    result = subprocess.run(
        ["node", "-e", "require('./app/testConnect/page.js')"],
        env=env,
        capture_output=True,
        text=True
    )
    assert "MONGODB_URI is missing" in result.stderr or result.returncode != 0