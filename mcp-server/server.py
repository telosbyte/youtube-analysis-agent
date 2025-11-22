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
from src.agent import YouTubeAnalysisAgent

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

# Initialize agent
try:
    agent = YouTubeAnalysisAgent(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
        claude_model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
        output_dir=Path(os.getenv("OUTPUT_DIR", "./output"))
    )
    logger.info("YouTube Analysis Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {str(e)}")
    agent = None

# Create MCP server
app = Server("youtube-analysis")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="analyze_youtube_video",
            description=(
                "YouTube 영상을 분석합니다. URL을 제공하면 자막을 추출하고 AI로 분석합니다. "
                "analysis_type: comprehensive(종합), sentiment(감성), summary(요약), "
                "key_points(핵심포인트), crypto(암호화폐)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "YouTube 영상 URL (예: https://www.youtube.com/watch?v=VIDEO_ID)"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["comprehensive", "sentiment", "summary", "key_points", "crypto"],
                        "description": "분석 유형",
                        "default": "comprehensive"
                    },
                    "use_gemini": {
                        "type": "boolean",
                        "description": "Gemini API 사용 여부 (true: Gemini, false: Transcript API)",
                        "default": True
                    }
                },
                "required": ["video_url"]
            }
        ),
        Tool(
            name="analyze_youtube_custom",
            description=(
                "YouTube 영상을 커스텀 프롬프트로 분석합니다. "
                "URL과 원하는 분석 방식을 자유롭게 지정할 수 있습니다."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "YouTube 영상 URL"
                    },
                    "custom_prompt": {
                        "type": "string",
                        "description": "커스텀 분석 프롬프트 (예: '이 영상의 핵심 메시지를 3가지로 정리해주세요')"
                    },
                    "use_gemini": {
                        "type": "boolean",
                        "description": "Gemini API 사용 여부",
                        "default": True
                    }
                },
                "required": ["video_url", "custom_prompt"]
            }
        ),
        Tool(
            name="get_youtube_transcript",
            description=(
                "YouTube 영상의 자막만 추출합니다. 분석 없이 텍스트만 필요한 경우 사용하세요."
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

    if agent is None:
        return [TextContent(
            type="text",
            text="Error: YouTube Analysis Agent not initialized. Please check your API keys."
        )]

    try:
        if name == "analyze_youtube_video":
            video_url = arguments.get("video_url")
            analysis_type = arguments.get("analysis_type", "comprehensive")
            use_gemini = arguments.get("use_gemini", True)

            logger.info(f"Analyzing video: {video_url} (type: {analysis_type})")

            # Perform analysis
            results = agent.analyze_video(
                video_url=video_url,
                analysis_type=analysis_type,
                use_gemini_extraction=use_gemini,
                save_results=True
            )

            if not results:
                return [TextContent(
                    type="text",
                    text="Error: Failed to analyze video. Please check the URL and try again."
                )]

            # Generate report
            report = agent.get_summary_report(results)

            return [TextContent(
                type="text",
                text=report
            )]

        elif name == "analyze_youtube_custom":
            video_url = arguments.get("video_url")
            custom_prompt = arguments.get("custom_prompt")
            use_gemini = arguments.get("use_gemini", True)

            logger.info(f"Custom analysis for video: {video_url}")

            # Perform custom analysis
            results = agent.analyze_with_custom_prompt(
                video_url=video_url,
                custom_prompt=custom_prompt,
                use_gemini_extraction=use_gemini,
                save_results=True
            )

            if not results:
                return [TextContent(
                    type="text",
                    text="Error: Failed to analyze video with custom prompt."
                )]

            report = agent.get_summary_report(results)

            return [TextContent(
                type="text",
                text=report
            )]

        elif name == "get_youtube_transcript":
            video_url = arguments.get("video_url")
            language = arguments.get("language", "ko")

            logger.info(f"Extracting transcript for video: {video_url}")

            # Extract transcript only
            transcript = agent.extractor.get_transcript(video_url, language=language)

            if not transcript:
                return [TextContent(
                    type="text",
                    text="Error: Failed to extract transcript. The video may not have subtitles."
                )]

            # Format output
            output = f"""
YouTube Transcript
==================
Video URL: {video_url}
Language: {language}
Length: {len(transcript)} characters

Transcript:
-----------
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
