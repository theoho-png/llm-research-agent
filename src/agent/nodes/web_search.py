from concurrent.futures import ThreadPoolExecutor, as_completed
from src.agent.tools import WebSearchTool
from src.agent.state import AgentState


def web_search_node(state: AgentState) -> AgentState:
    tool = WebSearchTool()
    docs = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(tool.search, q): q for q in state.queries}
        for future in as_completed(futures):
            try:
                docs.extend(future.result())
            except Exception:
                continue
    # Deduplicate by URL
    seen = set()
    merged = []
    for doc in docs:
        url = doc.get("url")
        if url and url not in seen:
            merged.append(doc)
            seen.add(url)
    state.docs = merged
    return state
