# Decision Subagent Design

## 为什么决策时也要用 Subagent

单一分析流程容易把趋势、箱体、风险、交易纪律、市场环境和消息面混在一起，导致正向证据被过度放大。Runtime Decision Subagents 把判断拆成独立角色，让 Bull Case 只找支持进入观察池的证据，让 Bear Case、Risk、Discipline 专门找反对理由、风险和 FOMO，再让三套流派审查分别给出选股、行情和舆论判断。

## 调度顺序

MarketDataSubagent → IndicatorSubagent → PatternDetectionSubagent → TrendSubagent → MarketRegimeSubagent → TechnicalThesisSubagent → BullCaseSubagent → BearCaseSubagent → RiskSubagent → DisciplineSubagent → DarvasDoctrineSubagent → SperandeoPrinciplesSubagent → LivermoreTapeReadingSubagent → ScoringSubagent → DecisionCommitteeSubagent → TradingSkillSubagent → ReportSubagent → HumanApprovalGate

## 职责、输入和输出

| Subagent | 职责边界 | 输入 | 输出 | v1 类型 | 未来升级 |
| --- | --- | --- | --- | --- | --- |
| MarketDataSubagent | 获取日线数据、统一字段、检查缺失，不做策略判断 | provider、symbol、start/end | normalized bars | 规则型 | 可加数据质量 LLM 摘要 |
| IndicatorSubagent | 计算 ma20、ma50、ma200、volume_ma20、volume_ratio、阶段指标 | bars | enriched bars | 规则型 | 无需 LLM |
| PatternDetectionSubagent | 识别达瓦斯箱体、突破，预留 1-2-3 和 2B | enriched bars、darvas config | structure signals | 规则型 | 可加形态解释 LLM |
| TrendSubagent | 判断趋势、均线结构、接近阶段新高 | enriched bars、trend config | trend_result | 规则型 | 无需 LLM |
| MarketRegimeSubagent | 从研究上下文提取市场环境、风险偏好、默认指数代理 | symbol、research_context | market_regime | 规则型 | 可接自动网页研究摘要 |
| TechnicalThesisSubagent | 只说明技术结构是否符合系统 | trend、pattern、volume | technical_thesis | 规则型 | 可升级 LLM 文案 |
| BullCaseSubagent | 只寻找支持进入观察池的证据 | structured results | bullish_evidence | 规则型 | 可升级 LLM，但必须引用结构化数据 |
| BearCaseSubagent | 寻找反对理由和风险 | structured results | bearish_evidence、serious_risk | 规则型 | 可升级 LLM 风险审查 |
| RiskSubagent | 计算止损参考、风险收益比、FOMO 风险 | bars、box result | risk_result | 规则型 | 无需 LLM |
| DisciplineSubagent | 检查追涨、止损、下跌趋势幻想等纪律 | trend、risk、pattern | discipline_flags | 规则型 | 可升级 LLM 复盘提醒 |
| DarvasDoctrineSubagent | 按达瓦斯箱体风格审查强势趋势、窄箱体、突破和追高风险 | trend、pattern、market、research_context | doctrine_reviews.DarvasDoctrineSubagent | 规则型 | 可升级为带引用的 LLM 审查 |
| SperandeoPrinciplesSubagent | 按专业投机原则审查趋势定义、风险参考和风险收益比 | trend、risk、market、research_context | doctrine_reviews.SperandeoPrinciplesSubagent | 规则型 | 可升级为带引用的 LLM 审查 |
| LivermoreTapeReadingSubagent | 按盘面阅读风格审查关键价位、成交确认和市场情绪 | trend、volume、market、research_context | doctrine_reviews.LivermoreTapeReadingSubagent | 规则型 | 可升级为带引用的 LLM 审查 |
| ScoringSubagent | 汇总结构分，用于排序 | trend、box、risk | score_result | 规则型 | 无需 LLM |
| DecisionCommitteeSubagent | 汇总多方输出，给辅助状态和降级理由；任一流派拒绝或等待会触发硬降级 | bull、bear、risk、discipline、score、doctrine_reviews | decision_result | 规则型 | 可升级为带 guardrails 的 LLM |
| TradingSkillSubagent | 生成可复制给 LLM 的分析 Prompt | candidate context | prompt text | 规则型 | 可接 OpenAI Agents SDK |
| ReportSubagent | 输出每日 Markdown 报告 | all candidates | report path | 规则型 | 可扩展周报 |
| HumanApprovalGate | 强制人工最终确认 | report path | human gate result | 规则型 | 无需 LLM |

## 禁止交给 Subagent 做的事

- 自动触发交易。
- 调用真实交易执行接口。
- 绕过配置中的风险收益比和止损规则。
- 编造新闻、基本面或确定性收益判断。
- 输出被禁止的交易指令语言。
- 把 `score` 解释为真实交易动作。

## 防止过度乐观和 FOMO

1. BullCase 只能基于结构化数据寻找观察池证据。
2. BearCase 必须寻找趋势不稳、假突破、买点过远、成交量不配合。
3. RiskSubagent 独立计算止损和风险收益比，任何止损不清晰都会限制状态。
4. DisciplineSubagent 专门检查 FOMO、追涨、没有止损、下跌趋势幻想。
5. 三个流派审查都要输出选股、行情和舆论判断；没有研究上下文时必须降低置信度，不能编造消息。
6. DecisionCommitteeSubagent 有硬规则：没有止损、突破无效、趋势不成立、风险收益比不足、FOMO、严重风险或流派审查未通过时，不能给最高辅助状态。
