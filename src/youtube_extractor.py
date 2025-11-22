"""
YouTube content extractor using Gemini API
"""
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
import json

logger = logging.getLogger(__name__)


class YouTubeExtractor:
    """Extract content from YouTube videos using Gemini API"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        """
        Initialize YouTube extractor

        Args:
            api_key: Gemini API key
            model: Gemini model name
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f"Initialized YouTubeExtractor with model: {model}")

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL

        Args:
            url: YouTube URL

        Returns:
            Video ID or None
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_transcript(self, video_url: str, language: str = 'ko') -> Optional[str]:
        """
        Get transcript from YouTube video using youtube-transcript-api

        Args:
            video_url: YouTube video URL
            language: Preferred language code (default: 'ko')

        Returns:
            Transcript text or None
        """
        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                logger.error(f"Invalid YouTube URL: {video_url}")
                return None

            # Try to get transcript in preferred language, fallback to English
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id, languages=[language]
                )
            except NoTranscriptFound:
                logger.warning(f"No {language} transcript found, trying English")
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id, languages=['en']
                )

            # Combine all transcript segments
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])
            logger.info(f"Successfully extracted transcript (length: {len(transcript_text)})")
            return transcript_text

        except TranscriptsDisabled:
            logger.error(f"Transcripts are disabled for video: {video_url}")
            return None
        except Exception as e:
            logger.error(f"Error extracting transcript: {str(e)}")
            return None

    def extract_with_gemini(self, video_url: str, classify: bool = True) -> Optional[Dict[str, Any]]:
        """
        Extract content from YouTube video using Gemini's multimodal capabilities
        Also classifies the video into categories

        Args:
            video_url: YouTube video URL
            classify: Whether to classify the video into categories

        Returns:
            Dictionary containing video information, content, and category
        """
        try:
            if classify:
                # Prompt for extraction AND classification
                prompt = f"""
                Analyze this YouTube video and provide the following in JSON format:

                1. Extract full transcript/script from the video
                2. Classify the video into ONE of these categories:
                   - crypto: 암호화폐/블록체인 (Bitcoin, Ethereum, DeFi, NFT, etc.)
                   - finance: 금융/투자 (주식, 채권, 부동산, ETF, etc.)
                   - tech: 기술/IT (프로그래밍, AI, 개발, 소프트웨어, etc.)
                   - news: 뉴스/시사 (뉴스, 속보, 정치, 경제 이슈, etc.)
                   - business: 비즈니스/창업 (스타트업, 경영, 마케팅, etc.)
                   - education: 교육/강의 (튜토리얼, 강의, 학습, etc.)
                   - general: 일반 (기타)

                3. Provide video metadata

                Respond in JSON format:
                {{
                  "transcript": "Full video transcript/script here...",
                  "category": "category_name",
                  "confidence": 0-100,
                  "metadata": {{
                    "title": "Video title",
                    "main_topics": ["topic1", "topic2"],
                    "summary": "Brief summary in Korean"
                  }}
                }}

                Video URL: {video_url}
                """
            else:
                # Simple extraction without classification
                prompt = f"""
                Extract the full transcript/script from this YouTube video.

                Video URL: {video_url}
                """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            logger.info("Successfully extracted content using Gemini")

            if classify:
                try:
                    # Try to parse JSON response
                    # Remove markdown code blocks if present
                    if response_text.startswith('```'):
                        response_text = response_text.split('```')[1]
                        if response_text.startswith('json'):
                            response_text = response_text[4:]
                        response_text = response_text.strip()

                    result = json.loads(response_text)

                    return {
                        'video_url': video_url,
                        'transcript': result.get('transcript', ''),
                        'category': result.get('category', 'general'),
                        'confidence': result.get('confidence', 0),
                        'metadata': result.get('metadata', {}),
                        'method': 'gemini_with_classification'
                    }
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON, using raw text")
                    return {
                        'video_url': video_url,
                        'transcript': response_text,
                        'category': 'general',
                        'confidence': 0,
                        'metadata': {},
                        'method': 'gemini_raw'
                    }
            else:
                return {
                    'video_url': video_url,
                    'transcript': response_text,
                    'category': 'general',
                    'method': 'gemini_simple'
                }

        except Exception as e:
            logger.error(f"Error extracting with Gemini: {str(e)}")
            return None

    def extract_content(
        self,
        video_url: str,
        use_gemini: bool = True,
        classify: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Extract content from YouTube video with optional classification

        Args:
            video_url: YouTube video URL
            use_gemini: Whether to use Gemini API (True) or transcript API (False)
            classify: Whether to classify the video category (only works with Gemini)

        Returns:
            Dictionary containing extracted content and category
        """
        logger.info(f"Extracting content from: {video_url}")

        if use_gemini:
            # Use Gemini with classification
            result = self.extract_with_gemini(video_url, classify=classify)
            if result:
                return result

        # Fallback to transcript API (without classification)
        transcript = self.get_transcript(video_url)
        if transcript:
            return {
                'video_url': video_url,
                'transcript': transcript,
                'category': 'general',  # Default category for transcript API
                'confidence': 0,
                'method': 'transcript_api'
            }

        logger.error("Failed to extract content from video")
        return None
