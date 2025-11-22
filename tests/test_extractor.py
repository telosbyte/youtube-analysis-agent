"""
Tests for YouTube extractor
"""
import pytest
from src.youtube_extractor import YouTubeExtractor


class TestYouTubeExtractor:
    """Test cases for YouTubeExtractor"""

    def test_extract_video_id_standard(self):
        """Test standard YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = YouTubeExtractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_video_id_short(self):
        """Test short YouTube URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = YouTubeExtractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_video_id_embed(self):
        """Test embed YouTube URL"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = YouTubeExtractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_video_id_with_params(self):
        """Test YouTube URL with parameters"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share"
        video_id = YouTubeExtractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_video_id_invalid(self):
        """Test invalid URL"""
        url = "https://www.google.com"
        video_id = YouTubeExtractor.extract_video_id(url)
        assert video_id is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
