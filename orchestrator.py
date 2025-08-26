import os
import sys
import time
import json
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Config with environment fallbacks
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "24"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_LINKEDIN_JOBS = int(os.getenv("MAX_LINKEDIN_JOBS", "600"))
MAX_DESC_PAGES = int(os.getenv("MAX_DESC_PAGES", "800"))
TOP_K_FOR_LLM = int(os.getenv("TOP_K_FOR_LLM", "400"))
DAYS_OLD = int(os.getenv("DAYS_OLD", "3"))

# Sources to run in parallel. Adjust names to match your repo.
CANDIDATE_SCRIPTS = [
    "linkedin_updated.py",
    "boolean.py",
    "github_intern.py",
    "github_newgrad.py",
    "intern_swe.py",
    "intern_da.py",
    "intern_ml_ai.py",
    "newgrad_swe.py",
    "newgrad_da.py",
    "newgrad_ml_ai.py",
]

def find_existing_scripts():
    root = Path(".")
    out = []
    for name in CANDIDATE_SCRIPTS:
        p = root / name
        if p.exists():
            out.append(str(p))
    return out

def run_script(path: str) -> tuple[str, int, str]:
    env = os.environ.copy()
    env["REQUEST_TIMEOUT"] = str(REQUEST_TIMEOUT)
    env["DAYS_OLD"] = str(DAYS_OLD)
    env["MAX_LINKEDIN_JOBS"] = str(MAX_LINKEDIN_JOBS)
    # Child scripts can read these caps; they should honor them if applicable
    start = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, path],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60 * 50  # 50 min per script hard cap
        )
        dur = int(time.time() - start)
        return (path, proc.returncode, proc.stdout[-8000:])  # tail logs
    except subprocess.TimeoutExpired as e:
        return (path, 124, f"TimeoutExpired after {int(time.time()-start)}s\n{e}")
    except Exception as e:
        return (path, 1, f"Exception: {e}")

def main():
    scripts = find_existing_scripts()
    print(f"[orchestrator] Running {len(scripts)} scripts in parallel: {scripts}", flush=True)

    results = []
    if scripts:
        with ThreadPoolExecutor(max_workers=min(len(scripts), 8)) as ex:
            futs = [ex.submit(run_script, s) for s in scripts]
            for f in as_completed(futs):
                results.append(f.result())

        ok = True
        for path, code, tail in results:
            print(f"\n=== {path} -> exit {code} ===\n{tail}\n", flush=True)
            if code != 0:
                ok = False

        if not ok:
            print("[orchestrator] One or more scripts failed", flush=True)
            sys.exit(1)
    else:
        print("[orchestrator] No source scripts found to run", flush=True)

    # After sources complete, run the analyzer exactly once
    print("[orchestrator] Running analyzer...", flush=True)
    proc = subprocess.run([sys.executable, "analyze.py"], text=True)
    sys.exit(proc.returncode)

if __name__ == "__main__":
    main()