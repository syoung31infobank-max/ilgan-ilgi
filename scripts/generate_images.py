"""Gemini (Nano Banana) 로 블로그 이미지 생성.

사용법:
    # 특정 포스트의 이미지 3장 생성
    python3 scripts/generate_images.py --post _posts/2026-04-15-갑목-...md

    # 이미지 아직 없는 모든 포스트 일괄 처리
    python3 scripts/generate_images.py --all

    # 프롬프트 직접 입력
    python3 scripts/generate_images.py --prompt "A tall pine tree..." --out assets/images/test.png

환경:
    GOOGLE_AI_API_KEY = Google AI Studio 키 (.env 파일 또는 환경변수)
    무료 티어로 일 수십 장 생성 가능.
"""
import os
import sys
import re
import json
import argparse
import base64
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config


# ---------- .env 로드 ----------
def load_env():
    env_path = os.path.join(config.REPO_ROOT, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


load_env()
API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")


# ---------- Gemini 이미지 생성 ----------
# 무료 티어에서 쓸 수 있는 이미지 생성 모델
# 최신 권장: gemini-2.5-flash-image-preview (Nano Banana)
# 대안: gemini-2.0-flash-exp-image-generation
MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")


def generate_image_gemini(prompt, output_path):
    """Gemini API로 이미지 1장 생성."""
    import google.generativeai as genai

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL)

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )
    except Exception as e:
        # 일부 SDK 버전에서는 response_modalities 파라미터가 다를 수 있음
        try:
            response = model.generate_content(prompt)
        except Exception as e2:
            print(f"  ❌ 생성 실패: {e2}")
            return False

    # 응답에서 이미지 바이트 추출
    try:
        for part in response.candidates[0].content.parts:
            # inline_data 가 이미지
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                data = inline.data
                # data 가 base64 str 인 경우와 bytes 인 경우 둘 다 처리
                if isinstance(data, str):
                    data = base64.b64decode(data)
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"  ❌ 응답 파싱 실패: {e}")
        return False

    print("  ❌ 응답에 이미지가 없어요 (프롬프트가 차단됐을 수 있음)")
    return False


# ---------- 포스트에서 프롬프트 추출 ----------
def extract_image_prompts(post_text):
    """HTML 주석 <!-- image_prompts: [...] --> 에서 프롬프트 3개 추출.

    포맷:
    [
      {"role": "thumbnail", "prompt": "English prompt", "alt": "한글"},
      ...
    ]
    """
    m = re.search(r"<!--\s*image_prompts:\s*(\[.*?\])\s*-->", post_text, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return [item["prompt"] for item in data if "prompt" in item][:3]
    except Exception:
        return []


def slug_from_post_filename(post_path):
    """_posts/YYYY-MM-DD-slug.md 에서 slug 추출."""
    stem = Path(post_path).stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


# ---------- 포스트 단위 처리 ----------
def process_post(post_path, overwrite=False):
    path = Path(post_path)
    if not path.exists():
        print(f"❌ 파일 없음: {post_path}")
        return 0

    text = path.read_text(encoding="utf-8")
    prompts = extract_image_prompts(text)

    if not prompts:
        print(f"⚠️  {path.name}: 이미지 프롬프트를 못 찾았어요 (HTML 주석 확인)")
        return 0

    slug = slug_from_post_filename(path)
    images_dir = Path(config.IMAGES_DIR)
    images_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📝 {path.name}")
    print(f"   → 이미지 {len(prompts)}장 생성 예정")

    created = 0
    for i, prompt in enumerate(prompts, 1):
        out = images_dir / f"{slug}-{i}.png"
        if out.exists() and not overwrite:
            print(f"   [{i}/{len(prompts)}] 이미 있음 (건너뜀): {out.name}")
            continue
        print(f"   [{i}/{len(prompts)}] 생성 중: {prompt[:70]}...")
        if generate_image_gemini(prompt, str(out)):
            print(f"   ✅ 저장: {out.relative_to(Path(config.REPO_ROOT))}")
            created += 1
    return created


def all_posts_needing_images():
    """이미지가 아직 없는 포스트만 리스트업."""
    posts = sorted(Path(config.POSTS_DIR).glob("*.md"))
    todo = []
    for p in posts:
        slug = slug_from_post_filename(p)
        first = Path(config.IMAGES_DIR) / f"{slug}-1.png"
        if not first.exists():
            todo.append(p)
    return todo


# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Gemini 이미지 생성")
    parser.add_argument("--post", help="특정 포스트 경로 (예: _posts/2026-04-15-...md)")
    parser.add_argument("--all", action="store_true", help="이미지 아직 없는 모든 포스트 처리")
    parser.add_argument("--prompt", help="프롬프트 직접 입력 (테스트용)")
    parser.add_argument("--out", default="assets/images/test.png", help="--prompt 와 함께 쓸 저장 경로")
    parser.add_argument("--overwrite", action="store_true", help="기존 이미지 덮어쓰기")
    args = parser.parse_args()

    if not API_KEY:
        print("❌ GOOGLE_AI_API_KEY 가 설정되지 않았어요.")
        print("   .env 파일에 GOOGLE_AI_API_KEY=... 를 추가하거나")
        print("   export GOOGLE_AI_API_KEY=... 로 환경변수 설정해주세요.")
        sys.exit(1)

    print(f"모델: {MODEL}")

    if args.prompt:
        out = os.path.join(config.REPO_ROOT, args.out)
        print(f"\n직접 프롬프트: {args.prompt[:80]}...")
        ok = generate_image_gemini(args.prompt, out)
        sys.exit(0 if ok else 1)

    if args.all:
        todo = all_posts_needing_images()
        if not todo:
            print("✅ 모든 포스트가 이미 이미지를 가지고 있어요.")
            return
        print(f"이미지 필요한 포스트: {len(todo)}개")
        total = 0
        for p in todo:
            total += process_post(str(p), overwrite=args.overwrite)
        print(f"\n🎉 총 {total}장 생성 완료")
        return

    if args.post:
        created = process_post(args.post, overwrite=args.overwrite)
        print(f"\n🎉 {created}장 생성 완료")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
