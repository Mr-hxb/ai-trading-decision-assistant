from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


MAX_LARK_FILE_NAME_CHARS = 27


@dataclass
class LarkImportPayload:
    file_name: str
    markdown: str
    source_report_path: str
    created_at: str
    publish_instruction: str


def build_lark_import_payload(report_path: Path, title: str | None = None) -> LarkImportPayload:
    report_path = report_path.expanduser().resolve()
    if not report_path.exists():
        raise FileNotFoundError(f"Report does not exist: {report_path}")
    markdown = report_path.read_text(encoding="utf-8")
    file_name = normalize_lark_file_name(title or default_title_from_report(report_path, markdown))
    return LarkImportPayload(
        file_name=file_name,
        markdown=markdown,
        source_report_path=str(report_path),
        created_at=datetime.now().isoformat(timespec="seconds"),
        publish_instruction=(
            "Import this payload with your document publishing integration using file_name and markdown."
        ),
    )


def write_lark_import_payload(payload: LarkImportPayload, output_path: Path | None = None) -> Path:
    if output_path is None:
        report_path = Path(payload.source_report_path)
        output_dir = report_path.parents[1] / "lark_import"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{report_path.stem}.lark_import.json"
    else:
        output_path = output_path.expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def default_title_from_report(report_path: Path, markdown: str) -> str:
    date_match = re.search(r"日期：\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", markdown)
    date_part = date_match.group(1).replace("-", "") if date_match else report_path.stem[:8]
    symbol_match = re.search(r"\|\s*([0-9A-Z.]+)\s*\|\s*[-0-9.]+\s*\|", markdown)
    if symbol_match:
        return f"{symbol_match.group(1)}日报{date_part}"
    return f"交易系统日报{date_part}"


def normalize_lark_file_name(title: str) -> str:
    cleaned = re.sub(r"[\r\n\t/\\:*?\"<>|]+", "", title).strip()
    if not cleaned:
        cleaned = "交易系统日报"
    if len(cleaned) <= MAX_LARK_FILE_NAME_CHARS:
        return cleaned
    return cleaned[:MAX_LARK_FILE_NAME_CHARS]
