#!/usr/bin/env python3
"""
YouTube Analysis MCP Server

Provides YouTube video analysis tools for Claude Desktop and Claude Code
"""
import os
import sys
import logging
import asyncio
from typing import Any, Sequence
from pathlib import Path

# Add parent directory to path to import src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from dotenv import load_dotenv
from src.youtube_extractor import YouTubeExtractor

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize YouTube extractor (only needs GEMINI_API_KEY)
try:
    extractor = YouTubeExtractor(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    )
    logger.info("YouTube Extractor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize extractor: {str(e)}")
    extractor = None

# Create MCP server
app = Server("youtube-analysis")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="extract_youtube_content",
            description=(
                "YouTube 영상의 스크립트를 추출하고 카테고리를 자동 분류합니다. "
                "분석은 Claude가 직접 수행합니다. "
                "카테고리: crypto(암호화폐), finance(금융), tech(기술), news(뉴스), "
                "business(비즈니스), education(교육), general(일반)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "YouTube 영상 URL (예: https://www.youtube.com/watch?v=VIDEO_ID)"
                    },
                    "classify": {
                        "type": "boolean",
                        "description": "카테고리 자동 분류 여부",
                        "default": True
                    }
                },
                "required": ["video_url"]
            }
        ),
        Tool(
            name="get_youtube_transcript",
            description=(
                "YouTube 영상의 자막만 빠르게 추출합니다. 카테고리 분류가 필요 없는 경우 사용하세요."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "YouTube 영상 URL"
                    },
                    "language": {
                        "type": "string",
                        "description": "자막 언어 코드 (예: 'ko', 'en')",
                        "default": "ko"
                    }
                },
                "required": ["video_url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls"""

    if extractor is None:
        return [TextContent(
            type="text",
            text="Error: YouTube Extractor not initialized. Please check your GEMINI_API_KEY."
        )]

    try:
        if name == "extract_youtube_content":
            video_url = arguments.get("video_url")
            classify = arguments.get("classify", True)

            logger.info(f"Extracting content from video: {video_url} (classify: {classify})")

            # Extract content with optional classification
            result = extractor.extract_with_gemini(video_url, classify=classify)

            if not result:
                return [TextContent(
                    type="text",
                    text="Error: Failed to extract content. Please check the URL and try again."
                )]

            # Format output for Claude to analyze
            if classify and "category" in result:
                output = f"""# YouTube 영상 콘텐츠

**영상 URL:** {video_url}
**카테고리:** {result['category']} (신뢰도: {result.get('confidence', 'N/A')}%)
**길이:** {len(result['content'])} characters

---

## 스크립트

{result['content']}

---

💡 **분석 가이드:**
이 영상은 **{result['category']}** 카테고리로 분류되었습니다.
다음 관점에서 분석해주세요:
"""
                # Add category-specific analysis suggestions
                category_guides = {
                    "crypto": "- 언급된 암호화폐/토큰\n- 시장 전망 및 근거\n- 투자 리스크 요인\n- 기술적/펀더멘털 분석",
                    "finance": "- 투자 전략 및 포트폴리오\n- 시장 분석 및 전망\n- 리스크 관리 방법",
                    "tech": "- 기술 스택 및 개념\n- 실용성 및 적용 방법\n- 학습 난이도",
                    "news": "- 핵심 이슈 및 배경\n- 파급 효과\n- 객관성 평가",
                    "business": "- 비즈니스 모델\n- 전략 및 실행 방법",
                    "education": "- 학습 목표 및 핵심 개념\n- 난이도 및 전제 지식",
                    "general": "- 핵심 메시지\n- 주요 인사이트"
                }
                output += category_guides.get(result['category'], "- 핵심 내용 요약\n- 주요 메시지")
            else:
                output = f"""# YouTube 영상 스크립트

**영상 URL:** {video_url}
**길이:** {len(result['content'])} characters

---

{result['content']}
"""

            return [TextContent(
                type="text",
                text=output
            )]

        elif name == "get_youtube_transcript":
            video_url = arguments.get("video_url")
            language = arguments.get("language", "ko")

            logger.info(f"Extracting transcript for video: {video_url}")

            # Extract transcript only
            transcript = extractor.get_transcript(video_url, language=language)

            if not transcript:
                return [TextContent(
                    type="text",
                    text="Error: Failed to extract transcript. The video may not have subtitles."
                )]

            # Format output
            output = f"""# YouTube 자막

**영상 URL:** {video_url}
**언어:** {language}
**길이:** {len(transcript)} characters

---

{transcript}
"""

            return [TextContent(
                type="text",
                text=output
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool: {name}"
            )]

    except Exception as e:
        logger.error(f"Error in tool call: {str(e)}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    logger.info("Starting YouTube Analysis MCP Server")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
