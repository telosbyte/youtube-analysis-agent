#!/usr/bin/env python3
"""
YouTube Analysis Agent CLI
"""
import logging
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from config.settings import get_settings
from src.agent import YouTubeAnalysisAgent

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youtube_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """YouTube Analysis Agent - AI-powered YouTube content analyzer"""
    pass


@cli.command()
@click.argument('video_url')
@click.option(
    '--type', '-t',
    type=click.Choice(['comprehensive', 'sentiment', 'summary', 'key_points', 'crypto']),
    default='comprehensive',
    help='Type of analysis to perform'
)
@click.option(
    '--use-gemini/--use-transcript',
    default=True,
    help='Use Gemini for extraction or fallback to transcript API'
)
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (default: auto-generated in output directory)'
)
def analyze(video_url: str, type: str, use_gemini: bool, output: str):
    """Analyze a YouTube video"""
    try:
        # Load settings
        settings = get_settings()

        # Initialize agent
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Initializing agent...", total=None)
            agent = YouTubeAnalysisAgent(
                gemini_api_key=settings.gemini_api_key,
                anthropic_api_key=settings.anthropic_api_key,
                gemini_model=settings.gemini_model,
                claude_model=settings.claude_model,
                output_dir=settings.output_dir
            )
            progress.update(task, description="Agent initialized ✓")

        console.print(f"\n[bold blue]Analyzing video:[/bold blue] {video_url}")
        console.print(f"[bold blue]Analysis type:[/bold blue] {type}")

        # Perform analysis
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing video...", total=None)
            results = agent.analyze_video(
                video_url=video_url,
                analysis_type=type,
                use_gemini_extraction=use_gemini,
                save_results=True
            )
            progress.update(task, description="Analysis complete ✓")

        if not results:
            console.print("[bold red]Error:[/bold red] Failed to analyze video")
            sys.exit(1)

        # Display results
        report = agent.get_summary_report(results)
        console.print(Panel(report, title="Analysis Report", border_style="green"))

        console.print(f"\n[bold green]✓[/bold green] Results saved to: {settings.output_dir}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        sys.exit(1)


@cli.command()
@click.argument('video_url')
@click.option(
    '--prompt', '-p',
    required=True,
    help='Custom analysis prompt'
)
@click.option(
    '--use-gemini/--use-transcript',
    default=True,
    help='Use Gemini for extraction or fallback to transcript API'
)
def custom(video_url: str, prompt: str, use_gemini: bool):
    """Analyze a video with custom prompt"""
    try:
        settings = get_settings()

        agent = YouTubeAnalysisAgent(
            gemini_api_key=settings.gemini_api_key,
            anthropic_api_key=settings.anthropic_api_key,
            gemini_model=settings.gemini_model,
            claude_model=settings.claude_model,
            output_dir=settings.output_dir
        )

        console.print(f"\n[bold blue]Analyzing video:[/bold blue] {video_url}")
        console.print(f"[bold blue]Custom prompt:[/bold blue] {prompt}")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing video...", total=None)
            results = agent.analyze_with_custom_prompt(
                video_url=video_url,
                custom_prompt=prompt,
                use_gemini_extraction=use_gemini,
                save_results=True
            )
            progress.update(task, description="Analysis complete ✓")

        if not results:
            console.print("[bold red]Error:[/bold red] Failed to analyze video")
            sys.exit(1)

        report = agent.get_summary_report(results)
        console.print(Panel(report, title="Custom Analysis Report", border_style="green"))

        console.print(f"\n[bold green]✓[/bold green] Results saved to: {settings.output_dir}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.error(f"Custom analysis error: {str(e)}", exc_info=True)
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration"""
    try:
        settings = get_settings()

        config_info = f"""
[bold]Current Configuration:[/bold]

[cyan]Gemini:[/cyan]
  Model: {settings.gemini_model}
  API Key: {'*' * 10 + settings.gemini_api_key[-4:] if settings.gemini_api_key else 'Not set'}

[cyan]Claude:[/cyan]
  Model: {settings.claude_model}
  Max Tokens: {settings.max_tokens}
  API Key: {'*' * 10 + settings.anthropic_api_key[-4:] if settings.anthropic_api_key else 'Not set'}

[cyan]Application:[/cyan]
  Log Level: {settings.log_level}
  Output Directory: {settings.output_dir}
"""
        console.print(Panel(config_info, title="Configuration", border_style="blue"))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
