"""Pure invented-mode arithmetic, with no ambient host capabilities."""

import json
import re

MAX_INPUT_BYTES = 16_384
MAX_OUTPUT_BYTES = 65_536
MAX_DEPTH = 6
MAX_NUMERIC_CHARS = 10
MAX_CASES = 16
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}", re.ASCII)
CONTEXT = {
    "default_acl": ("absent", "present", "unknown"),
    "parent_setgid": ("absent", "present", "unknown"),
    "filesystem_policy": ("ordinary_model", "other", "unknown"),
    "application_mode": ("as_requested", "later_change", "unknown"),
    "object_state": ("new", "existing", "unknown"),
}
ASSUMPTIONS = ("invented_operands", "declared_context_only", "ordinary_no_acl_subset")
NOT_VERIFIED = ("actual_creation", "actual_mode", "actual_access", "context_truth", "future_mode")


class _Invalid(ValueError):
    def __init__(self, reason: str, status: str = "rejected"):
        self.reason = reason
        self.status = status


def _outcome(status: str, reason: str) -> dict:
    return {"status": status, "complete": status == "model_complete", "reason": reason,
            "actual_creation": "unverified", "actual_mode": "unverified", "actual_access": "unverified",
            "assumptions": list(ASSUMPTIONS), "not_verified": list(NOT_VERIFIED)}


def _keys(value: object, expected: set[str]) -> dict:
    if type(value) is not dict or len(value) != len(expected):
        raise _Invalid("object_shape")
    # Reject custom keys before performing input-key hash/equality operations.
    if any(type(key) is not str for key in value) or set(value) != expected:
        raise _Invalid("object_shape")
    return value


def _identifier(value: object) -> str:
    if type(value) is not str or len(value) > 32 or IDENTIFIER.fullmatch(value) is None:
        raise _Invalid("identifier")
    return value


def _mode(value: object) -> int:
    if type(value) is not str or len(value) != 4 or re.fullmatch(r"[0-7]{4}", value, re.ASCII) is None:
        raise _Invalid("mode_grammar")
    return int(value, 8)


def _case(value: object) -> tuple:
    record = _keys(value, {"id", "kind", "requested_mode", "mask", "context"})
    case_id = _identifier(record["id"])
    kind = record["kind"]
    if type(kind) is not str or kind not in ("regular", "directory"):
        raise _Invalid("kind")
    requested, mask = _mode(record["requested_mode"]), _mode(record["mask"])
    context = _keys(record["context"], set(CONTEXT))
    declarations = []
    for field, values in CONTEXT.items():
        declaration = context[field]
        if type(declaration) is not str or declaration not in values:
            raise _Invalid("context_enum")
        declarations.append((field, declaration))
    return case_id, kind, requested, mask, tuple(declarations)


def _validated(request: object) -> tuple:
    envelope = _keys(request, {"version", "profile", "cases"})
    version = envelope["version"]
    if type(version) is not int or not 0 <= version <= 999_999_999:
        raise _Invalid("version_range")
    profile = _identifier(envelope["profile"])
    values = envelope["cases"]
    if type(values) is not list or not values:
        raise _Invalid("cases_shape")
    if len(values) > MAX_CASES:
        raise _Invalid("case_limit", "over_limit")
    # Eagerly validate every common record before any unsupported-context logic.
    # Unknown version/profile does not authorize parsing an unknown schema.
    cases = tuple(_case(value) for value in values)
    identifiers = [case[0] for case in cases]
    if len(set(identifiers)) != len(identifiers):
        raise _Invalid("duplicate_case")
    unsupported = []
    for reason, condition in (("version", version != 1), ("profile", profile != "ordinary_no_acl_v1")):
        if condition:
            unsupported.append({"case_id": None, "reason": reason})
    for case_id, _, requested, mask, context in cases:
        for reason, condition in (("high_requested_bits", requested > 0o777), ("high_mask_bits", mask > 0o777)):
            if condition:
                unsupported.append({"case_id": case_id, "reason": reason})
        for field, value in context:
            if value != CONTEXT[field][0]:
                unsupported.append({"case_id": case_id, "reason": f"{field}_{value}"})
    unsupported.sort(key=lambda item: (item["case_id"] or "", item["reason"]))
    return cases, unsupported


def _retained(requested: int, mask: int) -> int:
    return requested & ~mask & 0o777


def _calculate(case: tuple) -> dict:
    case_id, kind, requested, mask, _ = case
    retained = _retained(requested, mask)
    removed = requested & mask
    triplets = []
    for label, shift in (("owner", 6), ("group", 3), ("other", 0)):
        triplets.append({"class": label, "requested": (requested >> shift) & 7,
                         "mask": (mask >> shift) & 7, "retained": (retained >> shift) & 7,
                         "removed": (removed >> shift) & 7})
    return {"id": case_id, "kind": kind, "requested_mode": f"{requested:04o}", "mask": f"{mask:04o}",
            "derived_mode": f"{retained:04o}", "removed_bits": f"{removed:04o}", "triplets": triplets}


def evaluate(request: object) -> dict:
    """Calculate exact supplied-record ordinary mode bits, never host outcomes.

    Validate the entire current common schema before exclusions; unknown bounded
    version/profile is unsupported only after common records validate. No partial
    results or caller mutation. Empty/invalid input is never completed arithmetic.
    """
    try:
        cases, unsupported = _validated(request)
        if unsupported:
            return {**_outcome("unsupported", "outside_subset"), "unsupported_reasons": unsupported}
        return {**_outcome("model_complete", "ordinary_arithmetic_only"),
                "formula": "requested & ~mask & 0777", "results": [_calculate(case) for case in cases]}
    except _Invalid as error:
        return _outcome(error.status, error.reason)


def _depth(text: str) -> None:
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise _Invalid("depth_limit", "over_limit")
        elif char in "]}":
            depth -= 1


def _unique(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise _Invalid("duplicate_key")
        result[key] = value
    return result


def _integer(token: str) -> int:
    if len(token) > MAX_NUMERIC_CHARS:
        raise _Invalid("numeric_token_limit", "over_limit")
    return int(token)


def _reject_number(token: str) -> None:
    if len(token) > MAX_NUMERIC_CHARS:
        raise _Invalid("numeric_token_limit", "over_limit")
    raise _Invalid("non_integer_number")


def analyze_json(raw: object) -> dict:
    """Strict bounded exact UTF8 bytes -> current common-schema report."""
    if type(raw) is not bytes:
        return _outcome("rejected", "input_type")
    if len(raw) > MAX_INPUT_BYTES:
        return _outcome("over_limit", "input_limit")
    try:
        text = raw.decode("utf-8", errors="strict")
        _depth(text)
        return evaluate(json.loads(text, object_pairs_hook=_unique, parse_int=_integer,
                                   parse_float=_reject_number, parse_constant=_reject_number))
    except _Invalid as error:
        return _outcome(error.status, error.reason)
    except (UnicodeError, ValueError, RecursionError):
        return _outcome("rejected", "invalid_json_or_utf8")


def serialize_report(report: dict) -> bytes:
    """Escape/cap internally constructed reports; fallback is incomplete."""
    encoded = json.dumps(report, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":")).encode("utf-8") + b"\n"
    if len(encoded) > MAX_OUTPUT_BYTES:
        return serialize_report(_outcome("over_limit", "output_limit"))
    return encoded
