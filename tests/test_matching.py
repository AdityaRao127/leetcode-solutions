from job_utils_ext import stage1_score, is_senior_or_excluded

def test_stage1_score_prefers_role():
    rp = {"mlai": 1.2, "swe": 1.0, "da": 0.8, "exclude_levels":[]}
    s1 = stage1_score("Machine Learning Intern", "Acme", "NLP, PyTorch", "PyTorch, NLP, ML", rp)
    s2 = stage1_score("Data Analyst Intern", "Acme", "SQL, Tableau", "PyTorch, NLP, ML", rp)
    assert s1 >= s2

def test_exclude_senior_levels():
    rp = {"exclude_levels": ["senior","staff","principal","phd"]}
    assert is_senior_or_excluded("Senior Software Engineer", rp) is True
    assert is_senior_or_excluded("Software Engineer Intern", rp) is False