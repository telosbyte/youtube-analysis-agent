"use client";

import { useState } from "react";
import YouTubeInput from "@/components/YouTubeInput";
import AnalysisResult from "@/components/AnalysisResult";
import LoadingSpinner from "@/components/LoadingSpinner";
import { AnalysisResult as AnalysisResultType } from "@/lib/types";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResultType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (videoUrl: string, customPrompt?: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ videoUrl, customPrompt }),
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || "분석 실패");
      }

      setResult(data.data);
    } catch (err: any) {
      setError(err.message || "분석 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            🎥 YouTube Analysis
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            AI 기반 YouTube 영상 심층 분석 서비스
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        {!result && !loading && (
          <div className="space-y-8">
            {/* Features */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                ✨ 주요 기능
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl mb-2">🤖</div>
                  <h3 className="font-semibold mb-1">자동 카테고리 분류</h3>
                  <p className="text-sm text-gray-600">
                    Gemini AI가 영상을 7개 카테고리로 자동 분류
                  </p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl mb-2">📊</div>
                  <h3 className="font-semibold mb-1">카테고리별 최적화 분석</h3>
                  <p className="text-sm text-gray-600">
                    Claude가 각 카테고리에 특화된 심층 분석 제공
                  </p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl mb-2">⚡</div>
                  <h3 className="font-semibold mb-1">커스텀 분석</h3>
                  <p className="text-sm text-gray-600">
                    원하는 관점으로 자유롭게 분석 가능
                  </p>
                </div>
              </div>
            </div>

            {/* Input Form */}
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                YouTube 영상 분석하기
              </h2>
              <YouTubeInput onSubmit={handleAnalyze} loading={loading} />
            </div>

            {/* Categories Info */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                🏷️ 지원 카테고리
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="flex items-center gap-2 p-2 bg-yellow-50 rounded border border-yellow-200">
                  <span>🪙</span>
                  <span className="text-sm font-medium">암호화폐</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-green-50 rounded border border-green-200">
                  <span>💰</span>
                  <span className="text-sm font-medium">금융/투자</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-blue-50 rounded border border-blue-200">
                  <span>💻</span>
                  <span className="text-sm font-medium">기술/IT</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-red-50 rounded border border-red-200">
                  <span>📰</span>
                  <span className="text-sm font-medium">뉴스/시사</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-purple-50 rounded border border-purple-200">
                  <span>🏢</span>
                  <span className="text-sm font-medium">비즈니스</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-indigo-50 rounded border border-indigo-200">
                  <span>📚</span>
                  <span className="text-sm font-medium">교육/강의</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-gray-50 rounded border border-gray-200">
                  <span>📌</span>
                  <span className="text-sm font-medium">일반</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {loading && (
          <div className="bg-white rounded-lg shadow-md p-12">
            <LoadingSpinner text="YouTube 영상 분석 중... (1-2분 소요)" />
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-red-900 mb-2">❌ 오류 발생</h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={() => {
                setError(null);
                setResult(null);
              }}
              className="mt-4 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
            >
              다시 시도
            </button>
          </div>
        )}

        {result && <AnalysisResult result={result} />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            Powered by Gemini API & Claude API
          </p>
        </div>
      </footer>
    </div>
  );
}
