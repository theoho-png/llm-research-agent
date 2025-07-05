import json
from src.agent.prompts import REFLECT_PROMPT, SLOT_AWARE_REFLECT_PROMPT
from src.agent.tools import call_llm
from src.agent.state import AgentState


def reflect_node(state: AgentState, slot_aware: bool = False) -> AgentState:
    docs_str = ""
    for i, doc in enumerate(state.docs, 1):
        docs_str += f"{i}. {doc.get('title', '')}: {doc.get('snippet', '')}\n"
    if slot_aware:
        prompt = SLOT_AWARE_REFLECT_PROMPT.format(question=state.question, docs=docs_str)
    else:
        prompt = REFLECT_PROMPT.format(question=state.question, docs=docs_str)
    output = call_llm(prompt, max_tokens=256)
    try:
        reflect_out = json.loads(output)
    except Exception:
        # fallback: need more, repeat queries
        reflect_out = {"need_more": False, "new_queries": []}
    state.reflections.append(reflect_out)
    if slot_aware:
        # Try to parse slots and filled for slot-aware
        state.slots = reflect_out.get("slots", [])
        state.filled = reflect_out.get("filled", [])
        if reflect_out.get("need_more", False) and reflect_out.get("new_queries"):
            state.queries = reflect_out.get("new_queries", [])
            state.iter_count += 1
    else:
        if reflect_out.get("need_more", False) and reflect_out.get("new_queries"):
            state.queries = reflect_out.get("new_queries", [])
            state.iter_count += 1
    return state
