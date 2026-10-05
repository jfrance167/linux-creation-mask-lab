# Verification — October 5, 2026

Actual runtime Windows CPython3.13.7 (`evidence/runtime.json`). Commands executed
from this lab directory with installed Python313; no host umask/permission or
Linux filesystem experiments, no upstream test execution/dependency installation.

| Check | Observed result | Receipt |
|---|---|---|
| `python -m unittest discover -s tests -v` | 22 pass, exit0 | evidence/tests.txt |
| `python -O -m unittest discover -s tests -v` | 22 pass, exit0 | evidence/tests-optimized.txt |
| Property test within each suite | 8192 independent bit-set checks, intentional repeated pairs | test_independent_bit_set_properties in tests.txt |
| `python -m creation_mask demo` | ten fixed mode/triplet cases pass, exit0 | evidence/demo.json |
| `python tools/check_mutations.py` | two faults each cause one assertion failure/zero errors; restored regressions pass, exit0 | evidence/mutations.json |
| `python -m compileall -q creation_mask tests tools` | exit0 | evidence/compile.txt and functional-exits.json |
| Actual CLI stdin pipes | absent-mask-bit and zero modes complete exit0; unknown ACL unsupported exit2 | evidence/cli-*.json |
| `python -m bandit -r creation_mask tools -f json` | zero findings/errors, exit0;324 source lines analyzed | evidence/bandit.json |
| `python tools/verify_workflows.py` normal/optimized | local YAML policy PASS, exit0 each | evidence/workflows*.json |
| `python -m pip check` | no broken requirements, exit0 | evidence/pip-check.txt |
| Bounded common credential patterns/manual review | zero flagged files | evidence/content-review.json |

Actual exit summaries in evidence/functional-exits.json, security-exits.json and
cli-exits.json. Eight source/test/tool SHA256 bindings in source-hashes.json refer
to current local bytes, not an external attestation or future modifications.

Fixed oracles frozen in CONTRACT before code: ten modes/removed/owner/group/other
rows; tests run each with both object kinds. Property corpus:8 requested values
x512 masks plus512 requested values x8 masks, duplicates intentional, independent
binary-position sets. Verifies retained difference/subset/disjointness, removed
intersection/disjointness and reconstitution. Not all262144 pairs or a benchmark.
Mutations inject subtraction and missing requested intersection in memory only;
assertion failure required, test errors do not count; originals restored/rerun.

Boundary evidence: exact types/custom keys/coercion, unknown/missing fields/context,
duplicate cases/JSON keys, zero/empty distinction, all-case validation before known
exclusions or unknown bounded version/profile, high bits unsupported, malformed
UTF8 and trailing JSON, bytes at16384/one-over, counts16/17, identifiers32/33,
mode grammar, numeric tokens10/11, lexical depth6/7, delimiters inside strings,
input mutation, independent JSON/direct report agreement, escaped output and fixed
unverified claims. CLI bounded read and read/write/short/flush failure statuses.

Guard honesty: accepted schema needs depth4; depth6/7 probes malformed structure
and direct scanner seams, not valid deeper application records. Valid versions
fit9 decimal digits; numeric10/11 probes malicious/out-of-range lexical inputs.
Accepted report size cannot naturally reach64KiB; exact-output/one-over uses
oversized **trusted formatter payloads** and CLI fallback uses patched serialization.
Host-call guard preimports trusted setup; exercises model/evaluation/formatting with
open/eval/exec/available OSumask/stat/access/chmod/chown/identity/traversal/process/
network calls blocked. It is focused test evidence, not malware containment.

Initial test discovery launched in parent directory, failed before tests; corrected
lab-directory invocation passed. No application fix needed for that launch mistake.
ECC actual-code self-review found zero outstanding actionable defects; REVIEW.md.

Prepared CI copies reviewed prior lab baseline and adds compilation: Python3.13
Windows/Ubuntu, normal/optimized tests, demo/mutations/Bandit, weekly/manual CodeQL,
minimum permissions and checkout credential persistence disabled. Pins reused from
same-day official-source verification: checkout v7.0.1
`3d3c42e5aac5ba805825da76410c181273ba90b1`, setup-python v7.0.0
`5fda3b95a4ea91299a34e894583c3862153e4b97`, CodeQL v4.38.2 peeledcommit
`2892aa5e19bbd11bc0cff5427e3b750a04d9e3c2`. Local verifier checks these fixed
pins, YAML/triggers/permissions/persistence/schedule, not GitHub execution.

Limits: Windows-only runtime, no full Linux/POSIX conformance, actual creation/
mode/access/context verification, hosted Actions/CodeQL, GitHub eligibility/
protections, dedicated secret scanner/exhaustive history scan, dependency artifact
hash lock or comprehensive advisory audit. `pip check` tests compatibility only.
Bandit/ECC clean is not proof of safety/independent review. No paid/remote worker,
publication/merge/deployment. Prior completed repositories remain clean/unchanged.
