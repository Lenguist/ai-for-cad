import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { NextRequest, NextResponse } from "next/server";

// Only apply rate limiting if Upstash env vars are set.
// Graceful degradation: if not configured, all requests pass through.
function getRatelimiter() {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token) return null;

  const redis = new Redis({ url, token });
  return new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(5, "24 h"),
    prefix: "cad-arena:rl",
  });
}

const ratelimiter = getRatelimiter();

export async function middleware(req: NextRequest) {
  // Only rate-limit the generate API
  if (!req.nextUrl.pathname.startsWith("/api/generate")) {
    return NextResponse.next();
  }

  if (!ratelimiter) {
    return NextResponse.next();
  }

  // Use IP from Vercel header, fall back to x-forwarded-for
  const ip =
    req.headers.get("x-real-ip") ??
    req.headers.get("x-forwarded-for")?.split(",")[0].trim() ??
    "anonymous";

  const { success, limit, remaining, reset } = await ratelimiter.limit(ip);

  if (!success) {
    return NextResponse.json(
      {
        error: "Rate limit exceeded. You can submit 5 prompts per day.",
        limit,
        remaining: 0,
        reset,
      },
      {
        status: 429,
        headers: {
          "X-RateLimit-Limit": String(limit),
          "X-RateLimit-Remaining": "0",
          "X-RateLimit-Reset": String(reset),
        },
      }
    );
  }

  const res = NextResponse.next();
  res.headers.set("X-RateLimit-Limit", String(limit));
  res.headers.set("X-RateLimit-Remaining", String(remaining));
  res.headers.set("X-RateLimit-Reset", String(reset));
  return res;
}

export const config = {
  matcher: "/api/generate",
};
