# CAD Arena — Dynamic Benchmark ("Try It")

Live comparison tool: enter a text prompt, pick models, get STL outputs side by side.

## Architecture

- **Frontend**: Next.js page at `cadarena/site/app/try/page.tsx`
- **API route**: `cadarena/site/app/api/generate/route.ts`
  - Accepts: `{ prompt: string, models: string[] }`
  - Returns: `{ [modelId]: { stl_url: string, code: string, latency_s: number, error: string | null } }`
- **Backend**: Modal app (`cadarena/eval/modal_dynamic.py`) — spins up model inference per request

## Supported models (initial)

- `claude-opus-4-6` — Anthropic API, no GPU needed
- `gemini-2.5-flash` — Google API, no GPU needed
- `gpt-5` — OpenAI API, no GPU needed
- `zoo-ml-ephant` — Zoo API, no GPU needed
- `text2cadquery-qwen` — Modal GPU inference (Qwen 3B)

## Status

Not yet implemented. Static benchmark runs first.
