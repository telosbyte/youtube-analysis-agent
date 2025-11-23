import { GoogleGenerativeAI } from "@google/generative-ai";
import { Category, ExtractionResult } from "./types";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");

/**
 * Extract YouTube video content using Gemini API
 */
export async function extractYouTubeContent(
  videoUrl: string,
  classify: boolean = true
): Promise<ExtractionResult | null> {
  try {
    const model = genAI.getGenerativeModel({
      model: process.env.GEMINI_MODEL || "gemini-1.5-pro"
    });

    let prompt = `Extract the complete transcript/script from this YouTube video: ${videoUrl}

Instructions:
1. Extract all spoken content from the video
2. Maintain the original language
3. Provide complete text without summarization
4. Include important context if available`;

    if (classify) {
      prompt += `

5. Classify the video into ONE of these categories:
   - crypto: Cryptocurrency, blockchain, DeFi
   - finance: Finance, stocks, investment
   - tech: Technology, IT, programming
   - news: News, current events, politics
   - business: Business, entrepreneurship, management
   - education: Education, tutorials, courses
   - general: General content

6. Provide confidence score (0-100) for the classification

Return as JSON:
{
  "content": "full transcript here",
  "category": "category_name",
  "confidence": 95
}`;
    } else {
      prompt += `

Return as JSON:
{
  "content": "full transcript here"
}`;
    }

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Parse JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      console.error("Failed to parse JSON from Gemini response");
      return null;
    }

    const data = JSON.parse(jsonMatch[0]);

    return {
      content: data.content,
      category: data.category as Category,
      confidence: data.confidence
    };
  } catch (error) {
    console.error("Error extracting YouTube content:", error);
    return null;
  }
}

/**
 * Get category-specific analysis prompt
 */
export function getCategoryPrompt(category: Category): string {
  const prompts: Record<Category, string> = {
    crypto: `암호화폐 투자자 관점에서 다음 항목을 분석해주세요:
- 언급된 암호화폐/토큰
- 시장 전망 및 근거
- 투자 시그널 (매수/매도/보유)
- 리스크 요인
- 기술적/펀더멘털 분석
- 신뢰도 평가 (0-100)`,

    finance: `금융/투자 전문가 관점에서 다음 항목을 분석해주세요:
- 투자 전략 및 포트폴리오
- 시장 분석 및 전망
- 리스크 관리 방법
- 실행 가능한 조언`,

    tech: `기술 전문가 관점에서 다음 항목을 분석해주세요:
- 핵심 기술 스택 및 개념
- 실용성 및 적용 방법
- 학습 난이도 및 전제 지식
- 최신 트렌드와의 연관성`,

    news: `저널리스트 관점에서 다음 항목을 분석해주세요:
- 핵심 이슈 및 배경
- 파급 효과 및 영향
- 다양한 관점 정리
- 객관성 평가`,

    business: `비즈니스 전문가 관점에서 다음 항목을 분석해주세요:
- 비즈니스 모델 분석
- 전략 및 실행 방법
- 성공 요인 및 리스크
- 실무 적용 방안`,

    education: `교육 전문가 관점에서 다음 항목을 분석해주세요:
- 학습 목표 및 핵심 개념
- 난이도 및 전제 지식
- 학습 로드맵
- 실습/응용 방법`,

    general: `다음 항목을 종합적으로 분석해주세요:
- 핵심 주제 및 메시지
- 주요 내용 정리
- 타겟 청중
- 실행 가능한 인사이트`
  };

  return prompts[category] || prompts.general;
}
