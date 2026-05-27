from __future__ import annotations

from typing import Any


def build_trading_skill_prompt(context: dict[str, Any]) -> str:
    symbol = context["symbol"]
    latest = context["bars"].iloc[-1].to_dict()
    darvas = context["pattern_result"]["darvas_box"]
    risk = context["risk_result"]
    decision = context["decision_result"]
    bull = context.get("bullish_evidence", [])
    bear = context.get("bearish_evidence", [])
    market = context.get("market_regime", {})
    doctrine_reviews = context.get("doctrine_reviews", {})
    research_context = context.get("research_context", {})
    return f"""你是我的交易系统质检员，不是荐股老师，不直接给买卖指令。

请只分析下面股票是否符合我的交易系统，不预测未来一定上涨，不使用夸张或确定性语言，不鼓励重仓、梭哈、赌消息。

股票：{symbol}
当前状态：{decision["decision_status"]}

系统匹配度：
- 趋势：{context["trend_result"]}
- 达瓦斯箱体：box_high={darvas.get("box_high")}, box_low={darvas.get("box_low")}, breakout_signal={darvas.get("breakout_signal")}
- 成交量：volume_ratio={latest.get("volume_ratio")}
- 买点距离：{darvas.get("distance_from_box_high")}
- 风险收益比：{risk.get("rr_ratio")}
- 市场环境：{market}

三流派审查：
{_format_doctrine_reviews(doctrine_reviews)}

符合的规则：
{_numbered(bull)}

不符合或需要警惕：
{_numbered(bear + risk.get("risk_flags", []) + decision.get("discipline_flags", []))}

Bull Case：
- 支持进入观察池的证据：{bull}

Bear Case：
- 反对理由和风险：{bear}

可能买点：
- 突破买点：围绕有效箱体上沿做复核
- 回踩买点：回踩后不破关键结构再复核
- 右侧确认买点：趋势和成交量继续满足系统后再复核

失效条件：
- 跌回箱体
- 跌破突破 K 线低点
- 跌破关键均线
- 成交量放大但价格无法继续走强

止损参考：
- 价格：{risk.get("stop_loss")}
- 原因：{risk.get("stop_loss_reason")}

FOMO 检查：
- 是否已经远离买点：{darvas.get("chase_risk")}
- 是否连续大涨：请结合最近 K 线复核
- 是否只是消息刺激：{_research_context_status(research_context)}
- 是否无法设置清晰止损：{risk.get("stop_loss") is None}

最终结论：
- 只输出辅助判断
- 不输出“必须买入”
- 不输出“必须卖出”
- 不输出确定性收益预测
- 本内容不构成投资建议，最终交易决策必须由使用者自行判断
"""


def _numbered(items: list[str]) -> str:
    if not items:
        return "1. 暂无"
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def _format_doctrine_reviews(doctrine_reviews: dict) -> str:
    if not doctrine_reviews:
        return "- 暂无"
    lines: list[str] = []
    for review in doctrine_reviews.values():
        lines.append(
            f"- {review.get('name')}: verdict={review.get('verdict')}, score={review.get('score')}, "
            f"evidence={review.get('evidence', [])}, blockers={review.get('blockers', [])}"
        )
    return "\n".join(lines)


def _research_context_status(research_context: dict) -> str:
    if not research_context:
        return "未提供官方公告或主流新闻上下文，不允许编造消息"
    return research_context.get("sentiment_summary") or "已提供官方公告或主流新闻上下文，需引用来源复核"
