# SNS 자동 업로드 스크립트

환경 변수가 설정된 SNS에만 자동으로 업로드하고, 설정되지 않은 SNS는 건너뜁니다.

## 사용 방법

### Python 버전 (권장)

```bash
python scripts/post_to_social.py
```

### Bash 버전

```bash
bash scripts/post_to_social.sh
```

## 지원 플랫폼

- ✅ Instagram
- ✅ Twitter/X
- ✅ LinkedIn
- ✅ Threads
- ✅ 네이버 블로그

## 환경 변수 설정

각 플랫폼별로 필요한 환경 변수를 설정하세요. **설정하지 않은 플랫폼은 자동으로 건너뜁니다.**

### Instagram

```bash
export INSTAGRAM_ACCESS_TOKEN="your-access-token"
export INSTAGRAM_ACCOUNT_ID="your-account-id"
export INSTAGRAM_IMAGE_URL="https://example.com/image.png"
```

[Instagram 설정 가이드](../INSTAGRAM_SETUP.md) 참조

### Twitter/X

```bash
export TWITTER_API_KEY="your-api-key"
export TWITTER_API_SECRET="your-api-secret"
export TWITTER_ACCESS_TOKEN="your-access-token"
export TWITTER_ACCESS_TOKEN_SECRET="your-access-token-secret"
```

**참고**: Twitter API v2는 OAuth 1.0a 서명이 필요합니다. `tweepy` 라이브러리 사용 권장.

### LinkedIn

```bash
export LINKEDIN_ACCESS_TOKEN="your-access-token"
export LINKEDIN_PERSON_URN="urn:li:person:YOUR_ID"
```

**LinkedIn Person URN 확인 방법**:
```bash
curl -X GET \
  "https://api.linkedin.com/v2/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Threads

```bash
export THREADS_ACCESS_TOKEN="your-access-token"
export THREADS_USER_ID="your-user-id"
```

**참고**: Threads는 Instagram Graph API를 사용합니다.

### 네이버 블로그

```bash
export NAVER_CLIENT_ID="your-client-id"
export NAVER_CLIENT_SECRET="your-client-secret"
export NAVER_ACCESS_TOKEN="your-access-token"
```

**네이버 개발자 센터**: https://developers.naver.com/

## 동작 방식

1. **리포트 파일 자동 탐색**: `reports/*.md` 중 최신 파일 사용
2. **환경 변수 확인**: 각 플랫폼별로 필요한 변수 확인
3. **선택적 업로드**:
   - 환경 변수 있음 → 업로드 시도
   - 환경 변수 없음 → 경고 메시지 출력 후 건너뜀
4. **에러 허용**: 한 플랫폼 실패해도 다른 플랫폼 계속 진행
5. **항상 성공 종료**: `exit 0`으로 종료 (워크플로우 중단 방지)

## 출력 예시

```
============================================================
SNS 자동 업로드 시작
============================================================
📄 리포트 파일: reports/latest.md

📸 Instagram 업로드 확인 중...
✅ Instagram 업로드 완료

🐦 Twitter/X 업로드 확인 중...
⚠️  Twitter/X 환경 변수가 설정되지 않았습니다. 건너뜁니다.
   필요한 변수: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

💼 LinkedIn 업로드 확인 중...
⚠️  LinkedIn 환경 변수가 설정되지 않았습니다. 건너뜁니다.
   필요한 변수: LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN

🧵 Threads 업로드 확인 중...
⚠️  Threads 환경 변수가 설정되지 않았습니다. 건너뜁니다.
   필요한 변수: THREADS_ACCESS_TOKEN, THREADS_USER_ID

📝 네이버 블로그 업로드 확인 중...
⚠️  네이버 블로그 환경 변수가 설정되지 않았습니다. 건너뜁니다.
   필요한 변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, NAVER_ACCESS_TOKEN

============================================================
업로드 결과 요약
============================================================
✅ Instagram: success
⚠️ Twitter/X: skipped
⚠️ LinkedIn: skipped
⚠️ Threads: skipped
⚠️ 네이버 블로그: skipped

✅ SNS 자동 업로드 프로세스 완료
설정된 플랫폼에만 업로드되었으며, 나머지는 건너뛰었습니다.
```

## GitHub Actions 연동

`.github/workflows/post-to-social.yml` 예시:

```yaml
name: Post to Social Media

on:
  workflow_dispatch:
  push:
    paths:
      - 'reports/**/*.md'

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Post to Social Media
        env:
          # 설정하고 싶은 플랫폼만 환경 변수 추가
          INSTAGRAM_ACCESS_TOKEN: ${{ secrets.INSTAGRAM_ACCESS_TOKEN }}
          INSTAGRAM_ACCOUNT_ID: ${{ secrets.INSTAGRAM_ACCOUNT_ID }}
          INSTAGRAM_IMAGE_URL: ${{ secrets.INSTAGRAM_IMAGE_URL }}
          # LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
          # LINKEDIN_PERSON_URN: ${{ secrets.LINKEDIN_PERSON_URN }}
        run: python scripts/post_to_social.py
```

## 로컬 테스트

환경 변수를 `.env` 파일로 관리:

```bash
# .env 파일 생성
cat > .env << 'EOF'
INSTAGRAM_ACCESS_TOKEN=your-token
INSTAGRAM_ACCOUNT_ID=your-id
INSTAGRAM_IMAGE_URL=https://example.com/image.png
EOF

# 환경 변수 로드 후 실행
source .env
python scripts/post_to_social.py
```

## 주의사항

1. **API 제한**: 각 플랫폼의 API 호출 제한을 확인하세요
2. **Access Token 만료**: 정기적으로 갱신 필요
3. **이미지 URL**: Instagram, Threads는 공개 URL 필요 (로컬 파일 불가)
4. **콘텐츠 길이**: 각 플랫폼의 제한 준수
   - Instagram: 2,200자
   - Threads: 500자
   - LinkedIn: 3,000자

## 문제 해결

### 환경 변수가 설정되었는데도 건너뛰는 경우

환경 변수가 실제로 설정되었는지 확인:

```bash
echo $INSTAGRAM_ACCESS_TOKEN
```

비어있다면:
```bash
export INSTAGRAM_ACCESS_TOKEN="your-token"
```

### API 호출 실패

- Access Token 유효성 확인
- API 엔드포인트 URL 확인
- 네트워크 연결 확인
- 로그 메시지에서 상세 에러 확인

## 추가 개발

새로운 SNS 플랫폼 추가:

1. `post_to_social.py`에 새 메서드 추가
2. `post_all()` 메서드에 호출 추가
3. README에 환경 변수 문서 추가

## 라이선스

이 스크립트는 프로젝트 라이선스를 따릅니다.
