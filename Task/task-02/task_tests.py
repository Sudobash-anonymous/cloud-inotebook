import os
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def test_env_example_exists():
    assert os.path.exists(".env.example")

def test_gitignore_blocks_env():
    with open(".gitignore") as f:
        content = f.read()
    assert ".env" in content

def test_build_without_secrets_succeeds():
    out = run("docker build -t task02-test .")
    assert out.returncode == 0

def test_runtime_fails_without_env():
    out = run("docker run --rm task02-test")
    assert "Missing required environment variables" in out.stderr

def test_weak_secrets_rejected():
    env = "PASSWORD_SECRET_=123 JWT_SECRET_=123 MONGODB_URI=abc"
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Secret too weak" in out.stderr

def test_secrets_not_logged():
    env = "PASSWORD_SECRET_=superlongsecuresecretvalue JWT_SECRET_=ultralongjwtsecretvalue MONGODB_URI=abc"
    out = run(f'docker run --rm -e {env} task02-test')
    assert "superlongsecuresecretvalue" not in out.stdout

def test_dockerfile_has_no_env_args():
    with open("Dockerfile") as f:
        content = f.read()
    assert "ARG PASSWORD_SECRET_" not in content
    assert "ARG JWT_SECRET_" not in content