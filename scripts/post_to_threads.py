#!/usr/bin/env python3
"""
Meta Threads 자동 게시 스크립트
Threads API를 사용하여 텍스트를 자동으로 게시합니다.
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Optional


class ThreadsPoster:
    """Meta Threads API를 사용한 게시 클래스"""

    def __init__(self, access_token: str, threads_user_id: str):
        """
        Args:
            access_token: Meta Graph API 액세스 토큰
            threads_user_id: Threads 사용자 ID
        """
        self.access_token = access_token
        self.threads_user_id = threads_user_id
        self.base_url = "https://graph.threads.net/v1.0"

    def create_media_container(self, text: str, media_type: str = "TEXT",
                               image_url: Optional[str] = None) -> str:
        """
        미디어 컨테이너 생성 (1단계)

        Args:
            text: 게시물 텍스트
            media_type: "TEXT" 또는 "IMAGE"
            image_url: 이미지 URL (media_type이 "IMAGE"인 경우)

        Returns:
            creation_id: 생성된 컨테이너 ID
        """
        url = f"{self.base_url}/{self.threads_user_id}/threads"

        payload = {
            'media_type': media_type,
            'text': text,
            'access_token': self.access_token
        }

        if media_type == "IMAGE" and image_url:
            payload['image_url'] = image_url

        print(f"📦 Threads 컨테이너 생성 중...")
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result = response.json()
            creation_id = result.get('id')
            print(f"✅ 컨테이너 생성 완료: {creation_id}")
            return creation_id
        else:
            print(f"❌ 컨테이너 생성 실패: {response.status_code}")
            print(f"응답: {response.text}")
            raise Exception(f"Failed to create Threads container: {response.text}")

    def publish_media(self, creation_id: str) -> str:
        """
        미디어 게시 (2단계)

        Args:
            creation_id: 미디어 컨테이너 ID

        Returns:
            media_id: 게시된 미디어 ID
        """
        url = f"{self.base_url}/{self.threads_user_id}/threads_publish"

        payload = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }

        print(f"📤 Threads에 게시 중...")
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result = response.json()
            media_id = result.get('id')
            print(f"✅ 게시 완료! Media ID: {media_id}")
            return media_id
        else:
            print(f"❌ 게시 실패: {response.status_code}")
            print(f"응답: {response.text}")
            raise Exception(f"Failed to publish to Threads: {response.text}")

    def post(self, text: str, image_url: Optional[str] = None,
             wait_time: int = 5) -> str:
        """
        Threads에 게시 (전체 프로세스)

        Args:
            text: 게시물 텍스트
            image_url: 이미지 URL (선택)
            wait_time: 컨테이너 생성 후 대기 시간 (초)

        Returns:
            media_id: 게시된 미디어 ID
        """
        # 1단계: 컨테이너 생성
        media_type = "IMAGE" if image_url else "TEXT"
        creation_id = self.create_media_container(text, media_type, image_url)

        # 대기
        if wait_time > 0:
            print(f"⏳ {wait_time}초 대기 중...")
            time.sleep(wait_time)

        # 2단계: 게시
        media_id = self.publish_media(creation_id)

        return media_id


def read_threads_content(file_path: str) -> str:
    """
    Threads 텍스트 파일 읽기

    Args:
        file_path: *-threads.txt 파일 경로

    Returns:
        게시할 텍스트 전체
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content.strip()


def main():
    """메인 실행 함수"""
    # 환경 변수에서 인증 정보 가져오기
    access_token = os.getenv('THREADS_ACCESS_TOKEN')
    threads_user_id = os.getenv('THREADS_USER_ID')

    if not all([access_token, threads_user_id]):
        print("❌ 필수 환경 변수가 설정되지 않았습니다:")
        print("   - THREADS_ACCESS_TOKEN")
        print("   - THREADS_USER_ID")
        print("\n💡 Meta for Developers에서 Threads API 액세스를 설정하세요:")
        print("   https://developers.facebook.com/docs/threads")
        sys.exit(1)

    # Threads 텍스트 파일 경로
    if len(sys.argv) > 1:
        threads_file = sys.argv[1]
    else:
        # 최신 threads.txt 파일 찾기
        reports_dir = Path(__file__).parent.parent / 'reports'
        threads_files = list(reports_dir.glob('*-threads.txt'))
        if not threads_files:
            print("❌ Threads 텍스트 파일을 찾을 수 없습니다.")
            sys.exit(1)
        threads_file = max(threads_files, key=lambda p: p.stat().st_mtime)

    print(f"📄 Threads 파일: {threads_file}")

    # 텍스트 읽기
    text_content = read_threads_content(str(threads_file))
    char_count = len(text_content)

    print(f"\n📊 텍스트 길이: {char_count}자")
    print(f"\n미리보기:\n{text_content[:200]}...\n")

    # Threads 글자수 제한 확인 (500자로 가정, 실제는 확인 필요)
    # Threads는 긴 텍스트를 지원하므로 일반적으로 문제없음
    if char_count > 10000:
        print(f"⚠️  경고: 텍스트가 매우 깁니다 ({char_count}자)")
        print("계속하시겠습니까? (y/N): ", end='')
        confirm = input().strip().lower()
        if confirm != 'y':
            print("취소되었습니다.")
            sys.exit(0)

    # Threads에 게시
    try:
        poster = ThreadsPoster(access_token, threads_user_id)
        print("\n🚀 Threads에 게시 시작...\n")

        # 이미지 URL (선택사항 - 환경 변수로 설정 가능)
        image_url = os.getenv('THREADS_IMAGE_URL')
        if image_url:
            print(f"📷 이미지 포함: {image_url}")

        media_id = poster.post(text_content, image_url=image_url)

        print(f"\n🎉 Threads 게시 완료!")
        print(f"Media ID: {media_id}")

        # 결과 저장
        result_file = Path(threads_file).parent / f"{Path(threads_file).stem}-posted.json"
        import json
        with open(result_file, 'w') as f:
            json.dump({
                "media_id": media_id,
                "char_count": char_count,
                "has_image": bool(image_url)
            }, f, indent=2)
        print(f"\n📝 결과 저장: {result_file}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
