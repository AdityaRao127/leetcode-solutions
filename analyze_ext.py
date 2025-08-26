"""
Analyzer extension:
- Build unified dataframe from source CSVs
- Resolve careers pages (if missing) and fetch descriptions for triaged pool
- Two-stage matching with caching
"""

import os
import json
import asyncio
import hashlib
import pandas as pd
from pathlib import Path
from typing import List, Dict

from job_utils_ext import normalize_record, stage1_score, is_senior_or_excluded
from search_utils_ext import resolve_career_page, fetch_descriptions

OUT_DIR = Path("other_results")
CACHE_SCORES = Path(os.getenv("JOB_SCORES_CACHE", "job_scores_cache.json"))

def _load_role_prefs() -> dict:
    raw = os.getenv("ROLE_PREFERENCES", "{}")
    try:
        return json.loads(raw)
    except Exception:
        return {}

def _resume_text() -> str:
    return os.getenv("RESUME_TEXT", "")

def _hash_resume(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:12]

def load_all_sources() -> pd.DataFrame:
    frames = []
    for p in OUT_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(p)
            frames.append(df)
        except Exception:
            continue
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    # Normalize columns
    rows = [normalize_record(r._asdict() if hasattr(r, "_asdict") else dict(r)) for r in df.to_dict(orient="records")]
    return pd.DataFrame(rows)

async def resolve_missing_careers(df: pd.DataFrame) -> pd.DataFrame:
    need = df["Careers Page URL"].fillna("").eq("")
    todo = df[need]
    tasks = [resolve_career_page(r["Company"], r["Position Title"]) for _, r in todo.iterrows()]
    urls = await asyncio.gather(*tasks)
    # Convert None to empty string to avoid dtype issues
    urls = [url or "" for url in urls]
    df.loc[need, "Careers Page URL"] = urls
    df["URL"] = df["Careers Page URL"].fillna("")  # may be empty; downstream will fallback
    df.loc[df["URL"].eq(""), "URL"] = df["Third Party URL"].fillna("")
    return df

async def fetch_triaged_descriptions(df: pd.DataFrame, k_total: int) -> pd.DataFrame:
    rp = _load_role_prefs()
    resume = _resume_text()
    # Stage 1 triage
    df["Stage1"] = df.apply(lambda r: 0.0 if is_senior_or_excluded(str(r["Position Title"]), rp)
                            else stage1_score(str(r["Position Title"]), str(r["Company"]), str(r["Description"]), resume, rp), axis=1)
    top = df.sort_values("Stage1", ascending=False).head(k_total)
    urls = [u for u in top["URL"].fillna("") if u]
    descs = await fetch_descriptions(urls)
    # Update descriptions when empty
    def pick_desc(r):
        if r["Description"]:
            return r["Description"]
        return descs.get(r["URL"], "")
    df["Description"] = df.apply(pick_desc, axis=1)
    return df

def stage2_score(desc: str, resume: str) -> float:
    # Placeholder: embedding/LLM similarity; keep normalized [0..1]
    if not desc or not resume:
        return 0.0
    from rapidfuzz import fuzz
    return fuzz.token_set_ratio(resume.lower(), desc.lower()) / 100.0

def load_score_cache() -> Dict[str, float]:
    if CACHE_SCORES.exists():
        try:
            return json.load(open(CACHE_SCORES, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_score_cache(cache: Dict[str, float]):
    json.dump(cache, open(CACHE_SCORES, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def apply_stage2(df: pd.DataFrame, k_eval: int) -> pd.DataFrame:
    resume = _resume_text()
    rh = _hash_resume(resume)
    cache = load_score_cache()

    # Evaluate only top-k by Stage1
    cand = df.sort_values("Stage1", ascending=False).head(k_eval).copy()
    scores = []
    for _, r in cand.iterrows():
        key = f"{rh}|{r['URL']}"
        if key in cache:
            s = cache[key]
        else:
            s = stage2_score(str(r["Description"]), resume)
            cache[key] = s
        scores.append(s)
    save_score_cache(cache)
    cand["Stage2"] = scores

    # Merge back
    df = df.merge(cand[["URL", "Stage2"]], on="URL", how="left")
    df["Stage2"] = df["Stage2"].fillna(0.0)

    # Final score = blend
    df["Match Score"] = (df["Stage1"] * 0.4 + df["Stage2"] * 0.6).clip(0, 1)
    return df

def write_outputs(df: pd.DataFrame):
    out_all = Path("other_results") / f"all_listings_{pd.Timestamp.utcnow().date()}.parquet"
    df.to_parquet(out_all, index=False)

    # Keep your existing daily CSVs too if you have specific splits:
    # Example split by keywords:
    intern = df[df["Position Title"].str.contains("intern", case=False, na=False)]
    newgrad = df[df["Position Title"].str.contains("new grad|newgrad|graduate", case=False, na=False)]
    intern.to_csv(Path("other_results") / f"{pd.Timestamp.utcnow().date()}_listings_intern.csv", index=False)
    newgrad.to_csv(Path("other_results") / f"{pd.Timestamp.utcnow().date()}_listings_newgrad.csv", index=False)

def run():
    df = load_all_sources()
    if df.empty:
        print("[analyze_ext] No inputs found.")
        return
    # Resolve careers pages and descriptions
    df = asyncio.run(resolve_missing_careers(df))
    df = asyncio.run(fetch_triaged_descriptions(df, k_total=int(os.getenv("TOP_K_FOR_LLM", "400"))))
    df = apply_stage2(df, k_eval=int(os.getenv("TOP_K_FOR_LLM", "400")))
    # Ensure URL fallback
    df["URL"] = df["URL"].where(df["URL"].astype(str).str.len() > 0, df["Third Party URL"])
    write_outputs(df)
    print("[analyze_ext] Done.")

if __name__ == "__main__":
    run()