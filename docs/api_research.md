# API Research

第一版只处理日线 / 收盘后数据。所有 API Key 必须通过 `.env` 读取，Provider 只负责拿数据和标准化字段，不做策略分析。

| 数据源 | 官方来源 | 适合问题 | 第一版状态 | API Key | 日线适配 | 风险与 TODO | 推荐结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MockProvider | 本项目本地样例 | 本地开发、测试、完整流程演示 | 已实现 | 不需要 | 适合 | 样例数据不代表真实市场 | 默认启用 |
| AKShare | https://github.com/akfamily/akshare / https://akshare.akfamily.xyz/ | A 股、港股、美股历史日线数据 | 已实现 provider | 通常不需要 | 适合 | A 股 `成交量` 来源单位为手，provider 已转换为股；美股需使用 AKShare `stock_us_spot_em` 返回的东方财富代码 | 下一步优先真实数据源 |
| EODHD | https://eodhd.com/ | 港股、美股和全球 EOD 日线 | 已实现 provider | 需要 `EODHD_API_KEY` | 适合 | 免费套餐和付费套餐权限不同；A 股 v1 不走此 provider | 港股/美股稳定数据源优先接入 |
| Tushare | https://tushare.pro/document/2 | A 股 Pro 数据、财务和行情 | TODO | 需要 `TUSHARE_TOKEN` | 适合 | 权限、积分、复权口径需确认 | 数据质量更稳，但需要账号 |
| Futu OpenAPI | https://openapi.futunn.com/futu-api-doc/en/ | 港美 A 行情、账户生态 | TODO，仅限行情 | 需要网关/账户 | 适合 | 不能在 MVP 接交易执行能力 | 只可作为行情源扩展 |
| Longbridge OpenAPI | https://open.longportapp.com/en/docs | 港美股行情和账户生态 | TODO，仅限行情 | 需要 Key / Token | 适合 | 认证和限频需验证；不接执行能力 | 只可作为行情源扩展 |
| Alpha Vantage | https://www.alphavantage.co/documentation/ | 美股日线 API | TODO | 需要 `ALPHA_VANTAGE_API_KEY` | 适合 | 免费限频较严 | 快速验证备选 |
| Tiingo | https://www.tiingo.com/documentation/end-of-day | 美股 EOD 数据 | TODO | 需要 `TIINGO_API_KEY` | 适合 | 额度和字段映射需验证 | 美股日线备选 |
| Polygon | https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to | 美股聚合 K 线 | TODO | 需要 `POLYGON_API_KEY` | 适合 | 付费层级和限频需确认 | 生产级美股数据备选 |
| yfinance | https://github.com/ranaroussi/yfinance | Yahoo Finance 历史行情 | TODO | 不需要 | 适合 | 非官方源，稳定性和调整口径需注意 | 本地研究可用 |

## 标准字段

所有 Provider 必须返回：

- `date`
- `symbol`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `amount`，没有则允许为空
- `source`

## 推荐结论

第一版默认使用 `mock`，用于保证 CLI、Subagent、报告和测试不依赖外部网络。

真实数据源已支持 `AKShare` 和 `EODHD`：

1. A 股继续优先使用 `AKShare`。
2. 港股和美股可以使用 `EODHD`，通过 `.env` 中的 `EODHD_API_KEY` 启用。
3. `EODHD` 港股会先尝试 `09868.HK`，必要时 fallback 到 `9868.HK`。

如果后续要求更稳定的 A 股数据，再接 `Tushare`。如果优先美股，则先接 `yfinance` 做低成本验证，再评估 `Tiingo` 或 `Polygon`。
