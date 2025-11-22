"""
YouTube content extractor using Gemini API
"""
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

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

    def extract_with_gemini(self, video_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract content from YouTube video using Gemini's multimodal capabilities

        Args:
            video_url: YouTube video URL

        Returns:
            Dictionary containing video information and content
        """
        try:
            prompt = f"""
            Analyze this YouTube video and provide:
            1. Video title
            2. Main topics discussed
            3. Key points (bullet points)
            4. Overall summary
            5. Important timestamps (if visible)

            Provide the response in Korean.

            Video URL: {video_url}
            """

            response = self.model.generate_content(prompt)
            logger.info("Successfully extracted content using Gemini")

            return {
                'video_url': video_url,
                'gemini_analysis': response.text,
                'method': 'gemini_multimodal'
            }

        except Exception as e:
            logger.error(f"Error extracting with Gemini: {str(e)}")
            return None

    def extract_content(self, video_url: str, use_gemini: bool = True) -> Optional[Dict[str, Any]]:
        """
        Extract content from YouTube video

        Args:
            video_url: YouTube video URL
            use_gemini: Whether to use Gemini API (True) or transcript API (False)

        Returns:
            Dictionary containing extracted content
        """
        logger.info(f"Extracting content from: {video_url}")

        if use_gemini:
            # Try Gemini first
            result = self.extract_with_gemini(video_url)
            if result:
                return result

        # Fallback to transcript API
        transcript = self.get_transcript(video_url)
        if transcript:
            return {
                'video_url': video_url,
                'transcript': transcript,
                'method': 'transcript_api'
            }

        logger.error("Failed to extract content from video")
        return None
