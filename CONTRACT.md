# Frozen contract and oracles — October 5, before code

PLAN exact root/record/context keys, finite enums, cardinalities/strings and integer
ranges apply. Exact built-in dict/list/str/int only; bool/subclasses reject. Mode
strings exactly four octal characters, unknown kinds/context enums invalid, known
excluded context/high mode bits unsupported only after all current common fields
validate. Empty cases invalid; 16 maximum. IDs unique across complete batch,
ASCII [A-Za-z][A-Za-z0-9_-]{0,31}. Version0..999999999/profilevalididentifier
unknown -> unsupported after common validation; no unknown-schema semantics claim.

Status precedence: invalid encountered during complete common structural validation
-> rejected (size/depth/token/cardinality resource guards -> over_limit). No
unsupported or arithmetic decision before all records validate. When invalid data
exists, neither prior excluded context nor zero result masks it. If all valid but
any unsupported condition, entire envelope unsupported with no results. Otherwise
model_complete with results, including zero derived mode. First invalid reason
is deterministic validation order, not exhaustive diagnosis of every malformed field.

Raw resource units: bytes<=16384 inclusive before UTF8 decode/JSON, structural
nesting<=6 outside strings, numeric token<=10 characters including sign; float/
constant rejected, duplicate JSON keys rejected. API semantic cardinality/grammar
bounds apply independently. JSON decoder still authoritatively checks syntax.

Complete result: id/kind/requested_mode/mask canonical echoed values;
derived_mode=requested & ~mask & 0777, removed_bits=requested & mask, formatted
exactly four-octal-character strings. Triplets in fixed owner/group/other order:
class string, requested/mask/retained/removed exact integer digits0..7. No identity
class selection or bitwise permission authorization. Output tuple expectations
are fixed below before implementation, not generated from production code.

Reports always status, complete, reason, actual_creation/actual_mode/actual_access
unverified, fixed assumptions/not_verified arrays. Complete adds results and fixed
formula string. Unsupported adds reasons list of {case_id: id or null, reason:
fixed string}, sorted by (case_id or empty string, reason); global version/profile
reasons use null. Case reasons high_requested_bits/high_mask_bits and
<context_field>_<known_excluded_value>. Incomplete never adds results/formula.

Serialization internal reports only: ensure_ascii, no NaN, compact UTF8 JSON+LF
<=65536 bytes inclusive. If exceeded replace with incomplete output_limit; no
streaming partial model report. Full valid ordinary report under16 records/32-char
IDs cannot naturally reach64KiB; test formatter boundary with trusted oversized
internal payload and label as injected seam, not a reachable accepted input.
CLI read cap+1; exact write count and flush required. Short/read/write/flush failures
exit3 with fixed stderr JSON and possible partial stdout, no atomic write claim.
CLI0 completed arithmetic (zero included)/passing demo;1 failed demo;2 incomplete.

Ten oracles: columns requested/mask/derived/removed and owner,group,other rows
with each row (requested,mask,retained,removed). Source arithmetic hand-checked.

| Requested | Mask | Derived | Removed | Owner | Group | Other |
|---|---|---|---|---|---|---|
| 0666 | 0022 | 0644 | 0022 | 6,0,6,0 | 6,2,4,2 | 6,2,4,2 |
| 0777 | 0027 | 0750 | 0027 | 7,0,7,0 | 7,2,5,2 | 7,7,0,7 |
| 0666 | 0001 | 0666 | 0000 | 6,0,6,0 | 6,0,6,0 | 6,1,6,0 |
| 0400 | 0000 | 0400 | 0000 | 4,0,4,0 | 0,0,0,0 | 0,0,0,0 |
| 0000 | 0000 | 0000 | 0000 | 0,0,0,0 | 0,0,0,0 | 0,0,0,0 |
| 0777 | 0777 | 0000 | 0777 | 7,7,0,7 | 7,7,0,7 | 7,7,0,7 |
| 0400 | 0377 | 0400 | 0000 | 4,3,4,0 | 0,7,0,0 | 0,7,0,0 |
| 0510 | 0027 | 0510 | 0000 | 5,0,5,0 | 1,2,1,0 | 0,7,0,0 |
| 0753 | 0251 | 0502 | 0251 | 7,2,5,2 | 5,5,0,5 | 3,1,2,1 |
| 0755 | 0000 | 0755 | 0000 | 7,0,7,0 | 5,0,5,0 | 5,0,5,0 |

Property verification proposed corpus: eight representative requested values against
all512 masks and all512 requests against eight representative masks (8192 checks,
duplicates intentional). Independent bit-position set difference/intersection
oracle; retained subset, mask-disjoint, removed-set equality and reconstitution.
Not an exhaustive all-pair campaign, timing benchmark or real-filesystem test.
