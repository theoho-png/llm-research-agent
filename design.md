# LLM Research Agent — Design Document

## Overview

The LLM Research Agent is a Dockerized, CLI-only tool that orchestrates LLM-driven prompt engineering, concurrent web search, reflection, and answer synthesis. It is designed to automate the workflow of breaking down a user’s research query, performing web searches, reflecting on sufficiency of evidence, and synthesizing a concise, cited answer in JSON format.

---

## Architecture

### 1. Pipeline (LangGraph-inspired)

```
User Input
   │
   ▼
┌─────────────────┐
│ GenerateQueries │ ←──────────────┐
└─────────────────┘               │ (<= 2 iterations)
   │                              │
   ▼                              │
┌─────────────────┐               │
│ WebSearchTool   │               │
└─────────────────┘               │
   │                              │
   ▼                              │
┌─────────────────┐               │
│ Reflect         │───────────────┘
└─────────────────┘               
   │
   ▼
┌─────────────────┐
│ Synthesize      │
└─────────────────┘
   │
   ▼
Final JSON Output
```

- **Nodes**: `GenerateQueries`, `WebSearchTool`, `Reflect`, `Synthesize`
- **State**: Passed through all nodes, accumulates queries, docs, reflections, slots, etc.
- **Cycles**: Up to 2 rounds (configurable via `max_iter`)

---

### 2. Node Details

#### a. GenerateQueries
- **Input**: Original user question.
- **Output**: 3–5 English web search queries (JSON array).
- **Method**: LLM prompt.
- **Purpose**: Ensures coverage and decomposes complex questions.

#### b. WebSearchTool
- **Input**: List of queries.
- **Output**: Merged, deduplicated search result docs.
- **Method**: Concurrent Bing API (real or mock). 
- **Fallback**: Mock tool if no API key.
- **Purpose**: Gathers evidence for synthesis.

#### c. Reflect (Simple & Slot-Aware)
- **Input**: User question, docs so far.
- **Output**: 
    - If enough, passes to Synthesize.
    - If not, returns `need_more: true` and refined queries.
- **Slot-Aware Bonus**: Lists required slots, which are filled, and targets missing slots with new queries.
- **Purpose**: Ensures completeness, increases verifiability.

#### d. Synthesize
- **Input**: User question, docs.
- **Output**: ≤80 word English answer with markdown citations, in JSON object.
- **Method**: LLM prompt, citations formatted as `[1][2]`.

---

## Data Flow & State

- **AgentState** object holds:
    - `question`: user question
    - `queries`: list of queries to run
    - `docs`: accumulated and deduplicated search results
    - `reflections`: outputs from reflect node(s)
    - `max_iter`, `iter_count`: controls for cycle loop
    - `slots`, `filled`: for slot-aware mode

---

## Error & Edge Case Handling

- **No Results**: Falls back to a default answer and empty citations.
- **Timeouts/HTTP Errors**: Handled gracefully, agent continues or returns incomplete status.
- **API Absence**: Always works in mock/offline mode.
- **Tests**: ≥5 cases — happy path, no result, HTTP 429, timeout, two-round supplement.

---

## Directory Layout

```
llm-research-agent/
├── src/agent/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── prompts.py
│   ├── state.py
│   ├── tools.py
│   ├── nodes/
│   │   ├── generate_queries.py
│   │   ├── reflect.py
│   │   ├── synthesize.py
│   │   └── web_search.py
├── tests/
├── Dockerfile
├── compose.yaml
└── README.md
```

---

## Extensibility & Bonus Features

- **Slot-aware Reflect**: Tracks evidence for required slots/fields.
- **Redis LRU Cache**: For query/result caching.
- **OpenTelemetry/Prometheus**: For metrics/tracing.
- **Web streaming**: SSE/WebSocket for interactive UX.
- **Minimal Web UI**: Optional React/Vite frontend.

---

## Example Run

```bash
docker compose run --rm agent "Who won the 2022 FIFA World Cup?"
```
Output:
```json
{
  "answer": "Argentina won the 2022 FIFA World Cup, beating France on penalties after a 3-3 draw in extra time.[1]",
  "citations": [
    {
      "id": 1,
      "title": "Argentina win World Cup 2022",
      "url": "https://www.fifa.com/worldcup/news/argentin-win"
    }
  ]
}
```

---

## Implementation Notes

- **Python 3.9+** (for type annotations and modern syntax)
- **LLM**: OpenAI (default) via `OPENAI_API_KEY`. Can extend to Gemini etc.
- **Web Search**: Bing API (`BING_API_KEY`), fallback to mock.
- **Tests**: Pytest, all external calls monkeypatched.
- **Entrypoint**: `python -m agent.main "<question>"` (via Docker CMD).

---

## Limitations

- No GUI (CLI only).
- Synthesis limited to ~80 words and simple markdown numeric citations.
- Only basic concurrency and error handling (sufficient for MVP).
- Slot-aware reflect is an advanced/bonus extension.

---

## Extension Ideas

- Add memory/longer context for research trails.
- Progressive summarization for very large evidence sets.
- Multi-modal search (PDF, video, etc.).
- More advanced prompt engineering or chain-of-thought for tool/slot planning.