#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from yaml import safe_load

from .const import INTENTS_FILE
from .util import get_base_arg_parser

_TYPE_MAP = {
    "str": "string",
    "int": "integer",
    "float": "number",
}


def slot_to_schema(slot: dict[str, Any]) -> dict[str, Any]:
    """Convert one YAML slot definition to a JSON Schema property."""
    raw_type = slot.get("type", "str")
    raw_types = raw_type if isinstance(raw_type, list) else [raw_type]

    schema: dict[str, Any] = {
        "type": [_TYPE_MAP.get(t, t) for t in raw_types],
    }

    if len(schema["type"]) == 1:
        schema["type"] = schema["type"][0]

    if desc := slot.get("description"):
        schema["description"] = desc

    if "enum" in slot:
        # Important: if enum only applies to strings, split mixed schemas with anyOf.
        if isinstance(raw_type, list) and "str" in raw_type and len(raw_type) > 1:
            numeric_schemas = []
            if "int" in raw_type:
                int_schema: dict[str, Any] = {"type": "integer"}
                if "min" in slot:
                    int_schema["minimum"] = slot["min"]
                if "max" in slot:
                    int_schema["maximum"] = slot["max"]
                numeric_schemas.append(int_schema)

            schema = {
                "description": slot.get("description", ""),
                "anyOf": [
                    {"type": "string", "enum": slot["enum"]},
                    *numeric_schemas,
                ],
            }
            return schema

        schema["enum"] = slot["enum"]

    if "min" in slot:
        schema["minimum"] = slot["min"]
    if "max" in slot:
        schema["maximum"] = slot["max"]

    return schema


def intent_to_tool(intent_name: str, intent: dict[str, Any]) -> dict[str, Any]:
    """Convert one intent to an OpenAI tool/function spec."""
    slots = intent.get("slots") or {}
    combinations = intent.get("slot_combinations") or {}

    properties = {
        slot_name: slot_to_schema(slot_def) for slot_name, slot_def in slots.items()
    }

    valid_combinations = []
    for combo_name, combo in combinations.items():
        required = list(combo.get("slots") or [])

        # Only include slot names that actually exist as properties.
        missing = [s for s in required if s not in properties]
        if missing:
            raise ValueError(
                f"{intent_name}.{combo_name} references undefined slot(s): {missing}"
            )

        valid_combinations.append(
            {
                "title": combo_name,
                "description": combo.get("description", combo_name),
                "required": required,
                "properties": {name: properties[name] for name in required},
                "additionalProperties": False,
            }
        )

    parameters: dict[str, Any] = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }

    if valid_combinations:
        # This permits only the listed required slot combinations.
        # With additionalProperties:false, extra slots are still allowed unless blocked
        # by the alternative schemas below. See stricter variant below.
        parameters["anyOf"] = valid_combinations
    else:
        parameters["required"] = [
            name for name, slot in slots.items() if slot.get("required") is True
        ]

    return {
        "type": "function",
        "function": {
            "name": intent_name,
            "description": intent.get("description", intent_name),
            "parameters": parameters,
        },
    }


def yaml_intents_to_openai_tools(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert loaded YAML dict to OpenAI tools."""
    tools = []

    for intent_name, intent in data.items():
        if not isinstance(intent, dict):
            continue

        if intent.get("supported") is False:
            continue

        tools.append(intent_to_tool(intent_name, intent))

    return tools


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument("--intents", default=INTENTS_FILE, help="Intents YAML file")
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    with open(args.intents, "r", encoding="utf-8") as intents_file:
        intents_dict = safe_load(intents_file)

    tools = yaml_intents_to_openai_tools(intents_dict)
    json.dump(tools, sys.stdout, indent=2)

    return 0
