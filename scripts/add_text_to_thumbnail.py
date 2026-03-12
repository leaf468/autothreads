#!/usr/bin/env python3
"""
썸네일 이미지에 요약 텍스트 오버레이 추가
Instagram 포스팅용으로 이미지 상단에 "오늘의 한마디"를 추가합니다.
"""

import os
import sys
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Tuple


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
    """
    텍스트를 주어진 너비에 맞게 줄바꿈

    Args:
        text: 원본 텍스트
        font: PIL 폰트 객체
        max_width: 최대 너비 (픽셀)

    Returns:
        줄바꿈된 텍스트 리스트
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # 단어 자체가 너무 긴 경우
                lines.append(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def add_text_overlay(image_path: str, text: str, output_path: str,
                     position: str = 'top') -> str:
    """
    이미지에 텍스트 오버레이 추가

    Args:
        image_path: 원본 이미지 경로
        text: 오버레이할 텍스트
        output_path: 출력 이미지 경로
        position: 텍스트 위치 ('top' 또는 'bottom')

    Returns:
        생성된 이미지 경로
    """
    # 이미지 열기
    img = Image.open(image_path)
    width, height = img.size

    # Draw 객체 생성
    draw = ImageDraw.Draw(img, 'RGBA')

    # 폰트 설정
    font_size = int(height * 0.04)  # 이미지 높이의 4%
    try:
        # 시스템 폰트 경로 시도
        font_paths = [
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # macOS
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",  # Linux
            "C:\\Windows\\Fonts\\malgun.ttf",  # Windows
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
        ]

        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break

        if font is None:
            # 폰트를 찾지 못한 경우 기본 폰트 사용
            print("⚠️  시스템 폰트를 찾지 못했습니다. 기본 폰트 사용")
            font = ImageFont.load_default()

    except Exception as e:
        print(f"⚠️  폰트 로딩 실패: {e}, 기본 폰트 사용")
        font = ImageFont.load_default()

    # 텍스트 줄바꿈
    max_text_width = int(width * 0.85)  # 이미지 너비의 85%
    lines = wrap_text(text, font, max_text_width)

    # 각 줄의 높이 계산
    line_height = font_size + 10
    total_text_height = len(lines) * line_height + 40  # 패딩 포함

    # 배경 박스 위치 및 크기
    if position == 'top':
        box_y = 0
    else:  # bottom
        box_y = height - total_text_height

    # 반투명 배경 그리기
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # 그라데이션 효과를 위한 배경
    for i in range(total_text_height):
        alpha = int(180 * (1 - i / total_text_height * 0.3))  # 180에서 시작해서 점점 투명
        if position == 'top':
            y_pos = i
        else:
            y_pos = box_y + i

        overlay_draw.rectangle(
            [(0, y_pos), (width, y_pos + 1)],
            fill=(0, 0, 0, alpha)
        )

    # 오버레이 합성
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(img)

    # 텍스트 그리기
    y_offset = 20 if position == 'top' else box_y + 20

    for line in lines:
        # 텍스트 중앙 정렬을 위한 너비 계산
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2

        # 텍스트에 외곽선 효과 (가독성 향상)
        outline_range = 2
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y_offset + adj_y), line,
                         font=font, fill=(0, 0, 0, 200))

        # 실제 텍스트
        draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 255))

        y_offset += line_height

    # RGB로 변환 후 저장
    img = img.convert('RGB')
    img.save(output_path, quality=95)

    return output_path


def get_summary_from_report(report_path: str) -> str:
    """
    마크다운 리포트에서 "오늘의 한마디" 추출

    Args:
        report_path: 마크다운 리포트 파일 경로

    Returns:
        오늘의 한마디 텍스트
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 오늘의 한마디 추출
    summary_match = re.search(r'## 📊 오늘의 한마디\n\n(.+?)(?=\n---|\Z)', content, re.DOTALL)

    if summary_match:
        return summary_match.group(1).strip()
    else:
        return "AI 트렌드를 한눈에!"


def main():
    """메인 실행 함수"""
    if len(sys.argv) < 3:
        print("사용법: python add_text_to_thumbnail.py <썸네일_이미지> <리포트_마크다운>")
        print("예시: python add_text_to_thumbnail.py reports/images/20260311-1246-thumbnail.png reports/20260311-1246.md")
        sys.exit(1)

    thumbnail_path = sys.argv[1]
    report_path = sys.argv[2]

    if not os.path.exists(thumbnail_path):
        print(f"❌ 썸네일 이미지를 찾을 수 없습니다: {thumbnail_path}")
        sys.exit(1)

    if not os.path.exists(report_path):
        print(f"❌ 리포트 파일을 찾을 수 없습니다: {report_path}")
        sys.exit(1)

    print(f"🖼️  원본 이미지: {thumbnail_path}")
    print(f"📄 리포트: {report_path}")

    # 요약 텍스트 추출
    summary_text = get_summary_from_report(report_path)
    print(f"\n📝 오버레이 텍스트:\n{summary_text}\n")

    # 출력 경로 생성
    thumbnail_path_obj = Path(thumbnail_path)
    output_path = thumbnail_path_obj.parent / f"{thumbnail_path_obj.stem}-instagram{thumbnail_path_obj.suffix}"

    # 텍스트 오버레이 추가
    print("🎨 텍스트 오버레이 추가 중...")
    result_path = add_text_overlay(thumbnail_path, summary_text, str(output_path), position='top')

    print(f"✅ Instagram용 이미지 생성 완료!")
    print(f"   {result_path}")


if __name__ == '__main__':
    main()
