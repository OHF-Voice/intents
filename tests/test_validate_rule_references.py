"""Tests for validate.validate_rule_references (dangling rule/list refs)."""

import importlib
from typing import Any

import yaml

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
validate: Any = importlib.import_module("script.intentfest.validate")


def _write_rules(rules_dir, language, rules):
    lang_dir = rules_dir / language
    lang_dir.mkdir(parents=True, exist_ok=True)
    (lang_dir / "common.yaml").write_text(
        yaml.safe_dump({"language": language, "expansion_rules": rules}),
        encoding="utf-8",
    )


def test_clean_rules_no_errors(tmp_path, monkeypatch):
    """A rule body whose refs all resolve produces no errors."""
    monkeypatch.setattr(validate, "RULE_DIR", tmp_path)
    _write_rules(
        tmp_path,
        "xx",
        {
            "turn": "(turn|switch)",
            "act": "<turn> [<the>] {name}",
            "the": "[the]",
        },
    )

    errors: list[str] = []
    validate.validate_rule_references(
        "xx",
        available_list_names={"name", "area", "floor"},
        errors=errors,
    )

    assert not errors


def test_dangling_rule_reference_errors(tmp_path, monkeypatch):
    """A <ref> not defined in rules/<lang>/ is reported as an error."""
    monkeypatch.setattr(validate, "RULE_DIR", tmp_path)
    _write_rules(tmp_path, "xx", {"act": "<turn> the light"})

    errors: list[str] = []
    validate.validate_rule_references(
        "xx",
        available_list_names={"name", "area", "floor"},
        errors=errors,
    )

    assert len(errors) == 1
    assert "<act>" in errors[0]
    assert "<turn>" in errors[0]


def test_dangling_list_reference_errors(tmp_path, monkeypatch):
    """A {list} not in available lists is reported as an error."""
    monkeypatch.setattr(validate, "RULE_DIR", tmp_path)
    _write_rules(tmp_path, "xx", {"act": "set to {missing_list}"})

    errors: list[str] = []
    validate.validate_rule_references(
        "xx",
        available_list_names={"name", "area", "floor"},
        errors=errors,
    )

    assert len(errors) == 1
    assert "<act>" in errors[0]
    assert "{missing_list}" in errors[0]


def test_unicode_reference_names_resolve(tmp_path, monkeypatch):
    """Accented rule/list names are captured and resolve (no false positives)."""
    monkeypatch.setattr(validate, "RULE_DIR", tmp_path)
    _write_rules(
        tmp_path,
        "es",
        {
            "añadir": "pon <continúa> {habitación}",
            "continúa": "[continúa]",
        },
    )

    errors: list[str] = []
    validate.validate_rule_references(
        "es",
        available_list_names={"habitación", "name"},
        errors=errors,
    )

    assert not errors


def test_slot_form_list_reference(tmp_path, monkeypatch):
    """A {list:slot} reference resolves on the list name part."""
    monkeypatch.setattr(validate, "RULE_DIR", tmp_path)
    _write_rules(tmp_path, "xx", {"act": "to {brightness:level}"})

    errors: list[str] = []
    validate.validate_rule_references(
        "xx",
        available_list_names={"brightness"},
        errors=errors,
    )

    assert not errors
