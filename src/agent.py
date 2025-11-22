"""
Main YouTube Analysis Agent
"""
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime

from .youtube_extractor import YouTubeExtractor
from .content_analyzer import ContentAnalyzer

logger = logging.getLogger(__name__)


class YouTubeAnalysisAgent:
    """Main agent for YouTube video analysis"""

    def __init__(
        self,
        gemini_api_key: str,
        anthropic_api_key: str,
        gemini_model: str = "gemini-1.5-pro",
        claude_model: str = "claude-sonnet-4-5-20250929",
        output_dir: Path = Path("./output")
    ):
        """
        Initialize YouTube Analysis Agent

        Args:
            gemini_api_key: Gemini API key
            anthropic_api_key: Anthropic API key
            gemini_model: Gemini model name
            claude_model: Claude model name
            output_dir: Output directory for results
        """
        self.extractor = YouTubeExtractor(gemini_api_key, gemini_model)
        self.analyzer = ContentAnalyzer(anthropic_api_key, claude_model)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Initialized YouTubeAnalysisAgent")

    def analyze_video(
        self,
        video_url: str,
        analysis_type: str = "comprehensive",
        use_gemini_extraction: bool = True,
        save_results: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze YouTube video

        Args:
            video_url: YouTube video URL
            analysis_type: Type of analysis (comprehensive, sentiment, summary, key_points, crypto)
            use_gemini_extraction: Use Gemini for extraction (True) or transcript API (False)
            save_results: Save results to file

        Returns:
            Complete analysis results
        """
        logger.info(f"Starting analysis for video: {video_url}")
        logger.info(f"Analysis type: {analysis_type}")

        # Step 1: Extract content
        logger.info("Step 1: Extracting content...")
        extracted_content = self.extractor.extract_content(video_url, use_gemini=use_gemini_extraction)

        if not extracted_content:
            logger.error("Failed to extract content")
            return None

        # Step 2: Analyze with Claude
        logger.info("Step 2: Analyzing with Claude...")

        # Prepare content for analysis
        if extracted_content['method'] == 'gemini_multimodal':
            content_to_analyze = extracted_content['gemini_analysis']
        else:
            content_to_analyze = extracted_content['transcript']

        analysis_result = self.analyzer.analyze_transcript(content_to_analyze, analysis_type)

        if not analysis_result:
            logger.error("Failed to analyze content")
            return None

        # Step 3: Combine results
        complete_result = {
            'video_url': video_url,
            'timestamp': datetime.now().isoformat(),
            'extraction': extracted_content,
            'analysis': analysis_result
        }

        # Step 4: Save results
        if save_results:
            self._save_results(complete_result, video_url)

        logger.info("Analysis completed successfully")
        return complete_result

    def analyze_with_custom_prompt(
        self,
        video_url: str,
        custom_prompt: str,
        use_gemini_extraction: bool = True,
        save_results: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze video with custom prompt

        Args:
            video_url: YouTube video URL
            custom_prompt: Custom analysis prompt
            use_gemini_extraction: Use Gemini for extraction
            save_results: Save results to file

        Returns:
            Analysis results
        """
        logger.info(f"Starting custom analysis for video: {video_url}")

        # Extract content
        extracted_content = self.extractor.extract_content(video_url, use_gemini=use_gemini_extraction)

        if not extracted_content:
            logger.error("Failed to extract content")
            return None

        # Prepare content
        if extracted_content['method'] == 'gemini_multimodal':
            content_to_analyze = extracted_content['gemini_analysis']
        else:
            content_to_analyze = extracted_content['transcript']

        # Analyze with custom prompt
        analysis_result = self.analyzer.analyze_with_custom_prompt(content_to_analyze, custom_prompt)

        if not analysis_result:
            logger.error("Failed to analyze content")
            return None

        # Combine results
        complete_result = {
            'video_url': video_url,
            'timestamp': datetime.now().isoformat(),
            'extraction': extracted_content,
            'analysis': analysis_result,
            'custom_prompt': custom_prompt
        }

        # Save results
        if save_results:
            self._save_results(complete_result, video_url)

        logger.info("Custom analysis completed successfully")
        return complete_result

    def _save_results(self, results: Dict[str, Any], video_url: str) -> None:
        """
        Save analysis results to file

        Args:
            results: Analysis results
            video_url: Video URL (for filename)
        """
        try:
            # Create filename from timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_id = self.extractor.extract_video_id(video_url)
            filename = f"analysis_{video_id}_{timestamp}.json"
            filepath = self.output_dir / filename

            # Save to JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            logger.info(f"Results saved to: {filepath}")

        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

    def get_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Generate summary report from analysis results

        Args:
            results: Analysis results

        Returns:
            Formatted summary report
        """
        report = []
        report.append("=" * 80)
        report.append("YouTube Video Analysis Report")
        report.append("=" * 80)
        report.append(f"\nVideo URL: {results['video_url']}")
        report.append(f"Analysis Time: {results['timestamp']}")
        report.append(f"\nExtraction Method: {results['extraction']['method']}")
        report.append(f"Analysis Type: {results['analysis']['analysis_type']}")
        report.append(f"\nModel Used: {results['analysis']['model']}")
        report.append(f"Tokens Used: {results['analysis']['usage']['input_tokens']} + {results['analysis']['usage']['output_tokens']}")
        report.append("\n" + "-" * 80)
        report.append("Analysis Results:")
        report.append("-" * 80)
        report.append(f"\n{results['analysis']['analysis']}")
        report.append("\n" + "=" * 80)

        return "\n".join(report)
