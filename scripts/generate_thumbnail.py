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
        # Gemini Imagen 3 사용
        # 참고: API는 버전에 따라 변경될 수 있음
        model = genai.ImageGenerationModel("imagen-3.0-generate-001")

        result = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            safety_filter_level="block_some",
            person_generation="allow_adult",
            aspect_ratio="16:9",  # 썸네일에 적합한 비율
        )

        # 이미지 저장
        output_dir = Path("reports/images")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{timestamp}-thumbnail.png"

        # 첫 번째 이미지 저장
        image = result.images[0]
        image._pil_image.save(output_path)

        print(f"✅ Thumbnail saved to: {output_path}")
        print(f"📊 Image size: {image._pil_image.size}")

        # 메타데이터 저장
        metadata_path = output_dir / f"{timestamp}-metadata.txt"
        with open(metadata_path, "w") as f:
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Model: Gemini Imagen 3 (imagen-3.0-generate-001)\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Size: {image._pil_image.size}\n")
            f.write(f"Cost: $0.0033\n")

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
