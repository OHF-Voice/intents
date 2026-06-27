"""Tests for the intentfest ``migrate_language`` subset/duplicate detector."""

import importlib
from typing import Any

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
_migrate_language: Any = importlib.import_module("script.intentfest.migrate_language")
# pylint: disable=protected-access
_strip_optionals = _migrate_language._strip_optionals
_check_subset_templates = _migrate_language._check_subset_templates
# pylint: enable=protected-access
_MigrationResult = _migrate_language.MigrationResult


def test_strip_optionals():
    """All optional groups (incl. nested) are removed and whitespace collapsed."""
    assert _strip_optionals("enciende [la] luz") == "enciende luz"
    assert _strip_optionals("enciende [la [gran]] luz") == "enciende luz"
    assert _strip_optionals("enciende la luz") == "enciende la luz"


def _subset_details(result):
    return [
        flag.detail
        for flag in result.flags
        if flag.category == "subset/duplicate templates"
    ]


def test_flags_exact_duplicate():
    result = _MigrationResult()
    result.combos = {
        "name_only": [{"sentences": ["enciende {name}", "enciende {name}"]}]
    }
    _check_subset_templates(result)
    details = _subset_details(result)
    assert len(details) == 1
    assert "exact duplicate" in details[0]


def test_flags_optional_subset():
    result = _MigrationResult()
    result.combos = {
        "name_only": [{"sentences": ["enciende {name}", "enciende [la] {name}"]}]
    }
    _check_subset_templates(result)
    details = _subset_details(result)
    assert len(details) == 1
    # The one without the optional is the subset, subsumed by the one with it.
    assert "`enciende {name}`" in details[0]
    assert "subsumed by" in details[0]


def test_no_false_positive_on_distinct_required_text():
    result = _MigrationResult()
    result.combos = {"name_only": [{"sentences": ["enciende {name}", "apaga {name}"]}]}
    _check_subset_templates(result)
    assert not _subset_details(result)


def test_no_flag_when_optional_count_ties():
    """Different optionals but equal count is too close to call — stay quiet."""
    result = _MigrationResult()
    result.combos = {
        "name_only": [{"sentences": ["[por favor] {name}", "{name} [ahora]"]}]
    }
    _check_subset_templates(result)
    assert not _subset_details(result)
