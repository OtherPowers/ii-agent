from typing import Iterable, Mapping


def otherpowers_Mycelial_field(patterns: Iterable[str]) -> Mapping[str, object]:
    p = set(patterns)

    field = {
        "conditions": {},
        "flows": {},
        "sensitivities": {},
        "affordances": [],
        "signals": [],
    }

    if "care" in p:
        field["sensitivities"]["relational"] = "high"
        field["flows"]["pace"] = "slowing"
        field["affordances"].append("co-creation-ready")
        field["signals"].append("listening stabilizes the field")

    if "pressure" in p or "capture" in p:
        field["conditions"]["pressure"] = "uneven"
        field["sensitivities"]["extractive"] = "brittle"
        field["signals"].append("small actions carry farther than force")

    if "volatility" in p:
        field["conditions"]["stability"] = "turbulent"
        field["affordances"].append("observation-preferred")

    return {k: v for k, v in field.items() if v}

