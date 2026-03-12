# X (Twitter) API 연결 가이드

X (Twitter) API를 연결하여 자동 트윗 쓰레드를 게시할 수 있습니다.

## 1단계: X Developer Portal 계정 생성

1. [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)에 접속
2. 로그인 (본인의 X 계정 사용)
3. "Sign up for Free Account" 클릭
4. 간단한 설문 작성:
   - "What's your name?" → 본인 이름
   - "What country do you live in?" → South Korea
   - "What's your use case?" → "Making a bot" 선택
   - "Will you make Twitter content available to government entities?" → No

## 2단계: 앱 생성

1. Dashboard에서 "Projects & Apps" 클릭
2. "+ Create App" 버튼 클릭
3. App 이름 입력 (예: `ai-trends-kr-bot`)
4. API Keys가 표시됨 → **지금은 저장 안 해도 됨** (Bearer Token만 필요)

## 3단계: App 권한 설정

1. 생성된 App 클릭
2. "Settings" 탭으로 이동
3. "User authentication settings" 섹션에서 "Set up" 클릭
4. App permissions 설정:
   - ✅ **Read and write** 선택 (트윗 작성 권한)
5. Type of App:
   - **Automated App or bot** 선택
6. App info 입력:
   - Callback URI: `http://localhost:3000` (필수이지만 우리는 사용 안 함)
   - Website URL: GitHub 레포 URL 입력 (`https://github.com/필립아이디/ai-trends-kr`)
7. "Save" 클릭

## 4단계: Bearer Token 생성

1. App 페이지의 "Keys and tokens" 탭으로 이동
2. "Bearer Token" 섹션에서 "Generate" 클릭
3. 생성된 Bearer Token 복사 (예: `AAAAAAAAAAAAAAAAAAAAAxxxx...`)
   - ⚠️ **한 번만 표시되므로 반드시 복사하세요!**
   - 잃어버리면 "Regenerate" 해야 함

## 5단계: GitHub Secrets에 추가

1. GitHub 레포 페이지로 이동
2. "Settings" → "Secrets and variables" → "Actions" 클릭
3. "New repository secret" 클릭
4. Secret 추가:
   - Name: `TWITTER_BEARER_TOKEN`
   - Value: 복사한 Bearer Token (AAAAAAAAAAAAAAAAAAAAAxxxx...)
5. "Add secret" 클릭

## ✅ 완료!

이제 GitHub Actions 워크플로우가 자동으로 X에 트윗 쓰레드를 게시할 수 있습니다.

### 테스트 방법

로컬에서 테스트하려면:

```bash
# .env 파일에 토큰 추가
echo 'TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxx...' >> .env

# SNS 포맷 생성 (최신 리포트 기준)
cd scripts
python format_to_sns.py

# X에 트윗 쓰레드 게시
python post_to_twitter.py
```

### 문제 해결

**403 Forbidden 에러가 나는 경우:**
- App 권한이 "Read and write"로 설정되어 있는지 확인
- Bearer Token을 재생성해보세요 (권한 변경 후에는 새 토큰 필요)

**401 Unauthorized 에러가 나는 경우:**
- Bearer Token이 정확히 복사되었는지 확인
- 토큰 앞뒤에 공백이 없는지 확인

**트윗이 280자를 초과하는 경우:**
- `format_to_sns.py`가 자동으로 280자 이하로 분할합니다
- 각 트윗이 자동으로 쓰레드로 연결됩니다
