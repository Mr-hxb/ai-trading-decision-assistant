from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.config_loader import PROJECT_ROOT
from src.orchestrator import Orchestrator, build_provider
from src.publishers.lark_publisher import build_lark_import_payload, write_lark_import_payload
from src.research_context import load_research_contexts
from src.subagents import RUNTIME_SUBAGENT_ORDER, SUBAGENT_RESPONSIBILITIES


def main() -> None:
    parser = argparse.ArgumentParser(description="AI trading decision assistant MVP")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan")
    scan.add_argument("--provider", default="mock")
    scan.add_argument("--symbols", required=True)
    scan.add_argument("--start", required=True)
    scan.add_argument("--end", required=True)
    scan.add_argument("--adjust", choices=["", "qfq", "hfq"], default=None, help="AKShare adjustment mode. Default for akshare is qfq.")
    scan.add_argument("--research-context", default=None, help="Optional JSON file with researched market, company, news, and sentiment context.")

    scan_to_lark = subparsers.add_parser("scan-to-lark")
    scan_to_lark.add_argument("--provider", default="akshare")
    scan_to_lark.add_argument("--symbols", required=True)
    scan_to_lark.add_argument("--start", required=True)
    scan_to_lark.add_argument("--end", required=True)
    scan_to_lark.add_argument("--adjust", choices=["", "qfq", "hfq"], default=None, help="AKShare adjustment mode. Default for akshare is qfq.")
    scan_to_lark.add_argument("--lark-title", default=None, help="Optional Lark doc title, truncated to 27 characters if needed.")
    scan_to_lark.add_argument("--output", default=None, help="Optional output path for the Lark import JSON payload.")
    scan_to_lark.add_argument("--research-context", default=None, help="Optional JSON file with researched market, company, news, and sentiment context.")

    prepare_lark = subparsers.add_parser("prepare-lark")
    prepare_lark.add_argument("--report", required=True)
    prepare_lark.add_argument("--title", default=None)
    prepare_lark.add_argument("--output", default=None)

    subparsers.add_parser("research-frameworks")
    subparsers.add_parser("research-apis")
    subparsers.add_parser("show-subagents")
    subparsers.add_parser("show-implementation-protocol")

    args = parser.parse_args()

    if args.command == "scan":
        provider = build_provider(args.provider, adjust=args.adjust)
        symbols = [symbol.strip() for symbol in args.symbols.split(",") if symbol.strip()]
        result = Orchestrator(provider).run_scan(symbols, args.start, args.end, research_contexts=load_research_contexts(args.research_context))
        print("successful_symbols:", ",".join(result["successful_symbols"]) or "none")
        print("failed_symbols:", result["failed_symbols"])
        print("report_path:", result["report_path"])
        print("human_review_required:", result["human_gate"]["human_review_required"])
        return

    if args.command == "scan-to-lark":
        provider = build_provider(args.provider, adjust=args.adjust)
        symbols = [symbol.strip() for symbol in args.symbols.split(",") if symbol.strip()]
        result = Orchestrator(provider).run_scan(symbols, args.start, args.end, research_contexts=load_research_contexts(args.research_context))
        payload = build_lark_import_payload(Path(result["report_path"]), title=args.lark_title)
        payload_path = write_lark_import_payload(payload, Path(args.output) if args.output else None)
        print("successful_symbols:", ",".join(result["successful_symbols"]) or "none")
        print("failed_symbols:", result["failed_symbols"])
        print("report_path:", result["report_path"])
        print("lark_payload_path:", payload_path)
        print("lark_file_name:", payload.file_name)
        print("human_review_required:", result["human_gate"]["human_review_required"])
        return

    if args.command == "prepare-lark":
        payload = build_lark_import_payload(Path(args.report), title=args.title)
        payload_path = write_lark_import_payload(payload, Path(args.output) if args.output else None)
        print("lark_payload_path:", payload_path)
        print("lark_file_name:", payload.file_name)
        print("payload_preview:", json.dumps({"file_name": payload.file_name, "source_report_path": payload.source_report_path}, ensure_ascii=False))
        return

    if args.command == "research-frameworks":
        print(_doc_summary(PROJECT_ROOT / "docs/framework_research.md"))
        return

    if args.command == "research-apis":
        print(_doc_summary(PROJECT_ROOT / "docs/api_research.md"))
        return

    if args.command == "show-subagents":
        for index, name in enumerate(RUNTIME_SUBAGENT_ORDER, 1):
            print(f"{index}. {name}: {SUBAGENT_RESPONSIBILITIES[name]}")
        return

    if args.command == "show-implementation-protocol":
        print((PROJECT_ROOT / "docs/implementation_subagent_protocol.md").read_text(encoding="utf-8"))
        return


def _doc_summary(path: Path) -> str:
    if not path.exists():
        return f"{path} does not exist yet."
    text = path.read_text(encoding="utf-8")
    marker = "## 推荐结论"
    if marker in text:
        return text[text.index(marker) :].strip()
    return f"See {path}"


if __name__ == "__main__":
    main()
