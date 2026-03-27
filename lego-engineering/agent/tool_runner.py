"""
tool_runner.py — Thin CLI wrapper around agent/tools.py

Called by the Next.js API route via child_process.
Reads a JSON command from stdin, executes it, prints JSON result to stdout.

Usage:
    echo '{"fn": "place", "args": {"spec": {"id": "b1", "type": "2x4", "pos": [0,0,0]}}}' | python tool_runner.py
    echo '{"fn": "inspect"}' | python tool_runner.py
    echo '{"fn": "save"}' | python tool_runner.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.tools import (
    place, remove, clear, inspect, save, simulate,
    search_parts, get_part, feedback
)

def run(command: dict) -> dict:
    fn = command.get("fn")
    args = command.get("args", {})

    try:
        if fn == "place":
            return place(args["spec"])
        elif fn == "remove":
            return remove(args["brick_id"])
        elif fn == "clear":
            return clear()
        elif fn == "inspect":
            return inspect()
        elif fn == "save":
            return save(args.get("filename", "assembly.ldr"))
        elif fn == "simulate":
            return simulate(args.get("level", 2))
        elif fn == "search_parts":
            return {"results": search_parts(args["query"])}
        elif fn == "get_part":
            result = get_part(args["part_id"])
            return result if result else {"error": f"Part '{args['part_id']}' not found"}
        elif fn == "feedback":
            msg = feedback()
            return {"feedback": msg}
        else:
            return {"error": f"Unknown function: {fn}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    command = json.loads(raw)
    result = run(command)
    print(json.dumps(result))
