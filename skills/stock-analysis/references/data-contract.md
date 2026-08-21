# Data Contract

## v1 Web Evidence Contract

Web data is evidence, not a complete local dataset. Each analysis should collect the following fields when available:

- `symbol`: requested ticker or symbol.
- `market`: exchange or market.
- `instrument_type`: stock, ETF, ADR, fund, index proxy, or unknown.
- `analysis_horizon`: user-provided horizon or the documented default assumption.
- `analysis_time`: date and time of the analysis.
- `quote`: latest cited price context.
- `quote_timestamp`: timestamp shown by the source, or `unavailable`.
- `currency`: quote currency when available.
- `source_urls`: URLs used for price, events, news, and context.
- `daily_bars`: available only if a source or future MCP provides structured historical bars.
- `weekly_bars`: same logical OHLCV fields when weekly context is used.
- `market_benchmarks`: cited same-period index or proxy evidence used to determine market regime.
- `sector_context`: cited sector proxy, representative peers, breadth, and relative-strength evidence when used.
- `fundamental_evidence`: cited revenue, earnings, cash flow, balance-sheet, guidance, valuation, dilution, governance, or operating metrics used in the thesis.
- `company_events`: source-cited filings, announcements, earnings, guidance, corporate actions, or other material events.
- `news_items`: source-cited news with title, source, publication date, URL, and relevance.
- `market_context`: market, sector, or peer context with sources.
- `data_gaps`: unavailable quote timestamp, missing historical bars, missing volume, stale news, conflicting symbol mapping, or other limitations.

## Minimum Evidence For Decisions

A responsible main judgment requires a stable evidence packet. Use these thresholds before assigning `强关注`, `关注`, `等待`, or `回避`.

- Required for any current technical or setup judgment:
  - Confirmed symbol mapping, market, and instrument type.
  - Current or latest available quoted price context from a cited source.
  - Quote or source timestamp, or an explicit `unavailable` timestamp note.
  - Enough cited price context to support the claimed trend, range, support/resistance, or breakout/breakdown observation.
  - A stated analysis horizon so daily, weekly, and intraday claims are not mixed.
  - Visible data gaps, including missing daily bars, missing volume, delayed quotes, stale data, or conflicting symbol mapping.

- Required for box, 1-2-3, 2B, candlestick, volume-confirmation, or relative-strength claims:
  - Same-horizon OHLCV or an equally explicit source showing the complete bars used.
  - The lookback period or visible date range used for the structure.
  - A cited market or sector benchmark for relative-strength claims.
  - Subsequent same-horizon bars when the conclusion depends on follow-through or confirmation.
  - If these fields are unavailable, mark the framework contribution limited or blocked; do not reconstruct bars from a quote card or narrative chart summary.

- Required for a favorable fundamental or catalyst score:
  - At least one dated primary or high-quality source supporting the claimed improvement or catalyst.
  - A concrete falsifier or adverse fact that would weaken the thesis.
  - Clear separation of reported facts, guidance, consensus expectations, analyst opinion, and interpretation.

- Required for news, filing, event, or market-context claims:
  - Source URL, source name, and publication or filing date when available.
  - Clear separation between official facts, reputable news, analyst opinion, rumor, and interpretation.

- Use `信息不足` when:
  - Symbol mapping is unresolved.
  - Current quote or latest price context is unavailable for a current technical request.
  - Sources conflict on a fact that determines the conclusion and the conflict cannot be resolved.
  - The evidence only supports a news/context summary, but the user asked for a current setup or technical judgment.

- Use a limited judgment instead of `信息不足` when:
  - Symbol and quote context are usable, but daily bars, volume, or market context are partial.
  - The missing data only lowers confidence or limits technical depth, and the limitation is explicit in the final answer.
  - A bounded non-technical judgment remains possible, but unavailable OHLCV prevents a strong setup or candlestick conclusion.

## Future MCP Contract

Future MCP integration should provide the same logical fields in structured form:

- Quote with exchange, currency, session status, and timestamp.
- Daily bars with date, open, high, low, close, adjusted close when available, volume, and data source.
- Weekly bars or a deterministic weekly aggregation when weekly context is used.
- Market benchmarks, sector proxies, representative peers, and aligned timestamps for relative-strength and breadth review.
- Fundamental observations with metric name, period, value, unit, source, filing or publication date, and whether the value is reported, guided, estimated, or interpreted.
- Company events with source type, date, title, URL, and whether the source is official.
- News items with publication time, source, URL, summary, and sentiment if available.
- Market and sector context with proxy symbols and timestamps.

The Skill should not need to change its reviewer roles when MCP arrives. Only the evidence-gathering step should switch from web-cited collection to structured MCP output.

## Limitations

- A quote card or chart summary is not a full daily-bar dataset.
- Delayed quotes must be labeled as delayed when the source says so.
- News can support catalyst and risk review but cannot replace missing price evidence.
- If daily bars are unavailable, technical review must stay limited.
