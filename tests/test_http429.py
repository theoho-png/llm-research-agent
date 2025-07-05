import pytest
from src.agent.graph import run_pipeline

def test_http_429(monkeypatch):
    from src.agent import tools

    def raise429(*a, **k):
        raise Exception("HTTP 429: Too Many Requests")
    monkeypatch.setattr(tools.WebSearchTool, "search", raise429)
    monkeypatch.setattr(tools, "call_llm", lambda prompt, **kwargs: '["retry query"]' if "break it down" in prompt else '{"need_more": false, "new_queries": []}' if "reflection" in prompt else '{"answer": "Insufficient data to answer the question.", "citations": []}')
    result = run_pipeline("Trigger HTTP 429 error for search")
    assert "Insufficient data" in result["answer"]