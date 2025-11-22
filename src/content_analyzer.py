"""
Content analyzer using Claude API
"""
import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic
import json

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Analyze YouTube content using Claude API"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", max_tokens: int = 8000):
        """
        Initialize content analyzer

        Args:
            api_key: Anthropic API key
            model: Claude model name
            max_tokens: Maximum tokens for response
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        logger.info(f"Initialized ContentAnalyzer with model: {model}")

    def analyze_transcript(self, transcript: str, analysis_type: str = "comprehensive") -> Optional[Dict[str, Any]]:
        """
        Analyze YouTube transcript

        Args:
            transcript: Video transcript text
            analysis_type: Type of analysis (comprehensive, sentiment, summary, key_points)

        Returns:
            Analysis results
        """
        try:
            prompts = {
                "comprehensive": self._get_comprehensive_prompt(transcript),
                "sentiment": self._get_sentiment_prompt(transcript),
                "summary": self._get_summary_prompt(transcript),
                "key_points": self._get_key_points_prompt(transcript),
                "crypto": self._get_crypto_analysis_prompt(transcript)
            }

            prompt = prompts.get(analysis_type, prompts["comprehensive"])

            logger.info(f"Analyzing content with type: {analysis_type}")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = {
                'analysis_type': analysis_type,
                'analysis': response.content[0].text,
                'model': self.model,
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                }
            }

            logger.info(f"Analysis complete (tokens: {response.usage.input_tokens}+{response.usage.output_tokens})")
            return result

        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return None

    def _get_comprehensive_prompt(self, transcript: str) -> str:
        """Get comprehensive analysis prompt"""
        return f"""
다음은 YouTube 영상의 자막/스크립트입니다. 이를 종합적으로 분석해주세요:

{transcript}

다음 항목들을 포함하여 분석해주세요:

1. **핵심 주제**: 영상의 주요 주제와 테마
2. **주요 내용**: 중요한 포인트들을 구조화하여 정리
3. **감성 분석**: 전반적인 톤과 감정 (긍정적/부정적/중립적)
4. **타겟 청중**: 예상되는 시청 대상
5. **핵심 메시지**: 전달하고자 하는 주요 메시지
6. **실행 가능한 인사이트**: 시청자가 활용할 수 있는 구체적인 정보

JSON 형식으로 응답해주세요.
"""

    def _get_sentiment_prompt(self, transcript: str) -> str:
        """Get sentiment analysis prompt"""
        return f"""
다음 YouTube 영상 자막의 감성을 분석해주세요:

{transcript}

다음을 포함해주세요:
1. 전반적인 감성 (긍정/부정/중립) 및 점수 (0-100)
2. 감정의 변화 추이
3. 주요 감정 키워드
4. 톤과 스타일

JSON 형식으로 응답해주세요.
"""

    def _get_summary_prompt(self, transcript: str) -> str:
        """Get summary prompt"""
        return f"""
다음 YouTube 영상 자막을 요약해주세요:

{transcript}

다음을 포함해주세요:
1. 3줄 요약
2. 상세 요약 (200-300자)
3. 핵심 키워드 (5-10개)

JSON 형식으로 응답해주세요.
"""

    def _get_key_points_prompt(self, transcript: str) -> str:
        """Get key points extraction prompt"""
        return f"""
다음 YouTube 영상 자막에서 핵심 포인트를 추출해주세요:

{transcript}

다음을 포함해주세요:
1. 주요 논점 (bullet points)
2. 중요한 데이터/통계
3. 인용문이나 강조된 내용
4. 결론 또는 행동 요청사항

JSON 형식으로 응답해주세요.
"""

    def _get_crypto_analysis_prompt(self, transcript: str) -> str:
        """Get cryptocurrency-specific analysis prompt"""
        return f"""
다음 암호화폐 관련 YouTube 영상 자막을 분석해주세요:

{transcript}

다음을 포함해주세요:
1. **언급된 암호화폐**: 구체적으로 언급된 코인/토큰
2. **시장 전망**: 상승/하락/중립 및 근거
3. **투자 시그널**: 매수/매도/보유 시그널
4. **리스크 요인**: 언급된 위험 요소
5. **기술적 분석**: 차트, 지표 등 기술적 내용
6. **펀더멘털 분석**: 프로젝트, 뉴스, 이벤트 등
7. **신뢰도 평가**: 정보의 객관성과 신뢰도 (0-100)

JSON 형식으로 응답해주세요.
"""

    def analyze_with_custom_prompt(self, content: str, custom_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Analyze content with custom prompt

        Args:
            content: Content to analyze
            custom_prompt: Custom analysis prompt

        Returns:
            Analysis results
        """
        try:
            full_prompt = f"{custom_prompt}\n\n콘텐츠:\n{content}"

            logger.info("Analyzing content with custom prompt")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            )

            result = {
                'analysis_type': 'custom',
                'analysis': response.content[0].text,
                'model': self.model,
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                }
            }

            logger.info("Custom analysis complete")
            return result

        except Exception as e:
            logger.error(f"Error with custom analysis: {str(e)}")
            return None
