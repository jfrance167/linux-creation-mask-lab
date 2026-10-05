# Linux creation-mask lab

An offline Python learning tool that derives ordinary mode bits from **explicit
invented requested modes and masks**. It reports retained/removed bits and
owner/group/other digit arithmetic. Actual creation, mode and access remain
**unverified** in every report. No host permission or umask operations occur.

## Run

Python 3.13; application uses only the standard library. From this directory:

```powershell
python -m creation_mask demo
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python tools/check_mutations.py
python -m compileall -q creation_mask tests tools
```

Ten fixed demo oracles are recorded in [CONTRACT.md](CONTRACT.md) and
[evidence/demo.json](evidence/demo.json). Requested `0666`, mask `0001` retains
`0666`: masking removes bits, and that execute bit was never requested. Subtraction
would incorrectly produce `0665`. Neither regular nor directory kind chooses
implicit requested defaults; `0666` and `0777` are examples supplied by a caller.

For invented requests, pipe UTF-8 JSON bytes to `python -m creation_mask analyze`:

```json
{"version":1,"profile":"ordinary_no_acl_v1","cases":[{"id":"Example","kind":"regular","requested_mode":"0666","mask":"0001","context":{"default_acl":"absent","parent_setgid":"absent","filesystem_policy":"ordinary_model","application_mode":"as_requested","object_state":"new"}}]}
```

This returns `model_complete`, derived_mode `0666`, removed_bits `0000`, and
explicit unverified actual outcomes. Context declarations are assumptions, not
verified observations. To demonstrate uncertainty, set default_acl to `unknown`;
the whole request becomes unsupported and contains no calculated results.

CLI exit0: completed arithmetic, including zero mode, or passing demo; exit1:
failed demo; exit2: rejected/unsupported/over-limit; exit3: input/output failure.
Partial output can remain after write/flush failure; check exit status and complete
JSON before using a report. No atomic stdout promise.

## Architecture and contract

- `creation_mask/core.py`: exact bounded validation -> copied tuples -> excluded
  context -> requested AND complement(mask) -> bounded escaped report.
- `fixtures.py`: independent hand-fixed modes/triplet rows; no oracle generation
  through production arithmetic.
- `__main__.py`: bounded JSON stdin, synthetic demos, honest output/exit handling.
- `tests/` and `tools/`: trusted harness, fixed regressions, independent bit-set
  properties, mutation proof and local CI policy checker.

Public functions: `evaluate(request)` for the exact built-in object schema;
`analyze_json(raw)` for exact UTF-8 bytes; `serialize_report(report)` for internally
constructed reports only. Input is never mutated. Read [CONTRACT.md](CONTRACT.md)
for complete keys/enums, resource units, result/status and fixture definitions.
JSON capped16KiB, nesting6, numeric tokens10 characters, cases16, IDs32 ASCII
characters, modes four octal characters; final escaped JSON capped64KiB.

Every common record validates before any unsupported outcome. Invalid later
records cannot hide behind zero arithmetic, an earlier excluded context or an
unknown bounded profile/version. Unknown versions/profiles are unsupported after
current common-shape validation; that does not validate their unknown semantics.
Empty batches reject. Any excluded context disables results for the entire batch.
High requested/mask bits are deliberately unsupported, not syscall truncation.

## Security model and limitations

Threats: malformed/oversized/duplicate input, custom-object coercion, misleading
context, arithmetic granting omitted bits, partial batches or failed I/O appearing
complete, and learners interpreting calculations as system authority. Strict
types/bounds, whole-input validation, explicit unverified outcomes, independent
oracles and no ambient host capability address these model threats.

Default ACL, parent SGID, nonordinary filesystem policy, later application changes,
existing objects or unknown required context are unsupported. The model performs
no lookup of paths/users/ACLs/actual modes, no identity/access authorization, and
no syscall. It cannot prove declarations true, creation successful or future mode
stable. Descriptor rights, sticky-directory entry rules, root/capabilities/LSM/
namespace/idmap/races/ownership are excluded. A low-bit result is not a safe/secure
label, a permission grant or full Linux/POSIX conformance. [SECURITY.md](SECURITY.md)
and [RESEARCH.md](RESEARCH.md) give sources and boundaries.

## Verified local results

Windows CPython3.13.7: 22 normal/optimized tests, ten passing demos, 8,192 property
checks with independent bit-position sets, two assertion-detected/restored logic
mutations, compilation, Bandit zero, normal/optimized workflow-policy checks and
pip check. [VERIFICATION.md](VERIFICATION.md) links receipts and limits;
[REVIEW.md](REVIEW.md) records ECC checklist self-review, not independent review.

Prepared CI: Python3.13 Windows/Ubuntu tests, compilation, demo/mutations/Bandit;
weekly/manual CodeQL, immutable reviewed Actions/minimal permissions. No remote
repository/publication, hosted CI/CodeQL or Linux experiment. Development tools
version-pinned; artifact hash lock/advisory audit/dedicated secret scanner unavailable.

MIT. No third-party code copied or executed. Linux/LTP/uma/PyFilesystem source
comparisons and license assessments in RESEARCH. Boundary/harness/workflow patterns
adapted from Jake's previous local permission lab. Codex authored/reviewed code;
local Ollama ideas draft rejected, no remote inference or paid fallback. Historical
research checkpoint is planning evidence, not the final implementation receipt.

[DECISIONS.md](DECISIONS.md) · [LEARNING.md](LEARNING.md)

Optional exercise: explain why removing a mask bit absent from the requested mode
leaves the result unchanged, and why a zero result still completes the calculation.

## Publication status

See [publication review](PUBLICATION.md) for the October 5 source snapshot, fresh local checks, evidence boundaries and current hosted-check distinction.
