from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_daily_report(
    project_root: Path,
    report_date: str,
    analysis_results: list[dict[str, Any]],
    failed_symbols: list[dict[str, str]],
    subagent_order: list[str],
) -> Path:
    output_dir = project_root / "reports/daily"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report_date}_daily_report.md"
    prompt_text = "\n\n---\n\n".join(item.get("trading_skill_prompt", "") for item in analysis_results)

    lines: list[str] = [
        "# 每日交易系统筛选报告",
        "",
        f"日期：{report_date}",
        "",
        "## 1. 今日市场环境",
        "",
    ]
    if analysis_results:
        for item in analysis_results:
            market = item.get("market_regime", {})
            lines.append(f"- {item['symbol']}：{market.get('summary') or '未提供市场环境研究上下文。'}")
            if market.get("proxies"):
                lines.append(f"  - 默认基准：{', '.join(market.get('proxies', []))}")
    else:
        lines.append("暂无成功候选，无法生成市场环境摘要。")

    lines += [
        "",
        "## 2. 今日候选股总览",
        "",
        "| symbol | data_date | score | decision_status | confidence_level | close | box_high | box_low | volume_ratio | breakout_signal | chase_risk | stop_loss | rr_ratio |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: |",
    ]
    for item in analysis_results:
        latest = item["bars"].iloc[-1].to_dict()
        darvas = item["pattern_result"]["darvas_box"]
        decision = item["decision_result"]
        risk = item["risk_result"]
        score = item["score_result"]["score"]
        lines.append(
            f"| {item['symbol']} | {_fmt_date(latest.get('date'))} | {score} | {decision['decision_status']} | {decision['confidence_level']} | "
            f"{_fmt(latest.get('close'))} | {_fmt(darvas.get('box_high'))} | {_fmt(darvas.get('box_low'))} | "
            f"{_fmt(latest.get('volume_ratio'))} | {darvas.get('breakout_signal')} | {darvas.get('chase_risk')} | "
            f"{_fmt(risk.get('stop_loss'))} | {_fmt(risk.get('rr_ratio'))} |"
        )

    lines += [
        "",
        "## 3. Runtime Decision Subagent 摘要",
        "",
    ]
    for name in subagent_order:
        lines.append(f"- {name}")

    lines += [
        "",
        "## 4. 重点观察",
        "",
    ]
    watchlist = [item for item in sorted(analysis_results, key=lambda x: x["score_result"]["score"], reverse=True) if item["decision_result"]["decision_status"] != "放弃"][:5]
    if watchlist:
        for item in watchlist:
            lines.append(f"- {item['symbol']}：状态 {item['decision_result']['decision_status']}，评分 {item['score_result']['score']}")
    else:
        lines.append("- 暂无")

    lines += [
        "",
        "## 5. 放弃或警惕",
        "",
    ]
    for item in analysis_results:
        risk_flags = item["risk_result"].get("risk_flags", [])
        discipline_flags = item["discipline_result"].get("discipline_flags", [])
        negatives = item["decision_result"].get("key_negative_factors", [])
        if risk_flags or discipline_flags or negatives:
            lines.append(f"- {item['symbol']}：{'；'.join(risk_flags + discipline_flags + negatives)}")
    for failed in failed_symbols:
        lines.append(f"- {failed['symbol']}：数据或流程失败，原因：{failed['reason']}")
    if len(lines) > 0 and lines[-1] == "## 5. 放弃或警惕":
        lines.append("- 暂无")

    lines += [
        "",
        "## 6. 三流派审查",
        "",
    ]
    for item in analysis_results:
        lines += [f"### {item['symbol']}", ""]
        doctrine_reviews = item.get("doctrine_reviews", {})
        if not doctrine_reviews:
            lines.append("- 暂无三流派审查结果。")
            lines.append("")
            continue
        for review in doctrine_reviews.values():
            lines += [
                f"#### {review.get('name')}",
                "",
                f"- Verdict：{review.get('verdict')}，Score：{_fmt(review.get('score'))}",
                f"- 选股审查：{review.get('selection_view')}",
                f"- 行情审查：{review.get('market_view')}",
                f"- 舆论审查：{review.get('sentiment_view')}",
                f"- 依据：{'; '.join(review.get('evidence', [])) or '暂无'}",
                f"- 限制项：{'; '.join(review.get('blockers', [])) or '暂无'}",
                f"- 触发条件：{'; '.join(review.get('trigger_conditions', [])) or '暂无'}",
                f"- 失效条件：{'; '.join(review.get('invalid_conditions', [])) or '暂无'}",
                f"- 风险备注：{'; '.join(review.get('risk_notes', [])) or '暂无'}",
                "",
            ]

    lines += [
        "## 7. Bull / Bear / Risk / Discipline 汇总",
        "",
    ]
    for item in analysis_results:
        decision = item["decision_result"]
        lines += [
            f"### {item['symbol']}",
            "",
            f"- Bull Case：{'; '.join(item.get('bullish_evidence', [])) or '暂无'}",
            f"- Bear Case：{'; '.join(item.get('bearish_evidence', [])) or '暂无'}",
            f"- Risk Flags：{'; '.join(decision.get('risk_flags', [])) or '暂无'}",
            f"- Discipline Flags：{'; '.join(decision.get('discipline_flags', [])) or '暂无'}",
            f"- 为什么不是更高等级：{decision.get('why_not_higher_status')}",
            f"- 判断失效条件：{'; '.join(decision.get('invalid_conditions', []))}",
            "",
        ]

    lines += [
        "## 8. AI Skill 分析 Prompt",
        "",
        "```text",
        prompt_text,
        "```",
        "",
        "## 9. 风险声明",
        "",
        "本报告仅用于个人交易系统复盘和辅助决策，不构成投资建议，不代表任何确定性收益判断，也不自动触发交易。最终交易决策必须由使用者自行判断。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _fmt(value) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def _fmt_date(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "date"):
        return str(value.date())
    return str(value)[:10]
