"""Stable Diffusion (SDXL-Turbo) 로컬 이미지 생성.

사용법:
    # 특정 포스트의 이미지 3장 생성
    python3 scripts/generate_images_local.py --post _posts/2026-04-15-갑목-...md

    # 이미지 아직 없는 모든 포스트 일괄 처리
    python3 scripts/generate_images_local.py --all

    # 프롬프트 직접 입력
    python3 scripts/generate_images_local.py --prompt "A tall pine tree..." --out assets/images/test.png

환경:
    GPU: Apple Silicon MPS 자동 감지, 없으면 CPU fallback
    모델: SDXL-Turbo (stabilityai/sdxl-turbo) — 첫 실행 시 ~7GB 다운로드
    비용: 무료 (완전 로컬)
    속도: M1/M2 Pro 기준 이미지 1장 ~10-20초
"""
import os
import sys
import re
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

import torch
from diffusers import AutoPipelineForText2Image

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "mps" else torch.float32
MODEL_ID = os.environ.get("SD_MODEL", "stabilityai/sdxl-turbo")

_pipe = None


def get_pipe():
    global _pipe
    if _pipe is not None:
        return _pipe
    print(f"모델 로드 중: {MODEL_ID} (디바이스: {DEVICE})")
    print("  첫 실행 시 ~7GB 다운로드, 잠시 기다려주세요...")
    _pipe = AutoPipelineForText2Image.from_pretrained(
        MODEL_ID,
        torch_dtype=DTYPE,
        variant="fp16" if DTYPE == torch.float16 else None,
    )
    _pipe = _pipe.to(DEVICE)
    print("  모델 로드 완료!")
    return _pipe


def generate_image_local(prompt, output_path, width=1024, height=1024, steps=4):
    pipe = get_pipe()
    try:
        result = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=0.0,
            width=width,
            height=height,
        )
        image = result.images[0]
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return True
    except Exception as e:
        print(f"  ❌ 생성 실패: {e}")
        return False


def extract_image_prompts(post_text):
    m = re.search(r"<!--\s*image_prompts:\s*(\[.*?\])\s*-->", post_text, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return [item["prompt"] for item in data if "prompt" in item][:3]
    except Exception:
        return []


def slug_from_post_filename(post_path):
    stem = Path(post_path).stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


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
        if generate_image_local(prompt, str(out)):
            print(f"   ✅ 저장: {out.relative_to(Path(config.REPO_ROOT))}")
            created += 1
    return created


def all_posts_needing_images():
    posts = sorted(Path(config.POSTS_DIR).glob("*.md"))
    todo = []
    for p in posts:
        slug = slug_from_post_filename(p)
        first = Path(config.IMAGES_DIR) / f"{slug}-1.png"
        if not first.exists():
            todo.append(p)
    return todo


def main():
    parser = argparse.ArgumentParser(description="Stable Diffusion 로컬 이미지 생성")
    parser.add_argument("--post", help="특정 포스트 경로")
    parser.add_argument("--all", action="store_true", help="이미지 아직 없는 모든 포스트 처리")
    parser.add_argument("--prompt", help="프롬프트 직접 입력")
    parser.add_argument("--out", default="assets/images/test.png", help="--prompt 저장 경로")
    parser.add_argument("--overwrite", action="store_true", help="기존 이미지 덮어쓰기")
    args = parser.parse_args()

    if args.prompt:
        out = os.path.join(config.REPO_ROOT, args.out)
        print(f"\n직접 프롬프트: {args.prompt[:80]}...")
        ok = generate_image_local(args.prompt, out)
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
