"""Speech-to-Phrase subset verification (Method B).

A ``speech_to_phrase``-tagged data block is meant to be a *lean* phrasing that
the constrained Speech-to-Phrase STT grammar can enumerate cheaply. When a combo
also has untagged (rich) blocks, Home Assistant drops the tagged block from its
grammar (see ``partition_speech_to_phrase`` and the loader in
``test_slot_combinations.py``). That is only sound if the lean block's language
is a *subset* of the rich blocks' language -- otherwise Speech-to-Phrase could
recognise a phrasing HA never would.

We verify containment by enumeration rather than with an FST/OpenFST toolchain:
lean blocks are finite and small by construction, so we expand every phrasing on
both sides (slots rendered as literal ``{list}`` sentinels via
``expand_lists=False``) and assert ``lean_phrasings <= rich_phrasings``. This is
complete for the lean side (no recursion, bounded fan-out) and needs no slot
lists, entities, or intent context.

Only English is wired up for now; the collector is language-agnostic.
"""

import importlib
from pathlib import Path
from typing import Any

import pytest
import yaml
from hassil import Intents, normalize_whitespace
from hassil.sample import sample_sentence

from . import RULES_DIR, SENTENCES_DIR

_util: Any = importlib.import_module("script.intentfest.util")
partition_speech_to_phrase = _util.partition_speech_to_phrase

LANGUAGES = ["en"]


def _load_expansion_rules(language: str) -> dict[str, str]:
    rules: dict[str, str] = {}
    rules_dir = RULES_DIR / language
    if rules_dir.is_dir():
        for rule_path in rules_dir.glob("*.yaml"):
            rule_dict = yaml.safe_load(rule_path.read_text()) or {}
            rules.update(rule_dict.get("expansion_rules", {}))
    return rules


def _phrasings(sentences: list[str], language: str, rules: dict[str, str]) -> set[str]:
    """Every phrasing a set of templates can produce, with slots left as literal
    ``{list}`` sentinels (``expand_lists``/``expand_ranges`` disabled) so the two
    sides are compared on phrasing structure, not enumerated slot values."""
    intents = Intents.from_dict(
        {
            "language": language,
            "intents": {"_S2P": {"data": [{"sentences": sentences}]}},
            "expansion_rules": rules,
        }
    )
    parsed_rules = intents.expansion_rules
    out: set[str] = set()
    for intent_data in intents.intents["_S2P"].data:
        for sentence in intent_data.sentences:
            for text in sample_sentence(
                sentence,
                slot_lists=None,
                expansion_rules=parsed_rules,
                expand_lists=False,
                expand_ranges=False,
            ):
                out.add(normalize_whitespace(text).strip())
    return out


def _collect() -> list[tuple[str, str, str]]:
    """(language, intent, combo) for every combo file with a Speech-to-Phrase
    block that has an untagged sibling (i.e. something to verify)."""
    cases: list[tuple[str, str, str]] = []
    for language in LANGUAGES:
        lang_dir = SENTENCES_DIR / language
        for combo_path in sorted(lang_dir.glob("*/*.yaml")):
            data = (yaml.safe_load(combo_path.read_text()) or {}).get("data", [])
            _ha, s2p_only = partition_speech_to_phrase(data)
            if s2p_only:
                cases.append((language, combo_path.parent.name, combo_path.stem))
    return cases


_CASES = _collect()


@pytest.mark.parametrize("lang,intent,combo", _CASES)
def test_speech_to_phrase_is_subset(lang: str, intent: str, combo: str) -> None:
    combo_path = SENTENCES_DIR / lang / intent / f"{combo}.yaml"
    data = yaml.safe_load(combo_path.read_text())["data"]
    ha_blocks, s2p_only = partition_speech_to_phrase(data)

    assert (
        ha_blocks
    ), f"{intent}/{combo}: tagged block has no untagged sibling to verify"

    rules = _load_expansion_rules(lang)
    rich = _phrasings(
        [s for block in ha_blocks for s in block["sentences"]], lang, rules
    )

    for block in s2p_only:
        lean = _phrasings(block["sentences"], lang, rules)
        extra = lean - rich
        assert not extra, (
            f"{lang}/{intent}/{combo}: {len(extra)} Speech-to-Phrase phrasing(s) "
            f"not recognised by the Home Assistant (rich) block(s): "
            f"{sorted(extra)[:10]}"
        )


def test_speech_to_phrase_cases_exist() -> None:
    """Guard against the collector silently finding nothing (e.g. a rename that
    drops every tag), which would make the subset test vacuously pass."""
    assert _CASES, "No speech_to_phrase blocks with an untagged sibling were found"
