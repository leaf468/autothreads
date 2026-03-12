#!/usr/bin/env python3
"""
AI 트렌드 마크다운 리포트를 Threads 및 X(Twitter) 스타일로 변환하는 스크립트
"""

import re
import sys
from pathlib import Path
from typing import List, Dict


def read_markdown_report(file_path: str) -> str:
    """마크다운 리포트 파일 읽기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_report(content: str) -> Dict:
    """마크다운 리포트 파싱"""
    data = {
        'title': '',
        'publish_time': '',
        'major_news': [],
        'minor_discoveries': [],
        'summary': ''
    }

    # 발행 시각 추출
    time_match = re.search(r'\*\*발행 시각:\*\* (.+)', content)
    if time_match:
        data['publish_time'] = time_match.group(1)

    # 주요 뉴스 섹션 추출
    major_section = re.search(r'## 📰 주요 뉴스.*?\n(.*?)(?=## 🔍|$)', content, re.DOTALL)
    if major_section:
        news_items = re.findall(
            r'### \d+\. (.+?)\n\n> \*\*원제:\*\* (.+?)\n> \*\*출처:\*\* (.+?)\n(?:> \*\*발행:\*\* (.+?)\n)?\n(.*?)(?=\n---|\n### |\Z)',
            major_section.group(1),
            re.DOTALL
        )

        for item in news_items:
            title_kr = item[0].strip()
            title_en = item[1].strip()
            source = item[2].strip()
            content_text = item[4].strip()

            # 핵심 포인트 추출
            points = []
            points_match = re.search(r'\*\*💡 핵심 포인트\*\*\n((?:- .+\n?)+)', content_text)
            if points_match:
                points = [p.strip('- ').strip() for p in points_match.group(1).split('\n') if p.strip()]

            # 추가 인사이트 추출
            insight = ''
            insight_match = re.search(r'\*\*🤔 추가 인사이트.*?\*\*\n(.+?)(?=\n\*\*|\n!|\Z)', content_text, re.DOTALL)
            if insight_match:
                insight = insight_match.group(1).strip()

            # 메인 내용 (포인트/인사이트 제외)
            main_content = re.sub(r'\*\*💡 핵심 포인트\*\*.*', '', content_text, flags=re.DOTALL)
            main_content = re.sub(r'\*\*🤔 추가 인사이트.*?\*\*.*', '', main_content, flags=re.DOTALL)
            main_content = re.sub(r'!\[이미지\].*', '', main_content, flags=re.DOTALL)
            main_content = main_content.strip()

            data['major_news'].append({
                'title_kr': title_kr,
                'title_en': title_en,
                'source': source,
                'content': main_content,
                'points': points,
                'insight': insight
            })

    # 마이너 발견 섹션 추출
    minor_section = re.search(r'## 🔍 마이너 발견.*?\n(.*?)(?=## 📊|$)', content, re.DOTALL)
    if minor_section:
        minor_items = re.findall(
            r'### \d+\. (.+?)\n\n> \*\*출처:\*\* (.+?)\n(?:> \*\*링크:\*\* (.+?)\n)?\n(.*?)(?=\n---|\n### |\Z)',
            minor_section.group(1),
            re.DOTALL
        )

        for item in minor_items:
            title = item[0].strip()
            source = item[1].strip()
            link = item[2].strip() if item[2] else ''
            content_text = item[3].strip()

            # "왜 주목할까?" 추출
            why_match = re.search(r'왜 주목할까\?\s*\n(.+?)(?=\n\*출처:|\Z)', content_text, re.DOTALL)
            why_text = why_match.group(1).strip() if why_match else ''

            # 메인 설명 (왜 주목할까 제외)
            main_desc = re.sub(r'왜 주목할까\?.*', '', content_text, flags=re.DOTALL)
            main_desc = re.sub(r'\*출처:.*', '', main_desc, flags=re.DOTALL)
            main_desc = main_desc.strip()

            data['minor_discoveries'].append({
                'title': title,
                'source': source,
                'link': link,
                'description': main_desc,
                'why': why_text
            })

    # 오늘의 한마디 추출
    summary_match = re.search(r'## 📊 오늘의 한마디\n\n(.+?)(?=\n---|\Z)', content, re.DOTALL)
    if summary_match:
        data['summary'] = summary_match.group(1).strip()

    return data


def format_to_threads(data: Dict) -> str:
    """Threads 스타일로 포맷팅"""
    output = []

    # 헤더
    output.append("🤖 AI 트렌드 리포트")
    output.append(data['publish_time'])
    output.append("")
    output.append("오늘은 정말 흥미로운 소식들이 많네요!")
    output.append("")
    output.append("---")
    output.append("")

    # 주요 뉴스
    output.append("📰 주요 뉴스")
    output.append("")

    for i, news in enumerate(data['major_news'], 1):
        # 번호 이모지
        num_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣'][i-1] if i <= 4 else f"{i}️⃣"

        output.append(f"{num_emoji} {news['title_kr']}")
        output.append("")

        # 핵심 내용 요약 (첫 2-3문장)
        sentences = news['content'].split('.')
        summary_sentences = '. '.join(sentences[:2]).strip()
        if summary_sentences and not summary_sentences.endswith('.'):
            summary_sentences += '.'
        output.append(summary_sentences)
        output.append("")

        # 핵심 포인트
        if news['points']:
            output.append("💡 포인트:")
            for point in news['points'][:3]:  # 최대 3개
                output.append(f"• {point}")
            output.append("")

        # 한국 관점 인사이트
        if news['insight'] and '한국' in news['insight']:
            output.append("🤔 한국 관점:")
            # 첫 문장만
            insight_first = news['insight'].split('.')[0] + '.'
            output.append(insight_first)
            output.append("")

        output.append("---")
        output.append("")

    # 마이너 발견
    if data['minor_discoveries']:
        output.append("🔍 마이너 발견")
        output.append("")

        for discovery in data['minor_discoveries'][:3]:  # 최대 3개
            output.append(f"✨ {discovery['title']}")
            output.append("")

            # 설명 첫 2문장
            desc_sentences = discovery['description'].split('.')
            desc_summary = '. '.join(desc_sentences[:2]).strip()
            if desc_summary and not desc_summary.endswith('.'):
                desc_summary += '.'
            output.append(desc_summary)
            output.append("")

            # 왜 주목할까 (요약)
            if discovery['why']:
                why_lines = [line.strip() for line in discovery['why'].split('\n') if line.strip()]
                if why_lines:
                    output.append(f"👉 {why_lines[0]}")
                    output.append("")

        output.append("---")
        output.append("")

    # 오늘의 한마디
    if data['summary']:
        output.append("📊 오늘의 한마디")
        output.append("")
        output.append(data['summary'])
        output.append("")
        output.append("---")
        output.append("")

    # 푸터
    output.append("🔗 자세한 내용과 원문 링크는 댓글에 남겼어요!")
    output.append("")
    output.append("#AI트렌드 #인공지능 #테크뉴스 #머신러닝")

    return '\n'.join(output)


def format_to_twitter(data: Dict) -> str:
    """X(Twitter) 스레드 스타일로 포맷팅 - 자연스럽고 임팩트 있게"""
    tweets = []

    # 첫 번째 뉴스만 추출 (가장 중요한 것)
    top_news = data['major_news'][0] if data['major_news'] else None

    if not top_news:
        return "AI 트렌드 리포트를 생성할 수 없습니다."

    # 파싱용 데이터 준비
    def extract_source_link(news):
        """뉴스에서 출처 링크 추출"""
        # source 필드에서 링크 찾기 (예: "Wired — https://...")
        if ' — ' in news.get('source', ''):
            parts = news['source'].split(' — ')
            if len(parts) == 2:
                return {'name': parts[0], 'link': parts[1]}
        return None

    # 트윗 1: 임팩트 있는 훅 (단독으로도 가치있게)
    title = top_news['title_kr']
    sentences = top_news['content'].split('.')
    hook = sentences[0].strip() + '.'

    # X 알고리즘 최적화: 훅은 그 자체로 완결성 있어야 함
    tweet1 = f"""{title}

{hook}

🧵"""

    # 280자 체크
    if len(tweet1) > 280:
        # 제목만으로 임팩트
        if len(title) < 250:
            tweet1 = f"""{title}

🧵"""
        else:
            title_short = title[:240]
            tweet1 = f"""{title_short}...

🧵"""

    tweets.append(tweet1)

    # 트윗 2: 상세 내용 (읽기 쉽게 줄바꿈)
    detail_parts = []

    # 추가 문장
    if len(sentences) > 1:
        detail_parts.append(sentences[1].strip() + '.')

    # 핵심 포인트 (최대 2개)
    if top_news['points']:
        detail_parts.append("")  # 공백 라인
        for point in top_news['points'][:2]:
            detail_parts.append(point)

    tweet2 = '\n'.join(detail_parts)

    # 280자 체크
    if len(tweet2) > 280:
        # 첫 문장 + 포인트 1개만
        tweet2 = detail_parts[0] if detail_parts else ""
        if top_news['points']:
            tweet2 += f"\n\n{top_news['points'][0][:150]}"

    if tweet2.strip():
        tweets.append(tweet2.strip())

    # 나머지 주요 뉴스 (간결하게)
    for news in data['major_news'][1:]:
        title = news['title_kr']
        sentences = news['content'].split('.')

        # 핵심 1문장
        content = sentences[0].strip() + '.'

        tweet = f"""{title}

{content}"""

        # 여유 있으면 포인트 1개 추가
        if len(tweet) < 200 and news['points']:
            first_point = news['points'][0]
            if len(tweet) + len(first_point) < 270:
                tweet += f"\n\n{first_point}"

        # 280자 초과시 축약
        if len(tweet) > 280:
            # 제목 + 짧은 요약
            short_content = sentences[0].strip()[:140] + '...'
            tweet = f"""{title}

{short_content}"""

        tweets.append(tweet)

    # 마이너 발견 (간단히)
    if data['minor_discoveries']:
        minor_items = []
        for disc in data['minor_discoveries'][:3]:
            minor_items.append(disc['title'][:65])

        tweet_minor = "그 외 주목할 소식:\n\n" + '\n'.join(f"• {item}" for item in minor_items)

        if len(tweet_minor) > 280:
            # 2개만
            tweet_minor = "그 외:\n\n" + '\n'.join(f"• {item}" for item in minor_items[:2])

        tweets.append(tweet_minor)

    # 한줄 요약
    if data['summary']:
        summary = data['summary'].strip()

        # 간결하게
        if len(summary) > 250:
            summary = summary[:250].strip() + '...'

        tweet_summary = summary

        tweets.append(tweet_summary)

    # 원문 링크 (마지막 트윗)
    link_parts = []

    # 각 뉴스에서 출처 링크 추출
    for news in data['major_news'][:3]:
        source_info = extract_source_link(news)
        if source_info:
            link_parts.append(f"→ {source_info['link']}")

    if link_parts:
        # 최대 2개 링크
        links_text = '\n'.join(link_parts[:2])
        tweet_final = f"""원문은 여기서:

{links_text}

전체 리포트
github.com/leaf468/ai-trends-kr"""

        # 280자 초과시 링크만
        if len(tweet_final) > 280:
            tweet_final = f"""원문:
{link_parts[0]}

github.com/leaf468/ai-trends-kr"""
    else:
        # 링크가 없으면 레포만
        tweet_final = """전체 리포트:
github.com/leaf468/ai-trends-kr

매일 6회 업데이트 중"""

    tweets.append(tweet_final)

    return '\n\n---\n\n'.join(tweets)


def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("사용법: python format_to_sns.py <마크다운_파일_경로>")
        print("예시: python format_to_sns.py reports/20260311-1246.md")
        sys.exit(1)

    input_file = sys.argv[1]

    if not Path(input_file).exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    print(f"📖 리포트 읽는 중: {input_file}")
    content = read_markdown_report(input_file)

    print("🔍 리포트 파싱 중...")
    data = parse_report(content)

    # 출력 파일명 생성
    input_path = Path(input_file)
    base_name = input_path.stem  # 확장자 제외한 파일명
    output_dir = input_path.parent

    # Threads 버전 생성
    print("📱 Threads 버전 생성 중...")
    threads_content = format_to_threads(data)
    threads_file = output_dir / f"{base_name}-threads.txt"
    with open(threads_file, 'w', encoding='utf-8') as f:
        f.write(threads_content)
    print(f"✅ Threads 버전 저장: {threads_file}")

    # Twitter 버전 생성
    print("🐦 Twitter 스레드 생성 중...")
    twitter_content = format_to_twitter(data)
    twitter_file = output_dir / f"{base_name}-twitter.txt"
    with open(twitter_file, 'w', encoding='utf-8') as f:
        f.write(twitter_content)
    print(f"✅ Twitter 버전 저장: {twitter_file}")

    print("\n🎉 변환 완료!")
    print(f"   - 원본: {input_file}")
    print(f"   - Threads: {threads_file}")
    print(f"   - Twitter: {twitter_file}")


if __name__ == '__main__':
    main()
