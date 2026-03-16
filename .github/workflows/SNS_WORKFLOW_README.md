# SNS 콘텐츠 자동 생성 워크플로우

GitHub Actions를 통해 자동으로 SNS 콘텐츠를 생성하고 Issues에 등록합니다.

## 🚀 워크플로우 개요

### 1. `sns-content-generator.yml`
SNS 콘텐츠를 자동 생성하고 GitHub Issues에 등록

**실행 시간:**
- 매일 오전 9시 (KST)
- 매일 오후 2시 (KST)
- 매일 오후 7시 (KST)

**수동 실행:**
Actions 탭 → "SNS Content Generator" → "Run workflow"

### 2. `setup-sns-labels.yml`
SNS 관련 라벨 생성/업데이트 (최초 1회 실행)

## 📋 사용 방법

### 자동 실행 (스케줄)

1. **대기**: 설정된 시간에 자동 실행 (9시, 14시, 19시)
2. **확인**: [Issues 탭](../../issues?q=is%3Aissue+is%3Aopen+label%3Asns-content)에서 새 이슈 확인
3. **복사**: 각 플랫폼별 콘텐츠 복사
4. **게시**: SNS에 붙여넣기

### 수동 실행

1. [Actions 탭](../../actions/workflows/sns-content-generator.yml) 이동
2. "Run workflow" 클릭
3. (선택) 커스텀 콘텐츠 입력
4. "Run workflow" 실행

## 📊 워크플로우 상세

### 실행 단계

```
1. Checkout Repository
   ↓
2. Python 환경 설정
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
4. GitHub Issue 생성
   ├─ 제목: 📱 SNS 콘텐츠 생성 - YYYY-MM-DD HH:MM KST
   ├─ 본문: 모든 플랫폼 콘텐츠
   └─ 라벨: sns-content, auto-generated
   ↓
5. 아티팩트 업로드
   ├─ 이름: sns-content-YYYYMMDD_HHMMSS
   ├─ 보관 기간: 30일
   └─ 전체 파일 포함
   ↓
6. Issue에 아티팩트 링크 댓글
```

## 📱 생성되는 콘텐츠

### Issue 구조

```markdown
# SNS 콘텐츠 자동 생성

**생성 시간:** 2026년 03월 16일 14:00
**타임스탬프:** 20260316_140000

---

## 📋 사용 방법
1. 아래 각 섹션의 콘텐츠를 복사
2. 해당 SNS 플랫폼에서 새 게시물 작성
3. 붙여넣기 후 게시

---

[각 플랫폼별 콘텐츠]

---

## 📁 아티팩트
[다운로드 링크]
```

### 아티팩트 구조

```
sns-content-YYYYMMDD_HHMMSS.zip
├── instagram/
│   └── YYYYMMDD_HHMMSS.md
├── linkedin/
│   └── YYYYMMDD_HHMMSS.md
├── twitter/
│   └── YYYYMMDD_HHMMSS.md
├── threads/
│   └── YYYYMMDD_HHMMSS.md
├── naver_blog/
│   └── YYYYMMDD_HHMMSS.md
├── facebook/
│   └── YYYYMMDD_HHMMSS.md
└── all_platforms/
    └── YYYYMMDD_HHMMSS.txt
```

## 🏷️ 라벨

| 라벨 | 색상 | 설명 |
|------|------|------|
| `sns-content` | 🟢 녹색 | 자동 생성된 SNS 콘텐츠 |
| `auto-generated` | 🟡 노란색 | 봇이 자동으로 생성 |
| `instagram` | 🔴 분홍 | Instagram 콘텐츠 |
| `linkedin` | 🔵 파란색 | LinkedIn 콘텐츠 |
| `twitter` | 🔵 하늘색 | Twitter/X 콘텐츠 |
| `threads` | ⚫ 검은색 | Threads 콘텐츠 |
| `naver-blog` | 🟢 초록색 | 네이버 블로그 |
| `facebook` | 🔵 페이스북 파란색 | Facebook 콘텐츠 |

## ⚙️ 설정

### 스케줄 변경

`.github/workflows/sns-content-generator.yml`의 `cron` 수정:

```yaml
schedule:
  - cron: '0 0 * * *'   # 09:00 KST
  - cron: '0 5 * * *'   # 14:00 KST
  - cron: '0 10 * * *'  # 19:00 KST
```

**Cron 포맷:**
```
분(0-59) 시(0-23) 일(1-31) 월(1-12) 요일(0-6)
```

**시간대:** UTC (KST = UTC + 9시간)

**예시:**
- `0 0 * * *` → 매일 09:00 KST
- `0 */3 * * *` → 3시간마다
- `0 0 * * 1` → 매주 월요일 09:00 KST

### 아티팩트 보관 기간 변경

```yaml
- name: Upload SNS content as artifact
  uses: actions/upload-artifact@v4
  with:
    retention-days: 30  # ← 여기를 수정 (1-90일)
```

## 🔧 트러블슈팅

### Issue가 생성되지 않는 경우

1. **권한 확인**
   - Settings → Actions → General
   - "Workflow permissions" → "Read and write permissions" 선택
   - "Allow GitHub Actions to create and approve pull requests" 체크

2. **라벨 생성**
   ```bash
   # Actions 탭에서 "Setup SNS Labels" 워크플로우 수동 실행
   ```

3. **로그 확인**
   - Actions 탭 → 실패한 워크플로우 클릭
   - 각 스텝의 로그 확인

### 콘텐츠가 생성되지 않는 경우

1. **소스 파일 확인**
   ```bash
   # linkedin/ai-agents/post.md 또는 reports/*.md 파일 존재 확인
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

[Issues 탭](../../issues?q=is%3Aissue+label%3Asns-content)에서:
- 🟢 열린 콘텐츠 (게시 대기)
- ✅ 닫힌 콘텐츠 (게시 완료)

**추천 워크플로우:**
1. 콘텐츠 생성 → Issue 생성
2. SNS에 게시 → Issue 닫기
3. 주기적으로 닫힌 Issue 정리

## 🎯 베스트 프랙티스

### 1. 콘텐츠 검토
- Issue 생성 후 바로 게시하지 말고 검토
- 플랫폼별 최적화 확인
- 해시태그 및 멘션 추가

### 2. 게시 시간 조절
- 자동 생성 시간 ≠ 게시 시간
- 플랫폼별 최적 게시 시간 고려
- 주말/공휴일 조정

### 3. A/B 테스트
- 같은 콘텐츠를 다양한 버전으로 테스트
- 플랫폼별 반응 분석
- 성공한 패턴 학습

### 4. 백업
- 아티팩트는 30일 후 삭제됨
- 중요한 콘텐츠는 별도 백업
- Issue는 영구 보관 (닫기만 하면 됨)

## 🔗 관련 링크

- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Cron 표현식 도구](https://crontab.guru/)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

## 📝 변경 이력

- 2026-03-16: 초기 워크플로우 생성
  - 3회/일 자동 실행
  - Issue 자동 생성
  - 아티팩트 업로드
  - 6개 플랫폼 지원

## 💡 향후 개선 계획

- [ ] AI 기반 콘텐츠 자동 생성
- [ ] 플랫폼별 성과 분석
- [ ] 슬랙/디스코드 알림 연동
- [ ] 다국어 콘텐츠 지원
- [ ] 이미지 자동 생성 및 첨부

---

**문의:** Issues 탭에서 `question` 라벨로 질문 등록
