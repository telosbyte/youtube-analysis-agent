# YouTube Analysis MCP Server

Claude Desktop과 Claude Code에서 YouTube 영상을 분석할 수 있는 MCP(Model Context Protocol) 서버입니다.

## 개요

이 MCP 서버를 사용하면 Claude와 대화하면서 바로 YouTube 영상을 분석할 수 있습니다:
- Claude Desktop에서 대화 중 YouTube 분석
- Claude Code에서 코딩 중 YouTube 분석
- 별도의 CLI 실행 없이 자연스러운 대화로 분석

## 제공 도구

### 1. `analyze_youtube_video`
YouTube 영상을 분석합니다.

**파라미터:**
- `video_url` (필수): YouTube 영상 URL
- `analysis_type` (선택): 분석 유형
  - `comprehensive`: 종합 분석 (기본값)
  - `sentiment`: 감성 분석
  - `summary`: 요약
  - `key_points`: 핵심 포인트
  - `crypto`: 암호화폐 분석
- `use_gemini` (선택): Gemini API 사용 여부 (기본: true)

**예시:**
```
"이 YouTube 영상을 분석해줘: https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. `analyze_youtube_custom`
커스텀 프롬프트로 YouTube 영상을 분석합니다.

**파라미터:**
- `video_url` (필수): YouTube 영상 URL
- `custom_prompt` (필수): 커스텀 분석 프롬프트
- `use_gemini` (선택): Gemini API 사용 여부

**예시:**
```
"이 YouTube 영상에서 투자 전략만 정리해줘: https://www.youtube.com/watch?v=VIDEO_ID"
```

### 3. `get_youtube_transcript`
YouTube 영상의 자막만 추출합니다.

**파라미터:**
- `video_url` (필수): YouTube 영상 URL
- `language` (선택): 자막 언어 코드 (기본: 'ko')

**예시:**
```
"이 YouTube 영상의 자막을 가져와줘: https://www.youtube.com/watch?v=VIDEO_ID"
```

## 설치 및 설정

### 1. 의존성 설치

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

`.env` 파일:
```env
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. MCP 서버 테스트

```bash
python server.py
```

## Claude Desktop 연동

### macOS/Linux

`~/Library/Application Support/Claude/claude_desktop_config.json` 편집:

```json
{
  "mcpServers": {
    "youtube-analysis": {
      "command": "python",
      "args": ["/home/user/youtube-analysis-agent/mcp-server/server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key",
        "ANTHROPIC_API_KEY": "your_anthropic_api_key"
      }
    }
  }
}
```

### Windows

`%APPDATA%\Claude\claude_desktop_config.json` 편집:

```json
{
  "mcpServers": {
    "youtube-analysis": {
      "command": "python",
      "args": ["C:\\path\\to\\youtube-analysis-agent\\mcp-server\\server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key",
        "ANTHROPIC_API_KEY": "your_anthropic_api_key"
      }
    }
  }
}
```

### 사용 방법

Claude Desktop을 재시작한 후:

```
안녕 Claude! 이 YouTube 영상 분석해줄래?
https://www.youtube.com/watch?v=dQw4w9WgXcQ

암호화폐 관련 내용을 중심으로 분석해줘.
```

## Claude Code 연동

### 설정 파일 경로

`.claude/settings.json` 또는 프로젝트 루트의 `.mcp.json`:

```json
{
  "mcpServers": {
    "youtube-analysis": {
      "command": "python",
      "args": ["/home/user/youtube-analysis-agent/mcp-server/server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key",
        "ANTHROPIC_API_KEY": "your_anthropic_api_key"
      }
    }
  }
}
```

### 사용 방법

Claude Code에서 대화 중:

```
이 YouTube 영상 요약해줘:
https://www.youtube.com/watch?v=VIDEO_ID

핵심 포인트 3가지만 추려서 알려줘.
```

## 사용 예시

### 예시 1: 종합 분석

```
User: 이 암호화폐 뉴스 영상 분석해줘
      https://www.youtube.com/watch?v=CRYPTO_NEWS_ID

Claude: (analyze_youtube_video 도구 사용)

        분석 결과:
        - 핵심 주제: 비트코인 ETF 승인 관련 뉴스
        - 주요 내용: ...
        - 시장 전망: 상승세 예상
        ...
```

### 예시 2: 커스텀 분석

```
User: 이 영상에서 투자 리스크만 정리해줘
      https://www.youtube.com/watch?v=VIDEO_ID

Claude: (analyze_youtube_custom 도구 사용)

        투자 리스크 분석:
        1. 시장 변동성 높음
        2. 규제 불확실성
        3. ...
```

### 예시 3: 자막 추출

```
User: 이 영상 자막 텍스트만 가져와줘
      https://www.youtube.com/watch?v=VIDEO_ID

Claude: (get_youtube_transcript 도구 사용)

        자막 내용:
        안녕하세요. 오늘은 암호화폐 시장에 대해...
        ...
```

## 장점

### 기존 CLI 방식
```bash
python main.py analyze "URL" --type crypto
# 결과 확인
cat output/result.json
```

### MCP 서버 방식
```
"이 암호화폐 영상 분석해줘: URL"
→ Claude가 자동으로 분석하고 대화로 설명
→ 추가 질문 가능
"투자하기 좋을까?"
→ Claude가 분석 결과 기반으로 답변
```

## 문제 해결

### MCP 서버가 시작되지 않음
- Python 경로 확인
- 의존성 설치 확인: `pip install -r requirements.txt`
- 로그 확인: `mcp_server.log`

### API 키 오류
- `.env` 파일 확인
- MCP 설정의 `env` 섹션에 API 키 확인

### 도구가 보이지 않음
- Claude Desktop/Code 재시작
- MCP 설정 파일 경로 확인
- JSON 문법 오류 확인

## 로그

MCP 서버 로그는 `mcp_server.log`에 저장됩니다.

```bash
tail -f mcp_server.log
```

## 개발

### 새로운 도구 추가

`server.py`에서:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # 기존 도구...
        Tool(
            name="your_new_tool",
            description="도구 설명",
            inputSchema={...}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    if name == "your_new_tool":
        # 도구 로직
        pass
```

## 라이선스

MIT License

## 관련 링크

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/download)
- [YouTube Analysis Agent](../README.md)
