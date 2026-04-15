"""공통 설정 - 환경변수에서 값 읽기."""
import os
import json

# 티스토리
TISTORY_BLOG_NAME = os.environ.get("TISTORY_BLOG_NAME", "write36844")
TISTORY_USER_ID = os.environ.get("TISTORY_USER_ID", "")
TISTORY_APP_PASSWORD = os.environ.get("TISTORY_APP_PASSWORD", "")
TISTORY_API_ENDPOINT = f"https://{TISTORY_BLOG_NAME}.tistory.com/api/meta"

# 카테고리 ID 맵 (GitHub Secret의 JSON 문자열 파싱)
CATEGORY_MAP = {}
try:
    CATEGORY_MAP = json.loads(os.environ.get("CATEGORY_MAP", "{}"))
except json.JSONDecodeError:
    CATEGORY_MAP = {}

# Anthropic (Claude)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")

# Google AI (Imagen)
GOOGLE_AI_API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")

# 경로
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL_DIR = os.path.join(REPO_ROOT, "skill")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")
IMAGES_DIR = os.path.join(REPO_ROOT, "assets", "images")


# 티스토리 관련 헬퍼는 GitHub Pages로 이전하면서 더 이상 사용하지 않음
