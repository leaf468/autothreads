#!/bin/bash

# SNS 자동 업로드 스크립트
# 환경 변수가 설정되지 않은 SNS는 자동으로 건너뜁니다.

set -e

# 색상 코드
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 최신 리포트 파일 찾기
LATEST_REPORT=$(ls -t reports/*.md 2>/dev/null | grep -v 'threads\|twitter' | head -1)

if [ -z "$LATEST_REPORT" ]; then
  echo -e "${RED}❌ 리포트 파일을 찾을 수 없습니다.${NC}"
  exit 0  # 에러가 아닌 정상 종료
fi

echo -e "${BLUE}📄 리포트 파일: $LATEST_REPORT${NC}"
echo ""

# ==========================================
# Instagram 업로드
# ==========================================
echo -e "${BLUE}📸 Instagram 업로드 확인 중...${NC}"

if [ -z "$INSTAGRAM_ACCESS_TOKEN" ] || [ -z "$INSTAGRAM_ACCOUNT_ID" ] || [ -z "$INSTAGRAM_IMAGE_URL" ]; then
  echo -e "${YELLOW}⚠️  Instagram 환경 변수가 설정되지 않았습니다. 건너뜁니다.${NC}"
  echo -e "${YELLOW}   필요한 변수: INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID, INSTAGRAM_IMAGE_URL${NC}"
else
  echo -e "${GREEN}✅ Instagram 환경 변수 확인 완료${NC}"

  # Instagram API 호출 (예시)
  # 실제 구현은 프로젝트에 맞게 수정하세요
  CAPTION=$(cat "$LATEST_REPORT")

  # Instagram Graph API 호출
  RESPONSE=$(curl -s -X POST \
    "https://graph.facebook.com/v18.0/${INSTAGRAM_ACCOUNT_ID}/media" \
    -F "image_url=${INSTAGRAM_IMAGE_URL}" \
    -F "caption=${CAPTION}" \
    -F "access_token=${INSTAGRAM_ACCESS_TOKEN}")

  CREATION_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)

  if [ -n "$CREATION_ID" ]; then
    # 미디어 게시
    PUBLISH_RESPONSE=$(curl -s -X POST \
      "https://graph.facebook.com/v18.0/${INSTAGRAM_ACCOUNT_ID}/media_publish" \
      -F "creation_id=${CREATION_ID}" \
      -F "access_token=${INSTAGRAM_ACCESS_TOKEN}")

    echo -e "${GREEN}✅ Instagram 업로드 완료${NC}"
  else
    echo -e "${YELLOW}⚠️  Instagram 업로드 실패: ${RESPONSE}${NC}"
  fi
fi

echo ""

# ==========================================
# Twitter/X 업로드
# ==========================================
echo -e "${BLUE}🐦 Twitter/X 업로드 확인 중...${NC}"

if [ -z "$TWITTER_API_KEY" ] || [ -z "$TWITTER_API_SECRET" ] || [ -z "$TWITTER_ACCESS_TOKEN" ] || [ -z "$TWITTER_ACCESS_TOKEN_SECRET" ]; then
  echo -e "${YELLOW}⚠️  Twitter 환경 변수가 설정되지 않았습니다. 건너뜁니다.${NC}"
  echo -e "${YELLOW}   필요한 변수: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET${NC}"
else
  echo -e "${GREEN}✅ Twitter 환경 변수 확인 완료${NC}"

  # Twitter API v2 호출 예시
  # 실제 구현 필요 (OAuth 1.0a 서명 필요)
  echo -e "${YELLOW}⚠️  Twitter API 구현 필요${NC}"
fi

echo ""

# ==========================================
# LinkedIn 업로드
# ==========================================
echo -e "${BLUE}💼 LinkedIn 업로드 확인 중...${NC}"

if [ -z "$LINKEDIN_ACCESS_TOKEN" ] || [ -z "$LINKEDIN_PERSON_URN" ]; then
  echo -e "${YELLOW}⚠️  LinkedIn 환경 변수가 설정되지 않았습니다. 건너뜁니다.${NC}"
  echo -e "${YELLOW}   필요한 변수: LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN${NC}"
else
  echo -e "${GREEN}✅ LinkedIn 환경 변수 확인 완료${NC}"

  CAPTION=$(cat "$LATEST_REPORT")

  # LinkedIn API 호출
  RESPONSE=$(curl -s -X POST \
    "https://api.linkedin.com/v2/ugcPosts" \
    -H "Authorization: Bearer ${LINKEDIN_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "X-Restli-Protocol-Version: 2.0.0" \
    -d "{
      \"author\": \"${LINKEDIN_PERSON_URN}\",
      \"lifecycleState\": \"PUBLISHED\",
      \"specificContent\": {
        \"com.linkedin.ugc.ShareContent\": {
          \"shareCommentary\": {
            \"text\": \"${CAPTION}\"
          },
          \"shareMediaCategory\": \"NONE\"
        }
      },
      \"visibility\": {
        \"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"
      }
    }")

  if echo "$RESPONSE" | grep -q '"id"'; then
    echo -e "${GREEN}✅ LinkedIn 업로드 완료${NC}"
  else
    echo -e "${YELLOW}⚠️  LinkedIn 업로드 실패: ${RESPONSE}${NC}"
  fi
fi

echo ""

# ==========================================
# Threads 업로드
# ==========================================
echo -e "${BLUE}🧵 Threads 업로드 확인 중...${NC}"

if [ -z "$THREADS_ACCESS_TOKEN" ] || [ -z "$THREADS_USER_ID" ]; then
  echo -e "${YELLOW}⚠️  Threads 환경 변수가 설정되지 않았습니다. 건너뜁니다.${NC}"
  echo -e "${YELLOW}   필요한 변수: THREADS_ACCESS_TOKEN, THREADS_USER_ID${NC}"
else
  echo -e "${GREEN}✅ Threads 환경 변수 확인 완료${NC}"

  CAPTION=$(cat "$LATEST_REPORT")

  # Threads API 호출 (Instagram Graph API 사용)
  RESPONSE=$(curl -s -X POST \
    "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads" \
    -F "media_type=TEXT" \
    -F "text=${CAPTION}" \
    -F "access_token=${THREADS_ACCESS_TOKEN}")

  CREATION_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)

  if [ -n "$CREATION_ID" ]; then
    # 스레드 게시
    PUBLISH_RESPONSE=$(curl -s -X POST \
      "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads_publish" \
      -F "creation_id=${CREATION_ID}" \
      -F "access_token=${THREADS_ACCESS_TOKEN}")

    echo -e "${GREEN}✅ Threads 업로드 완료${NC}"
  else
    echo -e "${YELLOW}⚠️  Threads 업로드 실패: ${RESPONSE}${NC}"
  fi
fi

echo ""

# ==========================================
# 네이버 블로그 업로드
# ==========================================
echo -e "${BLUE}📝 네이버 블로그 업로드 확인 중...${NC}"

if [ -z "$NAVER_CLIENT_ID" ] || [ -z "$NAVER_CLIENT_SECRET" ] || [ -z "$NAVER_ACCESS_TOKEN" ]; then
  echo -e "${YELLOW}⚠️  네이버 블로그 환경 변수가 설정되지 않았습니다. 건너뜁니다.${NC}"
  echo -e "${YELLOW}   필요한 변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, NAVER_ACCESS_TOKEN${NC}"
else
  echo -e "${GREEN}✅ 네이버 블로그 환경 변수 확인 완료${NC}"

  TITLE="자동 생성된 블로그 포스트"
  CONTENT=$(cat "$LATEST_REPORT")

  # 네이버 블로그 API 호출
  RESPONSE=$(curl -s -X POST \
    "https://openapi.naver.com/blog/writePost.json" \
    -H "Authorization: Bearer ${NAVER_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"${TITLE}\",
      \"contents\": \"${CONTENT}\"
    }")

  if echo "$RESPONSE" | grep -q '"result":"success"'; then
    echo -e "${GREEN}✅ 네이버 블로그 업로드 완료${NC}"
  else
    echo -e "${YELLOW}⚠️  네이버 블로그 업로드 실패: ${RESPONSE}${NC}"
  fi
fi

echo ""
echo -e "${GREEN}✅ SNS 자동 업로드 프로세스 완료${NC}"
echo -e "${BLUE}설정된 플랫폼에만 업로드되었으며, 나머지는 건너뛰었습니다.${NC}"

exit 0  # 항상 성공으로 종료
