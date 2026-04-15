"""Google AI Studio Imagen으로 이미지 생성.

사용법:
    python scripts/generate_images.py --post posts/2026-04-15-갑목-...md

포스트 안의 이미지 프롬프트를 읽어서 posts/images/<slug>-{1,2,3}.png로 저장.
"""
import os
import sys
import re
import json
import argparse
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

# 로컬 .env 파일에서 키 로드 (있을 때만)
_env_path = os.path.join(config.REPO_ROOT, ".env")
if os.path.exists(_env_path) and not os.environ.get("GOOGLE_AI_API_KEY"):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line.startswith("GOOGLE_AI_API_KEY"):
                _val = _line.split("=", 1)[1].strip().strip('"').strip("'")
                os.environ["GOOGLE_AI_API_KEY"] = _val
                config.GOOGLE_AI_API_KEY = _val


def extract_image_prompts(post_text):
    """포스트에서 이미지 프롬프트 추출. HTML 주석 image_prompts JSON을 우선."""
    prompts = []

    # run_agents.py가 프론트매터 뒤에 남긴 HTML 주석에서 찾기
    m = re.search(r"<!--\s*image_prompts:\s*(\[.*?\])\s*-->", post_text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            prompts = [p.get("prompt") if isinstance(p, dict) else p for p in data]
            return [p for p in prompts if p][:3]
        except json.JSONDecodeError:
            pass

    # 코드블록 JSON fallback
    m = re.search(r"```json\s*\n(.*?)\n```", post_text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            if isinstance(data, dict) and "image_prompts" in data:
                prompts = [p.get("prompt", p) if isinstance(p, dict) else p for p in data["image_prompts"]]
                return prompts[:3]
        except json.JSONDecodeError:
            pass

    # blockquote에서 영어 프롬프트 추출
    for line in post_text.split("\n"):
        if line.strip().startswith("> ") and re.search(r"[a-zA-Z]{20,}", line):
            prompts.append(line.strip().lstrip("> ").strip())

    return prompts[:3]


def generate_image(prompt, output_path):
    """Imagen 3으로 이미지 생성."""
    genai.configure(api_key=config.GOOGLE_AI_API_KEY)

    # Imagen 3 모델 사용
    model = genai.GenerativeModel("imagen-3.0-generate-002")

    try:
        result = model.generate_content(
            prompt,
            generation_config={"response_modalities": ["IMAGE"]},
        )

        # 응답에서 이미지 추출
        for part in result.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                return True
    except Exception as e:
        print(f"[이미지 생성 실패] {e}")
        print(f"  프롬프트: {prompt[:100]}...")
        return False
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", required=True, help="포스트 파일 경로")
    args = parser.parse_args()

    post_path = Path(args.post)
    text = post_path.read_text(encoding="utf-8")

    prompts = extract_image_prompts(text)
    if not prompts:
        print("이미지 프롬프트를 찾지 못했어요.")
        return

    os.makedirs(config.IMAGES_DIR, exist_ok=True)
    # Jekyll 포스트 파일명은 YYYY-MM-DD-slug.md 이므로 날짜 부분 떼고 slug만 사용
    stem = post_path.stem
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)

    for i, prompt in enumerate(prompts, 1):
        out = os.path.join(config.IMAGES_DIR, f"{slug}-{i}.png")
        print(f"[{i}/{len(prompts)}] 생성 중: {prompt[:80]}...")
        if generate_image(prompt, out):
            print(f"  → {out}")


if __name__ == "__main__":
    main()
