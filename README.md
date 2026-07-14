# Skill-First Stock Analysis

This repository defines an advisory-only stock analysis Skill for Codex. It is a workflow and prompt package, not a trading bot, broker integration, local data pipeline, report generator, or document publishing app.

The Skill helps analyze stocks, ETFs, holdings, portfolios, watchlists, trading setups, and market symbols by combining source-cited web evidence, an explicit decision policy, four classic trading-book framework reviews, and independent quality gates. Every final answer must remain auxiliary analysis for human review, but it should still lead with a clear evidence-bound judgment when the data is usable.

## Use Model

Use `skills/stock-analysis/SKILL.md` when a user asks for market or symbol analysis. The Skill is the execution source of truth and defines:

- Current evidence gathered from cited sources.
- Data-quality, fundamental, technical, risk, news/context, and review-gate roles.
- Four framework reviews inspired by `股票作手回忆录`, `专业投机原理`, `我如何从股市赚了 200 万`, and `日本蜡烛图技术`.
- A five-dimension evidence scorecard with hard overrides and explicit subjective synthesis.
- Fallback named review passes when native Codex subagents are unavailable.
- Required final output fields, including `human_review_required: true`.
- Watchlist follow-up behavior after each company or symbol analysis.

## Advisory Boundary

This project must not:

- Connect to brokers or trading execution systems.
- Place, submit, create, cancel, or modify orders.
- Present any status as an instruction to enter or exit a position.
- Claim guaranteed returns or deterministic price movement.
- Store API keys, access tokens, credentials, or machine-local paths.

The final decision always belongs to the human user.

## Data Policy

v1 allows web data only as cited evidence. Do not treat a quote snippet, chart summary, or news article as a complete daily-bar dataset.

Every analysis must identify:

- Symbol and market.
- Analysis date and time.
- Quote or source timestamp when available.
- Source URLs.
- Data gaps and uncertainty.
- Whether technical conclusions are limited by incomplete price history.

Future MCP data sources should satisfy the same contract with structured quote, daily bars, company events, news, and market or sector context.

Book files are local research material, not runtime inputs. The executable method is the reviewed synthesis in `skills/stock-analysis/references/four-books-framework.md`; do not assume that placing an ebook in the repository trains or automatically loads it.

## Company Watchlist

Use `watchlists/company-watchlist.md` as the versioned persistent list of companies for recurring reviews. After any company or market-symbol analysis, ask the user whether that company should be recorded there, or whether an existing entry should be updated.

Watchlist entries are factual workflow state, not portfolio data. Do not store account information, position sizes, cost basis, broker instructions, or trade actions.

## Expected Output

Final stock analysis should follow `skills/stock-analysis/references/output-format.md` and include:

- Evidence summary.
- Main judgment and decision score.
- Evidence scorecard, workflow state, invalidation, and upgrade conditions.
- DataQualityAgent verdict.
- FundamentalQualityAgent verdict.
- TechnicalSystemAgent verdict.
- RiskDisciplineAgent verdict.
- NewsContextAgent verdict when news or market context is used.
- DarvasBoxAgent, SpeculationPrinciplesAgent, OperatorMemoirsAgent, and CandlestickContextAgent verdicts for broad setup or watch decisions.
- ReviewGateAgent result.
- Limitations and human-review wording.

## Repository Layout

```text
AGENTS.md
README.md
watchlists/company-watchlist.md
skills/stock-analysis/SKILL.md
skills/stock-analysis/agents/
skills/stock-analysis/references/
skills/stock-analysis/evals/
```

Local caches, virtual environments, generated reports, and deprecated local data scratch directories are intentionally excluded from the repository.
