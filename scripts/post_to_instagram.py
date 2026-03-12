#!/usr/bin/env python3
"""
Instagram 자동 포스팅 스크립트
Instagram Graph API를 사용하여 이미지와 캡션을 자동으로 업로드합니다.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path


class InstagramPoster:
    """Instagram Graph API를 사용한 포스팅 클래스"""

    def __init__(self, access_token: str, instagram_account_id: str):
        """
        Args:
            access_token: Facebook Graph API 액세스 토큰
            instagram_account_id: Instagram Business 계정 ID
        """
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_url = "https://graph.facebook.com/v19.0"

    def create_media_container(self, image_url: str, caption: str) -> str:
        """
        미디어 컨테이너 생성 (1단계)

        Args:
            image_url: 공개 접근 가능한 이미지 URL
            caption: 게시물 캡션

        Returns:
            creation_id: 생성된 컨테이너 ID
        """
        url = f"{self.base_url}/{self.instagram_account_id}/media"

        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }

        print(f"📦 미디어 컨테이너 생성 중...")
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result = response.json()
            creation_id = result.get('id')
            print(f"✅ 컨테이너 생성 완료: {creation_id}")
            return creation_id
        else:
            print(f"❌ 컨테이너 생성 실패: {response.status_code}")
            print(f"응답: {response.text}")
            raise Exception(f"Failed to create media container: {response.text}")

    def publish_media(self, creation_id: str) -> str:
        """
        미디어 게시 (2단계)

        Args:
            creation_id: 미디어 컨테이너 ID

        Returns:
            media_id: 게시된 미디어 ID
        """
        url = f"{self.base_url}/{self.instagram_account_id}/media_publish"

        payload = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }

        print(f"📤 Instagram에 게시 중...")
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result = response.json()
            media_id = result.get('id')
            print(f"✅ 게시 완료! Media ID: {media_id}")
            return media_id
        else:
            print(f"❌ 게시 실패: {response.status_code}")
            print(f"응답: {response.text}")
            raise Exception(f"Failed to publish media: {response.text}")

    def post(self, image_url: str, caption: str, wait_time: int = 10) -> str:
        """
        Instagram에 이미지 게시 (전체 프로세스)

        Args:
            image_url: 공개 접근 가능한 이미지 URL
            caption: 게시물 캡션
            wait_time: 컨테이너 생성 후 대기 시간 (초)

        Returns:
            media_id: 게시된 미디어 ID
        """
        # 1단계: 컨테이너 생성
        creation_id = self.create_media_container(image_url, caption)

        # 대기 (Instagram 서버가 이미지 처리할 시간 필요)
        print(f"⏳ {wait_time}초 대기 중 (이미지 처리)...")
        time.sleep(wait_time)

        # 2단계: 게시
        media_id = self.publish_media(creation_id)

        return media_id


def get_caption_from_summary(report_md_path: str) -> str:
    """
    마크다운 리포트에서 '오늘의 한마디' 추출하여 Instagram 캡션 생성

    Args:
        report_md_path: 마크다운 리포트 파일 경로

    Returns:
        Instagram 캡션 텍스트
    """
    with open(report_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 발행 시각 추출
    import re
    time_match = re.search(r'\*\*발행 시각:\*\* (.+)', content)
    publish_time = time_match.group(1) if time_match else ''

    # 오늘의 한마디 추출
    summary_match = re.search(r'## 📊 오늘의 한마디\n\n(.+?)(?=\n---|\Z)', content, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ''

    # Instagram 캡션 생성
    caption = f"""🤖 AI 트렌드 리포트

{summary}

{publish_time}

#AI트렌드 #인공지능 #테크뉴스 #머신러닝 #딥러닝 #AI #MachineLearning #DeepLearning #TechNews"""

    return caption


def main():
    """메인 실행 함수"""
    # 환경 변수에서 인증 정보 가져오기
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    image_url = os.getenv('INSTAGRAM_IMAGE_URL')  # 공개 접근 가능한 URL

    if not all([access_token, instagram_account_id, image_url]):
        print("❌ 필수 환경 변수가 설정되지 않았습니다:")
        print("   - INSTAGRAM_ACCESS_TOKEN")
        print("   - INSTAGRAM_ACCOUNT_ID")
        print("   - INSTAGRAM_IMAGE_URL")
        sys.exit(1)

    # 마크다운 리포트 경로 (인자로 받거나 최신 파일 사용)
    if len(sys.argv) > 1:
        report_path = sys.argv[1]
    else:
        # 최신 마크다운 리포트 찾기
        reports_dir = Path(__file__).parent.parent / 'reports'
        md_files = list(reports_dir.glob('*.md'))
        if not md_files:
            print("❌ 리포트 파일을 찾을 수 없습니다.")
            sys.exit(1)
        report_path = max(md_files, key=lambda p: p.stat().st_mtime)

    print(f"📄 리포트: {report_path}")

    # 캡션 생성
    caption = get_caption_from_summary(str(report_path))
    print(f"\n📝 캡션:\n{caption}\n")

    # Instagram에 게시
    try:
        poster = InstagramPoster(access_token, instagram_account_id)
        media_id = poster.post(image_url, caption)
        print(f"\n🎉 Instagram 게시 완료!")
        print(f"Media ID: {media_id}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
