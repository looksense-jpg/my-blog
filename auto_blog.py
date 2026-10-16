from google import genai
import sys
import os
from datetime import datetime

# ========== 설정 ==========
# YOUR_GEMINI_KEY 부분을 본인 키로 교체하세요
client = genai.Client(api_key="AIzaSyB6Q0yg1-DumVVGm4oYKpymMVl0IO-KlCI")

# ========== 입력 ==========
if len(sys.argv) < 2:
    print("사용법: python auto_blog.py \"키워드\"")
    print("예시: python auto_blog.py \"재택근무 키보드 추천\"")
    sys.exit(1)

키워드 = sys.argv[1]

파일명 = input("영문 파일명 입력 (예: keyboard-review): ").strip()
if not 파일명:
    파일명 = "post-" + datetime.now().strftime("%Y%m%d%H%M")

# ========== AI에게 글 생성 요청 ==========
프롬프트 = f"""
'{키워드}'에 대한 커뮤니티 Q&A 형식의 블로그 글을 작성하세요.

형식 (이 형식을 정확히 지켜주세요):

---
title: "{키워드}"
description: "재택근무자를 위한 {키워드} 정보"
pubDate: {datetime.now().strftime('%Y-%m-%d')}
---

<div class="qa-container">

<div class="question">
<div class="author">재택러_김대리</div>
<div class="content">
{키워드}에 대해 질문이 있습니다. 현재 상황과 예산을 함께 알려드립니다.
</div>
<div class="meta">2026-10-17</div>
</div>

<div class="answer accepted-answer">
<div class="author">모니터박사</div>
<div class="content">
(첫 번째 추천 - 가장 좋은 선택)

<a href="쿠팡링크1" class="cta-button" target="_blank" rel="noopener">👉 쿠팡 최저가 확인</a>
</div>
<div class="meta">2026-10-17 · 채택된 답변</div>
</div>

<div class="answer">
<div class="author">가성비헌터</div>
<div class="content">
(두 번째 추천 - 가성비)

<a href="쿠팡링크2" class="cta-button" target="_blank" rel="noopener">👉 쿠팡 최저가 확인</a>
</div>
<div class="meta">2026-10-17</div>
</div>

<div class="answer">
<div class="author">절약왕</div>
<div class="content">
(세 번째 추천 - 저가형)

<a href="쿠팡링크3" class="cta-button" target="_blank" rel="noopener">👉 쿠팡 최저가 확인</a>
</div>
<div class="meta">2026-10-17</div>
</div>

</div>

조건:
- 각 답변은 3~5문장
- 구체적인 제품명과 특징 포함
- 실제 한국어 커뮤니티 톤 (친근하고 캐주얼)
- 쿠팡링크1, 쿠팡링크2, 쿠팡링크3는 그대로 유지 (나중에 교체할 것)
- frontmatter의 pubDate는 오늘 날짜
"""

print("🤖 AI가 글을 생성 중...")

응답 = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=프롬프트
)

결과 = 응답.text

# ========== 파일로 저장 ==========
경로 = f"src/content/blog/{파일명}.md"

with open(경로, "w", encoding="utf-8") as f:
    f.write(결과)

print(f"✅ 생성 완료: {경로}")
print(f"👉 다음: 파일을 열어서 '쿠팡링크1', '쿠팡링크2', '쿠팡링크3'을 실제 링크로 교체하세요.")