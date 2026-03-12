# Instagram 자동 업로드 설정 가이드

Instagram API를 통한 자동 업로드를 위해서는 다음 환경 변수가 필요합니다.

## 필수 환경 변수

```bash
export INSTAGRAM_ACCESS_TOKEN="your-access-token"
export INSTAGRAM_ACCOUNT_ID="your-account-id"
export INSTAGRAM_IMAGE_URL="https://example.com/image.png"
```

## 환경 변수 없이 사용하기

Instagram 환경 변수가 설정되지 않은 경우, 시스템은 자동으로 다음과 같이 동작합니다:

1. **경고 메시지 출력**: Instagram 업로드를 건너뜁니다
2. **다른 플랫폼 정상 진행**: LinkedIn, Twitter 등은 정상적으로 동작
3. **로컬 파일 저장**: Instagram 콘텐츠는 `instagram/<slug>/post.md`에 저장됨

## Instagram API Access Token 발급 방법

### 1. Meta Developer 계정 생성
1. [Meta for Developers](https://developers.facebook.com/) 접속
2. 계정 생성 또는 로그인

### 2. 앱 생성
1. "My Apps" → "Create App" 클릭
2. Use Case: "Business" 선택
3. App Type: "Business" 선택
4. 앱 이름 입력

### 3. Instagram Basic Display 또는 Instagram Graph API 설정
- **개인 계정**: Instagram Basic Display API
- **비즈니스 계정**: Instagram Graph API (권장)

### 4. Access Token 발급
1. Dashboard → Tools → Graph API Explorer
2. User Token 생성
3. 필요한 권한 선택:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`

### 5. Instagram Account ID 확인
```bash
curl -X GET \
  "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_ACCESS_TOKEN"
```

## 선택적 사용

Instagram 업로드가 필수가 아닌 경우:
- 환경 변수를 설정하지 않아도 됩니다
- 콘텐츠는 로컬에 저장되며, 수동으로 Instagram에 업로드할 수 있습니다

## 로컬 파일 확인

Instagram 콘텐츠는 다음 위치에 저장됩니다:

```
instagram/
└── <slug>/
    ├── post.md      # 캡션 및 콘텐츠
    └── image.png    # 생성된 이미지 (선택사항)
```

## 문제 해결

### Q: "필수 환경 변수가 설정되지 않았습니다" 에러
**A**: 이것은 경고 메시지입니다. Instagram 업로드를 건너뛰고 다른 플랫폼은 정상 진행됩니다.

### Q: Access Token이 만료되었습니다
**A**: Meta Developer Console에서 새로운 토큰을 발급받으세요. Long-lived Token (60일)을 사용하면 더 편리합니다.

### Q: 이미지 URL이 필요한가요?
**A**: Instagram API는 공개 URL의 이미지만 업로드 가능합니다. 로컬 이미지는 먼저 CDN이나 공개 서버에 업로드해야 합니다.

## 대안: 수동 업로드

환경 변수 없이 사용하는 경우:

1. 콘텐츠 생성: `instagram/<slug>/post.md` 확인
2. 이미지 확인: `instagram/<slug>/image.png` 다운로드
3. Instagram 앱에서 수동 업로드
4. 저장된 캡션 복사하여 붙여넣기

이 방법이 개인 사용자에게는 더 간편할 수 있습니다!
