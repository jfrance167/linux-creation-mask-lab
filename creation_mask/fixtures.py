"""Hand-fixed invented arithmetic oracles, frozen independently before code."""


def case(requested="0666", mask="0022", *, case_id="Example", kind="regular") -> dict:
    return {"id": case_id, "kind": kind, "requested_mode": requested, "mask": mask,
            "context": {"default_acl": "absent", "parent_setgid": "absent",
                        "filesystem_policy": "ordinary_model", "application_mode": "as_requested",
                        "object_state": "new"}}


def request(*cases) -> dict:
    return {"version": 1, "profile": "ordinary_no_acl_v1", "cases": list(cases) if cases else [case()]}


def oracles() -> list[tuple]:
    # requested, mask, derived, removed, fixed owner/group/other integer rows.
    return [
        ("0666", "0022", "0644", "0022", ((6, 0, 6, 0), (6, 2, 4, 2), (6, 2, 4, 2))),
        ("0777", "0027", "0750", "0027", ((7, 0, 7, 0), (7, 2, 5, 2), (7, 7, 0, 7))),
        ("0666", "0001", "0666", "0000", ((6, 0, 6, 0), (6, 0, 6, 0), (6, 1, 6, 0))),
        ("0400", "0000", "0400", "0000", ((4, 0, 4, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ("0000", "0000", "0000", "0000", ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ("0777", "0777", "0000", "0777", ((7, 7, 0, 7), (7, 7, 0, 7), (7, 7, 0, 7))),
        ("0400", "0377", "0400", "0000", ((4, 3, 4, 0), (0, 7, 0, 0), (0, 7, 0, 0))),
        ("0510", "0027", "0510", "0000", ((5, 0, 5, 0), (1, 2, 1, 0), (0, 7, 0, 0))),
        ("0753", "0251", "0502", "0251", ((7, 2, 5, 2), (5, 5, 0, 5), (3, 1, 2, 1))),
        ("0755", "0000", "0755", "0000", ((7, 0, 7, 0), (5, 0, 5, 0), (5, 0, 5, 0))),
    ]


def observed(result: dict) -> tuple:
    return (result["derived_mode"], result["removed_bits"],
            tuple(tuple(row[field] for field in ("requested", "mask", "retained", "removed"))
                  for row in result["triplets"]))
