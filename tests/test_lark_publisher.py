import json
import subprocess
import sys

from src.publishers.lark_publisher import build_lark_import_payload, normalize_lark_file_name, write_lark_import_payload


REPORT_MARKDOWN = """# 每日交易系统筛选报告

日期：2026-05-25

| symbol | score | decision_status |
| --- | ---: | --- |
| 002475.SZ | 34.0 | 放弃 |

## 风险声明

本报告仅用于个人交易系统复盘和辅助决策，不构成投资建议。
"""


def test_build_lark_import_payload_from_report(tmp_path):
    report = tmp_path / "2026-05-25_daily_report.md"
    report.write_text(REPORT_MARKDOWN, encoding="utf-8")
    payload = build_lark_import_payload(report)
    assert payload.file_name == "002475.SZ日报20260525"
    assert payload.markdown == REPORT_MARKDOWN
    assert payload.source_report_path == str(report.resolve())


def test_lark_file_name_is_safely_truncated():
    title = "立讯精密股份有限公司每日交易系统筛选报告20260525超长标题"
    normalized = normalize_lark_file_name(title)
    assert len(normalized) == 27
    assert "/" not in normalized


def test_write_lark_import_payload(tmp_path):
    report = tmp_path / "2026-05-25_daily_report.md"
    report.write_text(REPORT_MARKDOWN, encoding="utf-8")
    payload = build_lark_import_payload(report, title="立讯精密日报20260525")
    output = write_lark_import_payload(payload, tmp_path / "payload.json")
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["file_name"] == "立讯精密日报20260525"
    assert saved["markdown"] == REPORT_MARKDOWN


def test_prepare_lark_cli(tmp_path):
    report = tmp_path / "report.md"
    output = tmp_path / "payload.json"
    report.write_text(REPORT_MARKDOWN, encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli",
            "prepare-lark",
            "--report",
            str(report),
            "--title",
            "立讯精密日报20260525",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "lark_payload_path:" in result.stdout
    assert output.exists()


def test_scan_to_lark_cli_mock_flow(tmp_path):
    output = tmp_path / "scan_payload.json"
    research_context = tmp_path / "research.json"
    research_context.write_text(
        json.dumps(
            {
                "symbol": "AAPL",
                "market_context": {"market": "us", "summary": "Market backdrop is supportive.", "risk_appetite": "positive"},
                "sentiment_summary": "Mainstream coverage is constructive.",
                "news_items": [{"title": "news", "sentiment": "positive"}],
            }
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli",
            "scan-to-lark",
            "--provider",
            "mock",
            "--symbols",
            "AAPL,TSLA,NVDA",
            "--start",
            "2024-01-01",
            "--end",
            "2026-05-25",
            "--lark-title",
            "Mock行情日报20260525",
            "--output",
            str(output),
            "--research-context",
            str(research_context),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "successful_symbols: AAPL,TSLA,NVDA" in result.stdout
    assert "human_review_required: True" in result.stdout
    assert output.exists()
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["file_name"] == "Mock行情日报20260525"
    assert "每日交易系统筛选报告" in payload["markdown"]
    assert "三流派审查" in payload["markdown"]
    assert "token" not in payload
    assert "api_key" not in json.dumps(payload, ensure_ascii=False).lower()
