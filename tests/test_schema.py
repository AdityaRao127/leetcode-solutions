import pandas as pd
from job_utils_ext import normalize_record, REQUIRED_COLUMNS

def test_normalize_record_minimums():
    raw = {"company":"Acme", "title":"ML Engineer Intern", "link":"https://linkedin.com/xyz"}
    rec = normalize_record(raw)
    for col in REQUIRED_COLUMNS:
        assert col in rec
    assert rec["Company"] == "Acme"
    assert rec["Position Title"] == "ML Engineer Intern"
    assert rec["Third Party URL"] == "https://linkedin.com/xyz"
    assert rec["URL"] == "https://linkedin.com/xyz"