# 일간일기 (ilgan-ilgi)

**사주 일간과 MBTI로 나와 사람을 읽는 블로그 — Claude Max + GitHub Pages 기반.**

- **블로그 URL**: `https://syoung31infobank-max.github.io/ilgan-ilgi/`
- **아키텍처**: Mac에서 Claude Code로 글 작성 → `git push` → GitHub Pages 자동 배포
- **비용**: Claude Max 구독만 있으면 추가 비용 **0원**

## 운영 흐름

```
[일요일 저녁 30~40분]
  Mac 터미널: cd ~/Documents/ilgan-ilgi && claude
    → "이번 주 글 3편 써줘"
    → Claude가 CLAUDE.md + skill/ 읽고 _posts/ 에 3편 저장
       + 이미지 프롬프트 포함
  시영님이 [내 경험] 빈칸 채우기
  python3 scripts/generate_images.py --post _posts/... (이미지 생성)
  git push

[1~2분 후]
  GitHub Actions (deploy.yml) 자동 실행
  Jekyll 빌드 → GitHub Pages 배포
  블로그에 공개 ✨
```

## 폴더 구조

```
ilgan-ilgi/
├── CLAUDE.md              🤖 Claude Code가 읽는 작업 가이드 (중요!)
├── SETUP.md               📘 세팅 가이드 (처음 한 번)
├── README.md              📖 이 파일
│
├── _config.yml            Jekyll 설정
├── Gemfile                Ruby 의존성
├── index.html             홈(글 목록)
├── about.md               소개 페이지
│
├── _layouts/              HTML 템플릿
├── _includes/             헤더/푸터/head
├── _posts/                📝 발행된 글 (여기에 추가하면 자동 배포)
├── assets/
│   ├── css/style.css      디자인 (한지 톤)
│   └── images/            포스트 이미지
│
├── .github/workflows/
│   └── deploy.yml         ✅ main 푸시 시 빌드·배포
│
├── scripts/
│   └── generate_images.py 이미지 생성 (Google Imagen, 무료 quota)
│
├── skill/                 🧠 Claude가 참고하는 블로그 DNA
│   ├── SKILL.md              전체 컨셉
│   ├── agents/               6개 역할 프롬프트
│   ├── references/           톤 예시, 금지 표현, 10일간 프로파일
│   └── templates/            30개 글감, 제목 패턴, 구조
│
├── requirements.txt       Python 의존성 (이미지 생성용만)
└── .env                   🔐 API 키 (로컬에만, git에 안 올라감)
```

## 처음 오셨다면

👉 **`SETUP.md`** 먼저 읽어주세요. 20~25분.

## 주간 작업 할 때

👉 **`CLAUDE.md`**에 쓰인 대로 Claude Code한테 요청하면 됩니다.

예:
- "이 리포의 CLAUDE.md 읽고, 다음 글로 을목 소개편 써줘"
- "이번 주 글 3편 써줘, 주제는 알아서 골라"
- "이미 쓴 갑목 글 톤 참고해서 병화 써줘"

## 디자인 원칙

- 한지 톤 웜 컬러 (sage green + warm ochre + 베이지)
- Pretendard 한글 폰트
- 모바일 우선
- 1,700~1,900자 중간 분량 (5~7분 읽기)
- 단정하지 않는 해요체
- 시그니처: "MBTI로는 ___, 일간으로는 ___"
