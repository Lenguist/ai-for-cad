import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Constrain output file tracing to this directory only.
  // Prevents Vercel from bundling the entire parent monorepo (compiler,
  // parts, agent, brickgpt, etc.) into the api/build serverless function.
  // On Vercel, MODAL_TOOL_URL is set so the local Python paths are never used.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  outputFileTracingRoot: path.join(__dirname) as any,
} as NextConfig;

export default nextConfig;
