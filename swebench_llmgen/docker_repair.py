#!/usr/bin/env python3
# docker_repair.py <gen_out_dir> [--model gpt-5-mini]
# For each instance folder, start its Epoch image and run every generated test inside the
# testbed conda env. For each test that fails to run, ask the model ONCE to fix it (feeding
# back the pytest error) and write the fix back in place. Run this before docker_validate.sh
# so the stress runs only see clean, runnable tests.
#
#   OPENAI_API_KEY=... python3 docker_repair.py gen_out --model gpt-5-mini
import argparse, re, subprocess
from pathlib import Path
from openai import OpenAI

client = OpenAI()
ACT = "source /opt/miniconda3/bin/activate && conda activate testbed"
REPAIR_SYSTEM = (
    "You previously wrote a pytest test that failed to run. I give you the test and its pytest "
    "error output. Fix it so it imports and runs. Return only the corrected code in one ```python block."
)


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def run_in(cid, fname):   # run one test file in the container -> (ok, tail_of_output)
    r = sh(f'docker exec {cid} bash -lc "{ACT} && cd /testbed && '
           f'python -m pytest _gen_tests/{fname} -q --tb=short -p no:cacheprovider"')
    out = r.stdout + r.stderr
    return r.returncode == 0, out[-1500:]


def fix(code, err, model):
    msg = f"# Test:\n{code}\n\n# pytest error:\n{err}\n\nFix it."
    kw = dict(model=model, messages=[{"role": "system", "content": REPAIR_SYSTEM},
                                     {"role": "user", "content": msg}])
    if model.startswith("gpt-5"):
        kw["reasoning_effort"] = "minimal"; kw["max_completion_tokens"] = 2500
    else:
        kw["max_tokens"] = 2500
    text = client.chat.completions.create(**kw).choices[0].message.content or ""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gen_out")
    ap.add_argument("--model", default="gpt-5-mini")
    a = ap.parse_args()

    for d in sorted(Path(a.gen_out).iterdir()):
        if not d.is_dir():
            continue
        inst = d.name
        img = f"ghcr.io/epoch-research/swe-bench.eval.x86_64.{inst}"
        print(f"===== {inst} =====", flush=True)
        if sh(f"docker pull -q {img}").returncode != 0:
            print("  PULL FAILED"); continue
        cid = sh(f'docker run -d -v "{d}":/testbed/_gen_tests {img} sleep infinity').stdout.strip()
        sh(f'docker exec {cid} bash -lc "{ACT} && pip install -q pytest"')

        for tf in sorted(d.glob("test_*.py")):
            ok, err = run_in(cid, tf.name)
            if ok:
                print(f"  ok          {tf.name}", flush=True); continue
            try:
                new = fix(tf.read_text(), err, a.model)
            except Exception as e:
                print(f"  repair_err  {tf.name} ({e})", flush=True); continue
            tf.write_text(new)                         # mounted -> container sees it
            ok2, _ = run_in(cid, tf.name)
            print(f"  {'fixed      ' if ok2 else 'still_fails '}{tf.name}", flush=True)

        sh(f"docker rm -f {cid}")


if __name__ == "__main__":
    main()
