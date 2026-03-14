"""
API clients for each model in the benchmark.
Each model exposes a single method: generate(prompt_id, prompt) -> GenerationResult
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

OPENSCAD_SYSTEM_PROMPT = """You are an expert CAD engineer specializing in OpenSCAD, a script-based parametric 3D modeling tool.

Your task: generate OpenSCAD code that models the part described by the user.

STRICT REQUIREMENTS:
1. Output ONLY the raw OpenSCAD code — no explanations, no markdown, no code fences
2. The model should render correctly with default OpenSCAD settings
3. All dimensions in millimeters

OPENSCAD BASICS:
- Box:        cube([length, width, height], center=true);
- Cylinder:   cylinder(h=height, r=radius, center=true);
- Sphere:     sphere(r=radius);
- Hole:       difference() { main_shape(); translate([x,y,z]) cylinder(...); }
- Union:      union() { shape1(); shape2(); }
- Difference: difference() { base(); cutout(); }
"""


# ── Result dataclass ───────────────────────────────────────────────────────

@dataclass
class GenerationResult:
    model_id: str
    prompt_id: str
    prompt: str
    raw_response: str = ""
    code: str = ""
    error: Optional[str] = None
    latency_s: float = 0.0
    output_type: str = "cadquery"   # "cadquery" | "openscad" | "kcl" | "error"
    attempts: int = 1               # >1 for self-correcting models
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model_id":    self.model_id,
            "prompt_id":   self.prompt_id,
            "prompt":      self.prompt,
            "code":        self.code,
            "error":       self.error,
            "latency_s":   round(self.latency_s, 2),
            "output_type": self.output_type,
            "attempts":    self.attempts,
            "metadata":    self.metadata,
        }


# ── Code extraction helper ─────────────────────────────────────────────────

def extract_code(text: str, lang: str = "python") -> str:
    """Strip markdown fences and prose, return just the code."""
    m = re.search(rf"```{lang}\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


# ── Claude Opus 4.6 ────────────────────────────────────────────────────────

class ClaudeModel:
    model_id    = "claude-opus-4-6"
    model_name  = "claude-opus-4-6"
    output_type = "cadquery"

    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(model_id=self.model_id, prompt_id=prompt_id,
                                  prompt=prompt, output_type=self.output_type)
        t0 = time.time()
        try:
            resp = self.client.messages.create(
                model=self.model_name,
                max_tokens=2048,
                system=CADQUERY_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            result.raw_response = resp.content[0].text
            result.code = extract_code(result.raw_response)
            result.metadata["tokens_in"]  = resp.usage.input_tokens
            result.metadata["tokens_out"] = resp.usage.output_tokens
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Claude Sonnet 4.6 ──────────────────────────────────────────────────────

class ClaudeSonnetModel(ClaudeModel):
    model_id   = "claude-sonnet-4-6"
    model_name = "claude-sonnet-4-6"


# ── GPT-5 ─────────────────────────────────────────────────────────────────

class GPT5Model:
    model_id    = "gpt-5"
    model_name  = "gpt-5"
    output_type = "cadquery"

    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(model_id=self.model_id, prompt_id=prompt_id,
                                  prompt=prompt, output_type=self.output_type)
        t0 = time.time()
        try:
            resp = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": CADQUERY_SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                max_completion_tokens=2048,
            )
            result.raw_response = resp.choices[0].message.content
            result.code = extract_code(result.raw_response)
            result.metadata["tokens_in"]  = resp.usage.prompt_tokens
            result.metadata["tokens_out"] = resp.usage.completion_tokens
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── GPT-5.4 ───────────────────────────────────────────────────────────────

class GPT54Model(GPT5Model):
    model_id   = "gpt-5.4"
    model_name = "gpt-5.4"


# ── Gemini 2.5 Flash ──────────────────────────────────────────────────────

class GeminiModel:
    model_id    = "gemini-2.5-flash"
    model_name  = "gemini-2.5-flash"
    output_type = "cadquery"

    def __init__(self):
        from google import genai
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        from google.genai import types
        result = GenerationResult(model_id=self.model_id, prompt_id=prompt_id,
                                  prompt=prompt, output_type=self.output_type)
        t0 = time.time()
        for attempt in range(5):
            try:
                resp = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=CADQUERY_SYSTEM_PROMPT,
                        temperature=0.1,
                        max_output_tokens=2048,
                    ),
                )
                result.raw_response = resp.text
                result.code = extract_code(result.raw_response)
                result.error = None
                break
            except Exception as e:
                err = str(e)
                if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                    wait = (2 ** attempt) * 5
                    print(f"    [Gemini] rate-limited, waiting {wait}s (attempt {attempt+1}/5)")
                    time.sleep(wait)
                    if attempt == 4:
                        result.error = err
                else:
                    result.error = err
                    break
        result.latency_s = time.time() - t0
        return result


# ── Gemini 3.1 Pro ────────────────────────────────────────────────────────

class GeminiProModel(GeminiModel):
    model_id   = "gemini-3.1-pro"
    model_name = "gemini-3.1-pro"


# ── DeepSeek V3 ───────────────────────────────────────────────────────────

class DeepSeekModel:
    model_id    = "deepseek-v3"
    output_type = "cadquery"

    def __init__(self):
        import openai
        self.client = openai.OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        )

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(model_id=self.model_id, prompt_id=prompt_id,
                                  prompt=prompt, output_type=self.output_type)
        t0 = time.time()
        try:
            resp = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": CADQUERY_SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=2048,
                temperature=0.1,
            )
            result.raw_response = resp.choices[0].message.content
            result.code = extract_code(result.raw_response)
            result.metadata["tokens_in"]  = resp.usage.prompt_tokens
            result.metadata["tokens_out"] = resp.usage.completion_tokens
        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Zoo ML-ephant ─────────────────────────────────────────────────────────

class ZooModel:
    model_id      = "zoo-ml-ephant"
    output_type   = "kcl"
    BASE_URL      = "https://api.zoo.dev"
    POLL_INTERVAL = 3
    MAX_WAIT      = 120

    def __init__(self):
        token = os.environ.get("ZOO_API_TOKEN")
        if not token:
            raise RuntimeError("ZOO_API_TOKEN not set")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        result = GenerationResult(model_id=self.model_id, prompt_id=prompt_id,
                                  prompt=prompt, output_type=self.output_type)
        t0 = time.time()
        try:
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

            elapsed = 0
            while elapsed < self.MAX_WAIT:
                time.sleep(self.POLL_INTERVAL)
                elapsed += self.POLL_INTERVAL
                status_resp = requests.get(
                    f"{self.BASE_URL}/user/text-to-cad/{job_id}",
                    headers=self.headers, timeout=30,
                )
                status_resp.raise_for_status()
                status_data = status_resp.json()
                status = status_data.get("status")
                result.metadata["final_status"] = status

                if status == "completed":
                    import base64
                    outputs = status_data.get("outputs", {})
                    def _b64(s):
                        s = s.replace("-", "+").replace("_", "/")
                        s += "=" * (-len(s) % 4)
                        return base64.b64decode(s)
                    stl_key  = next((k for k in outputs if k.endswith(".stl")),  None)
                    step_key = next((k for k in outputs if k.endswith(".step")), None)
                    kcl_code = status_data.get("code") or ""
                    if kcl_code:
                        result.code = kcl_code
                    if stl_key:
                        stl_bytes = _b64(outputs[stl_key])
                        result.metadata["stl_bytes_len"] = len(stl_bytes)
                        result.metadata["stl_bytes"] = base64.b64encode(stl_bytes).decode()
                    if step_key:
                        step_bytes = _b64(outputs[step_key])
                        result.metadata["step_bytes"] = base64.b64encode(step_bytes).decode()
                    if not stl_key and not step_key and not kcl_code:
                        result.error = f"No STL/STEP in outputs: {list(outputs.keys())}"
                    break
                elif status in ("failed", "cancelled"):
                    result.error = f"Job {status}: {status_data.get('error', 'unknown')}"
                    break
            else:
                result.error = f"Timeout after {self.MAX_WAIT}s"

        except Exception as e:
            result.error = str(e)
        result.latency_s = time.time() - t0
        return result


# ── Self-Correcting Wrapper ────────────────────────────────────────────────

class SelfCorrectingWrapper:
    """
    Wraps any CadQuery-outputting model with an error-feedback retry loop.

    On each failed execution the error is fed back to the LLM as a follow-up
    message, asking it to fix the code. Tracks total attempts in metadata.

    max_retries=3 means up to 4 total attempts (1 initial + 3 corrections).
    """

    def __init__(self, base_model, max_retries: int = 3):
        self.base       = base_model
        self.max_retries = max_retries
        self.model_id   = f"{base_model.model_id}-sc"
        self.output_type = "cadquery"

    def _try_execute(self, code: str) -> dict:
        """Quick in-process syntax check + subprocess CadQuery execution."""
        import ast
        try:
            ast.parse(code)
        except SyntaxError as e:
            return {"ok": False, "error": f"SyntaxError: {e}"}

        import sys, tempfile, subprocess
        from pathlib import Path
        eval_dir = Path(__file__).parent
        sys.path.insert(0, str(eval_dir))
        from execute import validate_cadquery
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            result = validate_cadquery(code, Path(tmp), "sc_check", timeout=45)
        if result.get("stl_exported"):
            return {"ok": True, "error": None}
        err = result.get("exec_error") or result.get("syntax_error") or "Unknown error"
        return {"ok": False, "error": err}

    def _correct(self, base_model, prompt: str, previous_code: str,
                 error: str) -> tuple[str, str, Optional[str]]:
        """Ask the model to fix code given an error. Returns (raw, code, error)."""
        correction_msg = (
            f"The code you generated failed with the following error:\n\n"
            f"```\n{error}\n```\n\n"
            f"Please fix the code. Return only the corrected Python code, "
            f"no explanations."
        )
        # Build multi-turn conversation
        messages = [
            {"role": "user",      "content": prompt},
            {"role": "assistant", "content": previous_code},
            {"role": "user",      "content": correction_msg},
        ]
        t0 = time.time()
        try:
            # Dispatch to the right API
            if isinstance(base_model, (ClaudeModel, ClaudeSonnetModel)):
                resp = base_model.client.messages.create(
                    model=base_model.model_name,
                    max_tokens=2048,
                    system=CADQUERY_SYSTEM_PROMPT,
                    messages=messages,
                )
                raw = resp.content[0].text
            elif isinstance(base_model, (GPT5Model, GPT54Model)):
                oai_msgs = [{"role": "system", "content": CADQUERY_SYSTEM_PROMPT}] + messages
                resp = base_model.client.chat.completions.create(
                    model=base_model.model_name,
                    messages=oai_msgs,
                    max_completion_tokens=2048,
                )
                raw = resp.choices[0].message.content
            elif isinstance(base_model, (GeminiModel, GeminiProModel)):
                from google.genai import types
                # Gemini uses contents list
                contents = []
                for m in messages:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": m["content"]}]})
                resp = base_model.client.models.generate_content(
                    model=base_model.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=CADQUERY_SYSTEM_PROMPT,
                        temperature=0.1,
                        max_output_tokens=2048,
                    ),
                )
                raw = resp.text
            else:
                return "", "", "SC not supported for this model type"
            code = extract_code(raw)
            return raw, code, None
        except Exception as e:
            return "", "", str(e)

    def generate(self, prompt_id: str, prompt: str) -> GenerationResult:
        # Initial generation via base model
        result = self.base.generate(prompt_id, prompt)
        result.model_id   = self.model_id
        result.attempts   = 1

        if result.error or not result.code:
            return result

        # Try to execute; if good, return immediately
        check = self._try_execute(result.code)
        if check["ok"]:
            return result

        # Retry loop
        current_code = result.code
        total_latency = result.latency_s

        for attempt in range(self.max_retries):
            error_msg = check["error"]
            print(f"    [SC/{self.model_id}] attempt {attempt+2}/{self.max_retries+1} — fixing: {error_msg[:80]}")

            t0 = time.time()
            raw, new_code, api_err = self._correct(self.base, prompt, current_code, error_msg)
            total_latency += time.time() - t0

            if api_err:
                result.error = api_err
                break

            current_code = new_code
            result.code  = new_code
            result.attempts += 1

            check = self._try_execute(new_code)
            if check["ok"]:
                result.error = None
                break
        else:
            # All retries exhausted — keep last generated code, mark final error
            result.metadata["sc_final_error"] = check.get("error")

        result.latency_s = total_latency
        return result


# ── Model registry ────────────────────────────────────────────────────────

ALL_MODELS = {
    # LLM baselines
    "claude-opus-4-6":     ClaudeModel,
    "claude-sonnet-4-6":   ClaudeSonnetModel,
    "gpt-5":               GPT5Model,
    "gpt-5.4":             GPT54Model,
    "gemini-2.5-flash":    GeminiModel,
    "gemini-3.1-pro":      GeminiProModel,
    "deepseek-v3":         DeepSeekModel,
    # Self-correcting variants
    "claude-opus-4-6-sc":   lambda: SelfCorrectingWrapper(ClaudeModel()),
    "claude-sonnet-4-6-sc": lambda: SelfCorrectingWrapper(ClaudeSonnetModel()),
    "gpt-5.4-sc":           lambda: SelfCorrectingWrapper(GPT54Model()),
    "gemini-3.1-pro-sc":    lambda: SelfCorrectingWrapper(GeminiProModel()),
    # Commercial
    "zoo-ml-ephant":       ZooModel,
}

ENV_KEYS = {
    "claude-opus-4-6":      "ANTHROPIC_API_KEY",
    "claude-sonnet-4-6":    "ANTHROPIC_API_KEY",
    "claude-opus-4-6-sc":   "ANTHROPIC_API_KEY",
    "claude-sonnet-4-6-sc": "ANTHROPIC_API_KEY",
    "gpt-5":                "OPENAI_API_KEY",
    "gpt-5.4":              "OPENAI_API_KEY",
    "gpt-5.4-sc":           "OPENAI_API_KEY",
    "gemini-2.5-flash":     "GOOGLE_API_KEY",
    "gemini-3.1-pro":       "GOOGLE_API_KEY",
    "gemini-3.1-pro-sc":    "GOOGLE_API_KEY",
    "deepseek-v3":          "DEEPSEEK_API_KEY",
    "zoo-ml-ephant":        "ZOO_API_TOKEN",
}


def load_model(model_id: str):
    """Instantiate a single model by ID."""
    if model_id not in ALL_MODELS:
        raise ValueError(f"Unknown model: {model_id}. Available: {list(ALL_MODELS)}")
    env_key = ENV_KEYS.get(model_id)
    if env_key and not os.environ.get(env_key):
        raise RuntimeError(f"{model_id} requires {env_key} to be set")
    factory = ALL_MODELS[model_id]
    return factory() if callable(factory) else factory


def load_available_models() -> dict:
    """Try to instantiate each model. Skip models whose API key is missing."""
    available = {}
    for model_id in ALL_MODELS:
        env_key = ENV_KEYS.get(model_id)
        if env_key and not os.environ.get(env_key):
            print(f"  ⚠  Skipping {model_id} — {env_key} not set")
            continue
        try:
            available[model_id] = load_model(model_id)
            print(f"  ✓  Loaded {model_id}")
        except Exception as e:
            print(f"  ✗  Failed to load {model_id}: {e}")
    return available
