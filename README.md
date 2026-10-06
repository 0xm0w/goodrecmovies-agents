# goodrecmovies — agents

Agent docs, skills, and the official Python SDK for
[goodrecmovies.com](https://goodrecmovies.com) — every movie above 7.0, ranked
by math, not vibes. A free public ranking of movies and TV series; no ads, no
tracking, no accounts.

## Python SDK

Thin official client (`goodrecmovies` on PyPI once published). Source lives in
[`packages/python/`](packages/python/).

```bash
pip install goodrecmovies
# from this repo before publish:
pip install -e packages/python
```

```python
from goodrecmovies import top_titles, search_titles, get_title, ask
```

There is also an [npm package](https://www.npmjs.com/package/goodrecmovies)
(`npm i goodrecmovies`) with the same surface.

## Agent entry points

- Machine guide: https://goodrecmovies.com/llms.txt
- Discovery: https://goodrecmovies.com/.well-known/ard.json
- Skills index: https://goodrecmovies.com/.well-known/agent-skills/index.json
- MCP server: https://goodrecmovies.com/mcp (card at /.well-known/mcp/server-card.json)
- Ask endpoint: https://goodrecmovies.com/ask (NLWeb)
- Markdown: send `Accept: text/markdown` or append `.md` to any page URL
