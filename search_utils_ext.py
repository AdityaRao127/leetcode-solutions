"""
Extensions to career-page resolution and description fetching.

Usage:
- Prefer ATS resolvers (Lever/Greenhouse/Workday) before generic search.
- Cache positive matches by (company_norm, title_norm).
"""

import os
import re
import json
import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any

import httpx
from rapidfuzz import fuzz

CACHE_PATH = os.getenv("CAREER_PAGE_CACHE", "career_page_cache.json")
DESC_CACHE_PATH = os.getenv("JOB_DESC_CACHE", "job_descriptions_cache.json")
CACHE_TTL_DAYS = int(os.getenv("CAREER_PAGE_CACHE_TTL_DAYS", "7"))
CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "24"))
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

SEMAPHORE = asyncio.Semaphore(CONCURRENCY)

def _now():
    return datetime.utcnow()

def _load_cache(path: str) -> Dict[str, Any]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(path: str, data: Dict[str, Any]):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

def _cache_key(company: str, title: str) -> str:
    return hashlib.sha1(f"{_norm(company)}|{_norm(title)}".encode()).hexdigest()

async def _get_json(client: httpx.AsyncClient, url: str) -> Optional[dict]:
    try:
        async with SEMAPHORE:
            r = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code == 200 and "application/json" in r.headers.get("content-type", ""):
            return r.json()
    except Exception:
        return None
    return None

async def resolve_career_page(company: str, title: str) -> Optional[str]:
    """
    Try ATS resolvers first; then fallback to None (caller may use original link).
    """
    cache = _load_cache(CACHE_PATH)
    key = _cache_key(company, title)
    hit = cache.get(key)
    if hit:
        ts = datetime.fromisoformat(hit.get("ts"))
        if _now() - ts < timedelta(days=CACHE_TTL_DAYS):
            return hit.get("url")

    async with httpx.AsyncClient(headers={"user-agent": "job-scraper/1.0"}) as client:
        # Lever: https://jobs.lever.co/{company}.json
        for cname in [_norm(company).replace(" ", ""), _norm(company).replace(" ", "-")]:
            url = f"https://jobs.lever.co/{cname}.json"
            data = await _get_json(client, url)
            if data and isinstance(data, list):
                best = _best_match_lever(data, title)
                if best:
                    cache[key] = {"url": best, "ts": _now().isoformat()}
                    _save_cache(CACHE_PATH, cache)
                    return best

        # Greenhouse: https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true
        for cname in [_norm(company).replace(" ", ""), _norm(company).replace(" ", "-")]:
            url = f"https://boards-api.greenhouse.io/v1/boards/{cname}/jobs?content=true"
            data = await _get_json(client, url)
            if data and isinstance(data, dict) and "jobs" in data:
                best = _best_match_greenhouse(data["jobs"], title)
                if best:
                    cache[key] = {"url": best, "ts": _now().isoformat()}
                    _save_cache(CACHE_PATH, cache)
                    return best

        # Workday: heuristic tenants; leaving as stub fallback (some tenants are private)
        # Caller should attempt site-limited search if this returns None.

    return None

def _best_match_lever(rows, title: str) -> Optional[str]:
    best = (0, None)
    t = _norm(title)
    for r in rows:
        job_title = _norm(r.get("text", ""))
        score = fuzz.token_set_ratio(t, job_title)
        if score > best[0]:
            best = (score, r.get("hostedUrl"))
    return best[1] if best[0] >= 85 else None

def _best_match_greenhouse(rows, title: str) -> Optional[str]:
    best = (0, None)
    t = _norm(title)
    for r in rows:
        job_title = _norm(r.get("title", ""))
        absolute_url = r.get("absolute_url")
        score = fuzz.token_set_ratio(t, job_title)
        if score > best[0]:
            best = (score, absolute_url)
    return best[1] if best[0] >= 85 else None

async def fetch_descriptions(urls: list[str]) -> Dict[str, str]:
    """
    Fetch descriptions concurrently; reuse cache.
    """
    cache = _load_cache(DESC_CACHE_PATH)
    out: Dict[str, str] = {}

    async def fetch_one(client: httpx.AsyncClient, u: str):
        if u in cache:
            out[u] = cache[u]
            return
        try:
            async with SEMAPHORE:
                r = await client.get(u, timeout=TIMEOUT, follow_redirects=True)
            text = r.text or ""
            # Naive strip; you can improve per-ATS selectors elsewhere
            text = re.sub(r"<script.*?>.*?</script>", " ", text, flags=re.S|re.I)
            text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.S|re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            cache[u] = text[:200000]  # cap
            out[u] = cache[u]
        except Exception:
            out[u] = ""
        finally:
            _save_cache(DESC_CACHE_PATH, cache)

    async with httpx.AsyncClient(headers={"user-agent": "job-scraper/1.0"}) as client:
        await asyncio.gather(*(fetch_one(client, u) for u in urls))

    return out