"""Tests for the intentfest ``prune`` liveness graph."""

from script.intentfest.prune import _liveness_graph


def test_liveness_graph_drops_dead_keeps_transitive():
    """A rule reached only via a dead rule is dead; transitive live rules stay.

    Graph:
      sentence -> <a>
      <a> -> <b>            (b is live: reached from a live rule)
      <c> -> <d>            (c, d are dead: nothing live reaches them)
    """
    rule_bodies = {
        "a": "hello <b>",
        "b": "world",
        "c": "<d> unused",
        "d": "leaf",
    }
    live_rules, _ = _liveness_graph(rule_bodies, seed_rules={"a"}, seed_lists=set())

    assert live_rules == {"a", "b"}
    assert "c" not in live_rules  # unreferenced root is dead
    assert "d" not in live_rules  # referenced only by the dead root is dead


def test_liveness_graph_collects_lists_unicode():
    """Lists in live rule bodies are live; accented names survive the regex."""
    rule_bodies = {
        # Unicode-aware: the accented rule/list names must be picked up.
        "añadir": "pon {habitación} en {brightness:level}",
        "muerto": "{nunca}",  # list reachable only via a dead rule
    }
    live_rules, live_lists = _liveness_graph(
        rule_bodies, seed_rules={"añadir"}, seed_lists={"seed_list"}
    )

    assert live_rules == {"añadir"}
    assert "habitación" in live_lists  # accented list name not dropped
    assert "brightness" in live_lists  # slot-form {list:slot} captured
    assert "seed_list" in live_lists
    assert "nunca" not in live_lists  # only a dead rule references it
