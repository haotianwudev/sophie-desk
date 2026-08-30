#!/usr/bin/env python3
"""Thin wrapper around the local Ollama API. Not an agent, not a worker --
Ollama is pure text/embeddings in, text/embeddings out. Whoever holds a task
(claude or agy) calls this as a tool for cheap bulk work (skimming many
papers, embedding text) and does everything else -- reading files, deciding
what matters, writing results, claiming/closing the task -- themselves.

Usage:
    python scripts/ollama_call.py generate "<prompt>" [--model qwen3.5]
    python scripts/ollama_call.py embed "<text>" [--model bge-m3]
"""

from __future__ import annotations
import argparse
import json
import sys
import urllib.request

BASE = "http://localhost:11434"


def generate(prompt: str, model: str = "qwen3.5") -> str:
    req = urllib.request.Request(
        f"{BASE}/api/generate",
        data=json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["response"]


def embed(text: str, model: str = "bge-m3") -> list[float]:
    req = urllib.request.Request(
        f"{BASE}/api/embed",
        data=json.dumps({"model": model, "input": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["embeddings"][0]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("prompt")
    g.add_argument("--model", default="qwen3.5")

    e = sub.add_parser("embed")
    e.add_argument("text")
    e.add_argument("--model", default="bge-m3")

    args = ap.parse_args()
    if args.cmd == "generate":
        print(generate(args.prompt, args.model))
    elif args.cmd == "embed":
        vec = embed(args.text, args.model)
        print(f"{len(vec)}-dim vector, first 5: {vec[:5]}")
