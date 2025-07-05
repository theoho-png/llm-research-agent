import pytest
from src.agent.graph import run_pipeline

def test_fact_happy(monkeypatch):
    # Monkeypatch LLM and WebSearchTool to deterministic
    from src.agent import tools, nodes

    monkeypatch.setattr(tools, "call_llm", lambda prompt, **kwargs: '["Who won the 2022 FIFA World Cup?", "2022 World Cup winner", "FIFA 2022 final result"]' if "break it down" in prompt else '{"need_more": false, "new_queries": []}' if "reflection" in prompt else '{"answer": "Argentina won the 2022 FIFA World Cup, beating France on penalties after a 3-3 draw.[1]", "citations": [{"id": 1, "title": "Argentina win", "url": "https://fifa.com/win"}]}')
    monkeypatch.setattr(tools.WebSearchTool, "search", lambda self, q: [{
        "title": "Argentina win", "url": "https://fifa.com/win", "snippet": "Argentina beat France in 2022 World Cup final."
    }])

    result = run_pipeline("Who won the 2022 FIFA World Cup?")
    assert "Argentina" in result["answer"]
    assert isinstance(result["citations"], list) and result["citations"]