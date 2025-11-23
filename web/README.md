# YouTube Analysis Web

Next.js 기반 YouTube 영상 AI 분석 웹 서비스

## 🌟 특징

- **자동 카테고리 분류**: Gemini AI가 영상을 7개 카테고리로 자동 분류
- **카테고리별 최적화 분석**: Claude가 각 카테고리에 특화된 심층 분석 제공
- **커스텀 분석**: 원하는 관점으로 자유롭게 분석 가능
- **실시간 분석**: 웹 인터페이스에서 즉시 결과 확인
- **JSON 내보내기**: 분석 결과를 JSON 파일로 저장 가능

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd web
npm install
```

### 2. 환경 변수 설정

```bash
cp .env.local.example .env.local
```

`.env.local` 파일을 열어 API 키 입력:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000) 열기

## 📦 프로젝트 구조

```
web/
├── app/
│   ├── api/
│   │   ├── extract/route.ts    # YouTube 스크립트 추출 API
│   │   └── analyze/route.ts    # 영상 분석 API
│   ├── layout.tsx              # 레이아웃
│   ├── page.tsx                # 메인 페이지
│   └── globals.css             # 글로벌 스타일
├── components/
│   ├── YouTubeInput.tsx        # URL 입력 폼
│   ├── AnalysisResult.tsx      # 분석 결과 표시
│   ├── CategoryBadge.tsx       # 카테고리 뱃지
│   └── LoadingSpinner.tsx      # 로딩 스피너
├── lib/
│   ├── types.ts                # TypeScript 타입 정의
│   ├── gemini.ts               # Gemini API 통합
│   └── claude.ts               # Claude API 통합
├── package.json
├── tsconfig.json
├── next.config.ts
└── tailwind.config.ts
```

## 🎨 지원 카테고리

| 카테고리 | 설명 | 분석 관점 |
|---------|------|----------|
| 🪙 **암호화폐/블록체인** | 비트코인, 이더리움 등 | 시장 전망, 투자 시그널, 리스크 |
| 💰 **금융/투자** | 주식, 부동산 등 | 투자 전략, 포트폴리오, 리스크 관리 |
| 💻 **기술/IT** | 프로그래밍, 소프트웨어 | 기술 스택, 실용성, 학습 난이도 |
| 📰 **뉴스/시사** | 뉴스, 시사 | 이슈 분석, 파급 효과, 객관성 |
| 🏢 **비즈니스/창업** | 비즈니스 모델 | 전략, 실행 방법, 성공 요인 |
| 📚 **교육/강의** | 강의, 튜토리얼 | 학습 목표, 난이도, 학습 로드맵 |
| 📌 **일반** | 일반 콘텐츠 | 종합 분석 |

## 🔧 API 엔드포인트

### POST `/api/extract`

YouTube 영상에서 스크립트 추출 및 카테고리 분류

**요청:**
```json
{
  "videoUrl": "https://www.youtube.com/watch?v=VIDEO_ID",
  "classify": true
}
```

**응답:**
```json
{
  "success": true,
  "data": {
    "content": "영상 스크립트...",
    "category": "crypto",
    "confidence": 95
  }
}
```

### POST `/api/analyze`

YouTube 영상 전체 분석 (추출 + 분석)

**요청:**
```json
{
  "videoUrl": "https://www.youtube.com/watch?v=VIDEO_ID",
  "customPrompt": "선택적 커스텀 프롬프트"
}
```

**응답:**
```json
{
  "success": true,
  "data": {
    "videoUrl": "...",
    "category": "crypto",
    "confidence": 95,
    "transcript": "...",
    "analysis": "...",
    "timestamp": "2025-11-23T...",
    "model": "claude-sonnet-4-5-20250929",
    "usage": {
      "inputTokens": 1500,
      "outputTokens": 800
    }
  }
}
```

## 🛠️ 기술 스택

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **AI APIs**:
  - Gemini API (YouTube 스크립트 추출 + 카테고리 분류)
  - Claude API (심층 분석)
- **Markdown**: react-markdown

## 📝 사용 예시

1. **기본 분석**
   - YouTube URL 입력
   - "분석 시작" 버튼 클릭
   - 자동으로 카테고리 분류 및 최적화 분석

2. **커스텀 분석**
   - "커스텀 프롬프트 사용" 체크
   - 원하는 분석 방향 입력
   - 예: "이 영상에서 투자 리스크만 정리해주세요"

3. **결과 활용**
   - 웹에서 바로 결과 확인
   - JSON 다운로드로 저장
   - 스크립트 전체 확인 가능

## 🚢 배포

### Vercel (추천)

1. GitHub 저장소에 푸시
2. [Vercel](https://vercel.com)에서 Import
3. 환경 변수 설정 (GEMINI_API_KEY, ANTHROPIC_API_KEY)
4. 자동 배포 완료!

### Docker

```bash
# Dockerfile 작성 후
docker build -t youtube-analysis-web .
docker run -p 3000:3000 \
  -e GEMINI_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  youtube-analysis-web
```

## 🔐 보안

- API 키는 서버 사이드에서만 사용 (`.env.local`)
- 클라이언트에 노출되지 않음
- HTTPS 사용 권장

## 📄 라이선스

MIT License

## 🤝 기여

이슈와 PR을 환영합니다!

## 📞 문의

프로젝트 이슈 페이지를 통해 문의해주세요.
