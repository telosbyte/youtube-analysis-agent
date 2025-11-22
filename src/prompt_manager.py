"""
Prompt Manager - 프롬프트 템플릿 관리
"""
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class PromptManager:
    """프롬프트 템플릿을 로드하고 관리하는 클래스"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize Prompt Manager

        Args:
            config_path: Path to prompts.yaml file
        """
        if config_path is None:
            # Default path: config/prompts.yaml
            config_path = Path(__file__).parent.parent / "config" / "prompts.yaml"

        self.config_path = config_path
        self.prompts_config = self._load_config()
        logger.info(f"Loaded prompts from: {config_path}")

    def _load_config(self) -> Dict[str, Any]:
        """Load prompts configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading prompts config: {str(e)}")
            return {}

    def get_categories(self) -> Dict[str, Any]:
        """
        Get all available categories

        Returns:
            Dictionary of categories with their metadata
        """
        return self.prompts_config.get('categories', {})

    def get_category_info(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific category

        Args:
            category: Category name

        Returns:
            Category metadata or None if not found
        """
        return self.prompts_config.get('categories', {}).get(category)

    def get_classification_prompt(self) -> str:
        """
        Get the classification prompt template

        Returns:
            Classification prompt template
        """
        return self.prompts_config.get('classification_prompt', '')

    def get_prompt(
        self,
        category: str,
        analysis_type: str = 'comprehensive',
        content: str = ""
    ) -> str:
        """
        Get analysis prompt for specific category and type

        Args:
            category: Category name (crypto, finance, tech, etc.)
            analysis_type: Type of analysis (comprehensive, sentiment, summary)
            content: Content to be analyzed (will replace {content} placeholder)

        Returns:
            Formatted prompt string
        """
        try:
            # Get prompt template
            prompts = self.prompts_config.get('prompts', {})
            category_prompts = prompts.get(category, prompts.get('general', {}))
            prompt_template = category_prompts.get(
                analysis_type,
                category_prompts.get('comprehensive', '')
            )

            # Replace content placeholder
            prompt = prompt_template.replace('{content}', content)

            return prompt

        except Exception as e:
            logger.error(f"Error getting prompt: {str(e)}")
            # Fallback to general comprehensive prompt
            return self._get_fallback_prompt(content)

    def _get_fallback_prompt(self, content: str) -> str:
        """Get fallback prompt if category-specific prompt fails"""
        return f"""
다음 YouTube 영상의 자막을 분석해주세요:

{content}

JSON 형식으로 분석 결과를 제공해주세요:
1. 핵심 주제
2. 주요 내용
3. 주요 포인트
4. 요약
"""

    def list_available_prompts(self) -> Dict[str, list]:
        """
        List all available prompts by category

        Returns:
            Dictionary mapping categories to their available analysis types
        """
        prompts = self.prompts_config.get('prompts', {})
        result = {}

        for category, category_prompts in prompts.items():
            result[category] = list(category_prompts.keys())

        return result

    def add_custom_prompt(
        self,
        category: str,
        analysis_type: str,
        prompt_template: str,
        save: bool = False
    ) -> bool:
        """
        Add a custom prompt template

        Args:
            category: Category name
            analysis_type: Type of analysis
            prompt_template: Prompt template string
            save: Whether to save to config file

        Returns:
            Success status
        """
        try:
            if 'prompts' not in self.prompts_config:
                self.prompts_config['prompts'] = {}

            if category not in self.prompts_config['prompts']:
                self.prompts_config['prompts'][category] = {}

            self.prompts_config['prompts'][category][analysis_type] = prompt_template

            if save:
                self._save_config()

            logger.info(f"Added custom prompt: {category}/{analysis_type}")
            return True

        except Exception as e:
            logger.error(f"Error adding custom prompt: {str(e)}")
            return False

    def _save_config(self) -> None:
        """Save current configuration to YAML file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.prompts_config,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False
                )
            logger.info("Prompts configuration saved")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")

    def get_category_keywords(self, category: str) -> list:
        """
        Get keywords for a specific category

        Args:
            category: Category name

        Returns:
            List of keywords
        """
        category_info = self.get_category_info(category)
        if category_info:
            return category_info.get('keywords', [])
        return []

    def suggest_category(self, text: str) -> Optional[str]:
        """
        Suggest category based on text keywords

        Args:
            text: Text to analyze

        Returns:
            Suggested category or None
        """
        text_lower = text.lower()
        categories = self.get_categories()

        max_matches = 0
        suggested_category = None

        for category, info in categories.items():
            keywords = info.get('keywords', [])
            matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)

            if matches > max_matches:
                max_matches = matches
                suggested_category = category

        return suggested_category if max_matches > 0 else 'general'
