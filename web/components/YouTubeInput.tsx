"use client";

import { useState } from "react";

interface YouTubeInputProps {
  onSubmit: (url: string, customPrompt?: string) => void;
  loading: boolean;
}

export default function YouTubeInput({ onSubmit, loading }: YouTubeInputProps) {
  const [url, setUrl] = useState("");
  const [customPrompt, setCustomPrompt] = useState("");
  const [useCustomPrompt, setUseCustomPrompt] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    onSubmit(url.trim(), useCustomPrompt && customPrompt ? customPrompt : undefined);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto space-y-4">
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
          YouTube URL
        </label>
        <input
          id="url"
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={loading}
        />
      </div>

      <div className="flex items-center gap-2">
        <input
          id="use-custom"
          type="checkbox"
          checked={useCustomPrompt}
          onChange={(e) => setUseCustomPrompt(e.target.checked)}
          className="w-4 h-4 text-blue-600 rounded"
          disabled={loading}
        />
        <label htmlFor="use-custom" className="text-sm text-gray-700">
          커스텀 프롬프트 사용
        </label>
      </div>

      {useCustomPrompt && (
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
            분석 프롬프트 (선택)
          </label>
          <textarea
            id="prompt"
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="예: 이 영상에서 투자 리스크만 정리해주세요"
            rows={3}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !url.trim()}
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "분석 중..." : "분석 시작"}
      </button>
    </form>
  );
}
