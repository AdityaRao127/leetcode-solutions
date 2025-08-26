"""
Schema normalization helpers and Stage 1 triage scoring.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import re
from rapidfuzz import fuzz

RE_SENIOR = re.compile(r"\b(senior|staff|principal|lead|phd)\b", re.I)

REQUIRED_COLUMNS = [
    "Company",
    "Position Title",
    "Posted",
    "Description",
    "Careers Page URL",
    "Third Party URL",
    "URL",
    "Source",
    "Match Score",
    "Location",
    "Salary",
]

def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    company = raw.get("Company") or raw.get("company") or ""
    title = raw.get("Position Title") or raw.get("title") or raw.get("job_title") or ""
    posted = raw.get("Posted") or raw.get("date") or ""
    desc = raw.get("Description") or raw.get("description") or ""
    source = raw.get("Source") or raw.get("source") or "unknown"
    loc = raw.get("Location") or raw.get("location") or ""
    salary = raw.get("Salary") or raw.get("salary") or ""

    careers_url = raw.get("Careers Page URL") or raw.get("careers_url") or ""
    third_party = raw.get("Third Party URL") or raw.get("link") or raw.get("url") or ""

    url = careers_url or third_party

    out = {
        "Company": company,
        "Position Title": title,
        "Posted": posted,
        "Description": desc,
        "Careers Page URL": careers_url,
        "Third Party URL": third_party,
        "URL": url,
        "Source": source,
        "Match Score": float(raw.get("Match Score", 0.0)),
        "Location": loc,
        "Salary": salary,
    }
    return out

def is_senior_or_excluded(title: str, role_prefs: dict) -> bool:
    levels = [s.lower() for s in role_prefs.get("exclude_levels", [])]
    if levels:
        pattern = re.compile("|".join(map(re.escape, levels)), re.I)
        if pattern.search(title or ""):
            return True
    return bool(RE_SENIOR.search(title or ""))

def stage1_score(title: str, company: str, description: str, resume_text: str, role_prefs: dict) -> float:
    """
    Lightweight triage score combining title/company heuristics with lexical similarity.
    """
    if not title:
        return 0.0
    tscore = 0.0
    t = title.lower()
    # Role weights
    if "ml" in t or "machine learning" in t or "ai" in t:
        tscore += role_prefs.get("mlai", 1.0)
    if "software" in t or "swe" in t or "developer" in t or "engineer" in t:
        tscore += role_prefs.get("swe", 1.0)
    if "data" in t and ("analyst" in t or "analytics" in t or "science" in t):
        tscore += role_prefs.get("da", 1.0)

    sim = fuzz.token_set_ratio((resume_text or "").lower(), (description or title or "").lower()) / 100.0
    return tscore * 0.5 + sim * 0.5