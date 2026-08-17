"""Tests for the per-sentence typo checks in validate.

Covers validate_sentence_scripts (look-alike letters from the wrong script) and
validate_rule_directions (a sentence reaching for the opposite direction's rule).
"""

import importlib
from typing import Any

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
validate: Any = importlib.import_module("script.intentfest.validate")


def _entries(*sentences, intent="HassTurnOn", path="sentences/xx/HassTurnOn/a.yaml"):
    return [(path, intent, sentence) for sentence in sentences]


def _scripts(*sentences, **kwargs):
    warnings: list[str] = []
    validate.validate_sentence_scripts(_entries(*sentences, **kwargs), warnings)
    return warnings


def _directions(*sentences, **kwargs):
    errors: list[str] = []
    validate.validate_rule_directions(_entries(*sentences, **kwargs), errors)
    return errors


# --------------------------------------------------------------------------
# validate_sentence_scripts
# --------------------------------------------------------------------------


def test_latin_letter_in_cyrillic_sentence_warns():
    """A bare Latin c standing in for Cyrillic с is reported."""
    warnings = _scripts(
        "включи таймер [c (именем|названием)] {name}",
        "выключи таймер на кухне",
    )

    assert len(warnings) == 1
    assert "U+0063" in warnings[0]
    assert "LATIN" in warnings[0]
    assert "CYRILLIC" in warnings[0]


def test_correct_cyrillic_letter_does_not_warn():
    """The same sentence with Cyrillic с is clean."""
    assert not _scripts(
        "включи таймер [с (именем|названием)] {name}",
        "выключи таймер на кухне",
    )


def test_latin_offered_as_alternative_does_not_warn():
    """A Latin spelling offered alongside the native one is intentional.

    Languages deliberately accept both "k" and "к"/"кельвин" for kelvin, so the
    letter being *one option among several* is the signal that it is wanted.
    """
    assert not _scripts(
        "установи температуру {temperature}[[ ](k|к|кельвин[ов|а])]",
        "установи температуру света в спальне",
    )


def test_latin_in_optional_alternative_does_not_warn():
    """The `[ k| келвина]` form (bg) is also an alternative, not a sequence."""
    assert not _scripts(
        "зададени температура {temperature}[ k| келвина]",
        "намали температурата в спалнята",
    )


def test_latin_language_does_not_warn_on_its_own_letters():
    """A Latin-script language is not reported for using Latin letters."""
    assert not _scripts(
        "turn on the light in the kitchen",
        "set a timer for 5 minutes",
    )


def test_cyrillic_letter_in_latin_sentence_warns():
    """The check works in the other direction too."""
    # "с" here is U+0441 CYRILLIC SMALL LETTER ES, not Latin c.
    warnings = _scripts(
        "turn on the light [с (named)] {name}",
        "set a timer for 5 minutes",
    )

    assert len(warnings) == 1
    assert "U+0441" in warnings[0]


def test_non_confusable_script_is_ignored():
    """Han mixed with Hiragana is normal Japanese, not a look-alike risk."""
    assert not _scripts(
        "キッチンの照明をつけて",
        "タイマーを5分に設定して",
    )


def test_multi_letter_foreign_word_is_ignored():
    """Loanwords are intentional; only single-letter tokens are look-alike risks."""
    assert not _scripts(
        "привет home assistant",
        "включи свет на кухне",
    )


def test_no_sentences_is_noop():
    """An empty language produces no warnings."""
    assert not _scripts()


# --------------------------------------------------------------------------
# validate_rule_directions
# --------------------------------------------------------------------------


def test_opposite_direction_rule_errors():
    """An increase intent referencing a decrease rule is an error."""
    errors = _directions(
        "<timer_decrease> {timer_hours:hours} часа таймеру",
        intent="HassIncreaseTimer",
        path="sentences/ru/HassIncreaseTimer/hours_only.yaml",
    )

    assert len(errors) == 1
    assert "increase" in errors[0]
    assert "timer_decrease" in errors[0]


def test_matching_direction_rule_is_clean():
    """The correct rule for the intent produces no error."""
    assert not _directions(
        "<timer_increase> {timer_hours:hours} часа таймеру",
        intent="HassIncreaseTimer",
        path="sentences/ru/HassIncreaseTimer/hours_only.yaml",
    )


def test_direction_check_is_symmetric():
    """A decrease intent referencing an increase rule is also caught."""
    errors = _directions(
        "<timer_increase> {timer_hours:hours} часа таймеру",
        intent="HassDecreaseTimer",
        path="sentences/ru/HassDecreaseTimer/hours_only.yaml",
    )

    assert len(errors) == 1
    assert "decrease" in errors[0]


def test_pause_unpause_pair():
    """pause/unpause is treated as a direction pair."""
    errors = _directions(
        "<timer_unpause> таймер",
        intent="HassPauseTimer",
        path="sentences/ru/HassPauseTimer/default.yaml",
    )

    assert len(errors) == 1
    assert "unpause" in errors[0]


def test_unpause_intent_does_not_match_its_own_pause_token():
    """HassUnpauseTimer with <timer_unpause> must not be flagged.

    "unpause" contains "pause", so a naive substring check would report the
    correct rule as the opposite one.
    """
    assert not _directions(
        "<timer_unpause> таймер",
        intent="HassUnpauseTimer",
        path="sentences/ru/HassUnpauseTimer/default.yaml",
    )


def test_rule_naming_both_directions_is_not_flagged():
    """A rule whose name covers both directions is not an opposite reference."""
    assert not _directions(
        "<timer_increase_decrease> таймер",
        intent="HassIncreaseTimer",
        path="sentences/ru/HassIncreaseTimer/hours_only.yaml",
    )


def test_on_off_is_deliberately_not_a_pair():
    """<on> is a preposition rule in several languages, so on/off is excluded."""
    assert not _directions(
        "<turn_off> [<the>] {name} (<in>|<of>|<at>|<on>) [<the>] {floor}",
        intent="HassTurnOff",
        path="sentences/it/HassTurnOff/name_floor.yaml",
    )


def test_unrelated_intent_is_clean():
    """An intent with no direction marker is never flagged."""
    assert not _directions(
        "<turn_on> [<the>] {name}",
        intent="HassTurnOn",
        path="sentences/en/HassTurnOn/name_only.yaml",
    )
