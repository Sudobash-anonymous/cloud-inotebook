import os
import subprocess

def run(cmd):
    """Helper to run shell commands and capture output."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def test_env_example_exists():
    """Docstring for test_env_example_exists"""
    assert os.path.exists(".env.example")

def test_gitignore_blocks_env():
    """Docstring for test_gitignore_blocks_env"""
    with open(".gitignore") as f:
        content = f.read()
    assert ".env" in content

def test_build_without_secrets_succeeds():
    """Docstring for test_build_without_secrets_succeeds"""
    out = run("docker build -t task02-test .")
    assert out.returncode == 0

def test_runtime_fails_without_env():
    """Docstring for test_runtime_fails_without_env"""
    out = run("docker run --rm task02-test")
    assert "Missing required environment variables" in out.stderr

def test_weak_secrets_rejected():
    """Docstring for test_weak_secrets_rejected"""
    env = "PASSWORD_SECRET_=123 JWT_SECRET_=123 MONGODB_URI=abc"
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Secret too weak" in out.stderr

def test_secrets_not_logged():
    """Docstring for test_secrets_not_logged"""
    env = "PASSWORD_SECRET_=superlongsecuresecretvalue JWT_SECRET_=ultralongjwtsecretvalue MONGODB_URI=abc"
    out = run(f'docker run --rm -e {env} task02-test')
    assert "superlongsecuresecretvalue" not in out.stdout

def test_dockerfile_has_no_env_args():
    """Docstring for test_dockerfile_has_no_env_args"""
    with open("Dockerfile") as f:
        content = f.read()
    assert "ARG PASSWORD_SECRET_" not in content
    assert "ARG JWT_SECRET_" not in content
    
    
    
    
def test_reject_partial_env():
    """Docstring for test_reject_partial_env"""
    env = "PASSWORD_SECRET_=supersecret"
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Missing required environment variables" in out.stderr
    
def test_accept_valid_secrets():
    """Docstring for test_accept_valid_secrets"""
    env = ("PASSWORD_SECRET_=strongpasswordsecret JWT_SECRET_=strongjwtsecret MONGODB_URI=mongodb://localhost:27017/testdb")
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Server started successfully" in out.stdout
    
def test_no_secrets_in_stderr():
    """Docstring for test_no_secrets_in_stderr"""
    env = ("PASSWORD_SECRET_=abcdef123456789 JWT_SECRET_=123456789abcdef MONGODB_URI=mongodb://localhost:27017/testdb")
    out = run(f'docker run --rm -e {env} task02-test')
    assert "abcdef123456789" not in out.stderr
    
def test_reject_short_secrets():
    """Docstring for test_reject_short_secrets"""
    env = ("PASSWORD_SECRET_=short JWT_SECRET_=tiny MONGODB_URI=mongodb://localhost:27017/testdb")
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Secret too weak" in out.stderr
    
def test_reject_secrets_with_spaces():
    """Docstring for test_reject_secrets_with_spaces"""
    env = ("PASSWORD_SECRET_='abc def' JWT_SECRET_='hello world' MONGODB_URI=mongodb://localhost:27017/testdb")
    out = run(f'docker run --rm -e {env} task02-test')
    assert "Invalid secret format" in out.stderr
    
def test_docker_image_has_no_env_file():
    """Docstring for test_docker_image_has_no_env_file"""
    out = run("docker run --rm task02-test sh -c 'ls -la /app/.env'")
    assert ".env" not in out.stderr
    
def test_dockerignore_exists_and_blocks_env():
    """Docstring for test_dockerignore_exists_and_blocks_env"""
    assert os.path.exists(".dockerignore")
    with open(".dockerignore") as f:
        content = f.read()
    assert ".env" in content
    
def test_entrypoint_rejects_env_in_cmd():
    """App must reject secrets passed as command args (unsafe)."""
    out = run("docker run --rm task02-test node app.js PASSWORD_SECRET_=abc")
    assert "Unsafe secret exposure" in out.stderr

def test_logs_do_not_show_raw_env_dump():
    """Application MUST NOT print the environment dump."""
    env = (
        "PASSWORD_SECRET_=goodsecret123 "
        "JWT_SECRET_=anothergoodsecret321 "
        "MONGODB_URI=db"
    )
    out = run(f"docker run --rm -e {env} task02-test")
    assert "PASSWORD_SECRET_" not in out.stdout
    assert "JWT_SECRET_" not in out.stdout

def test_application_boots_with_safe_message():
    """App must print a standard boot message with no sensitive info."""
    env = (
        "PASSWORD_SECRET_=supersecure111 "
        "JWT_SECRET_=ultrasafe222 "
        "MONGODB_URI=db"
    )
    out = run(f"docker run --rm -e {env} task02-test")
    assert "Server started successfully" in out.stdout

def test_dockerfile_does_not_copy_env_files():
    """Dockerfile must not COPY .env or secrets."""
    with open("Dockerfile") as f:
        content = f.read()
    assert ".env" not in content
    assert "COPY .env" not in content

def test_invalid_mongodb_uri_rejected():
    """App should reject invalid MongoDB URI patterns."""
    env = (
        "PASSWORD_SECRET_=validpass123 "
        "JWT_SECRET_=validjwt456 "
        "MONGODB_URI=invalid_uri"
    )
    out = run(f"docker run --rm -e {env} task02-test")
    assert "Invalid MongoDB URI" in out.stderr
