# Quick Start Guide

YouTube Analysis Agent를 5분 안에 시작하는 방법

## 1. 설치

```bash
cd youtube-analysis-agent

# 가상 환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 2. API 키 설정

### Gemini API 키 발급
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. "Get API Key" 클릭
3. API 키 복사

### Anthropic API 키 발급
1. [Anthropic Console](https://console.anthropic.com/) 접속
2. API Keys 메뉴에서 새 키 생성
3. API 키 복사

### 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
# GEMINI_API_KEY=your_actual_gemini_api_key
# ANTHROPIC_API_KEY=your_actual_anthropic_api_key
```

## 3. 첫 번째 분석 실행

```bash
# YouTube 영상 분석
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 4. 다양한 분석 시도

```bash
# 감성 분석
python main.py analyze "VIDEO_URL" --type sentiment

# 요약
python main.py analyze "VIDEO_URL" --type summary

# 암호화폐 분석 (암호화폐 관련 영상인 경우)
python main.py analyze "VIDEO_URL" --type crypto

# 커스텀 프롬프트
python main.py custom "VIDEO_URL" --prompt "이 영상의 핵심 메시지를 3가지로 정리해주세요."
```

## 5. Claude Code 연동 (선택)

프로젝트 루트에 `.mcp.json` 파일이 있어 Claude Code에서 "CLI에서 열기" 버튼이 활성화됩니다.

### 5.1. 환경 변수 설정

```bash
# .env 파일 생성 (아직 안 했다면)
cp .env.example .env

# .env 파일 편집하여 실제 API 키 입력
```

### 5.2. Claude Code에서 사용

1. **Claude Code 웹에서 프로젝트 열기**
2. **"CLI에서 열기" 버튼 클릭** (이제 활성화됨!)
3. **대화로 YouTube 분석:**
   ```
   이 YouTube 영상 분석해줘:
   https://www.youtube.com/watch?v=VIDEO_ID
   ```

Claude가 자동으로 `analyze_youtube_video` 도구를 사용하여 분석합니다.

## 6. 결과 확인

분석 결과는 `output/` 디렉토리에 JSON 파일로 저장됩니다.

```bash
# 결과 확인
ls -lh output/
```

## Python 코드로 사용

```python
from src.agent import YouTubeAnalysisAgent
import os

agent = YouTubeAnalysisAgent(
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

results = agent.analyze_video(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    analysis_type="comprehensive"
)

print(agent.get_summary_report(results))
```

## 문제 해결

### API 키 오류
```bash
# 설정 확인
python main.py config
```

### 자막을 찾을 수 없음
- 영상에 자막이 없는 경우 Gemini API 사용 시도:
  ```bash
  python main.py analyze "URL" --use-gemini
  ```

### 모듈을 찾을 수 없음
```bash
# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

## 다음 단계

- 전체 문서: [README.md](README.md)
- 예제 코드: [examples/basic_usage.py](examples/basic_usage.py)
- 설정 커스터마이징: [config/settings.py](config/settings.py)

## 팁

1. **비용 절약**: Transcript API 사용 (`--use-transcript`)
2. **정확도 향상**: Gemini API 사용 (`--use-gemini`)
3. **암호화폐 영상**: `--type crypto` 사용
4. **배치 처리**: Python 스크립트로 여러 영상 동시 분석

Happy Analyzing! 🎥✨
