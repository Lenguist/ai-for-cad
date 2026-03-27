import { NextRequest, NextResponse } from "next/server";
import partsData from "../../data/parts_library.json";

type Part = {
  name: string;
  category: string;
  length?: number | null;
  holes?: number[] | null;
  radius_studs?: number | null;
  teeth?: number | null;
  bl_id?: string;
  color?: string;
  description?: string;
};

const parts = partsData as Record<string, Part>;

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q")?.toLowerCase() ?? "";
  const cat = searchParams.get("category") ?? "";

  let results = Object.entries(parts).map(([id, part]) => ({ id, ...part }));

  if (q) {
    results = results.filter(
      (p) =>
        p.id.includes(q) ||
        p.name.toLowerCase().includes(q) ||
        (p.description ?? "").toLowerCase().includes(q)
    );
  }

  if (cat && cat !== "all") {
    results = results.filter((p) => p.category === cat);
  }

  const categories = [...new Set(Object.values(parts).map((p) => p.category))].sort();

  return NextResponse.json({ parts: results, categories, total: results.length });
}
