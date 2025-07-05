import json
from src.agent.prompts import GEN_QUERIES_PROMPT
from src.agent.tools import call_llm
from src.agent.state import AgentState


def generate_queries_node(state: AgentState) -> AgentState:
    prompt = GEN_QUERIES_PROMPT.format(question=state.question)
    output = call_llm(prompt, max_tokens=256)
    try:
        queries = json.loads(output)
        if not isinstance(queries, list) or not 3 <= len(queries) <= 5:
            raise ValueError
    except Exception:
        # fallback: split lines or return original question
        queries = [q.strip() for q in output.splitlines() if q.strip()]
        if not 3 <= len(queries) <= 5:
            queries = [state.question]
    state.queries = queries
    return state
