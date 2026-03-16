# SNS 콘텐츠 생성 스크립트

## 📋 개요

**`generate_all_sns_content.py`** - API 연결 없이 모든 SNS용 콘텐츠를 로컬 파일로 생성

환경 변수 설정이나 API 토큰 없이도 바로 사용 가능합니다.
생성된 파일을 복사하여 각 SNS에 직접 붙여넣으면 됩니다.

## 빠른 시작

### 모든 SNS 콘텐츠를 한 번에 생성

```bash
cd examples/content-builder-agent
python scripts/generate_all_sns_content.py
```

**결과물:**
```
sns_output/
├── instagram/20260316_115717.md     (이미지 경로 포함)
├── twitter/20260316_115717.md       (스레드 형식)
├── threads/20260316_115717.md       (전문 기술 정리)
└── all_platforms/20260316_115717.txt  ← 모든 플랫폼 통합본
```

**사용 방법:**
1. 각 파일 열기
2. 내용 복사 (Cmd+A → Cmd+C / Ctrl+A → Ctrl+C)
3. 해당 SNS에서 새 게시물 만들기
4. 붙여넣기 (Cmd+V / Ctrl+V)
5. 게시!

## 지원 플랫폼

- ✅ Instagram (이미지 자동 연결)
- ✅ Twitter/X (스레드 형식)
- ✅ Threads (전문 기술 정리 스타일)

## 동작 방식

1. **리포트 파일 자동 탐색**: `reports/*.md` 또는 `linkedin/*/post.md` 중 최신 파일 사용
2. **이미지 자동 탐색**: Instagram용 이미지 파일 찾기
   - `reports/images/*-instagram.png` (텍스트 오버레이 포함) 우선
   - 없으면 `reports/images/*-thumbnail.png` (기본 썸네일) 사용
3. **콘텐츠 생성**: 각 플랫폼별 최적화된 형식으로 변환
4. **로컬 저장**: `sns_output/` 디렉토리에 날짜/시간 기반 파일명으로 저장
5. **통합 파일**: 모든 플랫폼 콘텐츠를 하나의 텍스트 파일로도 제공

## 출력 예시

```
📄 소스 파일: ../../reports/20260312-0912.md
🖼️  Instagram 이미지: ../../reports/images/20260312-0912-thumbnail.png
============================================================
SNS 콘텐츠 생성 시작
============================================================

📸 Instagram 콘텐츠 생성 중...
✅ instagram: sns_output/instagram/20260316_154714.md

🐦 Twitter/X 콘텐츠 생성 중...
✅ twitter: sns_output/twitter/20260316_154714.md

🧵 Threads 콘텐츠 생성 중...
✅ threads: sns_output/threads/20260316_154714.md

📋 통합 텍스트 파일 생성 중...
✅ all_platforms: sns_output/all_platforms/20260316_154714.txt

✅ 모든 SNS 콘텐츠 생성 완료!
📋 각 파일을 열어서 복사하여 해당 SNS에 붙여넣으세요.
```

## 커스텀 콘텐츠 생성

명령줄 인자로 직접 콘텐츠 제공 가능:

```bash
python scripts/generate_all_sns_content.py "오늘 학습한 AI 에이전트 내용을 공유합니다."
```

## GitHub 이슈 자동 생성

생성된 SNS 콘텐츠를 GitHub 이슈로 자동 등록:

```bash
# 기본 사용 + 이슈 생성
python scripts/generate_all_sns_content.py --issue

# 또는 짧은 옵션
python scripts/generate_all_sns_content.py -i

# 커스텀 콘텐츠 + 이슈 생성
python scripts/generate_all_sns_content.py --issue "오늘 학습한 내용"
```

**요구사항:**
- [GitHub CLI (gh)](https://cli.github.com/) 설치 필요
- GitHub 인증 완료 필요 (`gh auth login`)

**이슈 내용:**
- 생성된 모든 파일 경로
- 각 플랫폼별 파일 링크
- 사용 방법 가이드
- `sns-content` 라벨 자동 추가

## 플랫폼별 최적화

각 플랫폼에 맞게 자동 최적화:

- **Instagram**:
  - 📸 이미지 자동 연결 (reports/images/*-instagram.png)
  - 캡션과 이미지 파일 경로 포함
  - 작성 가이드: 전문 기술 정리 스타일 (📌💡🔍 이모지 활용)

- **Twitter/X**:
  - 280자 스레드 형식
  - 전문 기술 스레드 스타일
  - 각 트윗에 하나의 개념/포인트

- **Threads**:
  - 전문 기술 정리 스타일
  - 구조화된 포맷 (이모지 사용)
  - 참고: @choi.openai, @unclejobs.ai 등의 스타일

## 문제 해결

### 리포트 파일을 찾을 수 없는 경우

다음 위치에 마크다운 파일이 있는지 확인:
- `reports/*.md`
- `linkedin/*/post.md`

샘플 콘텐츠로 테스트:
```bash
python scripts/generate_all_sns_content.py "테스트 콘텐츠입니다."
```

## 추가 기능

새로운 SNS 플랫폼 추가:

1. `generate_all_sns_content.py`의 `SNSContentGenerator` 클래스에 새 메서드 추가
2. `generate_all()` 메서드에 호출 추가
3. README에 플랫폼 문서 추가

## 라이선스

이 스크립트는 프로젝트 라이선스를 따릅니다.
