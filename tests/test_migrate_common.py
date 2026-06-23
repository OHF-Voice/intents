"""Tests for the intentfest ``migrate_common`` rule inlining."""

import importlib
from typing import Any

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
_migrate_common: Any = importlib.import_module("script.intentfest.migrate_common")
# pylint: disable=protected-access
_inline_optional_rules = _migrate_common._inline_optional_rules
_is_single_enclosing_group = _migrate_common._is_single_enclosing_group
_wrap_optional_body = _migrate_common._wrap_optional_body
# pylint: enable=protected-access


def test_is_single_enclosing_group():
    """Only a single bracket/paren enclosing the whole string counts."""
    assert _is_single_enclosing_group("[en|de]")
    assert _is_single_enclosing_group("([en|de] el)")
    assert not _is_single_enclosing_group("[en] [de]")  # two groups
    assert not _is_single_enclosing_group("en [el]")  # leading text
    assert not _is_single_enclosing_group("plain")


def test_wrap_optional_body_keeps_single_group():
    """An already-enclosing optional body is spliced as-is; others are wrapped."""
    assert _wrap_optional_body("[[en|de] [el|la]|del]") == "[[en|de] [el|la]|del]"
    assert _wrap_optional_body("[en] [el]") == "([en] [el])"


def test_inline_optional_rules_substitutes_and_reports():
    """A skipped optional rule is inlined into every referencing copied rule."""
    grouped = {
        "common": {
            "area": "<en_el> {area}",
            "planta": "<en_el> {floor}",
            "unrelated": "{name}",
        }
    }
    skipped_optional = {"en_el": "[[en|de] [el|la]|del]"}

    inlined = _inline_optional_rules(grouped, skipped_optional)

    assert grouped["common"]["area"] == "[[en|de] [el|la]|del] {area}"
    assert grouped["common"]["planta"] == "[[en|de] [el|la]|del] {floor}"
    assert grouped["common"]["unrelated"] == "{name}"  # untouched
    assert inlined == {"en_el": {"area", "planta"}}


def test_inline_optional_rules_resolves_chain():
    """A chain of optional rules resolves to a fixpoint."""
    grouped = {"common": {"area": "<en_el> {area}"}}
    skipped_optional = {
        "en_el": "[<de> [el|la]]",
        "de": "[en|de]",
    }

    inlined = _inline_optional_rules(grouped, skipped_optional)

    assert "<en_el>" not in grouped["common"]["area"]
    assert "<de>" not in grouped["common"]["area"]
    assert "area" in inlined["en_el"]
