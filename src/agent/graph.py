from src.agent.state import AgentState
from src.agent.nodes.generate_queries import generate_queries_node
from src.agent.nodes.web_search import web_search_node
from src.agent.nodes.reflect import reflect_node
from src.agent.nodes.synthesize import synthesize_node


def run_pipeline(question: str, slot_aware: bool = False, max_iter: int = 2) -> dict:
    state = AgentState(question=question, max_iter=max_iter)
    # Cycle 1
    state = generate_queries_node(state)
    state = web_search_node(state)
    state = reflect_node(state, slot_aware=slot_aware)
    # If reflection says need more and max_iter not reached, repeat
    if state.iter_count < state.max_iter and state.queries:
        state = web_search_node(state)
        state = reflect_node(state, slot_aware=slot_aware)
    result = synthesize_node(state)
    return result
