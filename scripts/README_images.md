# 이미지 자동 생성 가이드

Gemini (Nano Banana) 모델로 블로그 이미지를 만들어요. Google AI Studio 무료 티어로 충분.

## 최초 세팅 (한 번만)

### 1. API 키 발급
https://aistudio.google.com/app/apikey 에서 `Create API key` → 복사

### 2. `.env` 파일 생성
리포 루트(`ilgan-ilgi/`)에서:
```bash
echo 'GOOGLE_AI_API_KEY="붙여넣기"' > .env
```

`.env`는 `.gitignore`에 있어서 GitHub에 올라가지 않아요.

### 3. Python 의존성
```bash
python3 --version        # 3.9 이상 필요
pip3 install -r requirements.txt
```

## 사용법

### 특정 포스트의 이미지 3장 생성
```bash
python3 scripts/generate_images.py --post _posts/2026-04-15-갑목-성격-연애-궁합-총정리.md
```

### 이미지 아직 없는 모든 포스트 일괄 처리
```bash
python3 scripts/generate_images.py --all
```

### 프롬프트 직접 테스트
```bash
python3 scripts/generate_images.py --prompt "A tall pine tree on hanji paper, sage green palette, no people" --out assets/images/test.png
```

### 기존 이미지 덮어쓰기
```bash
python3 scripts/generate_images.py --post _posts/... --overwrite
```

## 생성된 이미지 경로

`assets/images/<포스트슬러그>-1.png`, `-2.png`, `-3.png` 식으로 저장돼요.

예:
- `assets/images/갑목-성격-연애-궁합-총정리-1.png` (썸네일)
- `assets/images/갑목-성격-연애-궁합-총정리-2.png` (본문)
- `assets/images/갑목-성격-연애-궁합-총정리-3.png` (궁합 섹션)

## 생성 후

이미지 확인하고 마음에 들면 커밋·푸시:
```bash
git add assets/images/
git commit -m "갑목 이미지 추가"
git push
```

1~2분 후 블로그에 반영됨.

## 마음에 안 들면

두 가지 방법:

**A. 같은 프롬프트로 다시 생성** (랜덤이라 매번 달라짐)
```bash
python3 scripts/generate_images.py --post _posts/... --overwrite
```

**B. 포스트의 프롬프트 수정 후 재생성**
`_posts/*.md` 맨 위 `<!-- image_prompts: [...] -->` 주석 안의 `"prompt": "..."` 부분 직접 수정 → 저장 → 재생성

## 모델 바꾸기

기본은 `gemini-2.5-flash-image-preview`예요. 다른 모델 쓰고 싶으면:

```bash
export GEMINI_IMAGE_MODEL="gemini-2.0-flash-exp-image-generation"
python3 scripts/generate_images.py --post ...
```

## 한도

Google AI Studio 무료 티어:
- 분당 요청 수 제한 있음 (보통 10회/분)
- 일일 총량 제한 있음 (모델별 다름, 수십 장 수준)

초과 시 몇 분 쉬었다가 다시 시도.

## 막히면

- **`GOOGLE_AI_API_KEY 가 설정되지 않았어요`**
  → `.env` 파일 경로 확인, 또는 `echo $GOOGLE_AI_API_KEY` 로 환경변수 체크

- **`이미지가 없어요 (프롬프트가 차단됐을 수 있음)`**
  → Gemini 안전 필터가 거부한 경우. 프롬프트에서 사람·얼굴 언급 빼고 다시 시도

- **`403` 또는 `401` 에러**
  → 키가 만료됐거나 잘못 복사됐어요. 재발급

- **이미지가 너무 안 이뻐요**
  → `--overwrite` 로 몇 번 다시 돌려보거나, 프롬프트에 `"painterly, soft, hanji paper background, no text, no people"` 같은 스타일 키워드 추가
