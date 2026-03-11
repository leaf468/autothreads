# AI 트렌드 리포터 스킬

이 스킬은 최신 AI/ML 트렌드를 수집하고 한글 보고서를 생성합니다.

## 검색 소스

### 메이저 소스 (2-3개)
- Hacker News (news.ycombinator.com)
- Reddit (r/MachineLearning, r/artificial)
- ArXiv (최신 AI/ML 논문)
- TechCrunch AI

### 마이너 소스 (2-3개)
- GitHub Trending (AI 프로젝트)
- Hugging Face (새 모델)
- ProductHunt AI
- 개인 연구 블로그

## 출력 형식

파일명: `reports/YYYYMMDD-HHMM.md`

```markdown
# 🤖 AI 트렌드 리포트

**발행 시각:** YYYY-MM-DD HH:MM KST
**수집 기간:** 최근 6시간

---

## 📰 주요 뉴스 (3-4개)

### 1. [재미있는 한글 제목]

> **원제:** [English Title]
> **출처:** [작성자/매체](URL)
> **발행:** YYYY-MM-DD

[기사 내용을 재미있고 이해하기 쉽게 한글로 요약. 3-5문단]

**💡 핵심 포인트**
- 포인트 1
- 포인트 2
- 포인트 3

**🤔 추가 인사이트**
[업계 영향, 한국 관점 등 분석]

![이미지](URL)
*출처: [매체](URL)*

---

## 🔍 마이너 발견 (3-4개)

### 1. [발견]

> **출처:** [GitHub/블로그](URL)

[메이저 미디어가 다루지 않은 흥미로운 내용]

**왜 주목할까?**
[설명]

---

## 📊 오늘의 한마디

[AI 트렌드 한 문장 요약]

---

*🤖 [DeepAgents](https://github.com/langchain-ai/deepagents)로 자동 생성*
*🎨 Gemini Imagen 3로 이미지 생성*
```

## 썸네일 프롬프트

`thumbnail_prompt.txt` 파일 생성:

```
[오늘의 트렌드를 시각화하는 영문 프롬프트]
예: "A futuristic AI laboratory with neural networks, vibrant colors, digital art"
```

## 규칙

1. **한글 우선**: 모든 외국 기사는 자연스러운 한글로
2. **재미있게**: 딱딱한 번역 금지
3. **출처 필수**: 모든 정보에 원문 링크
4. **균형**: 메이저 3-4개 + 마이너 3-4개
5. **중복 방지**: `reports/` 폴더의 이전 파일 확인
6. **신선도**: 최근 6시간 이내 우선
7. **이미지**: 원본 이미지 URL 포함
8. **썸네일**: thumbnail_prompt.txt 필수 생성

## 실행 순서

1. `ls reports/` - 기존 보고서 확인
2. 최근 2-3개 파일 읽어서 중복 체크
3. 웹 검색 (Hacker News, Reddit 등)
4. 보고서 작성
5. thumbnail_prompt.txt 생성
