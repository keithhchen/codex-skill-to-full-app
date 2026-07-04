#!/usr/bin/env python3
"""Audit a Skill-to-App plan for required AI-native app layers."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


CHECKS = {
    "first_useful_version": [r"first useful version", r"when .+ provides .+ produces"],
    "client_layer": [r"client layer", r"openai sdk", r"vercel ai sdk", r"litellm", r"baseurl"],
    "runtime_layer": [r"runtime layer", r"tool loop", r"langgraph", r"agents sdk", r"pydanticai"],
    "app_layer": [r"app layer", r"ui", r"api route", r"review screen", r"history"],
    "product_infrastructure": [r"product infrastructure", r"persistence", r"auth", r"object storage", r"queue", r"cron", r"webhook"],
    "deployment": [r"deployment", r"docker", r"vercel", r"cloudflare", r"railway", r"render", r"health"],
    "llm_provider": [r"llm provider", r"model provider", r"deepseek", r"kimi", r"glm", r"qwen", r"model_base_url"],
    "structured_output": [r"structured output", r"json schema", r"response_format", r"output schema"],
    "tool_calling": [r"tool call", r"tools", r"execute tool"],
    "state_trace": [r"state", r"trace", r"run history", r"tool_calls"],
    "human_review": [r"human review", r"approval", r"approve", r"review gate"],
    "evals": [r"eval", r"baseline", r"regression", r"bad case"],
}

SINGLE_CALL_PATTERNS = [r"single api call", r"one api call", r"/chat endpoint"]
REJECTION_PATTERNS = [
    r"avoid",
    r"reject",
    r"correct",
    r"anti-pattern",
    r"do not",
    r"not collapse",
    r"instead",
    r"no state",
    r"no output schema",
]


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: audit-app-plan.py path/to/plan.md", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    results = {}
    for key, patterns in CHECKS.items():
        results[key] = has_any(text, patterns)

    required_keys = list(CHECKS)
    missing = [key for key in required_keys if not results[key]]
    risk_flags = []
    single_call_mentioned = has_any(text, SINGLE_CALL_PATTERNS)
    single_call_rejected = has_any(text, REJECTION_PATTERNS)
    if single_call_mentioned and not single_call_rejected:
        risk_flags.append("mentions single-call/chat-endpoint pattern without rejecting or correcting it")

    report = {
        "path": str(path),
        "passed": not missing and not risk_flags,
        "missing": missing,
        "risk_flags": risk_flags,
        "single_call_mentioned": single_call_mentioned,
        "single_call_rejected_or_corrected": single_call_rejected,
        "checks": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
