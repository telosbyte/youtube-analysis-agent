#!/usr/bin/env python3
"""
YouTube Analysis Agent - 테스트 스크립트
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from src.agent import YouTubeAnalysisAgent
from src.prompt_manager import PromptManager

# Load environment variables
load_dotenv()

def test_prompt_manager():
    """프롬프트 매니저 테스트"""
    print("=" * 80)
    print("1. 프롬프트 매니저 테스트")
    print("=" * 80)

    pm = PromptManager()

    # 사용 가능한 카테고리 확인
    categories = pm.get_categories()
    print(f"\n✓ 로드된 카테고리: {len(categories)}개")
    for cat_name, cat_info in categories.items():
        print(f"  - {cat_name}: {cat_info['name']}")

    # 사용 가능한 프롬프트 확인
    prompts = pm.list_available_prompts()
    print(f"\n✓ 사용 가능한 프롬프트:")
    for category, types in prompts.items():
        print(f"  - {category}: {', '.join(types)}")

    # 샘플 프롬프트 가져오기
    sample_prompt = pm.get_prompt(
        category="crypto",
        analysis_type="comprehensive",
        content="[테스트 콘텐츠]"
    )
    print(f"\n✓ crypto/comprehensive 프롬프트 길이: {len(sample_prompt)} 문자")

    print("\n[성공] 프롬프트 매니저가 정상적으로 작동합니다!\n")


def test_api_keys():
    """API 키 확인"""
    print("=" * 80)
    print("2. API 키 확인")
    print("=" * 80)

    gemini_key = os.getenv("GEMINI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if gemini_key and gemini_key != "your_gemini_api_key_here":
        print(f"✓ Gemini API Key: {gemini_key[:10]}...{gemini_key[-4:]}")
    else:
        print("✗ Gemini API Key가 설정되지 않았습니다!")
        print("  .env 파일에 GEMINI_API_KEY를 설정하세요.")
        return False

    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print(f"✓ Anthropic API Key: {anthropic_key[:10]}...{anthropic_key[-4:]}")
    else:
        print("✗ Anthropic API Key가 설정되지 않았습니다!")
        print("  .env 파일에 ANTHROPIC_API_KEY를 설정하세요.")
        return False

    print("\n[성공] API 키가 정상적으로 설정되었습니다!\n")
    return True


def test_agent_initialization():
    """에이전트 초기화 테스트"""
    print("=" * 80)
    print("3. 에이전트 초기화 테스트")
    print("=" * 80)

    try:
        agent = YouTubeAnalysisAgent(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        print("✓ YouTubeAnalysisAgent 초기화 성공")
        print(f"✓ PromptManager 로드됨")
        print(f"✓ Output directory: {agent.output_dir}")

        print("\n[성공] 에이전트가 정상적으로 초기화되었습니다!\n")
        return agent
    except Exception as e:
        print(f"✗ 에이전트 초기화 실패: {str(e)}")
        return None


def test_youtube_analysis(agent, video_url=None):
    """YouTube 영상 분석 테스트 (실제 API 호출)"""
    print("=" * 80)
    print("4. YouTube 영상 분석 테스트")
    print("=" * 80)

    if not video_url:
        print("\n테스트할 YouTube URL을 입력하세요 (Enter로 건너뛰기):")
        video_url = input("YouTube URL: ").strip()

        if not video_url:
            print("\n[건너뜀] URL이 입력되지 않아 실제 분석 테스트를 건너뜁니다.")
            return

    print(f"\n분석 중: {video_url}")
    print("(Gemini가 스크립트 추출 + 카테고리 분류 → Claude가 분석)")
    print("\n이 과정은 1-2분 정도 걸릴 수 있습니다...\n")

    try:
        # 영상 분석 실행
        result = agent.analyze_video(
            video_url=video_url,
            analysis_type="comprehensive",
            use_gemini_extraction=True,
            save_results=True
        )

        if result:
            print("\n" + "=" * 80)
            print("분석 결과")
            print("=" * 80)

            # 카테고리 정보
            category = result['analysis'].get('category', 'N/A')
            confidence = result['analysis'].get('category_confidence', 0)
            print(f"\n카테고리: {category} (신뢰도: {confidence}%)")

            # 메타데이터
            metadata = result['extraction'].get('metadata', {})
            if metadata:
                print(f"제목: {metadata.get('title', 'N/A')}")
                print(f"주요 주제: {', '.join(metadata.get('main_topics', []))}")

            # 토큰 사용량
            usage = result['analysis']['usage']
            print(f"\n토큰 사용: {usage['input_tokens']} + {usage['output_tokens']} = {usage['input_tokens'] + usage['output_tokens']}")

            # 분석 결과 (일부만 출력)
            analysis_text = result['analysis']['analysis']
            print(f"\n분석 결과 (처음 500자):")
            print("-" * 80)
            print(analysis_text[:500] + "...")

            print("\n[성공] YouTube 영상 분석이 완료되었습니다!")
            print(f"전체 결과는 {agent.output_dir}에 저장되었습니다.\n")

        else:
            print("\n✗ 분석 실패")

    except Exception as e:
        print(f"\n✗ 분석 중 오류 발생: {str(e)}")


def run_all_tests():
    """모든 테스트 실행"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "YouTube Analysis Agent 테스트" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    # 1. 프롬프트 매니저 테스트
    test_prompt_manager()

    # 2. API 키 확인
    if not test_api_keys():
        print("\n⚠️  API 키를 설정한 후 다시 시도하세요.")
        print("   .env 파일을 수정하거나 환경 변수를 설정하세요.\n")
        return

    # 3. 에이전트 초기화
    agent = test_agent_initialization()
    if not agent:
        print("\n⚠️  에이전트 초기화에 실패했습니다.")
        return

    # 4. YouTube 분석 테스트 (선택적)
    print("\n실제 YouTube 영상을 분석하시겠습니까? (y/N): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        test_youtube_analysis(agent)
    else:
        print("\n[건너뜀] 실제 분석 테스트를 건너뜁니다.\n")

    print("=" * 80)
    print("테스트 완료!")
    print("=" * 80)
    print("\n사용 방법:")
    print("  CLI: python main.py analyze \"VIDEO_URL\"")
    print("  MCP: mcp-server/README.md 참조")
    print("  문서: ARCHITECTURE.md, README.md")
    print("\n")


if __name__ == "__main__":
    # 특정 URL로 바로 테스트하려면:
    # test_video_url = "https://www.youtube.com/watch?v=..."
    # 를 설정하고 run_all_tests() 대신 아래 코드 사용

    run_all_tests()
