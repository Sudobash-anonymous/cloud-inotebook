import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
API_DIR = os.path.join(BASE_DIR, "app", "api")
UTILS_DIR = os.path.join(BASE_DIR, "utils")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def test_redis_client_exists():
    path = os.path.join(UTILS_DIR, "redisClient.js")
    assert os.path.exists(path), "utils/redisClient.js must exist"
    content = read(path)
    assert "createClient" in content or "Redis" in content
    assert "getRedisClient" in content

def test_fetchtextcloud_uses_cache():
    path = os.path.join(API_DIR, "fetchtextcloud", "route.js")
    content = read(path)
    assert "getRedisClient" in content
    assert "text:" in content
    assert ".get(" in content
    assert ".set(" in content

def test_fetchemail_uses_cache():
    path = os.path.join(API_DIR, "fetchemail", "route.js")
    content = read(path)
    assert "getRedisClient" in content
    assert "email:" in content
    assert ".get(" in content
    assert ".set(" in content

def test_fetchimg_uses_cache():
    path = os.path.join(API_DIR, "fetchimg", "route.js")
    content = read(path)
    assert "getRedisClient" in content
    assert "img:" in content
    assert ".get(" in content
    assert ".set(" in content

def test_mutation_routes_invalidate_cache():
    files = [
        os.path.join(API_DIR, "textcloud", "route.js"),
        os.path.join(API_DIR, "deletetextcloud", "route.js"),
        os.path.join(API_DIR, "addimage", "route.js"),
        os.path.join(API_DIR, "deleteimage", "route.js"),
    ]
    for path in files:
        content = read(path)
        assert "getRedisClient" in content
        assert ".del(" in content

def test_docker_compose_has_redis_service():
    path = os.path.join(BASE_DIR, "docker-compose.yaml")
    assert os.path.exists(path), "docker-compose.yaml must exist at repo root"
    content = read(path)
    assert "redis:" in content
    assert "image: redis" in content