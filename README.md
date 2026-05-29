# Skill-First Stock Analysis

This repository defines an advisory-only stock analysis Skill for Codex. It is a workflow and prompt package, not a trading bot, broker integration, local data pipeline, report generator, or document publishing app.

The Skill helps analyze stocks, ETFs, holdings, portfolios, watchlists, trading setups, and market symbols by combining source-cited web evidence with independent review roles. Every final answer must remain auxiliary analysis for human review, but it should still lead with a clear evidence-bound judgment when the data is usable.

## Use Model

Use `skills/stock-analysis/SKILL.md` when a user asks for market or symbol analysis. The Skill requires:

- Current evidence gathered from cited sources.
- Clear source timestamps or an explicit note when a timestamp is unavailable.
- A data-quality check before technical or risk conclusions.
- Separate review passes for technical structure, risk discipline, news context when needed, and the final review gate.
- `human_review_required: true` in every final output.
- A main judgment, decision score, confidence, invalidation conditions, and upgrade conditions whenever evidence is sufficient.

Native Codex subagents should be used as independent reviewers when available. If they are not available, run the same roles as clearly separated review passes in the conversation.

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

## Expected Output

Final stock analysis should follow `skills/stock-analysis/references/output-format.md` and include:

- Evidence summary.
- Main judgment and decision score.
- DataQualityAgent verdict.
- TechnicalSystemAgent verdict.
- RiskDisciplineAgent verdict.
- NewsContextAgent verdict when news or market context is used.
- ReviewGateAgent result.
- Limitations and human-review wording.

## Repository Layout

```text
AGENTS.md
README.md
skills/stock-analysis/SKILL.md
skills/stock-analysis/agents/
skills/stock-analysis/references/
```
