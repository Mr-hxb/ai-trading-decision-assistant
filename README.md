# AI Trading Decision Assistant MVP

本项目是一个本地 Python MVP，用于把日线数据经过规则筛选、技术结构识别、风险收益比判断、多 Subagent 审查、AI Skill Prompt 生成和 Markdown 报告输出，最终交给人工做交易决策。

它不是自动交易系统，不接真实交易执行接口，不直接给出交易指令，也不输出确定性收益判断。

## Core Flow

```text
Daily bars
-> rule filtering
-> technical structure detection
-> risk/reward review
-> runtime decision subagents
-> AI Skill prompt generation
-> daily report
-> human approval
```

## Install

```bash
cd ai-trading-decision-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Mock Demo

```bash
python -m src.cli scan --provider mock --symbols AAPL,TSLA,NVDA --start 2024-01-01 --end 2026-05-25
```

## Run AKShare Data Scan

AKShare is optional because the mock demo and tests should work without external data packages.

```bash
source .venv/bin/activate
pip install -r requirements-akshare.txt
python -m src.cli scan --provider akshare --symbols 600519.SH,000001.SZ --start 2024-01-01 --end 2026-05-25 --adjust qfq
```

Supported AKShare routes in v1:

- A-share daily bars: `600519.SH`, `000001.SZ`, or raw 6-digit codes. The provider first tries `stock_zh_a_hist` and falls back to `stock_zh_a_daily` when that route is blocked.
- HK daily bars: `00700.HK` or raw 5-digit HK codes.
- US daily bars: AKShare Eastmoney US codes from `stock_us_spot_em`, such as `106.TTE`.

## Run EODHD Data Scan

EODHD is an optional paid/free-trial HTTP data source for HK and US daily bars. Put the key in `.env`:

```bash
EODHD_API_KEY=your_key_here
python -m src.cli scan --provider eodhd --symbols 09868.HK --start 2025-01-01 --end 2026-05-27
```

Supported EODHD routes in v1:

- HK daily bars: `09868.HK`. If EODHD rejects the leading-zero form, the provider retries `9868.HK`.
- US daily bars: `AAPL.US`.
- A-share symbols remain on `--provider akshare`; EODHD is not used for A-share routing in v1.

Reports are written to:

```text
reports/daily/YYYY-MM-DD_daily_report.md
```

## Run With Research Context

For single-stock deep review, prepare source-grounded context from official announcements, company events, mainstream news, and market background, then pass that context into the local scan. The local rules still own K-line, risk, and committee decisions; the research JSON only supplies context for market and sentiment review.

Example `research_context.json`:

```json
{
  "symbol": "AAPL.US",
  "sentiment_summary": "主流新闻整体偏中性，市场关注新品周期和盈利指引。",
  "market_context": {
    "market": "us",
    "proxies": ["SPY", "QQQ"],
    "sector_proxy": "XLK",
    "risk_appetite": "neutral",
    "trend": "mixed",
    "summary": "纳指处于高位震荡，科技板块风险偏好中性。"
  },
  "news_items": [
    {
      "title": "Example mainstream news title",
      "source": "Mainstream source",
      "url": "https://example.com/news",
      "sentiment": "neutral"
    }
  ],
  "company_events": [
    {
      "title": "Example company event",
      "source": "Official source",
      "url": "https://example.com/filing"
    }
  ]
}
```

Run with the context file:

```bash
python -m src.cli scan --provider eodhd --symbols AAPL.US --start 2025-01-01 --end 2026-05-27 --research-context research_context.json
python -m src.cli scan-to-lark --provider eodhd --symbols AAPL.US --start 2025-01-01 --end 2026-05-27 --research-context research_context.json --lark-title AAPL日报20260527
```

The report adds market regime review plus three doctrine reviews:

- `Darvas Box`: trend strength, box structure, breakout confirmation, and chase risk.
- `Sperandeo Principles`: trend definition, risk reference, and risk/reward quality.
- `Livermore Tape Reading`: price behavior, key levels, volume confirmation, and market tone.

## Prepare a Document Import Package

The project does not store document-platform tokens. It prepares a JSON package containing a safe file name and Markdown body for a separate document publishing workflow.

```bash
python -m src.cli scan-to-lark --provider akshare --symbols 002475.SZ --start 2024-01-01 --end 2026-05-25 --adjust qfq --lark-title 立讯精密日报20260525
```

The command prints the generated payload path. Use the JSON fields `file_name` and `markdown` with your own document publishing integration.

## Useful Commands

```bash
python -m src.cli show-implementation-protocol
python -m src.cli show-subagents
python -m src.cli research-frameworks
python -m src.cli research-apis
python -m src.cli prepare-lark --report reports/daily/YYYY-MM-DD_daily_report.md --title 股票日报YYYYMMDD
pytest
```

## Safety Boundaries

- Only daily / after-close data is handled in v1.
- All API keys must be loaded from `.env`.
- Provider modules standardize data only; they do not make strategy decisions.
- The orchestrator does not connect to broker execution APIs.
- `DecisionCommitteeSubagent` only emits auxiliary statuses: `可关注`, `等待`, `观察`, `放弃`.
- Human review is always required.

## First Version Architecture

The MVP uses:

- Local Python orchestrator
- Typed `SubagentResult`
- Structured decision committee
- Mock provider as the default runnable provider

The project intentionally does not require LangGraph, CrewAI, or OpenAI Agents SDK for v1. Those are documented as future extension points in `src/runtime/`.
