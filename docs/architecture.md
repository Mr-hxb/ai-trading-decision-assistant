# Architecture

## 定位

本项目是 AI 辅助交易决策系统 MVP。核心目标是把日线数据转成结构化的交易系统审查结果和日报，最终由人工决策。

## 模块边界

- `src/data/`：Provider 抽象与数据标准化。只获取和清洗日线数据，不做策略判断。
- `src/indicators/`：均线、成交量、相对强弱、达瓦斯箱体等指标计算。
- `src/strategy/`：趋势、箱体、风险收益比、评分等规则函数。
- `src/subagents/`：Runtime Decision Subagents，每个角色只做单一职责判断。
- `src/runtime/`：AgentRuntime 抽象。第一版使用 `LocalRuntime` 顺序调用。
- `src/skill/`：交易 Skill Prompt 生成，不直接调用 OpenAI API。
- `src/reports/`：Markdown 报告生成。
- `src/orchestrator.py`：装配配置、Provider、Runtime 和所有 Subagent。
- `src/cli.py`：命令入口。

## Orchestrator

Orchestrator 固定执行 Runtime Decision Subagent 顺序。每个 symbol 单独执行，单个 symbol 失败不会影响其他 symbol。所有步骤都保存 `SubagentResult`，便于调试。

## 安全边界

1. 不接自动下单。
2. 不调用真实交易执行接口。
3. 不把辅助状态升级为交易动作。
4. 所有密钥从 `.env` 读取。
5. 第一版只处理日线 / 收盘后数据。
