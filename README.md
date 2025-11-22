# YouTube Analysis Agent

AI 기반 YouTube 콘텐츠 분석 도구

## 개요

YouTube Analysis Agent는 Gemini API와 Claude API를 활용하여 YouTube 영상의 자막/스크립트를 추출하고 심층 분석하는 도구입니다.

## 주요 기능

### 1. 콘텐츠 추출
- **Gemini API**: YouTube URL에서 직접 콘텐츠 추출 (멀티모달 기능 활용)
- **Transcript API**: 자막 데이터 직접 추출 (백업 방식)

### 2. AI 기반 분석 (Claude)
- **종합 분석**: 핵심 주제, 주요 내용, 감성, 타겟 청중, 실행 가능한 인사이트
- **감성 분석**: 긍정/부정/중립 판단, 감정 키워드, 톤 분석
- **요약**: 3줄 요약, 상세 요약, 핵심 키워드
- **핵심 포인트**: 주요 논점, 데이터/통계, 인용문, 결론
- **암호화폐 분석**: 언급 코인, 시장 전망, 투자 시그널, 리스크 요인 (특화 기능)

### 3. 커스텀 분석
- 사용자 정의 프롬프트로 맞춤형 분석 가능

## 설치

```bash
# 저장소 클론
cd youtube-analysis-agent

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어서 API 키 입력
```

## 환경 설정

`.env` 파일에 다음 API 키를 설정하세요:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### API 키 발급

- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Anthropic API**: [Anthropic Console](https://console.anthropic.com/)

## 사용법

### CLI 인터페이스

#### 기본 분석

```bash
# 종합 분석 (기본)
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID"

# 감성 분석
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID" --type sentiment

# 요약
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID" --type summary

# 핵심 포인트
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID" --type key_points

# 암호화폐 분석
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID" --type crypto
```

#### 커스텀 분석

```bash
python main.py custom "https://www.youtube.com/watch?v=VIDEO_ID" \
  --prompt "이 영상에서 언급된 투자 전략을 정리하고, 각 전략의 장단점을 분석해주세요."
```

#### 추출 방식 선택

```bash
# Gemini API 사용 (기본)
python main.py analyze "URL" --use-gemini

# Transcript API 사용 (백업)
python main.py analyze "URL" --use-transcript
```

#### 설정 확인

```bash
python main.py config
```

### Python 코드로 사용

```python
from src.agent import YouTubeAnalysisAgent

# Agent 초기화
agent = YouTubeAnalysisAgent(
    gemini_api_key="your_gemini_key",
    anthropic_api_key="your_anthropic_key"
)

# 영상 분석
results = agent.analyze_video(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    analysis_type="comprehensive"
)

# 결과 출력
print(agent.get_summary_report(results))

# 커스텀 분석
custom_results = agent.analyze_with_custom_prompt(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    custom_prompt="이 영상의 핵심 메시지를 3가지로 요약해주세요."
)
```

## 프로젝트 구조

```
youtube-analysis-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py              # 메인 에이전트
│   ├── youtube_extractor.py  # YouTube 콘텐츠 추출
│   └── content_analyzer.py   # Claude 기반 분석
├── config/
│   └── settings.py           # 설정 관리
├── tests/                    # 테스트
├── output/                   # 분석 결과 저장
├── main.py                   # CLI 인터페이스
├── requirements.txt          # 의존성
├── .env.example             # 환경 변수 예시
└── README.md                # 문서
```

## 분석 결과

분석 결과는 `output/` 디렉토리에 JSON 형식으로 저장됩니다:

```json
{
  "video_url": "https://www.youtube.com/watch?v=...",
  "timestamp": "2025-11-22T10:30:00",
  "extraction": {
    "method": "gemini_multimodal",
    "gemini_analysis": "..."
  },
  "analysis": {
    "analysis_type": "comprehensive",
    "analysis": "...",
    "model": "claude-sonnet-4-5-20250929",
    "usage": {
      "input_tokens": 1500,
      "output_tokens": 800
    }
  }
}
```

## 분석 유형별 출력

### 1. Comprehensive (종합 분석)
- 핵심 주제
- 주요 내용 (구조화)
- 감성 분석
- 타겟 청중
- 핵심 메시지
- 실행 가능한 인사이트

### 2. Sentiment (감성 분석)
- 전반적인 감성 (긍정/부정/중립 + 점수)
- 감정 변화 추이
- 주요 감정 키워드
- 톤과 스타일

### 3. Summary (요약)
- 3줄 요약
- 상세 요약 (200-300자)
- 핵심 키워드 (5-10개)

### 4. Key Points (핵심 포인트)
- 주요 논점
- 중요한 데이터/통계
- 인용문 및 강조 내용
- 결론 및 행동 요청사항

### 5. Crypto (암호화폐 분석)
- 언급된 암호화폐
- 시장 전망 (상승/하락/중립 + 근거)
- 투자 시그널 (매수/매도/보유)
- 리스크 요인
- 기술적 분석
- 펀더멘털 분석
- 신뢰도 평가 (0-100)

## 기술 스택

- **Python 3.9+**
- **Gemini API**: YouTube 콘텐츠 추출
- **Claude API (Sonnet 4.5)**: 콘텐츠 분석
- **youtube-transcript-api**: 자막 추출 (백업)
- **Click**: CLI 인터페이스
- **Rich**: 터미널 UI
- **Pydantic**: 설정 관리

## 라이선스

MIT License

## 문의

이슈나 기능 요청은 GitHub Issues를 통해 제출해주세요.
