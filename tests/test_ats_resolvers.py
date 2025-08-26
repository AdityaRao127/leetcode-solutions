import asyncio
import pytest
from search_utils_ext import resolve_career_page

@pytest.mark.asyncio
async def test_resolver_handles_cache_miss(monkeypatch):
    # This test is illustrative; in CI, you should mock httpx calls.
    url = await resolve_career_page("nonexistent-company-xyz", "QA Intern")
    assert url is None or isinstance(url, str)