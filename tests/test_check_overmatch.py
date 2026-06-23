"""Tests for the intentfest ``check_overmatch`` cross-intent probe."""

import importlib
from typing import Any

from hassil import Intents, TextSlotList

# Loaded dynamically: a static ``from script.intentfest...`` import would make
# mypy resolve the module under both ``intentfest.*`` and ``script.intentfest.*``
# (the package has no ``script/__init__.py``), tripping "source file found twice".
_check_overmatch: Any = importlib.import_module("script.intentfest.check_overmatch")
check_sentence = _check_overmatch.check_sentence


def _build_intents() -> Intents:
    """A tiny two-intent language where one intent greedily steals the other.

    ``GreedyPlay`` has a wildcard ``{search_query}`` that swallows almost any
    sentence, including the one that should belong to ``LightSet`` -- this is the
    same shape as the real es bug ("pon la luz al máximo" stolen by
    HassMediaSearchAndPlay's greedy wildcard).
    """
    return Intents.from_dict(
        {
            "language": "xx",
            "lists": {
                "search_query": {"wildcard": True},
                "name": {"values": ["the lamp"]},
            },
            "intents": {
                "LightSet": {
                    "data": [
                        {
                            # Requires the {name} list to match; if that list is
                            # absent at recognize time, this never fires.
                            "sentences": ["set {name} to max"],
                            "metadata": {"slot_combination": "name_only"},
                        }
                    ]
                },
                "GreedyPlay": {
                    "data": [
                        {
                            "sentences": ["play {search_query}", "set {search_query}"],
                            "metadata": {"slot_combination": "query_only"},
                        }
                    ]
                },
            },
        }
    )


def test_check_sentence_flags_cross_intent_overmatch():
    """The greedy intent stealing a LightSet utterance is reported.

    The utterance is one LightSet has no template for (a template gap), so only
    GreedyPlay's wildcard matches it -- a cross-intent false positive that the
    per-intent suite, scoped to LightSet's own Intents, would never surface.
    """
    intents = _build_intents()
    finding = check_sentence(
        intents,
        slot_lists={
            "name": TextSlotList.from_strings(["the lamp"], name="name"),
        },
        language="xx",
        expected_intent="LightSet",
        expected_combo="name_only",
        sentence="set the lamp to maximum brightness",
    )

    assert finding is not None
    assert finding.kind == "mismatch"
    assert finding.won_intent == "GreedyPlay"
    assert finding.won_combo == "query_only"


def test_check_sentence_passes_when_expected_intent_wins():
    """A sentence only its own intent matches yields no finding."""
    intents = _build_intents()
    finding = check_sentence(
        intents,
        slot_lists={},
        language="xx",
        expected_intent="GreedyPlay",
        expected_combo="query_only",
        sentence="play some jazz",
    )

    assert finding is None


def test_check_sentence_reports_no_match():
    """A sentence nothing recognizes is reported as a no-match."""
    intents = Intents.from_dict(
        {
            "language": "xx",
            "intents": {
                "LightSet": {
                    "data": [{"sentences": ["turn on the light"]}],
                },
            },
        }
    )
    finding = check_sentence(
        intents,
        slot_lists={},
        language="xx",
        expected_intent="LightSet",
        expected_combo="name_only",
        sentence="completely unrelated gibberish xyzzy",
    )

    assert finding is not None
    assert finding.kind == "no_match"
