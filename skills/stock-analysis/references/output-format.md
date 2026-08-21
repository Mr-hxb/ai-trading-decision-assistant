# Output Format

Use a concise structure. Keep the answer advisory, source-grounded, and judgment-forward.

## Required Sections

```markdown
**结论**
- human_review_required: true
- 主判断: [强关注 / 关注 / 等待 / 回避 / 信息不足]
- decision_score: [0-10 setup-quality score, not return forecast]
- confidence: [high / medium / low]
- workflow_state: [S0 / S1 / S2 / S3, S4 / S5 / S2R only with explicit position context, or unavailable when blocked/not applicable]
- 一句话判断: [evidence-bound decision summary]
- 风险接受型判断: [only when useful or requested; how the view changes for a higher-risk user]
- 失效条件: [specific price, event, filing, data-quality, or thesis conditions that weaken the judgment]
- 升级条件: [specific confirmation that would improve the judgment]

**证据**
- 标的: [symbol, market, instrument type]
- 分析时间: [date/time]
- 行情时间: [quote/source timestamp or unavailable]
- 关键来源: [source names with URLs]
- 数据缺口: [missing or stale data]

**证据评分** [omit scores when the decision is blocked]
- 市场与板块: [0-2 and evidence reason]
- 基本面与催化: [0-2 and evidence reason]
- 相对强度、趋势与结构: [0-2 and evidence reason]
- 触发、成交量与 K 线语境: [0-2 and evidence reason]
- 风险与失效条件: [0-2 and evidence reason]
- 硬性覆盖规则: [none, or the rule that changed/capped the result]

**Agent 复核**
- DataQualityAgent: [verdict, decision permission, framework permissions, and key reason]
- FundamentalQualityAgent: [verdict, thesis direction, strongest fact, and falsifier]
- TechnicalSystemAgent: [verdict, decision contribution, and key reason]
- RiskDisciplineAgent: [verdict, risk acceptability, and key reason]
- NewsContextAgent: [verdict, context bias, and key reason, or skipped with reason]
- ReviewGateAgent: [pass/fail and required caveat]

**策略框架 Agent** [when run; default for setup/watch/trend reviews]
- DarvasBoxAgent: [status and key reason]
- SpeculationPrinciplesAgent: [status and key reason]
- OperatorMemoirsAgent: [status and key reason]
- CandlestickContextAgent: [status and key reason]
- 四方分歧: [where the frameworks agree or disagree]

**分析**
- 我的判断: [why this side is more likely than the alternatives]
- 主观裁决说明: [only when the final status differs from the raw score band; name the evidence interaction]
- 技术结构: [only supported by cited evidence]
- 风险与纪律: [invalidation, chase risk, event risk, limitations]
- 新闻/市场背景: [only if source-grounded context was gathered]
- 反方理由: [the strongest evidence against the main judgment]

**限制**
- [limitations that affect confidence]
- [what data would improve the review]
```

## Status Language

Allowed main judgments:

- `强关注`: strong evidence alignment; clear risk reference; no unresolved hard blocker.
- `关注`: favorable but imperfect evidence; worth tracking with explicit invalidation.
- `等待`: interesting but timing, confirmation, valuation, or risk reference is not clean enough.
- `回避`: unattractive setup or risk not justified by current evidence.
- `信息不足`: current evidence is not sufficient for a responsible judgment.

Decision score guide:

- `8-10`: strong setup quality; use `强关注` unless a hard risk blocker exists.
- `6-7`: constructive setup quality; use `关注`.
- `4-5`: mixed or timing-poor setup quality; use `等待`.
- `0-3`: weak or unattractive setup quality; use `回避`.
- No score: only when `信息不足` is required.

Calculate the score from `decision-policy.md`. Framework agents review overlapping evidence and must not be counted as independent votes.

Do not use command language. Do not convert any status into a transaction decision.

## Tone

- Be direct and concrete.
- Lead with the judgment before caveats.
- Say "我的判断是..." when evidence is sufficient.
- Distinguish facts, interpretations, and missing evidence.
- State confidence only after the agent review.
- Do not hide uncertainty.
- Do not overuse uncertainty language to avoid taking a side.
- When strategy-framework agents are used, describe them as framework simulations, not author impersonations.
