# 최초 세팅 가이드 (Claude Max 로컬 방식)

**API 키 없이, Claude Max 구독만으로 운영하는 방식이에요.**
Mac에서 Claude Code로 글을 쓰고 `git push`하면 GitHub Pages에 자동 배포됩니다.

순서대로 따라하세요. 총 20~25분.

---

## 1. GitHub 리포에 파일 업로드 (이미 하셨다면 스킵)

- 리포 주소: https://github.com/syoung31infobank-max/ilgan-ilgi
- 압축 푼 `ilgan-ilgi` 폴더 **안의 모든 파일**을 업로드
- 숨김파일(`.github`, `.gitignore`) 포함 주의

---

## 2. GitHub Pages 활성화 (2분)

1. https://github.com/syoung31infobank-max/ilgan-ilgi/settings/pages
2. **Build and deployment** → Source: **GitHub Actions** 선택
3. 저장

활성화되면 첫 배포가 자동 시작. 2~3분 후 블로그 확인:
👉 `https://syoung31infobank-max.github.io/ilgan-ilgi/`

---

## 3. `_config.yml` 수정 (1분)

리포 페이지에서 `_config.yml` 파일 클릭 → 연필 아이콘(Edit) 클릭 → 이 두 줄 찾아서 수정:

```yaml
url: "https://syoung31infobank-max.github.io"
baseurl: "/ilgan-ilgi"
```

(GitHub ID가 `syoung31infobank-max`이므로 위처럼 쓰면 돼요)

우측 `Commit changes` 클릭.

---

## 4. Node.js 설치 확인 (Mac, 2분)

터미널 앱 열기 (Spotlight에서 `터미널` 검색)

```bash
node --version
```

- `v18.x.x` 이상이면 OK
- 없거나 낮으면 → https://nodejs.org 접속 → **LTS** 버전 다운로드 → 설치

---

## 5. Claude Code 설치 (3분)

터미널에서:

```bash
npm install -g @anthropic-ai/claude-code
```

설치 끝나면 로그인:

```bash
claude
```

- 브라우저가 열림 → **Max 구독하신 계정**으로 로그인 → 승인
- 터미널로 돌아와서 채팅창이 뜨면 성공
- `exit` 눌러서 나가기

---

## 6. 리포를 Mac에 클론 (3분)

어디에 둘지 정하세요 (보통 `~/Documents` 아래):

```bash
cd ~/Documents
git clone https://github.com/syoung31infobank-max/ilgan-ilgi.git
cd ilgan-ilgi
```

이 폴더가 앞으로 **작업 홈베이스**예요.

---

## 7. Google AI Studio 키 발급 (3분, 이미지용만)

이미지 자동 생성할 때만 필요해요. 무료.

1. https://aistudio.google.com/app/apikey 접속 → 구글 로그인
2. `Create API key` → 복사

---

## 8. 로컬 `.env` 파일 만들기 (1분)

이 리포 폴더 안에 `.env` 파일 생성 (`.gitignore`에 이미 포함됨, 안 올라감):

터미널에서:
```bash
echo 'GOOGLE_AI_API_KEY="위에서복사한키"' > .env
```

이미지 생성 안 할 거면 이 단계 스킵 가능.

---

## 9. Python 준비 (이미지 생성용, 3분)

```bash
python3 --version
```

`3.9` 이상이면 OK. 없으면 https://python.org 에서 설치.

```bash
pip3 install -r requirements.txt
```

---

## 10. 첫 실행 테스트 (3분)

이 리포 폴더 안에서:

```bash
claude
```

Claude 채팅이 열리면 이렇게 말하세요:

> "이 리포의 CLAUDE.md 읽고, 다음 글로 을목 소개편 초안 써줘. _posts/에 저장해."

Claude(저)가 `CLAUDE.md` → `skill/` 폴더 → 갑목 예시글 참고해서 **을목 소개편**을 `_posts/2026-XX-XX-을목-...md`로 저장해 줄 거예요.

## 11. 발행 (2분)

저장된 글 열어서 `[내 경험]` 빈칸 채우고, 필요하면 이미지 생성:

```bash
python3 scripts/generate_images.py --post _posts/파일명.md
```

(Google AI 키 설정했을 때만. 안 했으면 이미지는 수동 추가해도 돼요.)

푸시:

```bash
git add .
git commit -m "add 을목 소개편"
git push
```

1~2분 후 블로그에 뜸 ✨

---

## 자주 쓰는 명령어

### 글 쓰기 세션 시작
```bash
cd ~/Documents/ilgan-ilgi
claude
```

### 발행
```bash
git add . && git commit -m "메모" && git push
```

### 리포 최신 상태 받아오기 (다른 기기에서 수정했을 때)
```bash
git pull
```

---

## 정상 세팅 후 주간 루틴

**일요일 저녁 30~40분**
1. 터미널 열고 리포로 이동 → `claude` 실행
2. "이번 주 글 3편 써줘" 말하기
3. Claude가 3편 초안 + 이미지 프롬프트 생성
4. 각 글 `[내 경험]` 빈칸 2~3줄씩 채우기
5. `python3 scripts/generate_images.py` 3번 실행 (선택)
6. `git push` 한 번 → 3편 모두 자동 배포

주 1회만 집중해서 돌리면 돼요.

---

## 비용 요약

| 항목 | 비용 |
|---|---|
| Claude Max 구독 | 이미 결제 중 |
| GitHub Pages | **무료** |
| Google AI Studio (이미지) | **무료** (일 수십 장) |
| Anthropic API 결제 | **0원** ❌ 안 씀 |
| 추가 비용 | **0원** |

---

## (선택) 커스텀 도메인 / 애드센스

블로그 20편 이상 쌓이고 트래픽 생긴 후에 추가 세팅:
- 커스텀 도메인: `SETUP.md` 이전 버전 9번 항목 참고 (필요하면 Claude에게 요청)
- 애드센스: `_config.yml`의 `adsense` 섹션에 퍼블리셔 ID 입력

---

## 막히면 체크리스트

- **블로그 페이지가 404** → 3단계(_config.yml의 url/baseurl) 다시 확인
- **Pages 활성화 안 됨** → Settings → Pages에서 Source가 "GitHub Actions"인지
- **`claude` 명령어 없음** → `npm install -g @anthropic-ai/claude-code` 재실행
- **`git push` 막힘** → GitHub 로그인 풀렸을 수 있음. 터미널에서 `git credential-manager` 또는 Personal Access Token 설정 필요
- **이미지 생성 실패** → `.env` 파일의 키 확인, 또는 일일 quota 초과 가능
