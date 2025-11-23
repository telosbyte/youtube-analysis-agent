import { NextRequest, NextResponse } from "next/server";
import { extractYouTubeContent } from "@/lib/gemini";
import { analyzeWithClaude } from "@/lib/claude";
import { ApiResponse, AnalysisResult } from "@/lib/types";

export async function POST(request: NextRequest) {
  try {
    const { videoUrl, customPrompt } = await request.json();

    if (!videoUrl) {
      return NextResponse.json<ApiResponse>(
        { success: false, error: "Video URL is required" },
        { status: 400 }
      );
    }

    // Validate YouTube URL
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    if (!youtubeRegex.test(videoUrl)) {
      return NextResponse.json<ApiResponse>(
        { success: false, error: "Invalid YouTube URL" },
        { status: 400 }
      );
    }

    // Step 1: Extract content with Gemini (with classification)
    const extraction = await extractYouTubeContent(videoUrl, true);

    if (!extraction || !extraction.content) {
      return NextResponse.json<ApiResponse>(
        { success: false, error: "Failed to extract content from video" },
        { status: 500 }
      );
    }

    // Step 2: Analyze with Claude
    const { analysis, usage } = await analyzeWithClaude(
      extraction.content,
      extraction.category || 'general',
      customPrompt
    );

    const result: AnalysisResult = {
      videoUrl,
      category: extraction.category || 'general',
      confidence: extraction.confidence,
      transcript: extraction.content,
      analysis,
      timestamp: new Date().toISOString(),
      model: process.env.CLAUDE_MODEL || "claude-sonnet-4-5-20250929",
      usage: {
        inputTokens: usage.input_tokens,
        outputTokens: usage.output_tokens
      }
    };

    return NextResponse.json<ApiResponse<AnalysisResult>>(
      { success: true, data: result },
      { status: 200 }
    );
  } catch (error: any) {
    console.error("Analyze API error:", error);
    return NextResponse.json<ApiResponse>(
      { success: false, error: error.message || "Internal server error" },
      { status: 500 }
    );
  }
}
