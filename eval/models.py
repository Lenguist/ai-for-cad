"""
API clients for each model in the benchmark.
Each model exposes a single method: generate(prompt) -> GenerationResult
"""

import os
import re
import time
import json
import requests
from dataclasses import dataclass, field
from typing import Optional


# ── System prompt used for all LLM-based text-to-CadQuery models ──────────

CADQUERY_SYSTEM_PROMPT = """You are an expert CAD engineer specializing in CadQuery, a Python library for parametric 3D solid modeling.

Your task: generate CadQuery Python code that models the part described by the user.

STRICT REQUIREMENTS:
1. Start with: import cadquery as cq
2. Assign the final shape to a variable named exactly: result
3. `result` must be a cadquery.Workplane object
4. Use ONLY cadquery and the Python standard library — no numpy, scipy, or other dependencies
5. Output ONLY the raw Python code — no explanations, no markdown, no code fences

CADQUERY BASICS (use these patterns):
- Box:        result = cq.Workplane("XY").box(length, width, height)
- Cylinder:   result = cq.Workplane("XY").cylinder(height, radius)
- Sphere:     result = cq.Workplane("XY").sphere(radius)
- Hole:       .faces(">Z").workplane().hole(diameter)
- Shell:      .shell(-thickness)  # hollow out, negative = inward
- Move:       .translate((x, y, z))
- Union:      a.union(b)
- Cut:        a.cut(b)
- Fillet:     .edges("|Z").fillet(radius)
- Chamfer:    .edges("|Z").chamfer(length)
- Polar holes: .workplane().polarArray(radius, 0, 360, count).hole(diameter)
- Rect array: .workplane().rarray(xSpacing, ySpacing, xCount, yCount).hole(diameter)
"""


# ── Result dataclass ───────────────────────────────────────────────────────

@dataclass
class GenerationResult:
    model_id: str
    prompt_id: str
    prompt: str
    raw_response: str = ""
    code: str = ""          # extracted Python/CadQuery code
    error: Optional[str] = None
    latency_s: float = 0.0
    output_type: str = "cadquery"  # "cadquery" | "zoo_stl" | "error"
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id,
            "prompt_id": self.prompt_id,
            "prompt": self.prompt,
            "code": self.code,
            "error": self.error,
            "latency_s": round(self.latency_s, 2),
            "output_type": self.output_type,
            "metadata": self.metadata,
        }


# ── Code extraction helper ─────────────────────────────────────────────────

def extract_code(text: str) -> str:
    """Strip markdown fences and prose, return just the Python code."""
    # Try ```python ... ``` block
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Try ``` ... ``` block
    m = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # No fences — return as-is (trim whitespace)
    return text.strip()


# ── GPT-4o ────────────────────────────────────────────────────────────────

class GPT4oModel:
    model_id = "gpt-4o"
    output_type = "cadquery"

    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(
            model_id=self.model_id,
            prompt_id=prompt_id,
            prompt=prompt,
            output_type=self.output_type,
        )
        t0 = time.time()
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": CADQUERY_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=2048,
            )
            result.raw_response = response.choices[0].message.content
            result.code = extract_code(result.raw_response)
            result.metadata["tokens_in"] = response.usage.prompt_tokens
            result.metadata["tokens_out"] = response.usage.completion_tokens
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Claude Sonnet ─────────────────────────────────────────────────────────

class ClaudeModel:
    model_id = "claude-sonnet-4-6"
    output_type = "cadquery"

    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(
            model_id=self.model_id,
            prompt_id=prompt_id,
            prompt=prompt,
            output_type=self.output_type,
        )
        t0 = time.time()
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=CADQUERY_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            result.raw_response = response.content[0].text
            result.code = extract_code(result.raw_response)
            result.metadata["tokens_in"] = response.usage.input_tokens
            result.metadata["tokens_out"] = response.usage.output_tokens
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Gemini 2.0 Flash ──────────────────────────────────────────────────────

class GeminiModel:
    model_id = "gemini-2.0-flash"
    output_type = "cadquery"

    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=CADQUERY_SYSTEM_PROMPT,
        )

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(
            model_id=self.model_id,
            prompt_id=prompt_id,
            prompt=prompt,
            output_type=self.output_type,
        )
        t0 = time.time()
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": 0.1, "max_output_tokens": 2048},
            )
            result.raw_response = response.text
            result.code = extract_code(result.raw_response)
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Zoo ML-ephant ─────────────────────────────────────────────────────────

class ZooModel:
    """
    Zoo text-to-CAD API. Submits a prompt, polls until complete, returns STL bytes.
    Docs: https://zoo.dev/machine-learning-api
    """
    model_id = "zoo-ml-ephant"
    output_type = "zoo_stl"
    BASE_URL = "https://api.zoo.dev"
    POLL_INTERVAL = 3   # seconds between status checks
    MAX_WAIT = 120      # seconds before timeout

    def __init__(self):
        token = os.environ.get("ZOO_API_TOKEN")
        if not token:
            raise RuntimeError("ZOO_API_TOKEN not set")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(
            model_id=self.model_id,
            prompt_id=prompt_id,
            prompt=prompt,
            output_type=self.output_type,
        )
        t0 = time.time()
        try:
            # Submit job
            resp = requests.post(
                f"{self.BASE_URL}/ai/text-to-cad/stl",
                headers=self.headers,
                json={"prompt": prompt},
                timeout=30,
            )
            resp.raise_for_status()
            job = resp.json()
            job_id = job.get("id")
            if not job_id:
                result.error = f"No job ID in response: {job}"
                return result

            result.metadata["job_id"] = job_id

            # Poll until complete
            elapsed = 0
            while elapsed < self.MAX_WAIT:
                time.sleep(self.POLL_INTERVAL)
                elapsed += self.POLL_INTERVAL

                status_resp = requests.get(
                    f"{self.BASE_URL}/user/text-to-cad/{job_id}",
                    headers=self.headers,
                    timeout=30,
                )
                status_resp.raise_for_status()
                status_data = status_resp.json()
                status = status_data.get("status")
                result.metadata["final_status"] = status

                if status == "completed":
                    # outputs is a dict of filename -> base64-encoded bytes
                    outputs = status_data.get("outputs", {})
                    stl_key = next((k for k in outputs if k.endswith(".stl")), None)
                    if stl_key:
                        import base64
                        stl_bytes = base64.b64decode(outputs[stl_key])
                        result.metadata["stl_bytes_len"] = len(stl_bytes)
                        result.metadata["stl_bytes"] = outputs[stl_key]  # keep b64
                        result.code = f"# Zoo API output — STL ({len(stl_bytes)} bytes)"
                    else:
                        result.error = f"No STL in outputs: {list(outputs.keys())}"
                    break
                elif status in ("failed", "cancelled"):
                    result.error = f"Job {status}: {status_data.get('error', 'unknown')}"
                    break
                # else: still running — keep polling

            else:
                result.error = f"Timeout after {self.MAX_WAIT}s (job_id={job_id})"

        except Exception as e:
            result.error = str(e)

        result.latency_s = time.time() - t0
        return result


# ── Model registry ────────────────────────────────────────────────────────

ALL_MODELS = {
    "gpt-4o": GPT4oModel,
    "claude-sonnet-4-6": ClaudeModel,
    "gemini-2.0-flash": GeminiModel,
    "zoo-ml-ephant": ZooModel,
}


def load_available_models() -> dict:
    """
    Try to instantiate each model. Skip models whose API key is missing.
    Returns dict of model_id -> model_instance.
    """
    available = {}
    key_map = {
        "gpt-4o": "OPENAI_API_KEY",
        "claude-sonnet-4-6": "ANTHROPIC_API_KEY",
        "gemini-2.0-flash": "GOOGLE_API_KEY",
        "zoo-ml-ephant": "ZOO_API_TOKEN",
    }
    for model_id, cls in ALL_MODELS.items():
        env_key = key_map[model_id]
        if not os.environ.get(env_key):
            print(f"  ⚠  Skipping {model_id} — {env_key} not set")
            continue
        try:
            available[model_id] = cls()
            print(f"  ✓  Loaded {model_id}")
        except Exception as e:
            print(f"  ✗  Failed to load {model_id}: {e}")
    return available
