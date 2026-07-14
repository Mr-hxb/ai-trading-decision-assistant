# Company Watchlist

Purpose: persistent list of companies to review when running the advisory-only `stock-analysis` Skill.

Use this file as the source list for recurring company reviews. Keep entries factual and lightweight; do not store credentials, account information, position sizes, cost basis, or broker instructions.

## Update Rules

- Add a company only after the user explicitly confirms it should be recorded here.
- Update an existing company only after the user explicitly confirms which factual fields should change.
- Preserve the exact symbol, market, and company name used in the analysis.
- If symbol mapping is ambiguous, record the ambiguity in `Notes` instead of guessing silently.
- Daily reviews must still gather current source-cited evidence and follow `skills/stock-analysis/SKILL.md`.
- Do not record account data, position sizes, cost basis, broker instructions, or trade actions.

## Companies

| Symbol | Market | Company name | Common Chinese name | Status | Added date | Source/context | Notes |
|---|---|---|---|---|---|---|---|
| SMCI | US | Super Micro Computer, Inc. | 超微电脑 | active | 2026-06-01 | Prior user-requested analysis of "超威电脑" | Chinese name was ambiguous; treated as SMCI, with AMD ambiguity noted. |
| AVGO | US | Broadcom Inc. | 博通 | active | 2026-06-01 | Prior all-agent candidate screening finalist | Previously identified as the closest fit in that candidate batch, advisory-only. |
| MSFT | US | Microsoft Corporation | 微软 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| GOOGL | US | Alphabet Inc. | 谷歌母公司 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| META | US | Meta Platforms, Inc. | Meta | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| NFLX | US | Netflix, Inc. | 奈飞 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| AMZN | US | Amazon.com, Inc. | 亚马逊 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| TSM | US ADR | Taiwan Semiconductor Manufacturing Company Limited | 台积电 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| NVDA | US | NVIDIA Corporation | 英伟达 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| AMD | US | Advanced Micro Devices, Inc. | 超威半导体 | active | 2026-06-01 | Prior all-agent candidate screening set and SMCI ambiguity note | Screening candidate only. |
| AAPL | US | Apple Inc. | 苹果 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| 0700.HK | HK | Tencent Holdings Limited | 腾讯控股 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| 9988.HK | HK | Alibaba Group Holding Limited | 阿里巴巴 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| 1810.HK | HK | Xiaomi Corporation | 小米集团 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| 3690.HK | HK | Meituan | 美团 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| 2318.HK | HK | Ping An Insurance (Group) Company of China, Ltd. | 中国平安 | active | 2026-06-01 | Prior all-agent candidate screening set | Screening candidate only. |
| IREN | US | IREN Limited | IREN | active | 2026-06-01 | User-requested analysis of IREN | AI Cloud / Bitcoin mining pivot; high execution and financing risk. |
