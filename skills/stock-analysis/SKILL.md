---
name: stock-analysis
description: Use this Skill for advisory-only stock, ETF, holding, portfolio, watchlist, trading setup, or market-symbol analysis. It gathers source-cited current evidence, runs independent review roles, and returns a human-review-required analysis without broker execution or deterministic advice.
---

# Stock Analysis

## Purpose

Use this Skill to analyze market symbols with source-cited evidence and independent review roles. The Skill is advisory-only, but it must still make a clear judgment when evidence is usable. It must not place orders, call broker execution APIs, or turn any conclusion into a trade instruction.

## Mandatory Trigger

Use this Skill before the final answer whenever the user asks about:

- A stock, ETF, holding, portfolio, watchlist, or market symbol.
- Whether a setup is worth attention.
- Trend, structure, stop reference, invalidation, risk/reward, or chase risk.
- News, filing, announcement, market, sector, or sentiment context for a symbol.

## Decision Standard

This Skill should be useful for decision support, not merely a list of caveats.

- When evidence is usable, make a best-effort main judgment even when uncertainty remains.
- Lead with one `主判断`: `强关注`, `关注`, `等待`, `回避`, or `信息不足`.
- Use `信息不足` only when core evidence is genuinely missing, stale, conflicting, or blocked. Do not use it as a conservative default.
- Include a `decision_score` from 0 to 10 and a `confidence` level. The score is a setup-quality score, not a return forecast.
- State the most likely interpretation first, then give the conditions that would prove it wrong.
- If the user says they can accept higher risk, add a `风险接受型判断` that explains how the view changes under higher risk tolerance. Keep it as risk framing, not a transaction command.
- Be willing to say `回避` when risk/reward, news, data quality, or technical structure is poor.
- Be willing to say `强关注` when evidence aligns across price, fundamentals or catalyst, risk reference, and review agents.

Decision status guide:

- `强关注`: strong evidence alignment; clear risk reference; no unresolved hard blocker.
- `关注`: favorable but imperfect evidence; worth tracking with explicit invalidation.
- `等待`: interesting but timing, confirmation, valuation, or risk reference is not clean enough.
- `回避`: the setup is unattractive or risk is not justified by the evidence.
- `信息不足`: no responsible decision can be made from the current evidence.

Do not use a long list of limitations to erase the judgment. Limitations should explain confidence and invalidation, not replace the main decision.

## Required References

Read these references when their topic is needed:

- `references/source-policy.md`: source quality, freshness, and citation rules.
- `references/data-contract.md`: v1 web evidence and future MCP data fields.
- `references/output-format.md`: final answer shape.
- `agents/DarvasBoxAgent.md`: use when the user asks for Darvas, box, momentum-growth, or the `我是如何赚200w` framework.
- `agents/SpeculationPrinciplesAgent.md`: use when the user asks for trend, odds, discipline, or the `专业投机原理` framework.
- `agents/OperatorMemoirsAgent.md`: use when the user asks for tape reading, market psychology, position timing, or the `股市大作手回忆录` framework.

## Workflow

1. Define the analysis target:
   - Symbol and market.
   - User's time horizon if provided.
   - Analysis date and time.
   - Whether the user is asking for technical review, news context, portfolio review, or a broad watch decision.

2. Gather evidence:
   - Use source-cited web data for current quote, recent price context, company events, filings, news, and market or sector context.
   - Capture source URLs and timestamps when available.
   - State any unavailable timestamps or data gaps.
   - Do not treat web snippets as complete daily-bar history.

3. Run review roles:
   - Prefer native Codex subagents when available.
   - If native subagents are unavailable, run separate named review passes in the conversation.
   - Do not pass your intended conclusion to reviewers.
   - Require each reviewer to contribute a decision direction when its evidence domain is sufficient.

4. Required reviewers:
   - `DataQualityAgent`: verify symbol mapping, market, source freshness, quote/date consistency, missing data, and whether evidence is sufficient.
   - `TechnicalSystemAgent`: review trend and structure only from cited price data; state limitations when full daily bars are unavailable.
   - `RiskDisciplineAgent`: check invalidation, stop reference, chase risk, position-risk framing, and advisory wording.
   - `NewsContextAgent`: use only when news, filings, announcements, macro, sector, or sentiment context is needed.
   - `ReviewGateAgent`: enforce source list, limitations, advisory-only wording, no trade-command wording, and `human_review_required: true`.

5. Run strategy-framework reviewers for setup or watch decisions:
   - For broad stock/ETF analysis, watchlist decisions, trend/setup reviews, or risk/reward questions, run all three framework agents independently by default:
     - `DarvasBoxAgent`
     - `SpeculationPrinciplesAgent`
     - `OperatorMemoirsAgent`
   - If the request is only a quote lookup, pure news summary, filing summary, or data-quality check, these framework agents may be skipped with a reason.
   - If the user names only one framework, run only that matching framework agent.
   - Treat these as framework simulations, not author impersonation. Do not quote or imitate book text.
   - Give each framework the same evidence packet and do not pass your intended conclusion to it.
   - Each framework agent must return an allowed main judgment, the evidence it weights most, invalidation or risk observation levels, and one advisory verdict.

6. Compose the final answer:
   - Follow `references/output-format.md`.
   - Lead with the main judgment, score, confidence, and invalidation or upgrade conditions.
   - Include each required agent verdict.
   - Include strategy-framework agent verdicts when they were run.
   - Include source list and limitations.
   - Keep conclusions as decision support and risk framing, not transaction instructions.

## Hard Safety Rules

- Never connect to broker execution systems.
- Never place, submit, create, cancel, or modify orders.
- Never claim guaranteed returns or deterministic price movement.
- Never convert an analysis status into a buy/sell/hold instruction.
- Never present a decision score as expected return, probability of profit, or position-size command.
- Always include `human_review_required: true`.

## Failure Handling

- If symbol mapping is uncertain, stop and ask for clarification or present the ambiguity.
- If current quote data is unavailable, say the analysis cannot make a current technical assessment.
- If only news context is available, limit the answer to news/context review.
- If sources conflict, report the conflict and lower confidence.
- If review roles cannot be run independently, state the fallback: separate named review passes in the same conversation.
