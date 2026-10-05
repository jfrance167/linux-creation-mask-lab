# Proposed creation-mask lab — October 5, 2026

Tier 3 learning/security semantics project, research/planning only. Coordinator
02:10 selection under Jake's previously verified direct successor mandate; the
message alone is not human authorization for broader actions. Sole writer existing
chat 01a10a3a-83b0-7623-97b5-930acdb8c864, separate linux-creation-mask-lab directory.
Stages 1–3 approved October5 02:31 by coordinator under Jake's verified mandate.
The addendum below and CONTRACT.md were recorded before code.
Cutoff for new scope October 6, 08:00 Eastern.

## Problem and success

Explain how an explicitly supplied requested mode and creation mask determine
ordinary permission bits under a narrow no-default-ACL model. Many examples hide
the application's requested mode or teach subtraction, which can invent unrequested
bits. Success: independently fixed arithmetic examples, explicit context exclusions,
complete-record validation, bounded deterministic API/CLI and source-backed limits.
Never output safe/secure, actual access or successful creation assertions.

Recommend original dependency-free Python 3.13 model. Source/candidate and alternate
assessment in RESEARCH.md. Sticky-directory entry semantics is the researched
alternate; defer it because ownership/capability/parent checks add a different
authorization contract. No upstream code copied/installed/executed.

## Scope, architecture and proposed frozen contract

Pure supplied-record calculator, JSON stdin/escaped JSON stdout and inert demo.
No real paths/users, filesystem permission experiments, process umask lookup/set,
chmod/chown/access/stat/identity/traversal, shell/container/VM/network/clock calls.
Trusted harness may read its own source/configuration/write documentation/evidence.
No system permission changes, publication/merge, new chats/subagents/schedulers,
parent/shared-tool edits or spending.

Runtime modules: pure core validation/arithmetic/report; fixed invented fixture
table; bounded CLI. Reuse reviewed previous lab's JSON/CLI boundary patterns and
local pinned workflow verifier after approval. Inspect/adapt, do not duplicate
or import previous project's authorization/OS capabilities. No runtime dependencies.

Proposed API root exact built-in dict keys `version`, `profile`, `cases`.
Version exact int 0–999999999 (bool rejected); version1 supported, otherwise
unsupported after structural validation. Profile exact ASCII identifier
`[A-Za-z][A-Za-z0-9_-]{0,31}`; `ordinary_no_acl_v1` supported, other valid profiles
unsupported. Cases exact built-in list, 1–16 records, unique IDs. Each exact dict:
`id`, `kind`, `requested_mode`, `mask`, `context`. ID same finite identifier grammar.
Kind exact `regular`/`directory`; other kinds rejected. Both mode operands exact
four-character octal `[0-7]{4}` strings; 0000–0777 supported. Special requested
bits **or high mask bits** yield unsupported (narrow contract, not syscall
truncation semantics). No numeric mode/coercion/symbolic mode/default guessing.

Required context exact dict with five enum-string fields:

| Field | Supported declaration | Other known declarations -> unsupported |
|---|---|---|
| default_acl | absent | present, unknown |
| parent_setgid | absent | present, unknown |
| filesystem_policy | ordinary_model | other, unknown |
| application_mode | as_requested | later_change, unknown |
| object_state | new | existing, unknown |

Unknown enum values/keys, wrong types, duplicate case IDs or mismatched shapes
reject; context declarations cannot establish actual conditions. A caller's
`as_requested` means arithmetic for that declared creation stage only; no future
mode stability claim. Neither object kind supplies default requested bits.

Validate every supplied case/context/operand before semantic reporting, even if
an earlier record is unsupported or computes zero. Any invalid/over-limit input
returns an incomplete envelope with no partial results. If all valid but any
excluded context/version/profile/special mode exists, entire batch unsupported,
sorted fixed reason records, no calculated modes. Do not hide later malformed
records behind context exclusions. Exact built-in types; no subclass hooks/key
coercion/iteration. No input mutation or caller-provided executable objects.

Complete arithmetic: low-nine-bit requested AND complement(mask), never subtraction,
OR, union with complement or unmasked complement. Retained bits subset of requested;
retained AND mask zero; removed=requested AND mask. Per-case output echoes validated
canonical operands/id/kind, derived_mode, removed_bits (both four-octal strings),
three fixed owner/group/other triplet rows (requested/mask/retained/removed digits).
Rows are explanatory arithmetic, not permission-class selection or authorization.

Envelope status model_complete/rejected/unsupported/over_limit, complete Boolean,
fixed reason/assumptions and actual_creation/actual_mode/actual_access all unverified.
Only complete adds results. Unsupported adds bounded safe case-ID/fixed-reason
records. No user strings in error messages or universal security score.

Bounds: exact UTF-8 bytes <=16384 before decode/JSON; depth<=6 outside strings;
numeric token<=10 including sign, floats/constants rejected, duplicate JSON keys
rejected. Mode lengths checked before regex, ID<=32, fixed finite enum cardinality.
API equivalent semantic limits. Output compact ensure_ascii JSON+LF <=65536;
over-limit formatter produces incomplete fallback. Formatter for internal reports
only. CLI read cap+1, check short writes/flush, no atomic stdout guarantee. Exit0
complete arithmetic (including zero mode)/passing demo, exit1 failed demo only,
exit2 invalid/unsupported/over-limit, exit3 I/O error with fixed stderr JSON.

## Independent proposed fixtures (freeze before implementation)

Both regular/directory kinds use supplied operands identically. Expected results
below are hand-derived triplet intersections, never calculated by the tested model.

| Case | Requested | Mask | Derived | Removed |
|---|---|---|---|---|
| Explicit file example | 0666 | 0022 | 0644 | 0022 |
| Explicit directory example | 0777 | 0027 | 0750 | 0027 |
| Mask has unrequested execute bit | 0666 | 0001 | 0666 | 0000 |
| No grant from complement | 0400 | 0000 | 0400 | 0000 |
| Zero requested | 0000 | 0000 | 0000 | 0000 |
| Remove every ordinary bit | 0777 | 0777 | 0000 | 0777 |
| All absent bits in mask | 0400 | 0377 | 0400 | 0000 |
| Explicit nonstandard application request | 0510 | 0027 | 0510 | 0000 |
| Overlapping mixed digits | 0753 | 0251 | 0502 | 0251 |
| Zero mask identity | 0755 | 0000 | 0755 | 0000 |

Example row oracle for 0666/0022: owner requested6/mask0/retained6/removed0;
group requested6/mask2/retained4/removed2; other same as group. Freeze all demo
row expectations independently before code. Same operands with either object kind
must give the same low-bit arithmetic. Changing an unrequested mask bit must not
change retained bits. No special bits silently dropped: requested4755 or mask1000
unsupported even when an arithmetic sub-result might be available. Any context
present/unknown unsupported; malformed later operands/IDs/context reject first.

## Threat model and tradeoffs

Assets: honest educational results, trustworthy incomplete status, bounded process
resource use and no ambient host capability. Adversary supplies malformed JSON,
duplicate IDs/keys, coercion objects, misleading unsupported context and oversized
operands; or interprets arithmetic as a host-security verdict. Strict types/limits,
whole-input validation, explicit assumptions and no access-success labels mitigate
these model threats. Fixtures protect against subtraction/default/complement bugs.

Records may be fabricated or false; model cannot prove actual parent ACL/SGID,
application behavior, filesystem identity/policy, existence/races or creation
success. No root/capability/LSM/namespace/idmap/sticky/access behavior is modeled.
Those affect real system interpretation, not permission-bit truth for invented
operands. Conservative context exclusions may decline cases where isolated low-bit
arithmetic is still useful; prefer whole-contract honesty. No malicious-code
isolation, full Linux/POSIX conformance, dependency safety or universal-safe claim.

## Stages and definitions of done

1. Freeze approved schema/precedence/context and independent mode/triplet fixtures.
   Implement pure stdlib selector/report and strict JSON API. Done: explicit
   operands, all-field validation, no complement grants/subtraction/defaults,
   unsupported rules, no mutation/host capability and bounded parsing.
2. Add CLI/demo and meaningful regressions. Done: fixed modes and rows, kind
   equivalence, absent-bit/all-bit boundaries, malformed/special/context precedence,
   exact types/duplicate IDs/keys, API/JSON byte/depth/token/count/string/output
   limits, invalid UTF-8/control/surrogate identifiers, short/failed I/O. Guard model
   against host umask/open/chmod/chown/access/stat/identity/traversal/process/network
   calls while preserving trusted harness setup. No actual Linux experiments.
3. ECC actual-code self-review, two isolated in-memory logic mutations (subtraction
   and missing requested intersection) detected by independent fixed expectations,
   restore/rerun, normal/optimized tests and available Bandit/workflow checks.
   Done: actual source bindings/exit evidence, corrected findings, README/security/
   license/AI disclosure/DECISIONS/LEARNING/STATE, authorized Obsidian milestone,
   clean independent local branch. CI pinned/minimal/manual-weekly CodeQL prepared;
   no hosted results or publication claim. No automatic dependency installation
   or exemption from current free-only/artifact/advisory limits.

Verification scales to untrusted-input/security semantics without promising arbitrary
coverage percentages. Reuse focused check commands, no upstream live-test execution.
Missing dedicated secret scanner/artifact hash lock/hosted CodeQL/Linux runtime
evidence remains disclosed. Local Ollama draft rejected; remote free capacity
unverified and shared-tool refresh excluded. No remote inference or paid fallback.

Next: implement and verify the three approved local stages.

## Approval addendum — October 5, 02:31 (before code)

SUCCESSORS.md Creation-mask implementation approval: all cases/current common
exact schema validate before unsupported outcomes. Empty batches/malformed required
values invalid; no partial modes for unsupported batch. Unknown bounded version/
profile unsupported only after current common-envelope/record validation, not a
claim to understand an unknown schema. High mask/requested bits deliberately
unsupported, no syscall truncation. No implicit object-kind modes; zero is complete.
Actual creation/mode/access unverified. Freeze units/status/oracles (CONTRACT).
Require subset/disjoint/removed properties, assertion-detected subtraction/missing
intersection mutations, normal/optimized/output/compile/Bandit/ECC checks. Label
unreachable production bounds and injected seams honestly. Trusted harness may
read/write own artifacts; no live umask/stat/access/chmod/chown/identity/real-target
experiments. Separate local Git/codex branch/pinned CI approved, no remote/parent
changes/publication. Complete records/vault; preserve prior limits/cutoff/free-only.
