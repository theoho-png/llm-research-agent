import json
from src.agent.prompts import SYNTHESIZE_PROMPT
from src.agent.tools import call_llm
from src.agent.state import AgentState


def synthesize_node(state: AgentState) -> dict:
    # Format docs as numbered list for prompt
    docs_str = ""
    for i, doc in enumerate(state.docs, 1):
        docs_str += f"{i}. {doc.get('title', '')}: {doc.get('snippet', '')} ({doc.get('url', '')})\n"
    prompt = SYNTHESIZE_PROMPT.format(question=state.question, docs=docs_str)
    output = call_llm(prompt, max_tokens=256)
    try:
        answer = json.loads(output)
        # Validate structure
        assert "answer" in answer and "citations" in answer
        # Ensure ≤80 words
        words = answer["answer"].split()
        if len(words) > 80:
            answer["answer"] = ' '.join(words[:80]) + " ..."
    except Exception:
        # fallback dummy answer
        answer = {
            "answer": "Insufficient data to answer the question.",
            "citations": []
        }
    return answer
