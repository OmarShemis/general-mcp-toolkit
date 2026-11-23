import httpx
from bs4 import BeautifulSoup


def read_webpage(url: str, max_chars: int = 50_000) -> dict:
    """Read visible HTML text from an HTTP(S) URL. Does not execute JavaScript."""
    if max_chars < 1:
        raise ValueError("max_chars must be positive.")
    if httpx.URL(url).scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https.")
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()
            if not any(kind in content_type for kind in ("text/html", "application/xhtml+xml", "text/plain")):
                raise ValueError("URL must return HTML or plain text.")
            content = bytearray()
            for chunk in response.iter_bytes():
                content.extend(chunk)
                if len(content) > 5_000_000:
                    raise ValueError("Page exceeds the 5 MB download limit.")
            text = content.decode(response.encoding or "utf-8", errors="replace")
            title = ""
            if "text/plain" not in content_type:
                soup = BeautifulSoup(text, "html.parser")
                title = soup.title.get_text(" ", strip=True) if soup.title else ""
                for tag in soup(["script", "style", "noscript", "template"]):
                    tag.decompose()
                text = soup.get_text("\n", strip=True)
            return {"url": str(response.url), "title": title, "text": text[:max_chars],
                    "truncated": len(text) > max_chars}
