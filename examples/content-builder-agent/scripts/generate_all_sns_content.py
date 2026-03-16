#!/usr/bin/env python3
"""
SNS 플랫폼용 기술 콘텐츠 생성
전문적인 기술 정리 스타일 (Instagram, Twitter, Threads)
"""

import os
import glob
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional


class SNSContentGenerator:
    """SNS 콘텐츠 생성 - 전문 기술 정리 스타일"""

    def __init__(self, source_content: Optional[str] = None, create_issue: bool = False):
        """
        초기화

        Args:
            source_content: 소스 콘텐츠 (None이면 최신 리포트 사용)
            create_issue: GitHub 이슈로 등록할지 여부
        """
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.date_str = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
        self.source_content = source_content or self._find_latest_report()
        self.output_base = Path("sns_output")
        self.output_base.mkdir(exist_ok=True)
        self.create_issue = create_issue
        self.generated_files = {}
        self.instagram_image = self._find_latest_instagram_image()

    def _find_latest_report(self) -> str:
        """최신 리포트 파일 찾기"""
        # 다양한 경로에서 리포트 찾기
        search_paths = [
            "reports/*.md",
            "../../reports/*.md",
            "../../../reports/*.md"
        ]

        for search_path in search_paths:
            reports = glob.glob(search_path)
            reports = [r for r in reports if "threads" not in r and "twitter" not in r]

            if reports:
                latest = max(reports, key=os.path.getmtime)
                print(f"📄 소스 파일: {latest}")
                with open(latest, 'r', encoding='utf-8') as f:
                    return f.read()

        # 리포트 없으면 linkedin에서 찾기
        linkedin_paths = [
            "linkedin/*/post.md",
            "../../linkedin/*/post.md"
        ]

        for search_path in linkedin_paths:
            linkedin_posts = glob.glob(search_path)
            if linkedin_posts:
                latest = max(linkedin_posts, key=os.path.getmtime)
                print(f"📄 소스 파일: {latest}")
                with open(latest, 'r', encoding='utf-8') as f:
                    return f.read()

        return "샘플 콘텐츠입니다. 실제 콘텐츠로 대체하세요."

    def _find_latest_instagram_image(self) -> Optional[str]:
        """최신 Instagram 이미지 찾기"""
        # 현재 디렉토리와 상위 디렉토리에서 모두 확인
        search_paths = [
            "reports/images/*-instagram.png",
            "../../reports/images/*-instagram.png",
            "../../../reports/images/*-instagram.png"
        ]

        # Instagram용 텍스트 오버레이 이미지 찾기
        for search_path in search_paths:
            instagram_images = glob.glob(search_path)
            if instagram_images:
                latest = max(instagram_images, key=os.path.getmtime)
                print(f"🖼️  Instagram 이미지: {latest}")
                return latest

        # Instagram 이미지가 없으면 일반 썸네일 찾기
        thumbnail_paths = [
            "reports/images/*-thumbnail.png",
            "../../reports/images/*-thumbnail.png",
            "../../../reports/images/*-thumbnail.png"
        ]

        for search_path in thumbnail_paths:
            thumbnails = glob.glob(search_path)
            thumbnails = [t for t in thumbnails if "instagram" not in t]
            if thumbnails:
                latest = max(thumbnails, key=os.path.getmtime)
                print(f"🖼️  썸네일 이미지: {latest}")
                return latest

        print("⚠️  이미지를 찾을 수 없습니다")
        return None

    def _save_file(self, platform: str, content: str, extension: str = "md"):
        """파일 저장"""
        platform_dir = self.output_base / platform
        platform_dir.mkdir(exist_ok=True)

        filename = f"{self.timestamp}.{extension}"
        filepath = platform_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {platform}: {filepath}")

        # 생성된 파일 기록 (이슈 생성용)
        self.generated_files[platform] = {
            'filepath': str(filepath),
            'content': content
        }

        return filepath

    def generate_instagram(self):
        """Instagram 콘텐츠 생성 - 전문 기술 정리 스타일"""
        print("\n📸 Instagram 콘텐츠 생성 중...")

        # 이미지 정보 섹션
        image_section = ""
        if self.instagram_image:
            image_section = f"""## 📸 이미지
파일 경로: {self.instagram_image}

**이미지 사용 방법:**
1. 위 파일을 Instagram 앱에서 선택
2. 또는 GitHub 리포지토리에서 다운로드하여 사용

"""

        # 사용자가 직접 작성한 콘텐츠 사용 (그대로 저장)
        content = f"""# Instagram 포스트
생성일시: {self.date_str}

{image_section}## 캡션
{self.source_content}

## 작성 가이드
**전문 기술 정리 스타일:**
- 📌 핵심 포인트를 구조화
- 💡 기술적 인사이트 + 실용적 시사점
- 🔍 전문 용어를 쉽게 설명
- 이모지로 섹션 구분
- 간결하면서도 밀도 높은 내용

## 사용 방법
1. Instagram 앱 열기
2. 새 게시물 만들기
3. 위 이미지 파일 선택
4. 위 캡션 복사하여 붙여넣기
5. 해시태그 추가 (3-5개 권장)
6. 게시

## 주의사항
- 첫 문장이 가장 중요 (125자 미리보기)
- 기술 내용 + 실용적 의미
- 해시태그: #AI #기술 #개발 등
"""
        self._save_file("instagram", content)

    def generate_twitter(self):
        """Twitter/X 콘텐츠 생성 - 전문 기술 스레드"""
        print("\n🐦 Twitter/X 콘텐츠 생성 중...")

        # 사용자가 직접 작성한 콘텐츠 사용 (그대로 저장)
        content = f"""# Twitter/X 스레드
생성일시: {self.date_str}

## 스레드 내용
{self.source_content}

## 작성 가이드
**전문 기술 스레드 스타일:**
- 첫 트윗에 핵심 요약
- 각 트윗은 하나의 개념/포인트
- 📌 bullet point 활용
- 💡 인사이트 강조
- 기술 용어 + 쉬운 설명
- 280자 내외로 분할

## 사용 방법
1. Twitter/X 앱/웹 열기
2. 새 트윗 작성
3. 첫 트윗에 "🧵 스레드" 표시
4. "+" 버튼으로 스레드 추가
5. 순서대로 내용 작성
6. 전체 게시

## 최적화 팁
- 각 트윗 280자 이내
- 첫 트윗이 가장 중요 (RT 결정)
- 해시태그 1-2개만
- 이모지로 가독성 향상
"""
        self._save_file("twitter", content)

    def generate_threads(self):
        """Threads 콘텐츠 생성 - 전문 기술 정리"""
        print("\n🧵 Threads 콘텐츠 생성 중...")

        # 사용자가 직접 작성한 콘텐츠 사용 (그대로 저장)
        content = f"""# Threads 포스트
생성일시: {self.date_str}

## 포스트 내용
{self.source_content}

## 작성 가이드
**전문 기술 정리 스타일:**
- 핵심 포인트를 섹션별로 정리
- 📌 구조화된 포맷 (이모지 사용)
- 💡 기술적 인사이트
- 🔍 실용적 시사점
- 전문성 + 접근성

**참고 스타일:**
- @choi.openai - AI 기술 정리
- @unclejobs.ai - AI 워크플로우
- 기술 블로거들의 간결한 설명

## 사용 방법
1. Threads 앱 열기
2. 새 스레드 작성
3. 위 내용 복사하여 붙여넣기
4. 해시태그 1-2개 추가
5. 게시

## 최적화 팁
- 해시태그는 1-2개만 (2026년 중요)
- 맥락 내 키워드 자연스럽게 포함
- 전문적이면서 읽기 쉽게
- 구조화된 정보 전달
"""
        self._save_file("threads", content)

    def generate_all_platforms_txt(self):
        """모든 플랫폼 통합 텍스트 파일"""
        print("\n📋 통합 텍스트 파일 생성 중...")

        content = f"""═══════════════════════════════════════════════════════════
SNS 콘텐츠 모음 (전문 기술 정리 스타일)
생성일시: {self.date_str}
═══════════════════════════════════════════════════════════

{'='*60}
Instagram
{'='*60}
{self.source_content}

{'='*60}
Twitter/X 스레드
{'='*60}
{self.source_content}

{'='*60}
Threads
{'='*60}
{self.source_content}

═══════════════════════════════════════════════════════════
"""
        self._save_file("all_platforms", content, "txt")

    def create_github_issue(self):
        """GitHub 이슈 생성"""
        print("\n" + "="*60)
        print("📝 GitHub 이슈 생성 중...")
        print("="*60)

        # gh CLI가 설치되어 있는지 확인
        try:
            subprocess.run(["gh", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ gh CLI가 설치되어 있지 않습니다.")
            print("   설치 방법: https://cli.github.com/")
            return

        # 이슈 본문 생성
        issue_body = f"""## SNS 콘텐츠 생성 완료

생성일시: {self.date_str}

"""
        # Instagram 이미지 추가
        if self.instagram_image:
            # GitHub 리포지토리에서 이미지 URL 생성 (리포지토리명은 환경에 따라 다를 수 있음)
            issue_body += f"""### 📸 Instagram 이미지

![Instagram Image]({self.instagram_image})

**이미지 파일:** `{self.instagram_image}`

"""

        issue_body += f"""### 생성된 파일

"""
        for platform, info in self.generated_files.items():
            if platform != 'all_platforms':
                filepath = info['filepath']
                issue_body += f"- **{platform.upper()}**: `{filepath}`\n"

        issue_body += f"\n### 통합 파일\n\n"
        if 'all_platforms' in self.generated_files:
            filepath = self.generated_files['all_platforms']['filepath']
            issue_body += f"- `{filepath}` (모든 플랫폼 통합)\n"

        issue_body += f"\n### 사용 방법\n\n"
        issue_body += "1. 각 플랫폼별 파일을 열어서 내용 확인\n"
        issue_body += "2. Instagram: 위 이미지 다운로드하여 사용\n"
        issue_body += "3. 내용을 복사 (Cmd+A → Cmd+C / Ctrl+A → Ctrl+C)\n"
        issue_body += "4. 해당 SNS에서 새 게시물 만들기\n"
        issue_body += "5. 붙여넣기 (Cmd+V / Ctrl+V)\n"
        issue_body += "6. 게시!\n"

        issue_body += f"\n---\n\n"
        issue_body += "✅ 이 이슈는 자동으로 생성되었습니다.\n"

        # 이슈 제목
        issue_title = f"SNS 콘텐츠 생성 완료 - {self.date_str}"

        # gh CLI로 이슈 생성
        try:
            result = subprocess.run(
                ["gh", "issue", "create", "--title", issue_title, "--body", issue_body, "--label", "sns-content"],
                capture_output=True,
                text=True,
                check=True
            )
            issue_url = result.stdout.strip()
            print(f"✅ GitHub 이슈 생성 완료: {issue_url}")
        except subprocess.CalledProcessError as e:
            print(f"❌ GitHub 이슈 생성 실패: {e.stderr}")

    def generate_summary(self):
        """생성 완료 요약"""
        print("\n" + "="*60)
        print("📁 저장 위치")
        print("="*60)
        print(f"📂 {self.output_base.absolute()}/")
        print(f"   ├── instagram/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── twitter/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── threads/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   └── all_platforms/")
        print(f"       └── {self.timestamp}.txt (모든 플랫폼 통합)")
        print("")
        print("✅ 모든 SNS 콘텐츠 생성 완료!")
        print("📋 각 파일을 열어서 복사하여 해당 SNS에 붙여넣으세요.")

    def generate_all(self):
        """모든 플랫폼 콘텐츠 생성"""
        print("="*60)
        print("SNS 콘텐츠 생성 시작")
        print("="*60)

        self.generate_instagram()
        self.generate_twitter()
        self.generate_threads()
        self.generate_all_platforms_txt()

        self.generate_summary()

        # GitHub 이슈 생성 (옵션)
        if self.create_issue:
            self.create_github_issue()


def main():
    """메인 함수"""
    import sys

    # 옵션 파싱
    create_issue = False
    content_args = []

    for arg in sys.argv[1:]:
        if arg in ['--issue', '-i']:
            create_issue = True
        else:
            content_args.append(arg)

    # 커스텀 콘텐츠를 인자로 받을 수 있음
    if content_args:
        content = " ".join(content_args)
        generator = SNSContentGenerator(content, create_issue=create_issue)
    else:
        generator = SNSContentGenerator(create_issue=create_issue)

    generator.generate_all()


if __name__ == "__main__":
    main()
