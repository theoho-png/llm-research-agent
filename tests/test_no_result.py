import pytest
from src.agent.graph import run_pipeline

def test_no_result(monkeypatch):
    # LLM output always empty, web search returns nothing
    from src.agent import tools

    monkeypatch.setattr(tools, "call_llm", lambda prompt, **kwargs: '["unknown term"]' if "break it down" in prompt else '{"need_more": false, "new_queries": []}' if "reflection" in prompt else '{"answer": "Insufficient data to answer the question.", "citations": []}')
    monkeypatch.setattr(tools.WebSearchTool, "search", lambda self, q: [])
    result = run_pipeline("What is the meaning of flibbertigibbet?")
    assert "Insufficient data" in result["answer"]
    assert result["citations"] == []