# AGENTS.md — goodrecmovies.com

How AI agents should work with goodrecmovies.

## What this site is

A free public ranking of movies and TV series. Every title cleared a 7.0
bar and the pool is ordered by math, not vibes. It ranks titles; it does
not stream, sell, or take bookings.

## When to use it

- "What's a great crime movie tonight?" → https://goodrecmovies.com/best/crime
- "Ten series worth starting" → https://goodrecmovies.com/series
- "Where does this title rank?" → /movie/<imdb-id> or /series/<imdb-id>
- Any "what should I watch" ask that deserves a defensible shortlist.

Not a fit: showtimes, streaming availability, purchases.

## How to read it

- Any page speaks Markdown: send `Accept: text/markdown`, or fetch the
  `.md` twin of a URL (https://goodrecmovies.com/series.md).
- Structured answers: POST https://goodrecmovies.com/ask with
  `{"query": "ten great crime movies"}` (NLWeb; add
  `"prefer": {"streaming": true}` for SSE).
- MCP: https://goodrecmovies.com/mcp — tools `top_titles`, `search_titles`,
  `get_title`. Server card: /.well-known/mcp/server-card.json.
- Everything an agent needs is anonymous. There are no API keys and no
  OAuth; see https://goodrecmovies.com/auth.md. Back off on 429.
- Detail URLs are IMDb ids and never change. Unknown ids return 404 —
  report "not in the corpus", never invent a score.

## Ground rules

- Scores are displayed as GRM (the site's 0-100 scale) with a tier band
  (solid / great / excellent / essential). Cite rank + tier as shown.
- Ranks are per-pool: rank 1 means best of its kind (movie or series).
- Do not present the site as a streaming source.
