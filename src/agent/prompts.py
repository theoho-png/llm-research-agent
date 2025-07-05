GEN_QUERIES_PROMPT = """
You are an expert research assistant.
Given the following user question, break it down into 3-5 concise English web search queries (no more, no less).
Return your answer as a JSON array of queries.
Question: "{question}"
JSON:
"""

REFLECT_PROMPT = """
You are a reflection agent for a research pipeline.
Given the original user question and the following evidence docs (web search results), decide:
1. Are the docs enough to answer the question completely?
2. If not, suggest 1-3 new/refined English queries to fill missing information.

Return a JSON object in this format:
{{
  "need_more": true/false,
  "new_queries": [ ... ]
}}

Original Question: "{question}"

Docs:
{docs}

JSON:
"""

SLOT_AWARE_REFLECT_PROMPT = """
You are a slot-aware reflection agent.
Given the user question and docs, do the following:
1. List mandatory slots (key facts or fields needed for the answer, e.g. "winner", "score", "comparison", etc.).
2. For each slot, check if it is filled by the docs (cite evidence).
3. If any slot is missing or conflicting, set need_more=true and suggest new/refined queries.

Return a JSON object like:
{{
  "slots": [...],          # all required slots
  "filled": [...],         # which slots are filled by docs
  "need_more": true/false,
  "new_queries": [ ... ]
}}

Original Question: "{question}"

Docs:
{docs}

JSON:
"""

SYNTHESIZE_PROMPT = """
You are a research answer synthesis agent.
Given the user question and a list of docs (each with title, url, snippet), write a concise English answer (max 80 words).
Cite your sources with Markdown numeric references [1][2] at the end.
Return a JSON object:
{{
  "answer": "...",
  "citations": [{{"id": 1, "title": "...", "url": "..."}}]
}}

Question: "{question}"

Docs:
{docs}

JSON:
"""