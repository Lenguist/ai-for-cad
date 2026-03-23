import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { NextRequest, NextResponse } from "next/server";

function createLimiters() {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token) return null;

  const redis = new Redis({ url, token });
  return {
    anon: new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(3, "7 d"),
      prefix: "cad-arena:anon",
    }),
    email: new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(10, "7 d"),
      prefix: "cad-arena:email",
    }),
  };
}

const limiters = createLimiters();

export async function middleware(req: NextRequest) {
  if (!req.nextUrl.pathname.startsWith("/api/generate")) {
    return NextResponse.next();
  }

  if (!limiters) return NextResponse.next();

  const ip =
    req.headers.get("x-real-ip") ??
    req.headers.get("x-forwarded-for")?.split(",")[0].trim() ??
    "anonymous";

  const hasEmail = req.cookies.get("cad_arena_email")?.value === "1";
  const limiter = hasEmail ? limiters.email : limiters.anon;
  const key = hasEmail ? `email:${ip}` : `anon:${ip}`;

  const { success, limit, remaining, reset } = await limiter.limit(key);

  if (!success) {
    return NextResponse.json(
      {
        error: hasEmail
          ? "You've used your 10 tries for this week. Check back next week!"
          : "You've used your 3 free tries. Enter your email to unlock 10 tries/week.",
        limit,
        remaining: 0,
        reset,
        needsEmail: !hasEmail,
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
