"""Official goodrecmovies API client — zero dependencies, Python ≥3.10.

Docs: https://goodrecmovies.com/docs · OpenAPI: /openapi.json
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Literal, Optional, TypedDict

__all__ = [
    "Title",
    "ApiError",
    "top_titles",
    "search_titles",
    "get_title",
    "ask",
    "BASE",
    "__version__",
]

__version__ = "0.1.0"

BASE = "https://goodrecmovies.com"

Kind = Literal["movie", "series"]
Tier = Literal["solid", "great", "excellent", "essential"]


class Title(TypedDict, total=False):
    title: str
    year: Optional[int]
    url: str
    kind: Kind
    rank: int
    tier: Tier
    grm: float
    rating: float


class ApiError(Exception):
    """HTTP or API error from goodrecmovies."""

    def __init__(self, message: str, *, code: str, status: int) -> None:
        super().__init__(message)
        self.code = code
        self.status = status


def _grm(raw: float) -> float:
    """Display helper: goodrecIndex → 0–100 GRM score."""
    return round((raw / 2 + 50) * 10) / 10


def _url(row: dict[str, Any]) -> str:
    kind = "series" if row.get("kind") == "series" else "movie"
    return f"{BASE}/{kind}/{row['tconst']}"


def _slim_list(row: dict[str, Any]) -> Title:
    title = row.get("primaryTitle")
    if title is None:
        title = row.get("title")
    year = row.get("startYear")
    if year is None:
        year = row.get("year")
    out: Title = {
        "title": title or "",
        "year": year,
        "url": _url(row),
        "kind": row.get("kind") or "movie",
    }
    if row.get("rank") is not None:
        out["rank"] = row["rank"]
    if row.get("tier") is not None:
        out["tier"] = row["tier"]
    if row.get("goodrecIndex") is not None:
        out["grm"] = _grm(float(row["goodrecIndex"]))
    return out


def _slim_search(row: dict[str, Any]) -> Title:
    out: Title = {
        "title": row.get("title") or "",
        "year": row.get("year"),
        "url": _url(row),
        "kind": row.get("kind") or "movie",
    }
    if row.get("poolRank") is not None:
        out["rank"] = row["poolRank"]
    if row.get("rating") is not None:
        out["rating"] = row["rating"]
    return out


def _request(
    method: str,
    path: str,
    *,
    body: Optional[dict[str, Any]] = None,
) -> Any:
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": f"goodrecmovies-python/{__version__}",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read()
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as e:
        err: dict[str, Any] = {
            "code": f"http_{e.code}",
            "message": e.reason or "request failed",
        }
        try:
            payload = json.loads(e.read().decode("utf-8"))
            if isinstance(payload.get("error"), dict):
                err = payload["error"]
        except Exception:
            pass
        raise ApiError(
            err.get("message") or "request failed",
            code=str(err.get("code") or f"http_{e.code}"),
            status=int(e.code),
        ) from None
    except urllib.error.URLError as e:
        raise ApiError(str(e.reason), code="network_error", status=0) from None


def top_titles(*, kind: Kind = "movie", count: int = 10) -> list[Title]:
    """The best titles in the pool, best first. kind: "movie" | "series"."""
    qs = urllib.parse.urlencode({"kind": kind, "pageSize": 20})
    data = _request("GET", f"/api/list?{qs}")
    rows = data.get("rows") or []
    return [_slim_list(r) for r in rows[:count]]


def search_titles(query: str) -> list[Title]:
    """Fuzzy title search (accent- and typo-tolerant)."""
    qs = urllib.parse.urlencode({"q": query})
    data = _request("GET", f"/api/search?{qs}")
    matches = data.get("matches") or []
    return [_slim_search(r) for r in matches]


def get_title(tconst: str) -> Optional[Title]:
    """One title by IMDb id, e.g. "tt0111161". Returns None if not in the corpus."""
    try:
        data = _request("POST", "/api/movies/batch", body={"ids": [tconst]})
    except ApiError:
        return None
    rows = data.get("rows") or []
    if not rows:
        return None
    return _slim_list(rows[0])


def ask(query: str) -> list[Any]:
    """Ask a natural-language question (NLWeb). Returns the ranked answer items."""
    data = _request("POST", "/ask", body={"query": query})
    return data.get("items") or []
