# Project Agent Instructions

This repository is a Skill-first, advisory-only stock analysis workflow. It is not a Python CLI, data-ingestion service, broker integration, automated trading system, or document publishing app.

## Mandatory Workflow

For any request to analyze a stock, ETF, holding, portfolio, watchlist, trading setup, or market symbol:

1. Read `skills/stock-analysis/SKILL.md`.
2. Follow the Skill workflow and references as the source of truth for evidence, review roles, output shape, and failure handling.
3. Final output must include `human_review_required: true`, advisory-only wording, source list, limitations, and each required agent verdict.

Do not answer from general market commentary alone. Do not let web snippets override missing, stale, or incomplete price evidence.

The four-book method is defined by `skills/stock-analysis/references/four-books-framework.md`. Use `skills/stock-analysis/references/decision-policy.md` for scoring, hard overrides, confidence, and subjective synthesis. Do not treat framework agents as independent votes.

## Company Watchlist

- Use `watchlists/company-watchlist.md` as the persistent list of companies to review.
- When the user asks to query, analyze, or summarize a company or market symbol, finish the answer by asking whether this company should be recorded in `watchlists/company-watchlist.md`.
- If the company is already recorded, ask whether the existing entry should be updated instead.
- Do not add or update a company entry without explicit user confirmation.
- Keep watchlist entries factual: symbol, market, company name, common name, status, added date, source/context, and notes.
- Do not record account data, position sizes, cost basis, broker instructions, or trade actions.

## Source And Data Rules

- Cite sources for quotes, company events, filings, announcements, news, and market context.
- Include source timestamps or state when timestamps are unavailable.
- Do not fabricate price history, volume, filings, news, or market context.
- Future MCP data must satisfy the same data contract described in `skills/stock-analysis/references/data-contract.md`.
- Do not infer box, 1-2-3, 2B, relative-strength, volume-confirmation, or candlestick conclusions without the same-horizon evidence required by the data contract.

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
