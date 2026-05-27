# Framework Research

调研原则：优先参考官方 GitHub README 或官方文档；本项目第一版只做日线 / 收盘后辅助决策，不做自动交易执行。

## 多 Agent 编排框架

| 项目 | GitHub / 官方文档来源 | 适合解决什么问题 | 是否适合第一版 MVP | 可借鉴设计 | 不建议照搬 | API Key | 日线 / 收盘后适配 | 后续扩展价值 | 推荐结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LangGraph | https://github.com/langchain-ai/langgraph / https://langchain-ai.github.io/langgraph/ | 状态化、多步骤、可恢复的 Agent 图编排 | 不作为硬依赖 | 状态图、节点边界、可观测执行路径 | v1 流程固定，强上图框架会增加部署和认知成本 | 取决于模型供应商 | 适合 | 高 | 后续用于状态化多 Agent 编排 |
| OpenAI Agents SDK | https://github.com/openai/openai-agents-python / https://openai.github.io/openai-agents-python/ | Agent、handoff、guardrails、tracing、工具调用 | 不作为硬依赖 | guardrails、tracing、handoff、结构化输出 | v1 不直接调用 LLM，先不引入网络和 Key 依赖 | 真实调用 OpenAI 时需要 | 适合 | 高 | 后续用于真实 LLM Subagent |
| CrewAI | https://github.com/crewAIInc/crewAI / https://docs.crewai.com/ | 角色任务式多 Agent 协作 | 不作为硬依赖 | 角色职责拆分、任务流、审查角色 | 可能把规则流程包装得过重 | 通常需要模型 Key | 适合 | 中 | 后续用于角色任务实验 |
| Microsoft Agent Framework | https://github.com/microsoft/agent-framework | 企业级 Agent 编排、工作流和多语言生态 | 不作为硬依赖 | workflow 概念、企业集成边界 | v1 本地规则型场景不需要企业级栈 | 取决于模型供应商 | 适合 | 中 | 观察后续成熟度 |
| AutoGen | https://github.com/microsoft/autogen / https://microsoft.github.io/autogen/ | 多 Agent 对话、工具协作、实验性 Agent 研究 | 不作为硬依赖 | 多角色审查、对话式协作 | v1 不需要开放式 Agent 对话 | 通常需要模型 Key | 适合 | 中 | 后续可做审查代理实验 |
| PydanticAI | https://github.com/pydantic/pydantic-ai / https://ai.pydantic.dev/ | 类型安全的 LLM 应用、结构化结果 | 暂不强制 | Typed output、schema 校验 | v1 可以用 dataclass 先保证结构 | 取决于模型供应商 | 适合 | 高 | 后续升级 LLM 输出校验 |
| LlamaIndex Workflows | https://docs.llamaindex.ai/en/stable/understanding/workflows/ / https://github.com/run-llama/llama_index | 事件驱动工作流、RAG/数据应用编排 | 不作为硬依赖 | step/event 思路、可观测流程 | v1 没有 RAG 核心需求 | 取决于模型供应商 | 适合 | 中 | 后续接文档/研报检索时考虑 |

## 金融多 Agent 项目

| 项目 | GitHub / 官方文档来源 | 适合解决什么问题 | 是否适合第一版 MVP | 可借鉴设计 | 不建议照搬 | API Key | 日线 / 收盘后适配 | 后续扩展价值 | 推荐结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TradingAgents | https://github.com/TauricResearch/TradingAgents | 多 Agent 金融分析角色协作 | 只参考设计 | Bull/Bear/Risk/Researcher 分工 | 不照搬新闻驱动和开放式荐股口径 | 通常需要 LLM / 数据 Key | 可适配 | 高 | 借鉴角色审查，不复制结论风格 |
| AI Hedge Fund | https://github.com/virattt/ai-hedge-fund | 多 Agent 投资分析示例 | 只参考设计 | 多策略分析员、风险经理、组合经理结构 | 名称和定位容易偏向投资决策自动化；v1 不照搬 | 通常需要 LLM / 数据 Key | 可适配 | 中 | 借鉴“委员会”但保留人工决策 |
| FinRobot | https://github.com/AI4Finance-Foundation/FinRobot | 金融 LLM Agent、报表分析、工具生态 | 不作为硬依赖 | 金融任务模块化、报告生成 | 第一版不接复杂外部工具链 | 通常需要 Key | 可适配 | 中 | 后续做财报/研报分析时考虑 |
| StockAgent | GitHub 搜索结果分散，未确认唯一权威仓库 | 股票 Agent 实验 | 不采用 | 仅参考“股票任务拆分”思想 | 未确认维护状态和权威来源，不作为依赖 | 不确定 | 不确定 | 低 | 暂不纳入技术选型 |
| FinMem | 论文/项目资料分散，未确认可直接复用的官方仓库 | 记忆增强交易研究 | 不采用 | 长期记忆、交易复盘记忆概念 | v1 不做黑箱记忆驱动决策 | 不确定 | 可研究 | 中 | 后续做复盘记忆再评估 |

## 量化 / 回测 / 金融数据框架

| 项目 | GitHub / 官方文档来源 | 适合解决什么问题 | 是否适合第一版 MVP | 可借鉴设计 | 不建议照搬 | API Key | 日线 / 收盘后适配 | 后续扩展价值 | 推荐结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qlib | https://github.com/microsoft/qlib | 量化研究、数据管理、模型训练、回测 | 不作为硬依赖 | 数据层、研究流程、回测分层 | v1 较重，不需要训练框架 | 不一定 | 适合 | 高 | 后续重研究阶段考虑 |
| vectorbt | https://github.com/polakowo/vectorbt | 向量化回测和组合分析 | 不作为硬依赖 | 快速参数实验、信号矩阵 | v1 先做单股结构审查 | 不需要 | 适合 | 高 | 后续回测信号有效性 |
| backtrader | https://github.com/mementum/backtrader | 事件驱动回测 | 不作为硬依赖 | 策略和经纪模拟分层 | v1 不做交易执行模拟 | 不需要 | 适合 | 中 | 后续传统回测可选 |
| backtesting.py | https://kernc.github.io/backtesting.py/ / https://github.com/kernc/backtesting.py | 简洁 Python 回测 | 不作为硬依赖 | 低门槛回测接口 | v1 先不做自动策略回测 | 不需要 | 适合 | 高 | 下一步优先接回测之一 |
| OpenBB | https://github.com/OpenBB-finance/OpenBB | 金融数据聚合与终端生态 | 不作为硬依赖 | provider 抽象、数据接口统一 | 依赖面较大 | 部分数据源需要 | 适合 | 中 | 后续多数据源聚合再评估 |
| AKShare | https://github.com/akfamily/akshare / https://akshare.akfamily.xyz/ | 国内公开金融数据 | 可选 provider | A 股日线接口、免 Key 数据源 | 接口细节可能变化，需封装错误 | 通常不需要 | 适合 | 高 | 可作为下一步真实数据源 |
| Tushare | https://tushare.pro/document/2 | A 股金融数据 Pro API | 预留 provider | token 管理、标准化字段 | 需要积分/权限，v1 不强制 | 需要 | 适合 | 高 | 数据质量更稳时接入 |
| Futu OpenAPI | https://openapi.futunn.com/futu-api-doc/en/ | 行情、账户、交易等 OpenAPI | 只预留行情 provider | 历史 K 线能力 | v1 禁止接交易执行能力 | 本地网关/账户 | 适合 | 中 | 仅限行情可考虑 |
| Tiingo | https://www.tiingo.com/documentation/end-of-day | 美股 EOD 数据 | 预留 provider | EOD API | 需要 Key，免费额度限制 | 需要 | 适合 | 中 | 美股日线数据备选 |
| Alpha Vantage | https://www.alphavantage.co/documentation/ | 股票日线 API | 预留 provider | TIME_SERIES_DAILY 标准格式 | 频率限制明显 | 需要 | 适合 | 中 | 快速验证备选 |
| yfinance | https://github.com/ranaroussi/yfinance | Yahoo Finance 历史行情下载 | 预留 provider | 快速美股样例数据 | 非官方数据源稳定性需注意 | 不需要 | 适合 | 中 | 本地研究便捷数据源 |

## 推荐结论

第一版默认采用：

- 本地 Python Orchestrator
- Typed `SubagentResult`
- 结构化决策委员会
- 不强制安装 LangGraph / CrewAI / OpenAI Agents SDK

原因：

1. 当前 MVP 的核心风险在于边界和纪律，而不是复杂 Agent 编排。
2. 日线 / 收盘后流程是固定顺序流水线，本地顺序调用更容易测试和审计。
3. 不强制 LLM 和 Agent SDK，可避免 API Key、网络、费用、追踪系统成为第一版阻塞。
4. `SubagentResult` 已提供稳定结构，后续可把规则型 Subagent 平滑迁移到真实 LLM Subagent。

后续可扩展：

- LangGraph：用于状态化、多步骤、多 Agent 编排。
- OpenAI Agents SDK：用于真实 LLM Subagent、handoff、guardrails、tracing。
- PydanticAI：用于类型安全的 LLM 输出。
- vectorbt / backtesting.py：用于回测。
- Qlib：用于更重的量化研究。
