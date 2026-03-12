#!/usr/bin/env python3
"""
X(Twitter) 자동 스레드 게시 스크립트
X API v2를 사용하여 스레드를 자동으로 게시합니다.
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional


class TwitterPoster:
    """X API v2를 사용한 스레드 게시 클래스"""

    def __init__(self, bearer_token: str):
        """
        Args:
            bearer_token: X API Bearer Token
        """
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

    def post_tweet(self, text: str, reply_to_tweet_id: Optional[str] = None) -> Dict:
        """
        단일 트윗 게시

        Args:
            text: 트윗 텍스트 (최대 280자)
            reply_to_tweet_id: 답글로 달 트윗 ID (스레드용)

        Returns:
            응답 데이터 (tweet_id 포함)
        """
        url = f"{self.base_url}/tweets"

        payload = {"text": text}

        # 스레드 연결: reply 설정
        if reply_to_tweet_id:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to_tweet_id}

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            result = response.json()
            tweet_id = result['data']['id']
            return {"success": True, "tweet_id": tweet_id, "data": result}
        else:
            print(f"❌ 트윗 게시 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return {"success": False, "error": response.text}

    def post_thread(self, tweets: List[str], delay: float = 2.0) -> List[str]:
        """
        스레드 게시 (여러 트윗을 체인으로 연결)

        Args:
            tweets: 트윗 텍스트 리스트
            delay: 각 트윗 사이 지연 시간 (초)

        Returns:
            게시된 트윗 ID 리스트
        """
        tweet_ids = []
        previous_tweet_id = None

        for i, tweet_text in enumerate(tweets, 1):
            print(f"\n🐦 트윗 {i}/{len(tweets)} 게시 중...")
            print(f"   {tweet_text[:50]}...")

            result = self.post_tweet(tweet_text, reply_to_tweet_id=previous_tweet_id)

            if result['success']:
                tweet_id = result['tweet_id']
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id
                print(f"✅ 성공! Tweet ID: {tweet_id}")

                # 다음 트윗 전 대기
                if i < len(tweets):
                    print(f"⏳ {delay}초 대기...")
                    time.sleep(delay)
            else:
                print(f"❌ 실패: {result['error']}")
                print(f"⚠️  스레드 게시 중단 (성공: {i-1}/{len(tweets)})")
                break

        return tweet_ids


def parse_twitter_thread_file(file_path: str) -> List[str]:
    """
    Twitter 스레드 텍스트 파일 파싱

    Args:
        file_path: *-twitter.txt 파일 경로

    Returns:
        트윗 텍스트 리스트
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # "---"로 구분된 각 트윗 추출
    tweets = [tweet.strip() for tweet in content.split('\n---\n') if tweet.strip()]

    # 각 트윗에서 "[트윗 X/Y]" 제거 (선택사항)
    # 실제로는 포함하는 게 좋을 수도 있음
    # cleaned_tweets = []
    # for tweet in tweets:
    #     # [트윗 1/10] 같은 부분 제거
    #     cleaned = re.sub(r'^\[트윗 \d+/\d+\]\n', '', tweet)
    #     cleaned_tweets.append(cleaned)

    return tweets


def main():
    """메인 실행 함수"""
    # 환경 변수에서 인증 정보 가져오기
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not bearer_token:
        print("❌ 필수 환경 변수가 설정되지 않았습니다:")
        print("   - TWITTER_BEARER_TOKEN")
        print("\n💡 X Developer Portal에서 Bearer Token을 발급받으세요:")
        print("   https://developer.twitter.com/en/portal/dashboard")
        sys.exit(1)

    # Twitter 스레드 파일 경로
    if len(sys.argv) > 1:
        twitter_file = sys.argv[1]
    else:
        # 최신 twitter.txt 파일 찾기
        reports_dir = Path(__file__).parent.parent / 'reports'
        twitter_files = list(reports_dir.glob('*-twitter.txt'))
        if not twitter_files:
            print("❌ Twitter 스레드 파일을 찾을 수 없습니다.")
            sys.exit(1)
        twitter_file = max(twitter_files, key=lambda p: p.stat().st_mtime)

    print(f"📄 Twitter 스레드 파일: {twitter_file}")

    # 스레드 파싱
    tweets = parse_twitter_thread_file(str(twitter_file))
    print(f"\n📊 총 {len(tweets)}개 트윗 준비 완료\n")

    # 확인
    print("=" * 60)
    for i, tweet in enumerate(tweets, 1):
        char_count = len(tweet)
        status = "✅" if char_count <= 280 else f"❌ ({char_count}자)"
        print(f"트윗 {i}: {status}")
        print(f"{tweet[:80]}...")
        print()

    print("=" * 60)

    # 280자 초과 확인
    over_limit = [i for i, t in enumerate(tweets, 1) if len(t) > 280]
    if over_limit:
        print(f"\n⚠️  경고: {len(over_limit)}개 트윗이 280자를 초과합니다:")
        for i in over_limit:
            print(f"   - 트윗 {i}: {len(tweets[i-1])}자")
        print("\n계속하시겠습니까? (y/N): ", end='')
        confirm = input().strip().lower()
        if confirm != 'y':
            print("취소되었습니다.")
            sys.exit(0)

    # 스레드 게시
    try:
        poster = TwitterPoster(bearer_token)
        print("\n🚀 X(Twitter)에 스레드 게시 시작...\n")

        tweet_ids = poster.post_thread(tweets, delay=2.0)

        if len(tweet_ids) == len(tweets):
            print(f"\n🎉 스레드 게시 완료! ({len(tweet_ids)}개 트윗)")
            print(f"\n🔗 첫 번째 트윗 보기:")
            print(f"   https://twitter.com/i/web/status/{tweet_ids[0]}")
        else:
            print(f"\n⚠️  부분 완료: {len(tweet_ids)}/{len(tweets)} 트윗 게시됨")

        # 결과 저장
        result_file = Path(twitter_file).parent / f"{Path(twitter_file).stem}-posted.json"
        import json
        with open(result_file, 'w') as f:
            json.dump({
                "tweet_ids": tweet_ids,
                "thread_url": f"https://twitter.com/i/web/status/{tweet_ids[0]}" if tweet_ids else None,
                "total": len(tweets),
                "posted": len(tweet_ids)
            }, f, indent=2)
        print(f"\n📝 결과 저장: {result_file}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
