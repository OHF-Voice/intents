"""Tests for validate.validate_undeclared_files (files no combination points at)."""

import importlib
from typing import Any

import yaml

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
validate: Any = importlib.import_module("script.intentfest.validate")

INTENT_SCHEMAS: dict[str, Any] = {
    "HassTurnOn": {"slot_combinations": {"name_only": {}, "area_domain": {}}},
    "HassStartTimer": {"slot_combinations": {"name_hours": {}}},
}


def _write(top_dir, language, intent, stem, doc=None):
    intent_dir = top_dir / language / intent
    intent_dir.mkdir(parents=True, exist_ok=True)
    (intent_dir / f"{stem}.yaml").write_text(
        yaml.safe_dump(doc or {"language": language}, allow_unicode=True),
        encoding="utf-8",
    )


def _validate(tmp_path, monkeypatch, language="xx"):
    monkeypatch.setattr(validate, "SENTENCE_DIR", tmp_path / "sentences")
    monkeypatch.setattr(validate, "TESTS_DIR", tmp_path / "tests")
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    errors: list[str] = []
    validate.validate_undeclared_files(INTENT_SCHEMAS, language, errors)
    return errors


def test_declared_files_no_errors(tmp_path, monkeypatch):
    """Files named after a declared combination produce no errors."""
    _write(tmp_path / "sentences", "xx", "HassTurnOn", "name_only")
    _write(tmp_path / "sentences", "xx", "HassTurnOn", "area_domain")
    _write(tmp_path / "tests", "xx", "HassTurnOn", "name_only")

    assert not _validate(tmp_path, monkeypatch)


def test_undeclared_sentence_file_errors(tmp_path, monkeypatch):
    """A sentence file no combination points at is reported."""
    _write(tmp_path / "sentences", "xx", "HassTurnOn", "name_only")
    _write(tmp_path / "sentences", "xx", "HassTurnOn", "hours_seconds")

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "sentences/xx/HassTurnOn/hours_seconds.yaml" in errors[0]
    assert "HassTurnOn" in errors[0]


def test_undeclared_test_file_errors(tmp_path, monkeypatch):
    """A test file no combination points at is reported.

    This is the case that was live in the repo: tests/ca/HassStartTimer held six
    ``*_only``-suffixed files whose combinations are named without the suffix, so
    the test harness never generated a case for them and the matching sentence
    files went untested.
    """
    _write(tmp_path / "tests", "xx", "HassStartTimer", "name_hours_only")

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "tests/xx/HassStartTimer/name_hours_only.yaml" in errors[0]


def test_unknown_intent_dir_reported_once(tmp_path, monkeypatch):
    """An intent directory not in intents.yaml is one error, not one per file."""
    _write(tmp_path / "sentences", "xx", "HassNotAnIntent", "name_only")
    _write(tmp_path / "sentences", "xx", "HassNotAnIntent", "area_domain")

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "sentences/xx/HassNotAnIntent/" in errors[0]
    assert "not an intent defined in intents.yaml" in errors[0]


def test_both_trees_are_walked(tmp_path, monkeypatch):
    """An undeclared file in each of sentences/ and tests/ is reported."""
    _write(tmp_path / "sentences", "xx", "HassTurnOn", "bogus")
    _write(tmp_path / "tests", "xx", "HassTurnOn", "bogus")

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 2
    assert any(error.startswith("sentences/") for error in errors)
    assert any(error.startswith("tests/") for error in errors)


def test_top_level_files_are_ignored(tmp_path, monkeypatch):
    """Language-level files such as _common.yaml are not combination files."""
    language_dir = tmp_path / "sentences" / "xx"
    language_dir.mkdir(parents=True, exist_ok=True)
    (language_dir / "_common.yaml").write_text("language: xx\n", encoding="utf-8")

    assert not _validate(tmp_path, monkeypatch)


def test_missing_language_dir_is_noop(tmp_path, monkeypatch):
    """A language with no sentence or test directory produces no errors."""
    assert not _validate(tmp_path, monkeypatch, language="zz")
