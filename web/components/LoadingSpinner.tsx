export default function LoadingSpinner({ text = "처리 중..." }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p className="text-gray-600">{text}</p>
    </div>
  );
}
