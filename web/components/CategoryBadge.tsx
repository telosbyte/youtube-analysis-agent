import { Category, CATEGORIES } from "@/lib/types";

interface CategoryBadgeProps {
  category: Category;
  confidence?: number;
}

export default function CategoryBadge({ category, confidence }: CategoryBadgeProps) {
  const info = CATEGORIES[category];

  return (
    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border-2 ${info.color}`}>
      <span className="text-2xl">{info.emoji}</span>
      <div>
        <div className="font-semibold">{info.name}</div>
        {confidence !== undefined && (
          <div className="text-xs opacity-75">신뢰도: {confidence}%</div>
        )}
      </div>
    </div>
  );
}
