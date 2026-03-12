# 🤖 AI 트렌드 리포터 (한국어)

자동으로 AI/ML 트렌드를 수집하고 한글 보고서를 생성하는 GitHub Actions 기반 서비스

[![AI Trends](https://img.shields.io/badge/AI-Trends-blue?style=for-the-badge)](../../issues?q=label%3Aai-trends)
[![Powered by DeepAgents](https://img.shields.io/badge/Powered%20by-DeepAgents-purple?style=for-the-badge)](https://github.com/langchain-ai/deepagents)
[![Gemini Imagen 3](https://img.shields.io/badge/Images-Gemini%20Imagen%203-green?style=for-the-badge)](https://ai.google.dev/)

## ⏰ 발행 시간

하루 6회 자동 발행 (한국시간 기준):

| 시간 | 이모지 | 타겟 독자 |
|------|--------|-----------|
| 09:00 | 🌅 | 출근길 |
| 12:00 | 🌞 | 점심시간 |
| 15:00 | ☀️ | 오후 휴식 |
| 18:00 | 🌆 | 퇴근길 |
| 21:00 | 🌃 | 저녁 시간 |
| 23:00 | 🌙 | 취침 전 |

## 🎯 특징

- ✅ **자동 수집**: 메이저 + 마이너 AI 뉴스 균형있게
- ✅ **한글 번역**: 외국 기사를 자연스러운 한글로
- ✅ **AI 썸네일**: Gemini Imagen 3로 자동 생성 (초저비용)
- ✅ **SNS 포맷**: Threads & X(Twitter) 스타일 자동 변환
- ✅ **출처 명시**: 모든 정보에 원문 링크 포함
- ✅ **중복 방지**: 이전 보고서 자동 체크
- ✅ **무료 호스팅**: GitHub Actions (public repo)
- ✅ **재미있게**: 딱딱한 번역 대신 읽기 쉬운 글

## 📰 콘텐츠 소스

### 메이저 소스
- 🔥 Hacker News
- 📱 Reddit (r/MachineLearning, r/artificial)
- 📄 ArXiv (최신 논문)
- 📰 TechCrunch AI

### 마이너 소스
- 💻 GitHub Trending
- 🤗 Hugging Face (새 모델)
- 🚀 ProductHunt AI
- 📝 개인 연구 블로그
- 🐦 AI 인플루언서

## 💰 월 비용

```
실행: 6회/일 × 30일 = 180회

1. Claude API (콘텐츠 생성)
   - 입력: 360K tokens × $3/M = $1.08
   - 출력: 540K tokens × $15/M = $8.10
   - 소계: $9.18

2. Gemini Imagen 3 (이미지 생성)
   - 180개 × $0.0033 = $0.60
   - (DALL-E 대비 12배 저렴!)

3. Tavily Search (웹 검색)
   - 900회 < 1000회/월
   - 무료 ✅

총 월 비용: 약 $10
```

## 🚀 설치 방법

### 1. 레포지토리 준비

```bash
# Fork this repository
# 또는 새 레포지토리 생성 후 파일 복사

git clone https://github.com/YOUR_USERNAME/ai-trends-kr
cd ai-trends-kr
```

### 2. API 키 발급

#### Anthropic (Claude)
1. https://console.anthropic.com/ 접속
2. API Keys → Create Key
3. `ANTHROPIC_API_KEY` 복사

#### Google (Gemini Imagen 3)
1. https://ai.google.dev/ 접속
2. Get API Key 클릭
3. `GOOGLE_API_KEY` 복사

#### Tavily (Search)
1. https://tavily.com/ 접속
2. 무료 가입 (1000회/월)
3. `TAVILY_API_KEY` 복사

### 3. GitHub Secrets 설정

1. GitHub Repository → **Settings**
2. **Secrets and variables** → **Actions**
3. **New repository secret** 클릭
4. 다음 3개 추가:

```
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-xxxxx

Name: GOOGLE_API_KEY
Value: AIzaSyxxxxx

Name: TAVILY_API_KEY
Value: tvly-xxxxx
```

### 4. GitHub Actions 활성화

1. **Actions** 탭 클릭
2. "I understand my workflows, go ahead and enable them" 클릭

### 5. 첫 실행 (테스트)

1. **Actions** 탭
2. **AI Trends Reporter (KR)** 선택
3. **Run workflow** 클릭
4. `test_mode: false` 선택
5. **Run workflow** 버튼 클릭

⏱️ 약 3-5분 후 완료됩니다!

## 📖 보고서 보기

### GitHub Issues (메인)
- [모든 AI 트렌드 보기](../../issues?q=label%3Aai-trends)
- 각 시간대별로 새 Issue 생성됨
- 댓글 기능 활용 가능

### Markdown 파일
- [`reports/`](./reports/) 폴더에서 전체 보고서 확인
- 파일명: `YYYYMMDD-HHMM.md`

### SNS 포맷 파일
- **Threads 버전**: `reports/YYYYMMDD-HHMM-threads.txt`
  - 캐주얼한 톤, 짧은 문단, 이모지 활용
  - Meta Threads에 바로 복붙 가능
- **X(Twitter) 버전**: `reports/YYYYMMDD-HHMM-twitter.txt`
  - 280자 제한 준수, 스레드 형식
  - 트윗 번호 포함, 해시태그 최적화

### 썸네일 이미지
- [`reports/images/`](./reports/images/) 폴더
- Gemini Imagen 3로 생성된 고품질 이미지

## 📱 SNS 포맷 변환

매 리포트마다 자동으로 소셜 미디어 친화적인 버전을 생성합니다.

### Threads 스타일 특징
- ✍️ 캐주얼하고 친근한 어투 ("~요", "~네요")
- 📝 짧은 문단 (3-5문장)
- ✨ 적절한 이모지 활용
- 🔗 링크는 "댓글 참고" 안내
- 📏 가독성 최적화

### X(Twitter) 스타일 특징
- 🐦 280자 제한 엄격 준수
- 🧵 스레드 형식 (번호 표시)
- #️⃣ 해시태그 최적화
- 💡 핵심 포인트만 압축
- 🔗 마지막 트윗에만 링크

### 수동 변환

기존 마크다운 리포트를 SNS 포맷으로 변환하려면:

```bash
python scripts/format_to_sns.py reports/20260311-1246.md
```

출력:
- `reports/20260311-1246-threads.txt`
- `reports/20260311-1246-twitter.txt`

### 사용 예시

**Threads에 포스팅**
1. `reports/YYYYMMDD-HHMM-threads.txt` 열기
2. 전체 복사 (Cmd/Ctrl + A)
3. Threads 앱에 붙여넣기
4. 세로형 이미지 첨부 (선택)
5. 게시!

**X(Twitter)에 스레드 작성**
1. `reports/YYYYMMDD-HHMM-twitter.txt` 열기
2. `---` 구분선으로 각 트윗 분리
3. 첫 트윗부터 순서대로 작성
4. "Reply" 버튼으로 스레드 연결
5. 마지막 트윗에 리포지토리 링크

## 📤 SNS 자동 업로드 (선택사항)

리포트를 Instagram, X(Twitter), Threads에 자동으로 업로드할 수 있습니다.

### 지원 플랫폼

| 플랫폼 | 기능 | 사용 API |
|--------|------|----------|
| 📸 **Instagram** | 이미지 + 캡션 | Instagram Graph API |
| 🐦 **X(Twitter)** | 스레드 게시 | X API v2 |
| 🧵 **Threads** | 텍스트 게시 | Threads API |

### Instagram 설정

1. **Instagram Business 계정 필요**
   - Instagram을 Facebook 페이지에 연결
   - Business 계정으로 전환

2. **Facebook 개발자 앱 생성**
   - [Meta for Developers](https://developers.facebook.com/) 접속
   - 새 앱 생성 → Instagram Graph API 추가

3. **액세스 토큰 발급**
   - Graph API Explorer에서 토큰 생성
   - 권한: `instagram_basic`, `instagram_content_publish`

4. **GitHub Secrets 추가**
   ```
   INSTAGRAM_ACCESS_TOKEN=your_access_token
   INSTAGRAM_ACCOUNT_ID=your_instagram_business_id
   ```

### X(Twitter) 설정

1. **X Developer Account 필요**
   - [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) 접속
   - 무료 플랜으로 시작 가능

2. **App 생성 및 Bearer Token 발급**
   - Standalone App 생성
   - Authentication Settings에서 Bearer Token 복사
   - Read and Write 권한 설정

3. **GitHub Secrets 추가**
   ```
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

### Threads 설정

1. **Threads API 액세스 신청**
   - [Meta for Developers](https://developers.facebook.com/docs/threads) 접속
   - Threads API 사용 신청

2. **액세스 토큰 및 사용자 ID 발급**
   - Facebook 앱에서 Threads API 추가
   - 토큰 및 User ID 발급

3. **GitHub Secrets 추가**
   ```
   THREADS_ACCESS_TOKEN=your_access_token
   THREADS_USER_ID=your_threads_user_id
   ```

### 자동 업로드 활성화

GitHub Secrets에 API 키를 추가하면 자동으로 활성화됩니다.
- Secret이 없으면 해당 플랫폼은 건너뜀
- 에러 발생 시 워크플로우는 계속 진행

### 수동 업로드 (테스트용)

```bash
# Instagram
python scripts/post_to_instagram.py reports/20260311-1246.md

# X(Twitter)
python scripts/post_to_twitter.py reports/20260311-1246-twitter.txt

# Threads
python scripts/post_to_threads.py reports/20260311-1246-threads.txt
```

## 🔧 커스터마이징

### 발행 시간 변경

[`.github/workflows/ai-trends.yml`](.github/workflows/ai-trends.yml#L5-L8) 수정:

```yaml
schedule:
  # 한국시간 기준으로 원하는 시간 설정
  # 예: 08:00, 20:00만 = UTC 23:00, 11:00
  - cron: '0 23,11 * * *'
```

💡 Cron 표현식 도움: https://crontab.guru

### 모델 변경

```yaml
model: claude-sonnet-4-6  # 또는
model: gpt-4o             # 또는
model: gemini-2.0-flash
```

### 프롬프트 커스터마이징

[`.github/workflows/ai-trends.yml`](.github/workflows/ai-trends.yml#L45-L150)에서 프롬프트 수정 가능

## 🔄 자동화 플로우

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions (하루 6회 자동 실행)                          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│  1. AI 트렌드 수집 (DeepAgents)                              │
│     - 메이저/마이너 뉴스 검색                                 │
│     - 한글 번역 및 리포트 생성                                │
│     → reports/YYYYMMDD-HHMM.md                              │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│  2. AI 썸네일 생성 (Gemini Imagen 3)                         │
│     - 프롬프트 기반 이미지 생성                               │
│     → reports/images/YYYYMMDD-HHMM-thumbnail.png            │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│  3. SNS 포맷 변환                                            │
│     - Threads 스타일: YYYYMMDD-HHMM-threads.txt             │
│     - Twitter 스타일: YYYYMMDD-HHMM-twitter.txt             │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Instagram 이미지 생성                                     │
│     - 썸네일에 "오늘의 한마디" 텍스트 오버레이                │
│     → reports/images/YYYYMMDD-HHMM-instagram.png            │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌──────────────┬──────────────┬──────────────┬────────────────┐
│  📸 Instagram │  🐦 X(Twitter)│  🧵 Threads  │  📝 GitHub     │
│              │              │              │                │
│  이미지 +     │  스레드      │  텍스트      │  Issue 생성    │
│  캡션 자동    │  자동 게시   │  자동 게시   │                │
│  업로드       │              │              │                │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

## 📊 프로젝트 구조

```
ai-trends-kr/
├── .deepagents/
│   └── skills/
│       ├── ai-trends-reporter/     # AI 트렌드 수집 스킬
│       │   └── SKILL.md
│       └── sns-formatter/          # SNS 포맷 변환 스킬
│           └── SKILL.md
├── .github/
│   └── workflows/
│       └── ai-trends.yml           # GitHub Actions 워크플로우
├── scripts/
│   ├── generate_thumbnail.py       # Gemini Imagen 3 이미지 생성
│   └── format_to_sns.py            # SNS 포맷 변환 스크립트
├── reports/
│   ├── images/
│   │   ├── 20260310-0900-thumbnail.png
│   │   └── 20260310-0900-metadata.txt
│   ├── 20260310-0900.md            # 마크다운 보고서
│   ├── 20260310-0900-threads.txt   # Threads 버전
│   └── 20260310-0900-twitter.txt   # X(Twitter) 버전
├── .env.example                    # 환경 변수 예시
├── .gitignore
└── README.md
```

## 🐛 문제 해결

### Workflow가 실행되지 않아요
- **Actions** 탭에서 workflow가 활성화되어 있는지 확인
- Repository가 **Public**인지 확인 (Private은 유료)
- Secrets가 올바르게 설정되었는지 확인

### 이미지 생성이 실패해요
- `GOOGLE_API_KEY`가 올바른지 확인
- Google AI Studio에서 API 할당량 확인
- Gemini API가 활성화되어 있는지 확인

### 같은 기사가 반복돼요
- `enable_memory: true` 설정 확인
- `reports/` 폴더에 이전 보고서가 있는지 확인

### 비용이 너무 많이 나와요
- Workflow 실행 횟수 줄이기 (cron 수정)
- `timeout` 값 줄이기 (기본 30분)
- Test mode 활용 (이미지 생성 스킵)

## 🤝 기여하기

이슈나 PR은 언제나 환영입니다!

## 📝 라이선스

MIT License

## 🙏 Credits

- **[DeepAgents](https://github.com/langchain-ai/deepagents)** - AI Agent Framework
- **[Claude (Anthropic)](https://anthropic.com/)** - Content Generation
- **[Gemini Imagen 3 (Google)](https://ai.google.dev/)** - Image Generation
- **[Tavily](https://tavily.com/)** - Web Search API

---

**Made with ❤️ and AI**

궁금한 점이 있으시면 [Issue](../../issues/new)를 열어주세요!
