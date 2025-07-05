import pytest
from src.agent.graph import run_pipeline

def test_timeout(monkeypatch):
    import time
    from src.agent import tools

    def slow_search(*a, **k):
        time.sleep(2)
        return []
    monkeypatch.setattr(tools.WebSearchTool, "search", slow_search)
    monkeypatch.setattr(tools, "call_llm", lambda prompt, **kwargs: '["timeout search"]' if "break it down" in prompt else '{"need_more": false, "new_queries": []}' if "reflection" in prompt else '{"answer": "Insufficient data to answer the question.", "citations": []}')
    result = run_pipeline("This should timeout and return fallback")
    assert "Insufficient data" in result["answer"]