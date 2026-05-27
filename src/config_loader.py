from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = PROJECT_ROOT / file_path
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_project_env() -> None:
    load_dotenv(PROJECT_ROOT / ".env")


def load_strategy_config() -> dict[str, Any]:
    config = load_yaml("config/strategy_rules.yaml")
    strategy_styles = load_yaml("config/strategy_styles.yaml")
    if strategy_styles:
        config["strategy_styles"] = strategy_styles
    return config


def load_runtime_config() -> dict[str, Any]:
    return load_yaml("config/agent_runtime.yaml")


def load_data_source_config() -> dict[str, Any]:
    return load_yaml("config/data_sources.yaml")
