import { NextRequest, NextResponse } from "next/server";
import { extractYouTubeContent } from "@/lib/gemini";
import { ApiResponse, ExtractionResult } from "@/lib/types";

export async function POST(request: NextRequest) {
  try {
    const { videoUrl, classify = true } = await request.json();

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

    const result = await extractYouTubeContent(videoUrl, classify);

    if (!result) {
      return NextResponse.json<ApiResponse>(
        { success: false, error: "Failed to extract content from video" },
        { status: 500 }
      );
    }

    return NextResponse.json<ApiResponse<ExtractionResult>>(
      { success: true, data: result },
      { status: 200 }
    );
  } catch (error: any) {
    console.error("Extract API error:", error);
    return NextResponse.json<ApiResponse>(
      { success: false, error: error.message || "Internal server error" },
      { status: 500 }
    );
  }
}
