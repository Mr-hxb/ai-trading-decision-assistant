import re
from pathlib import Path


def test_no_real_trade_execution_functions_in_src():
    root = Path(__file__).resolve().parents[1] / "src"
    forbidden = re.compile(r"\bdef\s+(execute_order|place_order|submit_order|create_order|cancel_order)\b")
    offenders = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if forbidden.search(text):
            offenders.append(str(path))
    assert offenders == []


def test_no_broker_execution_patterns_in_project_code():
    root = Path(__file__).resolve().parents[1]
    scanned_roots = [root / "src", root / "skills", root / "README.md", root / "AGENTS.md"]
    forbidden_patterns = [
        re.compile(r"\bdef\s+(execute_order|place_order|submit_order|create_order|cancel_order)\b"),
        re.compile(r"\b(buy|sell)\s*\("),
        re.compile(r"\bbroker\.\w*order\b"),
    ]
    offenders = []
    for item in scanned_roots:
        paths = [item] if item.is_file() else list(item.rglob("*"))
        for path in paths:
            if path.suffix not in {".py", ".md", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                if pattern.search(text):
                    offenders.append(f"{path}: {pattern.pattern}")
    assert offenders == []


def test_forbidden_investment_claims_are_only_used_as_prohibitions():
    root = Path(__file__).resolve().parents[1]
    terms = ["必须买入", "必须卖出", "稳赚", "确定上涨"]
    allowed_context = ["不输出", "不要", "Do not", "禁止", "forbidden", "Forbidden"]
    offenders = []
    for path in [*list((root / "src").rglob("*")), *list((root / "skills").rglob("*")), root / "README.md", root / "AGENTS.md"]:
        if path.is_dir() or path.suffix not in {".py", ".md", ".yaml"}:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(term in line for term in terms) and not any(marker in line for marker in allowed_context):
                offenders.append(f"{path}:{line_no}:{line}")
    assert offenders == []
