// Category types
export type Category =
  | 'crypto'
  | 'finance'
  | 'tech'
  | 'news'
  | 'business'
  | 'education'
  | 'general';

// YouTube extraction result
export interface ExtractionResult {
  content: string;
  category?: Category;
  confidence?: number;
  metadata?: {
    title?: string;
    duration?: string;
    [key: string]: any;
  };
}

// Analysis request
export interface AnalysisRequest {
  videoUrl: string;
  customPrompt?: string;
  category?: Category;
}

// Analysis result
export interface AnalysisResult {
  videoUrl: string;
  category: Category;
  confidence?: number;
  transcript: string;
  analysis: string;
  timestamp: string;
  model: string;
  usage?: {
    inputTokens: number;
    outputTokens: number;
  };
}

// API response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

// Category metadata
export interface CategoryInfo {
  name: string;
  emoji: string;
  description: string;
  color: string;
}

export const CATEGORIES: Record<Category, CategoryInfo> = {
  crypto: {
    name: '암호화폐/블록체인',
    emoji: '🪙',
    description: '암호화폐, 블록체인, DeFi 관련',
    color: 'bg-yellow-100 text-yellow-800 border-yellow-300'
  },
  finance: {
    name: '금융/투자',
    emoji: '💰',
    description: '주식, 부동산, 투자 전략',
    color: 'bg-green-100 text-green-800 border-green-300'
  },
  tech: {
    name: '기술/IT',
    emoji: '💻',
    description: '프로그래밍, 소프트웨어, 하드웨어',
    color: 'bg-blue-100 text-blue-800 border-blue-300'
  },
  news: {
    name: '뉴스/시사',
    emoji: '📰',
    description: '뉴스, 시사, 정치',
    color: 'bg-red-100 text-red-800 border-red-300'
  },
  business: {
    name: '비즈니스/창업',
    emoji: '🏢',
    description: '비즈니스, 창업, 경영',
    color: 'bg-purple-100 text-purple-800 border-purple-300'
  },
  education: {
    name: '교육/강의',
    emoji: '📚',
    description: '강의, 튜토리얼, 학습',
    color: 'bg-indigo-100 text-indigo-800 border-indigo-300'
  },
  general: {
    name: '일반',
    emoji: '📌',
    description: '일반적인 콘텐츠',
    color: 'bg-gray-100 text-gray-800 border-gray-300'
  }
};
