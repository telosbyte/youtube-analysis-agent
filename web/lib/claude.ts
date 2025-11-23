import Anthropic from "@anthropic-ai/sdk";
import { Category } from "./types";
import { getCategoryPrompt } from "./gemini";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

/**
 * Analyze content with Claude
 */
export async function analyzeWithClaude(
  content: string,
  category: Category,
  customPrompt?: string
): Promise<{ analysis: string; usage: any }> {
  try {
    const systemPrompt = customPrompt || getCategoryPrompt(category);

    const message = await anthropic.messages.create({
      model: process.env.CLAUDE_MODEL || "claude-sonnet-4-5-20250929",
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: `${systemPrompt}

다음 YouTube 영상 스크립트를 분석해주세요:

${content}

분석 결과를 명확하고 구조화된 형식으로 작성해주세요. 마크다운 형식을 사용해도 좋습니다.`
        }
      ]
    });

    const textContent = message.content.find(block => block.type === 'text');

    return {
      analysis: textContent?.type === 'text' ? textContent.text : '',
      usage: message.usage
    };
  } catch (error) {
    console.error("Error analyzing with Claude:", error);
    throw error;
  }
}
