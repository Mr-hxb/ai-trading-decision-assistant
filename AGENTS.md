# Project Agent Instructions

This repository is a Skill-first, advisory-only stock analysis workflow. It is not a Python CLI, data-ingestion service, broker integration, automated trading system, or document publishing app.

## Mandatory Workflow

For any request to analyze a stock, ETF, holding, portfolio, watchlist, trading setup, or market symbol:

1. Read `skills/stock-analysis/SKILL.md`.
2. Gather current source-cited evidence. Use web sources only as cited evidence, not as a complete market dataset.
3. Record symbol, market, analysis date/time, quote/source timestamp when available, source URLs, missing data, and uncertainty.
4. Run independent review roles:
   - `DataQualityAgent`
   - `TechnicalSystemAgent`
   - `RiskDisciplineAgent`
   - `NewsContextAgent` only when source-grounded news, filings, announcements, or market context are needed.
   - `ReviewGateAgent`
5. Prefer native Codex subagents as independent reviewers when available. If native subagents are unavailable, run separate named review passes in the same conversation.
6. Final output must include `human_review_required: true`, advisory-only wording, source list, limitations, and each required agent verdict.

Do not answer from general market commentary alone. Do not let web snippets override missing, stale, or incomplete price evidence.

## Source And Data Rules

- Cite sources for quotes, company events, filings, announcements, news, and market context.
- Include source timestamps or state when a timestamp is unavailable.
- If full daily bars are unavailable, say that technical conclusions are limited.
- Do not fabricate price history, volume, filings, news, or market context.
- Future MCP data must satisfy the same data contract described in `skills/stock-analysis/references/data-contract.md`.

## Safety Rules

- Do not store API keys, access tokens, credentials, or local machine paths in the repository.
- Do not implement or call broker execution, order placement, or automatic position-changing logic.
- Do not present analysis status as a trade command.
- Do not output deterministic investment advice or guaranteed-return claims.
- Keep all analysis advisory and require human review.

## Out Of Scope

- No local CLI scan workflow.
- No local provider modules.
- No generated Markdown report pipeline.
- No document-platform publishing path.
- No Python test suite is expected after this refactor because the repository contains workflow documents rather than executable Python code.
