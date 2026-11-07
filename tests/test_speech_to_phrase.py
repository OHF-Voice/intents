"""Speech-to-Phrase subset verification.

A ``speech_to_phrase``-tagged data block is meant to be a *lean* phrasing that
the constrained Speech-to-Phrase STT grammar can enumerate cheaply. When a combo
also has untagged (rich) blocks, Home Assistant drops the tagged block from its
grammar (see ``partition_speech_to_phrase`` and the loader in
``test_slot_combinations.py``). That is only sound if the lean block's language
is a *subset* of the rich blocks' language -- otherwise Speech-to-Phrase could
recognise a phrasing Home Assistant never would.

Containment is checked by *matching*, not by enumerating both sides. The lean
side is enumerated (it is small and non-recursive by construction) and each
phrasing is then handed to hassil's recognizer built from the rich blocks: if
the rich grammar accepts it, it is in the rich language. Enumerating the rich
side instead is what the first version of this test did, and it does not scale
-- English is small enough to get away with it, but e.g. the Spanish
``HassTurnOn`` blocks expand into billions of phrasings and exhaust memory.

Slots are neutralised on both sides: every ``{list}`` reference is replaced with
a per-list sentinel word, and the rich grammar gets a one-value text list for
each, so matching compares phrasing structure rather than slot contents (which
would need entities, areas and floors that this test deliberately does not load).

Languages are discovered from the tagged blocks themselves.
"""

import importlib
import re
from typing import Any

import pytest
import yaml
from hassil import Intents, SlotList, TextSlotList, normalize_whitespace, recognize
from hassil.sample import sample_sentence

from . import RULES_DIR, SENTENCES_DIR

_util: Any = importlib.import_module("script.intentfest.util")
partition_speech_to_phrase = _util.partition_speech_to_phrase


def _languages_with_s2p_blocks() -> list[str]:
    """Every language that has at least one ``speech_to_phrase``-tagged block.

    Discovered rather than hard-coded so adding a language's lean blocks does
    not also require editing this list (and so a branch per language does not
    collide here)."""
    langs = []
    for lang_dir in sorted(p for p in SENTENCES_DIR.iterdir() if p.is_dir()):
        for combo_path in lang_dir.glob("*/*.yaml"):
            data = (yaml.safe_load(combo_path.read_text()) or {}).get("data", [])
            if any(b.get("speech_to_phrase") for b in data):
                langs.append(lang_dir.name)
                break
    return langs


LANGUAGES = _languages_with_s2p_blocks()

_SLOT_REF = re.compile(r"\{([^{}]+)\}")


def _load_expansion_rules(language: str) -> dict[str, str]:
    rules: dict[str, str] = {}
    rules_dir = RULES_DIR / language
    if rules_dir.is_dir():
        for rule_path in rules_dir.glob("*.yaml"):
            rule_dict = yaml.safe_load(rule_path.read_text()) or {}
            rules.update(rule_dict.get("expansion_rules", {}))
    return rules


def _list_name(ref: str) -> str:
    """``timer_hours:hours`` -> ``timer_hours``; ``0..100`` -> ``_range``."""
    name = ref.split(":", 1)[0].strip()
    return "_range" if re.match(r"^-?\d+\s*\.\.", name) else name


def _sentinel(list_name: str) -> str:
    """A single word that cannot collide with real vocabulary."""
    return "zz" + re.sub(r"[^a-z0-9]+", "", list_name.lower()) + "zz"


def _lean_phrasings(
    sentences: list[str], language: str, rules: dict[str, str]
) -> set[str]:
    """Every phrasing the lean templates produce, with each slot reference
    replaced by its sentinel word."""
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
                text = _SLOT_REF.sub(lambda m: _sentinel(_list_name(m.group(1))), text)
                out.add(normalize_whitespace(text).strip())
    return out


def _referenced_lists(sentences: list[str], rules: dict[str, str]) -> set[str]:
    """List names reachable from these templates, following expansion rules."""
    seen_rules: set[str] = set()
    names: set[str] = set()
    pending = list(sentences)
    while pending:
        text = pending.pop()
        names.update(_list_name(m) for m in _SLOT_REF.findall(text))
        for rule_name in re.findall(r"<([a-zA-Z0-9_]+)>", text):
            if rule_name in rules and rule_name not in seen_rules:
                seen_rules.add(rule_name)
                pending.append(rules[rule_name])
    return names


def _rich_intents(
    sentences: list[str], language: str, rules: dict[str, str]
) -> tuple[Intents, dict[str, SlotList]]:
    """Rich blocks as a recognizer, with every referenced list bound to its
    sentinel so slot *contents* never affect the match."""
    intents = Intents.from_dict(
        {
            "language": language,
            "intents": {
                "_S2P": {"data": [{"sentences": sentences, "slots": {"x": "y"}}]}
            },
            "expansion_rules": rules,
        }
    )
    slot_lists: dict[str, SlotList] = {
        name: TextSlotList.from_strings([_sentinel(name)])
        for name in _referenced_lists(sentences, rules)
    }
    # An inline range (`{0..100}`) keeps its own ref text, so bind that too.
    slot_lists.setdefault("_range", TextSlotList.from_strings([_sentinel("_range")]))
    return intents, slot_lists


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
    rich_sentences = [s for block in ha_blocks for s in block["sentences"]]
    rich, slot_lists = _rich_intents(rich_sentences, lang, rules)

    for block in s2p_only:
        extra = [
            phrasing
            for phrasing in sorted(_lean_phrasings(block["sentences"], lang, rules))
            if recognize(phrasing, rich, slot_lists=slot_lists) is None
        ]
        assert not extra, (
            f"{lang}/{intent}/{combo}: {len(extra)} Speech-to-Phrase phrasing(s) "
            f"not recognised by the Home Assistant (rich) block(s): "
            f"{extra[:10]}"
        )


def test_speech_to_phrase_cases_exist() -> None:
    """Guard against the collector silently finding nothing (e.g. a rename that
    drops every tag), which would make the subset test vacuously pass."""
    assert _CASES, "No speech_to_phrase blocks with an untagged sibling were found"
