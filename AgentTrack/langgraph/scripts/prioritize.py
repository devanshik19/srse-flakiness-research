#!/usr/bin/env python3
import re, sys
from collections import Counter
SRC = sys.argv[1] if len(sys.argv) > 1 else "tests_all.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "tests_queue.txt"
TIERS = [                       # first match wins; higher = more likely non-deterministic
    (r"async|_aio|aio_", 100),
    (r"concurr|parallel|thread|worksteal|race", 95),
    (r"stream", 85),
    (r"interleave|arrival|order", 80),
    (r"retry|timeout|interrupt|defer|debounce", 75),
    (r"cache|checkpoint|sqlite|postgres|store|pool|pipe|ttl|durability", 70),
    (r"pregel|large_cases|subgraph|remote|command|\bsend\b", 60),
    (r"pydantic|runtime|config|managed", 40),
]
def score(nid):
    s = nid.lower()
    for rx, sc in TIERS:
        if re.search(rx, s): return sc
    return 10
tests = sorted((l.strip() for l in open(SRC) if "::" in l), key=lambda t: (-score(t), t))
open(OUT, "w").write("\n".join(tests) + "\n")
print(f"queued {len(tests)} tests -> {OUT}")
for sc, n in sorted(Counter(score(t) for t in tests).items(), reverse=True):
    print(f"  score {sc}: {n}")
