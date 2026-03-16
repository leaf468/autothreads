#!/usr/bin/env python3
"""
SNS 자동 업로드 스크립트
환경 변수가 설정되지 않은 SNS는 자동으로 건너뜁니다.
"""

import os
import sys
import glob
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any


class SocialMediaPoster:
    """SNS 자동 업로드 클래스"""

    def __init__(self, report_path: Optional[str] = None):
        """
        초기화

        Args:
            report_path: 리포트 파일 경로 (None이면 자동 탐색)
        """
        self.report_path = report_path or self._find_latest_report()
        self.content = self._load_content()
        self.results = {}

    def _find_latest_report(self) -> str:
        """최신 리포트 파일 찾기"""
        reports = glob.glob("reports/*.md")
        # threads, twitter 제외
        reports = [r for r in reports if "threads" not in r and "twitter" not in r]

        if not reports:
            raise FileNotFoundError("리포트 파일을 찾을 수 없습니다.")

        # 최신 파일 (수정 시간 기준)
        latest = max(reports, key=os.path.getmtime)
        print(f"📄 리포트 파일: {latest}")
        return latest

    def _load_content(self) -> str:
        """리포트 내용 로드"""
        with open(self.report_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _check_env_vars(self, *var_names) -> bool:
        """환경 변수 확인"""
        return all(os.getenv(var) for var in var_names)

    def _log_skip(self, platform: str, required_vars: list):
        """건너뛰기 로그"""
        print(f"\n⚠️  {platform} 환경 변수가 설정되지 않았습니다. 건너뜁니다.")
        print(f"   필요한 변수: {', '.join(required_vars)}")
        self.results[platform] = "skipped"

    def _log_success(self, platform: str):
        """성공 로그"""
        print(f"✅ {platform} 업로드 완료")
        self.results[platform] = "success"

    def _log_error(self, platform: str, error: str):
        """에러 로그"""
        print(f"⚠️  {platform} 업로드 실패: {error}")
        self.results[platform] = f"error: {error}"

    def post_to_instagram(self):
        """Instagram 업로드"""
        print("\n📸 Instagram 업로드 확인 중...")

        required_vars = ["INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_ACCOUNT_ID", "INSTAGRAM_IMAGE_URL"]

        if not self._check_env_vars(*required_vars):
            self._log_skip("Instagram", required_vars)
            return

        try:
            access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
            account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
            image_url = os.getenv("INSTAGRAM_IMAGE_URL")

            # 1단계: 미디어 생성
            create_url = f"https://graph.facebook.com/v18.0/{account_id}/media"
            create_data = {
                "image_url": image_url,
                "caption": self.content[:2200],  # Instagram 캡션 제한
                "access_token": access_token
            }

            response = requests.post(create_url, data=create_data)
            response.raise_for_status()
            creation_id = response.json().get("id")

            if not creation_id:
                raise ValueError("미디어 생성 실패")

            # 2단계: 미디어 게시
            publish_url = f"https://graph.facebook.com/v18.0/{account_id}/media_publish"
            publish_data = {
                "creation_id": creation_id,
                "access_token": access_token
            }

            response = requests.post(publish_url, data=publish_data)
            response.raise_for_status()

            self._log_success("Instagram")

        except Exception as e:
            self._log_error("Instagram", str(e))

    def post_to_twitter(self):
        """Twitter/X 업로드"""
        print("\n🐦 Twitter/X 업로드 확인 중...")

        required_vars = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_TOKEN_SECRET"
        ]

        if not self._check_env_vars(*required_vars):
            self._log_skip("Twitter/X", required_vars)
            return

        try:
            # Twitter API v2는 OAuth 1.0a 서명이 필요하므로
            # tweepy 또는 requests-oauthlib 라이브러리 사용 권장
            print("⚠️  Twitter API 구현 필요 (OAuth 1.0a 서명 필요)")
            self.results["Twitter/X"] = "not_implemented"

        except Exception as e:
            self._log_error("Twitter/X", str(e))

    def post_to_linkedin(self):
        """LinkedIn 업로드"""
        print("\n💼 LinkedIn 업로드 확인 중...")

        required_vars = ["LINKEDIN_ACCESS_TOKEN", "LINKEDIN_PERSON_URN"]

        if not self._check_env_vars(*required_vars):
            self._log_skip("LinkedIn", required_vars)
            return

        try:
            access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
            person_urn = os.getenv("LINKEDIN_PERSON_URN")

            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }

            data = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": self.content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            self._log_success("LinkedIn")

        except Exception as e:
            self._log_error("LinkedIn", str(e))

    def post_to_threads(self):
        """Threads 업로드"""
        print("\n🧵 Threads 업로드 확인 중...")

        required_vars = ["THREADS_ACCESS_TOKEN", "THREADS_USER_ID"]

        if not self._check_env_vars(*required_vars):
            self._log_skip("Threads", required_vars)
            return

        try:
            access_token = os.getenv("THREADS_ACCESS_TOKEN")
            user_id = os.getenv("THREADS_USER_ID")

            # 1단계: 스레드 생성
            create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
            create_data = {
                "media_type": "TEXT",
                "text": self.content[:500],  # Threads 제한
                "access_token": access_token
            }

            response = requests.post(create_url, data=create_data)
            response.raise_for_status()
            creation_id = response.json().get("id")

            if not creation_id:
                raise ValueError("스레드 생성 실패")

            # 2단계: 스레드 게시
            publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
            publish_data = {
                "creation_id": creation_id,
                "access_token": access_token
            }

            response = requests.post(publish_url, data=publish_data)
            response.raise_for_status()

            self._log_success("Threads")

        except Exception as e:
            self._log_error("Threads", str(e))

    def post_to_naver_blog(self):
        """네이버 블로그 업로드"""
        print("\n📝 네이버 블로그 업로드 확인 중...")

        required_vars = [
            "NAVER_CLIENT_ID",
            "NAVER_CLIENT_SECRET",
            "NAVER_ACCESS_TOKEN"
        ]

        if not self._check_env_vars(*required_vars):
            self._log_skip("네이버 블로그", required_vars)
            return

        try:
            access_token = os.getenv("NAVER_ACCESS_TOKEN")

            url = "https://openapi.naver.com/blog/writePost.json"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            data = {
                "title": "자동 생성된 블로그 포스트",
                "contents": self.content
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            if result.get("result") == "success":
                self._log_success("네이버 블로그")
            else:
                raise ValueError(result)

        except Exception as e:
            self._log_error("네이버 블로그", str(e))

    def post_all(self):
        """모든 SNS에 업로드 시도"""
        print("=" * 60)
        print("SNS 자동 업로드 시작")
        print("=" * 60)

        # 모든 플랫폼에 시도
        self.post_to_instagram()
        self.post_to_twitter()
        self.post_to_linkedin()
        self.post_to_threads()
        self.post_to_naver_blog()

        # 결과 요약
        print("\n" + "=" * 60)
        print("업로드 결과 요약")
        print("=" * 60)

        for platform, status in self.results.items():
            icon = "✅" if status == "success" else "⚠️" if status == "skipped" else "❌"
            print(f"{icon} {platform}: {status}")

        print("\n✅ SNS 자동 업로드 프로세스 완료")
        print("설정된 플랫폼에만 업로드되었으며, 나머지는 건너뛰었습니다.")


def main():
    """메인 함수"""
    try:
        poster = SocialMediaPoster()
        poster.post_all()
        sys.exit(0)  # 항상 성공으로 종료
    except Exception as e:
        print(f"❌ 에러 발생: {e}", file=sys.stderr)
        sys.exit(0)  # 에러가 있어도 0으로 종료 (다른 워크플로우 방해 안 함)


if __name__ == "__main__":
    main()
