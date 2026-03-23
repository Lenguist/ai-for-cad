import { Redis } from "@upstash/redis";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const { prompt, winner, models } = (await req.json()) as {
    prompt: string;
    winner: string;
    models: string[];
  };

  if (!prompt || !winner) {
    return NextResponse.json({ error: "missing fields" }, { status: 400 });
  }

  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (url && token) {
    const redis = new Redis({ url, token });
    await Promise.all([
      redis.rpush("cad-arena:votes", JSON.stringify({ prompt, winner, models, ts: new Date().toISOString() })),
      redis.hincrby("cad-arena:win-counts", winner, 1),
    ]);
  }

  return NextResponse.json({ ok: true });
}
