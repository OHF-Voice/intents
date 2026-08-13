"""Tests for validate.validate_sentence_references (dangling refs in sentences)."""

import importlib
from typing import Any

import yaml

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
validate: Any = importlib.import_module("script.intentfest.validate")

LISTS = {"name", "area", "floor", "brightness"}
RULES = {"turn", "the"}


def _write_sentences(sentence_dir, language, intent, combo, data):
    combo_dir = sentence_dir / language / intent
    combo_dir.mkdir(parents=True, exist_ok=True)
    (combo_dir / f"{combo}.yaml").write_text(
        yaml.safe_dump({"language": language, "data": data}, allow_unicode=True),
        encoding="utf-8",
    )


def _validate(tmp_path, monkeypatch, language="xx", lists=None, rules=None):
    monkeypatch.setattr(validate, "SENTENCE_DIR", tmp_path)
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    errors: list[str] = []
    validate.validate_sentence_references(
        language,
        validate.load_language_sentences(language),
        available_list_names=set(LISTS if lists is None else lists),
        available_rule_names=set(RULES if rules is None else rules),
        errors=errors,
    )
    return errors


def test_clean_sentences_no_errors(tmp_path, monkeypatch):
    """Sentences whose refs all resolve produce no errors."""
    _write_sentences(
        tmp_path,
        "xx",
        "HassTurnOn",
        "name_only",
        [{"sentences": ["<turn> on [<the>] {name}"], "response": "default"}],
    )

    assert not _validate(tmp_path, monkeypatch)


def test_dangling_rule_reference_errors(tmp_path, monkeypatch):
    """A <rule> not defined for the language is reported as an error."""
    _write_sentences(
        tmp_path,
        "xx",
        "HassTurnOn",
        "name_only",
        [{"sentences": ["<swithc> on {name}"], "response": "default"}],
    )

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "<swithc>" in errors[0]
    assert "name_only.yaml" in errors[0]


def test_dangling_list_reference_errors(tmp_path, monkeypatch):
    """A {list} not available for the language is reported as an error."""
    _write_sentences(
        tmp_path,
        "xx",
        "HassLightSet",
        "name_brightness",
        [
            {
                "sentences": ["<turn> {name} to {brightnes:brightness}"],
                "response": "default",
            }
        ],
    )

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "{brightnes}" in errors[0]


def test_orphan_combo_file_is_checked(tmp_path, monkeypatch):
    """A file whose name is not a declared slot combination is still checked.

    This is the gap the check exists to close: validate_slot_combinations only
    opens files named after a combination in intents.yaml, so a copied file with
    a name belonging to another intent was never validated at all.
    """
    _write_sentences(
        tmp_path,
        "xx",
        "HassIncreaseTimer",
        "not_a_declared_combination",
        [{"sentences": ["<timer_inccrease> {name}"], "response": "default"}],
    )

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "<timer_inccrease>" in errors[0]


def test_block_local_expansion_rules_do_not_resolve(tmp_path, monkeypatch):
    """A rule defined in the data block itself is still reported as dangling.

    The slot-combination format has no per-block expansion_rules: the schema
    rejects the key, and the conversion to hassil format keeps only sentences /
    slots / metadata / requires_context / response, so such a rule would be
    dropped before the sentence ever runs. Treating it as defined would hide a
    reference that cannot resolve at runtime.
    """
    _write_sentences(
        tmp_path,
        "xx",
        "HassTurnOn",
        "name_only",
        [
            {
                "expansion_rules": {"local": "(please|kindly)"},
                "sentences": ["<local> <turn> on {name}"],
                "response": "default",
            }
        ],
    )

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 1
    assert "<local>" in errors[0]


def test_unicode_reference_names_resolve(tmp_path, monkeypatch):
    """Accented rule/list names resolve (no false positives)."""
    _write_sentences(
        tmp_path,
        "es",
        "HassTurnOn",
        "name_only",
        [{"sentences": ["<añadir> {habitación}"], "response": "default"}],
    )

    errors = _validate(
        tmp_path,
        monkeypatch,
        language="es",
        lists={"habitación"},
        rules={"añadir"},
    )

    assert not errors


def test_refs_inside_alternatives_and_optionals(tmp_path, monkeypatch):
    """Refs nested in (a|b) and [c] are reached by the parser walk."""
    _write_sentences(
        tmp_path,
        "xx",
        "HassTurnOn",
        "name_only",
        [
            {
                "sentences": ["(<turn>|<swithc>) on [{arae}] {name}"],
                "response": "default",
            }
        ],
    )

    errors = _validate(tmp_path, monkeypatch)

    assert len(errors) == 2
    assert any("<swithc>" in error for error in errors)
    assert any("{arae}" in error for error in errors)


def test_unparseable_sentence_is_skipped(tmp_path, monkeypatch):
    """A sentence the parser rejects is left to the sentence schema to report."""
    _write_sentences(
        tmp_path,
        "xx",
        "HassTurnOn",
        "name_only",
        [{"sentences": ["<turn> on {name"], "response": "default"}],
    )

    assert not _validate(tmp_path, monkeypatch)


def test_missing_language_dir_is_noop(tmp_path, monkeypatch):
    """A language with no sentence directory produces no errors."""
    assert not _validate(tmp_path, monkeypatch, language="zz")
