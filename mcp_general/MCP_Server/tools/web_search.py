import os

from tavily import TavilyClient


def web_search(query: str, max_results: int = 5) -> dict:
    """Search the web using Tavily; requires TAVILY_API_KEY."""
    if not query.strip():
        raise ValueError("query cannot be empty.")
    if not 1 <= max_results <= 20:
        raise ValueError("max_results must be between 1 and 20.")
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing. Set it in mcp_general/.env and restart the MCP server.")
    return TavilyClient(api_key=api_key).search(query=query, max_results=max_results)
