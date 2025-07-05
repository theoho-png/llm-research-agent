import pytest
from src.agent.graph import run_pipeline

def test_two_round(monkeypatch):
    from src.agent import tools

    call_count = {"reflect": 0}
    def fake_llm(prompt, **kwargs):
        if "break it down" in prompt:
            return '["Kubernetes HPA vs KEDA", "HPA features", "KEDA features"]'
        if "reflection" in prompt:
            call_count["reflect"] += 1
            if call_count["reflect"] == 1:
                return '{"need_more": true, "new_queries": ["KEDA use cases"]}'
            else:
                return '{"need_more": false, "new_queries": []}'
        return '{"answer": "HPA is for event-driven workloads; KEDA for batch jobs.[1][2]", "citations": [{"id": 1, "title": "Kubernetes HPA", "url": "https://k8s.io/hpa"}, {"id": 2, "title": "KEDA", "url": "https://keda.sh"}]}'
    monkeypatch.setattr(tools, "call_llm", fake_llm)
    monkeypatch.setattr(tools.WebSearchTool, "search", lambda self, q: [{"title": q, "url": f"https://example.com/{q}", "snippet": f"Info about {q}."}])
    result = run_pipeline("Compare Kubernetes HPA and KEDA: key features and use cases.")
    assert "KEDA" in result["answer"]
    assert "HPA" in result["answer"]
    assert len(result["citations"]) >= 2