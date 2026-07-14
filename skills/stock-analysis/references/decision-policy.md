# Personal Decision Policy

This file converts evidence into a stable but still subjective advisory judgment. It is the current repository policy, not a claim that the four books prescribe these exact scores or defaults.

## Default Assumptions

- `direction`: evaluate long-side setup quality by default; do not infer a short recommendation.
- `horizon`: when the user gives no horizon, use daily structure with weekly context and describe the result as a weeks-to-months review.
- `risk_style`: moderate unless the user explicitly states otherwise.
- `portfolio_context`: unknown unless the user provides it. Do not infer holdings, account size, cost basis, or position size from the watchlist.
- `execution_boundary`: provide a judgment, invalidation, and upgrade conditions; do not provide an order or personalized position command.

State these assumptions when they materially affect the answer. Ask for clarification only when different reasonable assumptions would change the main judgment.

## Evidence Scorecard

Score five evidence dimensions from 0 to 2. Use only cited, timestamped, and DataQualityAgent-approved evidence.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Market and sector | Clear headwind, weak breadth, or no usable context | Mixed or partial alignment | Market and sector evidence align with the setup |
| Fundamentals and catalyst | Thesis weakening, unsupported, or materially adverse | Plausible but mixed, mature, or incompletely verified | Improving fundamentals or a verified catalyst with a clear falsifier |
| Relative strength, trend, and structure | Weak structure or underperformance | Mixed structure, rebound, or incomplete confirmation | Clear relative strength and constructive same-horizon structure |
| Trigger, volume, and candlestick context | Rejection, failed setup, or contradictory confirmation | Incomplete or mixed confirmation | Price, volume, location, and follow-through align |
| Risk and invalidation | Risk is unjustified or invalidation is unavailable | Risk is stretched or partially defined | Clear invalidation and favorable evidence-bound asymmetry |

Total score mapping:

- `8-10`: `强关注`
- `6-7`: `关注`
- `4-5`: `等待`
- `0-3`: `回避`
- No score: `信息不足`

The score measures current setup quality. It is not expected return, probability of profit, or a position-size recommendation.

## Hard Overrides

Apply these before the score mapping:

- `DataQualityAgent=blocked`: use `信息不足` and do not assign a score.
- Unresolved symbol mapping or a conflict in a decision-critical fact: use `信息不足`.
- Current technical request without usable current price context: use `信息不足` for the technical conclusion.
- Core thesis is already falsified or risk is `unacceptable`: use `回避`; positive technical evidence cannot offset it.
- Missing same-horizon price history or volume for a setup claim: do not use `强关注`; state the technical limitation.
- A single candlestick pattern without location and follow-through cannot upgrade the judgment.
- News or narrative cannot replace missing price evidence for a current setup decision.

## Subjective Synthesis

The scorecard disciplines the judgment; it does not replace judgment.

After scoring:

1. State the most likely interpretation in plain language.
2. Identify the two or three pieces of evidence carrying the most weight.
3. Give the strongest opposing interpretation.
4. Explain framework disagreement without treating agents as votes.
5. State specific invalidation and upgrade conditions.

The final judgment may move at most one status band away from the raw score when an important evidence interaction is not captured by the additive score. The answer must name that interaction and cannot override a hard blocker.

Examples of legitimate interactions:

- Strong company evidence but an unusually extended price structure may reduce `关注` to `等待`.
- Mixed market context but exceptional relative strength with a clean invalidation may preserve `关注`.
- Apparently constructive price action immediately before a material binary event may reduce the judgment because gap risk dominates the setup.

## Confidence

Confidence measures evidence quality, not enthusiasm:

- `high`: current primary sources or reliable structured data, clear timestamps, no material conflict, and sufficient same-horizon evidence.
- `medium`: usable evidence with explicit gaps or moderate framework disagreement.
- `low`: a limited decision is still possible, but important price, volume, fundamental, or context evidence is partial.

`信息不足` has no score. Explain the blocking evidence instead of assigning artificial confidence.

## Workflow State

- Use `S0-S3` for ordinary research and watch decisions.
- Use `S4`, `S5`, or `S2R` only when the user explicitly provides existing-position or prior-invalidation context.
- Use `unavailable` when DataQualityAgent is blocked or a workflow state is not applicable to the request.
- `workflow_state` never replaces `main_judgment` and never implies an order.

## Risk Framing

Do not provide default account-risk percentages or initial-position fractions. Those are user-specific policy parameters and are currently unset.

If the user explicitly asks for educational position-risk framing, explain the general relationship between account risk, structural invalidation distance, gap/liquidity risk, and concentration. Keep inputs ephemeral and never store account values in the watchlist.

## Policy Changes

Update this file only after the user explicitly confirms a preference such as:

- default horizon or market universe;
- growth, quality, valuation, or catalyst priority;
- acceptable event, liquidity, leverage, or drawdown risk;
- score weights or hard vetoes;
- portfolio concentration or correlation policy.
