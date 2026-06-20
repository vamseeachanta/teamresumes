"""Targeted tests for deterministic code-review fixes (review 2026-05-23).

All fixtures are synthetic. These tests exercise the behavioral bug fixes:
  - modules/reporting/utils/path_utils.py : missing ``import os`` (NameError)
  - execute-tasks.py : parse_tasks subtask regex matched stripped line
  - .common/parallel_utils.py : USE_PARALLEL now read from environment
"""

import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_module(name: str, relpath: str):
    """Load a module from a file path (handles hyphenated filenames)."""
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# path_utils.relative_path_from_report -- the fallback branch used os.path
# without importing os, raising NameError. Force the fallback with two
# absolute paths that share no common parent prefix.
# ---------------------------------------------------------------------------
def test_relative_path_fallback_does_not_raise_nameerror():
    path_utils = _load_module(
        "path_utils_under_test",
        "modules/reporting/utils/path_utils.py",
    )
    # Two absolute paths sharing a common root ('/') but where data is not
    # under report.parent -> relative_to raises ValueError -> fallback runs.
    result = path_utils.relative_path_from_report(
        "/synthetic/data/processed/data.csv",
        "/synthetic/reports/analysis.html",
    )
    assert isinstance(result, str)
    assert "data.csv" in result
    assert ".." in result  # walked up from report dir to common root


# ---------------------------------------------------------------------------
# execute-tasks.parse_tasks -- subtask regex now matches indented raw lines.
# ---------------------------------------------------------------------------
def test_parse_tasks_collects_indented_subtasks(tmp_path):
    execute_tasks = _load_module("execute_tasks_under_test", "execute-tasks.py")

    tasks_md = tmp_path / "tasks.md"
    tasks_md.write_text(
        "- [x] 1. First main task\n"
        "  - [x] Subtask one\n"
        "  - [ ] Subtask two\n"
        "- [ ] 2. Second main task\n"
        "  - [ ] Subtask three\n",
        encoding="utf-8",
    )

    tasks = execute_tasks.parse_tasks(str(tasks_md))

    assert len(tasks) == 2
    assert len(tasks[0]["subtasks"]) == 2
    assert tasks[0]["subtasks"][0]["completed"] is True
    assert tasks[0]["subtasks"][1]["completed"] is False
    assert len(tasks[1]["subtasks"]) == 1
    assert tasks[1]["subtasks"][0]["description"] == "Subtask three"


# ---------------------------------------------------------------------------
# parallel_utils.USE_PARALLEL -- now derived from the environment.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("value", ["1", "yes", "true"])
def test_use_parallel_enabled_values_import_and_set_true(monkeypatch, value):
    monkeypatch.setenv("USE_PARALLEL", value)
    sys.modules.pop("parallel_utils_under_test", None)
    mod = _load_module(
        "parallel_utils_under_test", ".common/parallel_utils.py"
    )
    assert mod.USE_PARALLEL is True


def test_use_parallel_defaults_true_when_unset(monkeypatch):
    monkeypatch.delenv("USE_PARALLEL", raising=False)
    sys.modules.pop("parallel_utils_under_test", None)
    mod = _load_module(
        "parallel_utils_under_test", ".common/parallel_utils.py"
    )
    assert mod.USE_PARALLEL is True


@pytest.mark.parametrize("value", ["0", "false", "no", "off"])
def test_use_parallel_falsy_values_block_import(monkeypatch, value):
    # With parallelism disabled the module enforces its "mandatory" contract by
    # raising ImportError at import time. This path was previously unreachable
    # because USE_PARALLEL was a hardcoded True constant.
    monkeypatch.setenv("USE_PARALLEL", value)
    sys.modules.pop("parallel_utils_under_test", None)
    with pytest.raises(ImportError):
        _load_module("parallel_utils_under_test", ".common/parallel_utils.py")


# ---------------------------------------------------------------------------
# DataValidator.generate_interactive_report -- partial results dict should no
# longer raise a bare KeyError (missing keys default to safe values).
# Skipped if plotly/pandas are unavailable in the environment.
# ---------------------------------------------------------------------------
def test_interactive_report_tolerates_partial_results(tmp_path):
    pytest.importorskip("plotly")
    pytest.importorskip("pandas")
    src_dir = REPO_ROOT / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    from validators.data_validator import DataValidator

    validator = DataValidator()
    # Intentionally partial dict: omit total_rows/total_columns/issues/valid.
    partial = {"quality_score": 73.0}
    out = tmp_path / "report.html"
    # Must not raise KeyError on the missing summary keys.
    validator.generate_interactive_report(partial, out)
    assert out.exists()
