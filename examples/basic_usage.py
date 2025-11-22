"""
Basic usage examples for YouTube Analysis Agent
"""
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.agent import YouTubeAnalysisAgent

# Load environment variables
load_dotenv()


def example_comprehensive_analysis():
    """Example: Comprehensive analysis"""
    print("=" * 80)
    print("Example 1: Comprehensive Analysis")
    print("=" * 80)

    agent = YouTubeAnalysisAgent(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with actual URL

    results = agent.analyze_video(
        video_url=video_url,
        analysis_type="comprehensive"
    )

    if results:
        print(agent.get_summary_report(results))
    else:
        print("Analysis failed")


def example_crypto_analysis():
    """Example: Cryptocurrency-specific analysis"""
    print("\n" + "=" * 80)
    print("Example 2: Cryptocurrency Analysis")
    print("=" * 80)

    agent = YouTubeAnalysisAgent(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    # Replace with actual crypto YouTube video URL
    video_url = "https://www.youtube.com/watch?v=CRYPTO_VIDEO_ID"

    results = agent.analyze_video(
        video_url=video_url,
        analysis_type="crypto"
    )

    if results:
        print(agent.get_summary_report(results))


def example_custom_prompt():
    """Example: Custom prompt analysis"""
    print("\n" + "=" * 80)
    print("Example 3: Custom Prompt Analysis")
    print("=" * 80)

    agent = YouTubeAnalysisAgent(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    video_url = "https://www.youtube.com/watch?v=VIDEO_ID"

    custom_prompt = """
    이 영상을 다음 관점에서 분석해주세요:
    1. 투자자들이 알아야 할 핵심 정보
    2. 위험 요소와 주의사항
    3. 실행 가능한 액션 아이템
    """

    results = agent.analyze_with_custom_prompt(
        video_url=video_url,
        custom_prompt=custom_prompt
    )

    if results:
        print(agent.get_summary_report(results))


def example_multiple_videos():
    """Example: Analyze multiple videos"""
    print("\n" + "=" * 80)
    print("Example 4: Multiple Videos Analysis")
    print("=" * 80)

    agent = YouTubeAnalysisAgent(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    video_urls = [
        "https://www.youtube.com/watch?v=VIDEO_ID_1",
        "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "https://www.youtube.com/watch?v=VIDEO_ID_3"
    ]

    for i, url in enumerate(video_urls, 1):
        print(f"\n--- Analyzing Video {i}/{len(video_urls)} ---")
        results = agent.analyze_video(
            video_url=url,
            analysis_type="summary"
        )
        if results:
            print(f"Video {i} analyzed successfully")
            print(results['analysis']['analysis'][:200] + "...")


if __name__ == "__main__":
    # Run examples (uncomment the ones you want to try)

    # example_comprehensive_analysis()
    # example_crypto_analysis()
    # example_custom_prompt()
    # example_multiple_videos()

    print("\nUncomment the examples you want to run in the __main__ section")
