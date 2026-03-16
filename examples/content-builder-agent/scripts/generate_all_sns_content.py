#!/usr/bin/env python3
"""
모든 SNS 플랫폼용 콘텐츠를 로컬 파일로 생성
API 연결 없이 날짜/시간 기반 파일명으로 저장
옵션: GitHub 이슈로 자동 등록
"""

import os
import glob
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional


class SNSContentGenerator:
    """SNS 콘텐츠 로컬 생성 및 GitHub 이슈 등록"""

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

    def _find_latest_report(self) -> str:
        """최신 리포트 파일 찾기"""
        reports = glob.glob("reports/*.md")
        reports = [r for r in reports if "threads" not in r and "twitter" not in r]

        if reports:
            latest = max(reports, key=os.path.getmtime)
            print(f"📄 소스 파일: {latest}")
            with open(latest, 'r', encoding='utf-8') as f:
                return f.read()

        # 리포트 없으면 linkedin에서 찾기
        linkedin_posts = glob.glob("linkedin/*/post.md")
        if linkedin_posts:
            latest = max(linkedin_posts, key=os.path.getmtime)
            print(f"📄 소스 파일: {latest}")
            with open(latest, 'r', encoding='utf-8') as f:
                return f.read()

        return "샘플 콘텐츠입니다. 실제 콘텐츠로 대체하세요."

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
        """Instagram 콘텐츠 생성"""
        print("\n📸 Instagram 콘텐츠 생성 중...")

        # Instagram은 캡션 2,200자 제한
        caption = self.source_content[:2200]

        content = f"""# Instagram 포스트
생성일시: {self.date_str}

## 캡션
{caption}

## 사용 방법
1. Instagram 앱 열기
2. 새 게시물 만들기
3. 사진 선택 (또는 이미지 생성)
4. 위 캡션 복사하여 붙여넣기
5. 게시

## 주의사항
- 해시태그는 5개까지만! (2026년 제한)
- 첫 줄이 가장 중요 (125자 미리보기)
- 이미지가 80%, 캡션은 20%
"""
        self._save_file("instagram", content)

    def generate_linkedin(self):
        """LinkedIn 콘텐츠 생성"""
        print("\n💼 LinkedIn 콘텐츠 생성 중...")

        # LinkedIn 최적 길이: 150-300자 (한국어)
        # 전체 내용 포함하되 가이드 추가
        content = f"""# LinkedIn 포스트
생성일시: {self.date_str}

## 포스트 내용
{self.source_content}

## 사용 방법
1. LinkedIn 앱/웹 열기
2. "게시물 시작하기" 클릭
3. 위 내용 복사하여 붙여넣기
4. 게시

## 최적화 팁
- 첫 두 줄이 가장 중요 (미리보기)
- 해시태그는 1-2개만 (선택사항)
- 전문적이지만 진솔하게
- 댓글 참여 유도
"""
        self._save_file("linkedin", content)

    def generate_twitter(self):
        """Twitter/X 콘텐츠 생성"""
        print("\n🐦 Twitter/X 콘텐츠 생성 중...")

        # 280자씩 나눠서 스레드 생성
        lines = self.source_content.split('\n')
        tweets = []
        current_tweet = ""

        for line in lines:
            if len(current_tweet) + len(line) + 1 <= 270:  # 280자 여유
                current_tweet += line + "\n"
            else:
                if current_tweet.strip():
                    tweets.append(current_tweet.strip())
                current_tweet = line + "\n"

        if current_tweet.strip():
            tweets.append(current_tweet.strip())

        # 스레드 번호 추가
        thread_content = ""
        for i, tweet in enumerate(tweets[:10], 1):  # 최대 10개 트윗
            if i == 1:
                thread_content += f"{i}/🧵\n{tweet}\n\n"
            else:
                thread_content += f"{i}/\n{tweet}\n\n"

        content = f"""# Twitter/X 스레드
생성일시: {self.date_str}

## 스레드 내용 (총 {min(len(tweets), 10)}개 트윗)
{thread_content}

## 사용 방법
1. Twitter/X 앱/웹 열기
2. 새 트윗 작성
3. 첫 번째 트윗 (1/🧵) 작성
4. "+" 버튼으로 스레드 추가
5. 순서대로 복사하여 붙여넣기
6. 전체 게시

## 최적화 팁
- 각 트윗 280자 이내
- 해시태그 1-3개
- 이모지 활용
- 첫 트윗이 가장 중요
"""
        self._save_file("twitter", content)

    def generate_threads(self):
        """Threads 콘텐츠 생성"""
        print("\n🧵 Threads 콘텐츠 생성 중...")

        # Threads는 500자 제한
        main_content = self.source_content[:500]

        content = f"""# Threads 포스트
생성일시: {self.date_str}

## 포스트 내용
{main_content}

## 사용 방법
1. Threads 앱 열기
2. 새 스레드 작성
3. 위 내용 복사하여 붙여넣기
4. 게시

## 최적화 팁
- 해시태그는 1개만! (2026년 중요)
- 맥락 내 키워드 자연스럽게 포함
- 솔직하고 투명한 톤
- 과정과 경험 공유
"""
        self._save_file("threads", content)

    def generate_naver_blog(self):
        """네이버 블로그 콘텐츠 생성"""
        print("\n📝 네이버 블로그 콘텐츠 생성 중...")

        # 블로그는 긴 형식
        content = f"""# 네이버 블로그 포스트
생성일시: {self.date_str}

## 제목 (23-24자로 수정 필요)
[핵심 키워드를 앞쪽에] AI 에이전트 활용법

## 본문
{self.source_content}

## 마무리
지금까지 내용을 정리해드렸습니다. 도움이 되셨기를 바랍니다!

## 사용 방법
1. 네이버 블로그 접속
2. "글쓰기" 클릭
3. 제목 입력 (23-24자)
4. 본문 복사하여 붙여넣기
5. 이미지 5장 이상 추가
6. 해시태그 5-10개 추가
7. 발행

## 최적화 팁
- 제목 23-24자, 키워드 앞쪽
- 첫 두 문장에 키워드 포함
- 소제목(H2, H3) 활용
- 이미지 최소 5장
- 해시태그: #키워드1 #키워드2 #키워드3 (5-10개)
"""
        self._save_file("naver_blog", content)

    def generate_facebook(self):
        """Facebook 콘텐츠 생성"""
        print("\n📘 Facebook 콘텐츠 생성 중...")

        # Facebook은 100-250자 최적
        short_content = '\n'.join(self.source_content.split('\n')[:5])

        content = f"""# Facebook 포스트
생성일시: {self.date_str}

## 포스트 내용
{short_content}

## 사용 방법
1. Facebook 앱/웹 열기
2. "무슨 생각을 하고 계신가요?" 클릭
3. 위 내용 복사하여 붙여넣기
4. 사진/동영상 추가 (선택)
5. 게시

## 최적화 팁
- 첫 3줄이 미리보기에 노출
- 해시태그 1-3개 (선택)
- 영상 콘텐츠 효과적
- 질문으로 댓글 유도
"""
        self._save_file("facebook", content)

    def generate_all_platforms_txt(self):
        """모든 플랫폼 한 번에 텍스트 파일로"""
        print("\n📋 통합 텍스트 파일 생성 중...")

        content = f"""═══════════════════════════════════════════════════════════
SNS 콘텐츠 모음
생성일시: {self.date_str}
═══════════════════════════════════════════════════════════

{'='*60}
Instagram (캡션 2,200자 제한)
{'='*60}
{self.source_content[:2200]}

{'='*60}
LinkedIn (150-300자 권장)
{'='*60}
{self.source_content}

{'='*60}
Twitter/X (280자씩 스레드)
{'='*60}
1/🧵
{self.source_content[:270]}

2/
(계속...)

{'='*60}
Threads (500자 제한)
{'='*60}
{self.source_content[:500]}

{'='*60}
네이버 블로그
{'='*60}
제목: [23-24자로 작성]

{self.source_content}

해시태그: #키워드1 #키워드2 #키워드3 #키워드4 #키워드5

{'='*60}
Facebook (100-250자 권장)
{'='*60}
{self.source_content[:250]}

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

### 생성된 파일

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
        issue_body += "2. 내용을 복사 (Cmd+A → Cmd+C / Ctrl+A → Ctrl+C)\n"
        issue_body += "3. 해당 SNS에서 새 게시물 만들기\n"
        issue_body += "4. 붙여넣기 (Cmd+V / Ctrl+V)\n"
        issue_body += "5. 게시!\n"

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
        print(f"   ├── linkedin/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── twitter/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── threads/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── naver_blog/")
        print(f"   │   └── {self.timestamp}.md")
        print(f"   ├── facebook/")
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
        self.generate_linkedin()
        self.generate_twitter()
        self.generate_threads()
        self.generate_naver_blog()
        self.generate_facebook()
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
