# YouTube Analysis Agent - Architecture

## 시스템 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    YouTube Analysis Agent                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │    1. Gemini API (YouTube 처리)       │
        │    - 스크립트/자막 추출                │
        │    - 카테고리 자동 분류                │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │    2. Prompt Manager                  │
        │    - 카테고리별 프롬프트 선택          │
        │    - 분석 유형별 템플릿 적용          │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │    3. Claude API (분석)               │
        │    - 카테고리별 최적화 분석           │
        │    - JSON 형식 결과 반환              │
        └──────────────────────────────────────┘
```

## 워크플로우

### 1. 콘텐츠 추출 및 분류 (Gemini)

```python
# YouTubeExtractor
video_url → Gemini API → {
    "transcript": "전체 스크립트...",
    "category": "crypto",  # 자동 분류
    "confidence": 95,
    "metadata": {...}
}
```

**지원 카테고리:**
- `crypto`: 암호화폐/블록체인
- `finance`: 금융/투자
- `tech`: 기술/IT
- `news`: 뉴스/시사
- `business`: 비즈니스/창업
- `education`: 교육/강의
- `general`: 일반

### 2. 프롬프트 선택 (PromptManager)

```python
# PromptManager
category + analysis_type → 적절한 프롬프트 템플릿

예: crypto + comprehensive → crypto 특화 종합 분석 프롬프트
예: finance + sentiment → 금융 시장 심리 분석 프롬프트
```

**프롬프트 템플릿 위치:**
`config/prompts.yaml`

### 3. 분석 실행 (Claude)

```python
# ContentAnalyzer
transcript + category_prompt → Claude API → {
    "analysis": "분석 결과...",
    "category": "crypto",
    "analysis_type": "comprehensive",
    "usage": {...}
}
```

## 주요 컴포넌트

### YouTubeExtractor (`src/youtube_extractor.py`)

**역할:**
- YouTube 영상 스크립트 추출
- 영상 카테고리 자동 분류

**메서드:**
- `extract_with_gemini(url, classify=True)`: Gemini로 추출 + 분류
- `get_transcript(url)`: youtube-transcript-api로 자막 추출 (백업)

### PromptManager (`src/prompt_manager.py`)

**역할:**
- 카테고리별 프롬프트 템플릿 관리
- 동적 프롬프트 생성

**메서드:**
- `get_prompt(category, analysis_type, content)`: 프롬프트 생성
- `get_categories()`: 사용 가능한 카테고리 목록
- `add_custom_prompt(category, type, template)`: 프롬프트 추가

### ContentAnalyzer (`src/content_analyzer.py`)

**역할:**
- Claude API로 콘텐츠 분석
- 구조화된 결과 반환

**메서드:**
- `analyze_with_custom_prompt(content, prompt)`: 커스텀 프롬프트로 분석

### YouTubeAnalysisAgent (`src/agent.py`)

**역할:**
- 전체 워크플로우 통합 관리
- 결과 저장 및 리포팅

**메서드:**
- `analyze_video(url, analysis_type, category_override)`: 영상 분석
- `analyze_with_custom_prompt(url, prompt)`: 커스텀 분석

## 프롬프트 시스템

### 프롬프트 구조 (`config/prompts.yaml`)

```yaml
categories:
  crypto:
    name: "암호화폐/블록체인"
    keywords: ["비트코인", "이더리움", ...]

prompts:
  crypto:
    comprehensive: |
      암호화폐 투자자 관점에서 분석...
      1. 언급된 암호화폐
      2. 시장 분석
      3. 투자 시그널
      ...
    sentiment: |
      시장 심리 분석...
```

### 프롬프트 추가/수정

**방법 1: YAML 직접 수정**
```yaml
prompts:
  crypto:
    my_analysis: |
      커스텀 분석 프롬프트...
```

**방법 2: Python 코드**
```python
from src.prompt_manager import PromptManager

pm = PromptManager()
pm.add_custom_prompt(
    category="crypto",
    analysis_type="my_analysis",
    prompt_template="커스텀 프롬프트...",
    save=True  # YAML에 저장
)
```

## 확장성

### 새로운 카테고리 추가

1. `config/prompts.yaml`에 카테고리 추가:
```yaml
categories:
  new_category:
    name: "새 카테고리"
    description: "설명"
    keywords: ["키워드1", "키워드2"]

prompts:
  new_category:
    comprehensive: |
      프롬프트 템플릿...
```

2. `src/youtube_extractor.py`의 Gemini 분류 프롬프트에 추가:
```python
- new_category: 새 카테고리 (설명)
```

### 새로운 분석 유형 추가

`config/prompts.yaml`에 분석 유형 추가:
```yaml
prompts:
  crypto:
    new_analysis_type: |
      새로운 분석 프롬프트...
```

사용:
```python
agent.analyze_video(url, analysis_type="new_analysis_type")
```

## MCP 서버 통합

MCP 서버(`mcp-server/server.py`)는 자동으로 카테고리 기반 분석을 사용합니다:

```
User: "이 YouTube 영상 분석해줘: URL"
  ↓
MCP Server → YouTubeAnalysisAgent
  ↓
Gemini: 스크립트 추출 + 카테고리 분류
  ↓
PromptManager: 카테고리별 프롬프트 선택
  ↓
Claude: 최적화된 분석
  ↓
User: 결과 표시
```

## 데이터 흐름

```
Input: YouTube URL
  ↓
[Gemini] Extract + Classify
  ↓
{
  transcript: "...",
  category: "crypto",
  confidence: 95
}
  ↓
[PromptManager] Select Prompt
  ↓
prompt_template + transcript
  ↓
[Claude] Analyze
  ↓
{
  analysis: "...",
  category: "crypto",
  analysis_type: "comprehensive"
}
  ↓
Output: Analysis Results (JSON + Report)
```

## 성능 최적화

### 비용 절감
- Transcript API 사용: `use_gemini_extraction=False`
- 카테고리 분류 비활성화: `classify=False` (일반 프롬프트 사용)

### 정확도 향상
- Gemini API 사용: `use_gemini_extraction=True`
- 카테고리별 특화 프롬프트 활용
- 카테고리 수동 지정: `category_override="crypto"`

## 예제

### 기본 사용
```python
agent = YouTubeAnalysisAgent(gemini_key, claude_key)

# 자동 분류 + 카테고리별 분석
result = agent.analyze_video("https://youtube.com/watch?v=...")
# → Gemini가 'crypto'로 분류
# → crypto 특화 프롬프트로 Claude 분석
```

### 카테고리 강제 지정
```python
result = agent.analyze_video(
    "https://youtube.com/watch?v=...",
    category_override="finance"  # 금융 분석 프롬프트 강제 사용
)
```

### 커스텀 프롬프트
```python
result = agent.analyze_with_custom_prompt(
    "https://youtube.com/watch?v=...",
    "이 영상에서 투자 리스크만 정리해줘"
)
```

## 테스트

```bash
# 프롬프트 매니저 테스트
python -c "from src.prompt_manager import PromptManager; pm = PromptManager(); print(pm.get_categories())"

# 전체 워크플로우 테스트
python main.py analyze "VIDEO_URL"
```
