# LLM Research Agent

A fully Dockerized, CLI-based research agent that orchestrates LLM-driven prompt engineering, concurrent web search, reflection, and answer synthesis. 

## Features

- **LangGraph Pipeline**: 4-node pipeline: GenerateQueries → WebSearchTool → Reflect → Synthesize. Up to 2 cycles.
- **Prompt Engineering**: LLM breaks down questions into 3-5 web search queries.
- **Tool Orchestration**: Concurrent Bing (or Mock) web search, deduplication & merging of results.
- **Reflect Node**: Determines sufficiency of `docs`. Optionally slot-aware for bonus points.
- **Concise Answers**: Synthesizes JSON answer with ≤80 English words and Markdown citations.
- **One-Command Run**: `docker compose run --rm agent "<question>"` prints final JSON.
- **Unit Tests**: ≥ 5 Pytest cases (happy, empty, HTTP error, timeout, supplement).
- **Extensible**: Bonus features: slot-aware reflect, Redis caching, tracing, etc.

---

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                               CLI Entrypoint                              │
└───────────────┬───────────────┬──────────────────┬─────────────┬──────────┘
                ↓               ↓                  ↓             ↓
         GenerateQueries → WebSearchTool → Reflect → Synthesize
                ↑                                   ↓
                └─────────────(≤1 extra cycle)──────┘

(State passed between nodes. Docs & queries merged/deduped. Final output is JSON.)
```

---

## Directory Layout

```
llm-research-agent/
├── src/agent/
│   ├── __init__.py
│   ├── state.py               # Pipeline state object
│   ├── prompts.py             # Node prompts
│   ├── tools.py               # Web search, mock search, LLM wrappers
│   ├── nodes/                 # Node logic for pipeline (queries, search, reflect, synthesize)
│   └── graph.py               # LangGraph pipeline definition
├── tests/                     # Pytest cases + mock data
├── Dockerfile
├── compose.yaml
└── README.md
```

---

## Usage

```bash
docker compose run --rm agent "<your research question>"
```

Example:
```bash
docker compose run --rm agent "Who won the 2022 FIFA World Cup?"
```

Returns:
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

## Configuration

- **Python**: ≥3.9
- **LLM Provider**: Set `OPENAI_API_KEY` or `GEMINI_API_KEY` in environment (default: OpenAI).
- **Search API**: Set `BING_API_KEY` (optional). Falls back to mock search if absent.

---

## Testing

Run all Pytest cases:

```bash
docker compose run --rm agent pytest -q
```

Covers:
- Happy path
- No result
- HTTP error (429)
- Timeout
- Two-round supplement
- Slot-aware completeness (bonus)

---

## Extending

### Bonus Features

- Slot-aware reflection (see `src/agent/nodes/reflect.py`)
- Redis LRU cache for search results
- Tracing/metrics via OpenTelemetry
- Minimal web frontend (optional)

---

## Design Doc

See [design.md](design.md) for architecture, pipeline details, and extension ideas.

---

## Submission Checklist

- [x] All tests pass: `pytest -q`
- [x] One-command run works locally and offline (mock)
- [x] Design doc + architecture diagram
- [ ] (Optional) Screencast demo

---

## License

MIT