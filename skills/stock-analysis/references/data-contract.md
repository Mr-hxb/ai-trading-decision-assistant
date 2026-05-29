# Data Contract

## v1 Web Evidence Contract

Web data is evidence, not a complete local dataset. Each analysis should collect the following fields when available:

- `symbol`: requested ticker or symbol.
- `market`: exchange or market.
- `instrument_type`: stock, ETF, ADR, fund, index proxy, or unknown.
- `analysis_time`: date and time of the analysis.
- `quote`: latest cited price context.
- `quote_timestamp`: timestamp shown by the source, or `unavailable`.
- `currency`: quote currency when available.
- `source_urls`: URLs used for price, events, news, and context.
- `daily_bars`: available only if a source or future MCP provides structured historical bars.
- `company_events`: source-cited filings, announcements, earnings, guidance, corporate actions, or other material events.
- `news_items`: source-cited news with title, source, publication date, URL, and relevance.
- `market_context`: market, sector, or peer context with sources.
- `data_gaps`: unavailable quote timestamp, missing historical bars, missing volume, stale news, conflicting symbol mapping, or other limitations.

## Future MCP Contract

Future MCP integration should provide the same logical fields in structured form:

- Quote with exchange, currency, session status, and timestamp.
- Daily bars with date, open, high, low, close, adjusted close when available, volume, and data source.
- Company events with source type, date, title, URL, and whether the source is official.
- News items with publication time, source, URL, summary, and sentiment if available.
- Market and sector context with proxy symbols and timestamps.

The Skill should not need to change its reviewer roles when MCP arrives. Only the evidence-gathering step should switch from web-cited collection to structured MCP output.

## Limitations

- A quote card or chart summary is not a full daily-bar dataset.
- Delayed quotes must be labeled as delayed when the source says so.
- News can support catalyst and risk review but cannot replace missing price evidence.
- If daily bars are unavailable, technical review must stay limited.
