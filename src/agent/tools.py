import os
import requests
from typing import List, Dict, Any


class WebSearchTool:
    """
    Calls Bing Search API or falls back to mock.
    """

    def __init__(self):
        self.api_key = os.environ.get("BING_API_KEY")

    def search(self, query: str) -> List[Dict[str, Any]]:
        if self.api_key:
            return self._search_bing(query)
        else:
            return self._mock_search(query)

    def _search_bing(self, query: str) -> List[Dict[str, Any]]:
        # Minimal Bing Search implementation (pseudo, not production)
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "count": 5, "responseFilter": "Webpages"}
        resp = requests.get(endpoint, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        webPages = resp.json().get("webPages", {}).get("value", [])
        return [{
            "title": item["name"],
            "url": item["url"],
            "snippet": item["snippet"]
        } for item in webPages]

    def _mock_search(self, query: str) -> List[Dict[str, Any]]:
        # Always returns a canned result for demonstration and offline test
        return [{
            "title": f"Mock result for {query}",
            "url": f"https://example.com/{query.replace(' ', '_')}",
            "snippet": f"This is a mock search result for '{query}'."
        }]


def call_llm(prompt: str, max_tokens: int = 512, model: str = "gpt-3.5-turbo") -> str:
    """
    Calls OpenAI or Gemini LLM (OpenAI default).
    """
    import openai
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    return response['choices'][0]['message']['content'].strip()
