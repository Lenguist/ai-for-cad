# Preliminary Benchmark Results — Run 1
*Date: 2026-03-03*
*Run ID: 20260303_210402*

## Setup
- **Prompts**: 20 across 4 difficulty tiers (5 per tier)
- **Models**: GPT-5, Claude Opus 4.6, Gemini 2.5 Flash, Zoo ML-ephant
- **LLM output format**: CadQuery Python code (executed locally via subprocess)
- **Zoo output format**: STL + STEP direct from API
- **Execution**: CadQuery installed locally, STL exported per valid result
- **Hardware**: Local Mac (eval pipeline), GPU not required for API models

## Results Table

| Model | API Success | Syntax Valid | Exec Valid | STL Exported | Avg Latency |
|-------|-------------|-------------|------------|-------------|-------------|
| Claude Opus 4.6 | 20/20 (100%) | 20/20 (100%) | 17/20 (85%) | **16/20 (80%)** | **8.6s** |
| GPT-5 | 20/20 (100%) | 14/20 (70%) | 14/20 (70%) | 14/20 (70%) | 23.3s |
| Zoo ML-ephant | 16/20 (80%) | 16/20 (80%) | 16/20 (80%) | 16/20 (80%) | 64.8s |
| Gemini 2.5 Flash | 7/20 (35%) | 7/20 (35%) | 7/20 (35%) | 7/20 (35%) | ~3s* |

*Gemini: 13/20 failed due to free-tier rate limiting (429 quota exceeded), not model failure.

## Per-Tier Breakdown (estimated from logs)

| Tier | Description | Claude | GPT-5 | Zoo |
|------|-------------|--------|-------|-----|
| T1 | Simple primitives | 4/5 | 5/5 | 5/5 |
| T2 | Single part + features | 5/5 | 4/5 | 4/5 |
| T3 | Multi-feature parts | 4/5 | 3/5 | 5/5 |
| T4 | Complex functional | 3/5 | 2/5 | 2/5 |

## Key Findings

1. **Claude Opus 4.6 leads**: Best syntax validity (100%), fastest (8.6s avg), 80% STL export rate. Every generated code file was syntactically valid Python.

2. **GPT-5 slower and less consistent**: 23s avg latency vs 8.6s for Claude. Drops to 70% on harder prompts — generates valid-looking but non-executable CadQuery more often.

3. **Zoo is quality-competitive but slow**: Matches Claude at 80% success on T1-T3, but fails on complex T4 geometry (pipe elbow, spring timed out at 120s). Avg 64.8s is ~8× slower than Claude. Commercial overhead is significant.

4. **Gemini rate-limited**: Free tier hit quota after 7 requests. Not a signal about model quality — need upgraded API key or retry-with-backoff logic.

5. **Tier 4 is hard for everyone**: Complex functional parts (gears, pipe elbows, springs) fail across all models. Expected — this validates our difficulty tiers are meaningful.

## Pipeline Validation

The evaluation pipeline is working end-to-end:
- ✓ API calls to all 4 models
- ✓ CadQuery code extraction from LLM responses (markdown stripping)
- ✓ Subprocess execution with 120s timeout
- ✓ STL export via CadQuery exporters
- ✓ STEP + STL export from Zoo API
- ✓ Results saved to JSONL + summary JSON

## Next Steps

1. Fix Gemini rate limiting (retry-with-backoff or upgrade API key)
2. Add per-tier breakdown to analyze.py output
3. Add self-hosted models (Text2CAD, FlexCAD, CADFusion) on cloud GPU
4. Add Chamfer Distance metric against ground truth STEP files
5. Display results on website leaderboard page
