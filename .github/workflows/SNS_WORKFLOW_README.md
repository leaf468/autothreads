# AI 트렌드 & SNS 콘텐츠 자동화 워크플로우

GitHub Actions를 통해 AI 트렌드를 수집하고 SNS 콘텐츠를 자동 생성합니다.

## 🚀 워크플로우 개요

### 1. `ai-trends.yml` (통합 워크플로우) ⭐
AI 트렌드 수집 → SNS 콘텐츠 생성 → GitHub Issues 등록

**실행 시간 (하루 6번):**
- 한국시간: 09:00, 12:00, 15:00, 18:00, 21:00, 23:00
- UTC: 00:00, 03:00, 06:00, 09:00, 12:00, 14:00

**수동 실행:**
Actions 탭 → "AI Trends Reporter (KR)" → "Run workflow"

**주요 기능:**
1. AI 트렌드 뉴스 수집 (메이저 3개 + 마이너 3개)
2. 한글 리포트 생성
3. 썸네일 이미지 생성 (Gemini Imagen 3)
4. SNS 플랫폼별 콘텐츠 변환
5. GitHub Issue로 자동 등록 (2개):
   - 🤖 AI 트렌드 리포트
   - 📱 SNS 콘텐츠

### 2. `setup-sns-labels.yml`
SNS 관련 라벨 생성/업데이트 (최초 1회 실행)

## 📋 사용 방법

### 자동 실행 (권장)

1. **대기**: 하루 6번 자동 실행
2. **확인**: [Issues 탭](../../issues?q=is%3Aissue+is%3Aopen+label%3Asns-content)에서 새 이슈 확인
3. **복사**: 각 플랫폼별 콘텐츠 복사
4. **게시**: SNS에 붙여넣기

### 수동 실행

1. [Actions 탭](../../actions/workflows/ai-trends.yml) 이동
2. "Run workflow" 클릭
3. (선택) Test mode 설정
4. "Run workflow" 실행

## 📊 워크플로우 상세

### 실행 단계

```
1. AI 트렌드 수집
   ├─ DeepAgents로 AI 뉴스 수집
   ├─ 중복 체크 (이전 리포트 확인)
   ├─ 한글 번역
   └─ reports/YYYYMMDD-HHMM.md 저장
   ↓
2. 썸네일 생성
   ├─ Gemini Imagen 3 사용
   ├─ AI 트렌드 시각화
   └─ reports/images/*-thumbnail.png 저장
   ↓
3. SNS 콘텐츠 생성
   ├─ Instagram (캡션 2,200자)
   ├─ LinkedIn (150-300자)
   ├─ Twitter/X (스레드)
   ├─ Threads (500자)
   ├─ 네이버 블로그 (SEO 최적화)
   ├─ Facebook (100-250자)
   └─ 통합 텍스트 파일
   ↓
4. GitHub Issues 생성
   ├─ AI 트렌드 리포트 이슈
   │  ├─ 제목: 🤖 AI 트렌드 리포트 - YYYY-MM-DD HH:MM KST
   │  ├─ 본문: 썸네일 + 전체 리포트
   │  └─ 라벨: ai-trends, automated, YYYY-MM-DD
   └─ SNS 콘텐츠 이슈
      ├─ 제목: 📱 SNS 콘텐츠 - YYYY-MM-DD HH:MM KST
      ├─ 본문: 모든 플랫폼 콘텐츠
      └─ 라벨: sns-content, auto-generated, ai-trends
```

## 🏷️ GitHub 라벨 (왜 필요한가?)

라벨은 **자동 생성된 이슈를 쉽게 필터링하고 관리**하기 위해 사용합니다.

| 라벨 | 색상 | 설명 | 용도 |
|------|------|------|------|
| `ai-trends` | 🟢 녹색 | AI 트렌드 리포트 | 트렌드 리포트만 필터링 |
| `sns-content` | 🟢 녹색 | SNS 콘텐츠 | SNS 콘텐츠만 필터링 |
| `auto-generated` | 🟡 노란색 | 자동 생성 콘텐츠 | 봇 생성 이슈 구분 |
| `automated` | 🟡 노란색 | 자동화 프로세스 | 워크플로우로 생성됨 |
| `YYYY-MM-DD` | 🔵 파란색 | 날짜별 구분 | 특정 날짜 이슈 검색 |

**라벨 활용 예시:**
```
# SNS 콘텐츠만 보기
https://github.com/USER/REPO/issues?q=is:issue+label:sns-content

# 오늘 생성된 AI 트렌드만 보기
https://github.com/USER/REPO/issues?q=is:issue+label:ai-trends+label:2026-03-16

# 게시 대기 중인 SNS 콘텐츠
https://github.com/USER/REPO/issues?q=is:issue+is:open+label:sns-content
```

## 📱 생성되는 콘텐츠

### 1. AI 트렌드 리포트 Issue

```markdown
![AI Trends Thumbnail](https://github.com/USER/REPO/raw/main/reports/images/20260316-1200-thumbnail.png)

# AI 트렌드 리포트

## 🔥 메이저 뉴스
1. [뉴스 제목]
   - 내용...
   - 출처: URL

## 💡 마이너 뉴스
1. [뉴스 제목]
   - 내용...
   - 출처: URL
```

### 2. SNS 콘텐츠 Issue

```markdown
# SNS 콘텐츠 자동 생성

**생성 시간:** 2026년 03월 16일 12:00
**소스:** AI 트렌드 리포트

---

[각 플랫폼별 콘텐츠]

---

## 📁 파일 위치
- Instagram: `sns_output/instagram/20260316_120000.md`
- LinkedIn: `sns_output/linkedin/20260316_120000.md`
...
```

## ⚙️ 설정

### 스케줄 변경 (하루 6번)

`.github/workflows/ai-trends.yml`의 `cron` 수정:

```yaml
schedule:
  # 한국시간 09:00, 12:00, 15:00, 18:00, 21:00, 23:00
  - cron: '0 0,3,6,9,12,14 * * *'
```

**Cron 포맷:**
```
분(0-59) 시(0-23) 일(1-31) 월(1-12) 요일(0-6)
```

**시간대:** UTC (KST = UTC + 9시간)

**예시:**
- `0 0,3,6,9,12,14 * * *` → 09:00, 12:00, 15:00, 18:00, 21:00, 23:00 KST
- `0 */3 * * *` → 3시간마다
- `0 0 * * 1` → 매주 월요일 09:00 KST

## 🔧 트러블슈팅

### Issue가 생성되지 않는 경우

1. **권한 확인**
   - Settings → Actions → General
   - "Workflow permissions" → "Read and write permissions" 선택
   - "Allow GitHub Actions to create and approve pull requests" 체크

2. **라벨 생성**
   - Actions 탭 → "Setup SNS Labels" 워크플로우 수동 실행

3. **로그 확인**
   - Actions 탭 → 실패한 워크플로우 클릭
   - 각 스텝의 로그 확인

### 콘텐츠가 생성되지 않는 경우

1. **소스 파일 확인**
   ```bash
   # reports/*.md 파일 존재 확인
   ls -t reports/*.md | head -1
   ```

2. **Python 스크립트 테스트**
   ```bash
   cd examples/content-builder-agent
   python scripts/generate_all_sns_content.py
   ```

## 📊 모니터링

### GitHub Actions 대시보드

[Actions 탭](../../actions)에서:
- ✅ 성공한 실행
- ❌ 실패한 실행
- ⏱️ 실행 시간
- 📊 워크플로우 통계

### Issues 대시보드

필터링 예시:
```
# AI 트렌드만
is:issue label:ai-trends

# SNS 콘텐츠만
is:issue label:sns-content

# 오늘 생성된 것만
is:issue created:2026-03-16

# 게시 대기 중
is:issue is:open label:sns-content
```

## 🎯 베스트 프랙티스

### 1. 이슈 관리
- SNS 게시 후 → Issue 닫기
- 닫힌 Issue = 게시 완료
- 열린 Issue = 게시 대기

### 2. 콘텐츠 검토
- Issue 생성 후 바로 게시하지 말고 검토
- 플랫폼별 최적화 확인
- 해시태그 및 멘션 추가

### 3. 게시 시간 조절
- 자동 생성 시간 ≠ 게시 시간
- 플랫폼별 최적 게시 시간 고려
- 주말/공휴일 조정

## 🔗 관련 링크

- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Cron 표현식 도구](https://crontab.guru/)
- [DeepAgents GitHub](https://github.com/langchain-ai/deepagents)
- [Gemini API](https://ai.google.dev/)

## 📝 변경 이력

- 2026-03-16: 워크플로우 통합
  - AI Trends Reporter + SNS Content Generator 통합
  - 하루 6번 실행 (09:00, 12:00, 15:00, 18:00, 21:00, 23:00 KST)
  - 2개 Issue 자동 생성 (트렌드 + SNS)
  - 라벨 자동 관리

---

**문의:** Issues 탭에서 `question` 라벨로 질문 등록
