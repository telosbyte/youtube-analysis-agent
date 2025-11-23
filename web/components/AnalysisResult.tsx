"use client";

import { AnalysisResult as AnalysisResultType } from "@/lib/types";
import CategoryBadge from "./CategoryBadge";
import ReactMarkdown from "react-markdown";

interface AnalysisResultProps {
  result: AnalysisResultType;
}

export default function AnalysisResult({ result }: AnalysisResultProps) {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <h2 className="text-2xl font-bold text-gray-900">분석 결과</h2>

        <div className="flex items-center gap-4">
          <CategoryBadge category={result.category} confidence={result.confidence} />
        </div>

        <div className="text-sm text-gray-600">
          <p>영상 URL: <a href={result.videoUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{result.videoUrl}</a></p>
          <p>분석 시간: {new Date(result.timestamp).toLocaleString('ko-KR')}</p>
          {result.usage && (
            <p className="text-xs">
              토큰 사용: {result.usage.inputTokens.toLocaleString()} 입력 / {result.usage.outputTokens.toLocaleString()} 출력
            </p>
          )}
        </div>
      </div>

      {/* Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📊 분석 내용</h3>
        <div className="prose prose-slate max-w-none">
          <ReactMarkdown>{result.analysis}</ReactMarkdown>
        </div>
      </div>

      {/* Transcript (collapsible) */}
      <details className="bg-white rounded-lg shadow-md p-6">
        <summary className="text-lg font-semibold text-gray-900 cursor-pointer hover:text-blue-600">
          📝 스크립트 전체 보기
        </summary>
        <div className="mt-4 text-sm text-gray-700 whitespace-pre-wrap max-h-96 overflow-y-auto border-t pt-4">
          {result.transcript}
        </div>
      </details>

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={() => window.location.reload()}
          className="flex-1 bg-gray-200 text-gray-800 py-3 px-6 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
        >
          새로운 분석
        </button>
        <button
          onClick={() => {
            const data = JSON.stringify(result, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analysis-${Date.now()}.json`;
            a.click();
          }}
          className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          JSON 다운로드
        </button>
      </div>
    </div>
  );
}
