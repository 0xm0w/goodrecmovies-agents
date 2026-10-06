# goodrecmovies

Official Python client for the [goodrecmovies](https://goodrecmovies.com) API —
every movie above 7.0, ranked by math, not vibes. Free, no API key. Zero
dependencies (stdlib `urllib`), Python ≥3.10.

## Install

```bash
pip install goodrecmovies
```

Until the first PyPI release, install from this repo:

```bash
pip install -e packages/python
# or from a clone:
pip install ./packages/python
```

## Usage

```python
from goodrecmovies import top_titles, search_titles, get_title, ask

top_titles(kind="movie", count=5)   # the shortlist, best first
search_titles("godfather")          # typo-tolerant search
get_title("tt0111161")              # one title by IMDb id
ask("ten great crime movies")       # natural language (NLWeb)
```

Each list/lookup result is a slim dict:

`{title, year, url, kind, rank, tier, grm}` — rank is within its kind pool,
tier is the site's band (solid / great / excellent / essential), grm is the
0–100 display score. Search results may include `rating` instead of
`tier`/`grm` when those fields are not on the search payload. `ask` returns
the NLWeb `items` list as-is.

## Links

- API docs: https://goodrecmovies.com/docs · OpenAPI: /openapi.json
- MCP server: https://goodrecmovies.com/mcp
- Machine guide: https://goodrecmovies.com/llms.txt
- npm client: `npm i goodrecmovies`
- Rate limits: per IP, `RateLimit-Policy` header; 429 carries `Retry-After`.
