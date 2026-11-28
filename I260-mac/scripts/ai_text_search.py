#!/usr/bin/env python3
"""ai_text_search.py: search every text/*.pypdf.txt for text that addresses an AI agent or a language model (instructions to AI,
prompt-injection phrasing). Prints the matches with context; the count is the last line."""
import os, re
rx = re.compile(r"(ignore (all |any )?(the )?(previous|prior|above) (instructions|prompts)|as an AI( language model)?|you are an? (AI|assistant|language model)|"
                r"language model|large language model|\bLLMs?\b|ChatGPT|\bGPT-?[0-9]|\bClaude\b|Anthropic|AI (agent|assistant|reviewer)|"
                r"(note|message|instruction)s? (to|for) (the )?(AI|reviewer|referee|model)|do not (mention|cite|report)|when (summari[sz]ing|reviewing) this (paper|article))", re.I)
td = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "text")
n = 0
for f in sorted(os.listdir(td)):
    if not f.endswith(".pypdf.txt"): continue
    t = re.sub(r"\s+", " ", open(os.path.join(td, f), errors="replace").read())
    for m in rx.finditer(t):
        n += 1
        print(f"[{f[:-10]}] ...{t[max(0, m.start()-100): m.end()+100]}...")
print(n, "matches")
