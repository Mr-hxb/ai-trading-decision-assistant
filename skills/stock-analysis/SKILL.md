---
name: stock-analysis
description: Use this Skill for advisory-only stock, ETF, holding, portfolio, watchlist, trading setup, or market-symbol analysis. It combines source-cited current evidence with four classic trading-book frameworks, an explicit decision policy, and independent review roles to return a clear human-review-required judgment without broker execution or deterministic advice.
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
- Calculate the score from `references/decision-policy.md`; do not invent an untraceable number or average agent votes.
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
- `references/decision-policy.md`: current default horizon, evidence scorecard, hard overrides, confidence, and subjective synthesis rules.
- `references/four-books-framework.md`: the Chinese source of truth for the four-book method, workflow states, invalidation layers, re-entry, and review principles.
- `references/output-format.md`: final answer shape.
- `agents/FundamentalQualityAgent.md`: use for broad company, setup, watchlist, thesis, growth, quality, valuation, or catalyst review.
- `agents/DarvasBoxAgent.md`: use when the user asks for Darvas, box, momentum-growth, or the `我是如何赚200w` framework.
- `agents/SpeculationPrinciplesAgent.md`: use when the user asks for trend, odds, discipline, or the `专业投机原理` framework.
- `agents/OperatorMemoirsAgent.md`: use when the user asks for tape reading, market psychology, position timing, or the `股市大作手回忆录` framework.
- `agents/CandlestickContextAgent.md`: use when the user asks about candlesticks, rejection, confirmation, breakout quality, or the `日本蜡烛图技术` framework.

## Workflow

1. Define the analysis target:
   - Symbol and market.
   - User's time horizon. If absent, use the default in `references/decision-policy.md` and state the assumption.
   - Analysis date and time.
   - Whether the user is asking for screening, technical review, news context, portfolio review, an existing-position review, or a broad watch decision.

2. Gather evidence:
   - Use source-cited web data for current quote, recent price context, company events, filings, news, and market or sector context.
   - Capture source URLs and timestamps when available.
   - State any unavailable timestamps or data gaps.
   - Do not treat web snippets as complete daily-bar history.

3. Run the data-quality gate first:
   - `DataQualityAgent` must return `can_decide`, `limited_decision`, or `blocked` before technical, framework, or risk conclusions.
   - If blocked, return `信息不足` with no score and explain exactly what evidence is required.
   - If limited, pass only the usable evidence and limitations to later reviewers.

4. Run review roles:
   - Prefer native Codex subagents when available.
   - If native subagents are unavailable, run separate named review passes in the conversation.
   - Do not pass your intended conclusion to reviewers.
   - Require each reviewer to contribute a decision direction when its evidence domain is sufficient.
   - Use the fallback template below when review roles run in the same conversation.

5. Required domain reviewers:
   - `FundamentalQualityAgent`: review source-grounded company quality, growth, cash flow, valuation expectations, catalysts, and thesis falsifiers.
   - `TechnicalSystemAgent`: review trend and structure only from cited price data; state limitations when full daily bars are unavailable.
   - `RiskDisciplineAgent`: check invalidation, stop reference, chase risk, position-risk framing, and advisory wording.
   - `NewsContextAgent`: use only when news, filings, announcements, macro, sector, or sentiment context is needed.

6. Run strategy-framework reviewers for setup or watch decisions:
   - For broad stock/ETF analysis, watchlist decisions, trend/setup reviews, or risk/reward questions, run all four framework agents independently by default:
     - `DarvasBoxAgent`
     - `SpeculationPrinciplesAgent`
     - `OperatorMemoirsAgent`
     - `CandlestickContextAgent`
   - If the request is only a quote lookup, pure news summary, filing summary, or data-quality check, these framework agents may be skipped with a reason.
   - If the user names only one framework, run only that matching framework agent.
   - Treat these as framework simulations, not author impersonation. Do not quote or imitate book text.
   - Give each framework the same evidence packet and do not pass your intended conclusion to it.
   - Each framework agent must return an allowed main judgment, the evidence it weights most, invalidation or risk observation levels, and one advisory verdict.
   - Framework verdicts are reviews of overlapping evidence, not independent votes. Do not count or average them.

7. Synthesize a draft judgment:
   - Apply the evidence scorecard and hard overrides in `references/decision-policy.md`.
   - Explain the strongest evidence for and against the calculated direction.
   - Resolve framework disagreement explicitly and state why one interpretation is more persuasive.
   - Use `workflow_state` only when supported by the user's context. Never infer a holding state from a watchlist request.

8. Run the final gate:
   - Give the complete draft, evidence packet, scorecard, domain verdicts, and framework verdicts to `ReviewGateAgent`.
   - If the gate fails, apply the required fixes and run the gate again. Do not return a failed draft.

9. Compose the final answer:
   - Follow `references/output-format.md`.
   - Lead with the main judgment, score, confidence, and invalidation or upgrade conditions.
   - Include each required agent verdict.
   - Include strategy-framework agent verdicts when they were run.
   - Include source list and limitations.
   - Keep conclusions as decision support and risk framing, not transaction instructions.
   - After the analysis, ask whether the analyzed company should be recorded in `watchlists/company-watchlist.md`; if it is already present, ask whether the entry should be updated.
   - Do not add or update `watchlists/company-watchlist.md` unless the user explicitly confirms.

## Fallback Named Review Passes

Use this template when native Codex subagents are unavailable. Run each pass separately and keep the evidence packet stable across passes.

1. Evidence packet:
   - Target symbol, market, instrument type, analysis horizon, analysis time, quote/source timestamp, source URLs, gathered price context, market/sector benchmarks, fundamental evidence, company events, news/context, and known data gaps.
   - Do not include a draft conclusion or preferred main judgment.

2. Required passes:
   - `DataQualityAgent`: decide `can_decide`, `limited_decision`, or `blocked` before any technical or risk judgment.
   - `FundamentalQualityAgent`: separate reported facts, expectations, interpretation, financial quality, catalysts, and thesis falsifiers.
   - `TechnicalSystemAgent`: use only price evidence allowed by `DataQualityAgent`; mark conclusions limited when daily bars or volume are missing.
   - `RiskDisciplineAgent`: evaluate invalidation, stop/risk reference, chase risk, event risk, and advisory wording.
   - `NewsContextAgent`: run only when news, filings, announcements, macro, sector, or sentiment context is part of the answer; otherwise mark skipped with reason.

3. Strategy-framework passes:
   - For setup, trend, watchlist, or broad stock/ETF decisions, run `DarvasBoxAgent`, `SpeculationPrinciplesAgent`, `OperatorMemoirsAgent`, and `CandlestickContextAgent` with the same evidence packet.
   - Skip them only for quote lookup, pure news summary, filing summary, or data-quality-only tasks, and state why.

4. Synthesis and gate:
   - Build the evidence scorecard without averaging agent verdicts.
   - Draft the answer, then run `ReviewGateAgent` against the complete draft and all verdicts.
   - Apply every required fix and rerun the gate until it passes or the evidence is downgraded to `信息不足`.

## Watchlist Updates

- `watchlists/company-watchlist.md` is repository content and the persistent company list for recurring reviews.
- Ask before adding a new company or updating an existing row.
- Update only factual fields: symbol, market, company name, common Chinese name, status, added date, source/context, and notes.
- Preserve symbol-mapping ambiguity in `Notes`; do not silently normalize an ambiguous company name.
- Never store account data, position sizes, cost basis, broker instructions, or trade actions in the watchlist.

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
