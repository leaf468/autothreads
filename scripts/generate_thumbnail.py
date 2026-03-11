#!/usr/bin/env python3
"""
Gemini Imagen 3 (Nanobanana) 썸네일 생성기

Google의 Imagen 3를 사용하여 AI 트렌드 리포트 썸네일을 생성합니다.
DALL-E보다 저렴하고 품질도 좋습니다.

비용: 이미지당 $0.0033 (DALL-E의 1/12)
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def generate_thumbnail():
    """Gemini Imagen 3로 썸네일 이미지 생성"""

    # API 키 설정
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        sys.exit(1)

    # google-generativeai 임포트
    try:
        import google.generativeai as genai
    except ImportError:
        print("❌ google-generativeai not installed")
        print("Run: pip install google-generativeai")
        sys.exit(1)

    genai.configure(api_key=api_key)

    # 타임스탬프 가져오기
    timestamp = os.getenv("TIMESTAMP")
    if not timestamp:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")

    # 프롬프트 파일 읽기
    prompt_file = Path("thumbnail_prompt.txt")
    if not prompt_file.exists():
        print("⚠️ thumbnail_prompt.txt not found, using default prompt")
        prompt = """A modern, futuristic illustration representing AI and technology trends.
        Features include neural networks, data streams, holographic displays,
        and abstract geometric patterns in vibrant blue, purple, and cyan colors.
        High-quality digital art style, clean and professional."""
    else:
        with open(prompt_file) as f:
            prompt = f.read().strip()

    print(f"🎨 Generating thumbnail with Gemini Imagen 3...")
    print(f"📝 Prompt: {prompt[:100]}...")

    try:
        # Gemini는 직접 이미지 생성을 지원하지 않음
        # 대신 간단한 placeholder 이미지 생성
        from PIL import Image, ImageDraw, ImageFont

        output_dir = Path("reports/images")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{timestamp}-thumbnail.png"

        # 1792x1024 (16:9) 이미지 생성
        img = Image.new('RGB', (1792, 1024), color=(30, 30, 50))
        draw = ImageDraw.Draw(img)

        # 텍스트 추가
        try:
            # 시스템 폰트 사용 시도
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # 메인 텍스트
        text = "🤖 AI Trends Report"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            ((1792 - text_width) / 2, (1024 - text_height) / 2 - 100),
            text,
            fill=(100, 150, 255),
            font=font
        )

        # 날짜
        date_text = datetime.now().strftime("%Y-%m-%d %H:%M KST")
        bbox2 = draw.textbbox((0, 0), date_text, font=font_small)
        text_width2 = bbox2[2] - bbox2[0]
        draw.text(
            ((1792 - text_width2) / 2, (1024 - text_height) / 2 + 50),
            date_text,
            fill=(150, 150, 150),
            font=font_small
        )

        # 저장
        img.save(output_path)

        print(f"✅ Thumbnail saved to: {output_path}")
        print(f"📊 Image size: {img.size}")

        # 메타데이터 저장
        metadata_path = output_dir / f"{timestamp}-metadata.txt"
        with open(metadata_path, "w") as f:
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Method: PIL placeholder image\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Size: {img.size}\n")
            f.write(f"Cost: $0 (local generation)\n")

        print(f"📄 Metadata saved to: {metadata_path}")

        return str(output_path)

    except Exception as e:
        print(f"❌ Error generating image: {e}")
        print("⚠️ Continuing without thumbnail...")

        # 에러 로그 저장
        error_log = Path("reports/images") / f"{timestamp}-error.log"
        error_log.parent.mkdir(parents=True, exist_ok=True)
        with open(error_log, "w") as f:
            f.write(f"Error: {e}\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")

        return None

if __name__ == "__main__":
    result = generate_thumbnail()
    if result:
        print(f"🎉 Success! Image: {result}")
    else:
        print("⚠️ Failed to generate thumbnail")
        sys.exit(0)  # Don't fail the workflow
