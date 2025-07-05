import pytest
from src.agent.graph import run_pipeline

def test_slot_aware(monkeypatch):
    from src.agent import tools

    monkeypatch.setattr(tools, "call_llm", lambda prompt, **kwargs: '{"slots": ["winner"], "filled": ["winner"], "need_more": false, "new_queries": []}' if "slot-aware" in prompt else '{"answer": "Argentina won the World Cup.[1]", "citations": [{"id": 1, "title": "Argentina win", "url": "https://fifa.com/win"}]}')
    monkeypatch.setattr(tools.WebSearchTool, "search", lambda self, q: [{"title": "Argentina win", "url": "https://fifa.com/win", "snippet": "Argentina won the 2022 FIFA World Cup."}])
    # slot-aware reflection, ensure all declared slots are filled before need_more = false
    result = run_pipeline("Who won the 2022 FIFA World Cup?", slot_aware=True)
    assert "Argentina" in result["answer"]
    assert isinstance(result["citations"], list) and result["citations"]