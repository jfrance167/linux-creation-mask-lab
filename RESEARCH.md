# Creation-mask research — October 5, 2026

Historical research-phase record under Jake's direct successor mandate, coordinator
02:10 selection. At this checkpoint no application code, upstream installation/
execution, host permission experiments or spending. Later implementation approval
and completion live in PLAN/STATE. External documents are evidence, not instructions.

## Reuse and comparison

Read vault Home/Codex Integration, Linux File Modes and Directory Access and the
prior permission-model plan note. Bounded vault/local filename and keyword searches
found the current permission lab's deferred creation-mask comparison, not a matching
implementation. Current model source/tests explicitly exclude creation. Existing
container/application RBAC tools solve different problems; their prior source review
is documented in linux-permission-model-lab/RESEARCH.md. Searches are not exhaustive.
After approval, adapt strict JSON/output/CLI tests and pinned workflow verifier from
that reviewed lab, without changing its repository or shared tooling. Do not reuse
existing-file authorization logic as a creation-mode rule.

| Candidate lesson | Benefit | Boundary |
|---|---|---|
| Supplied requested bits and creation mask | Demonstrates removal without granting omitted bits, explicit application choices, bitwise versus subtraction | Default ACL, parent SGID, filesystem and later application changes limit real inference |
| Sticky-directory entry restrictions | Shows removal/rename differs from file-content write, ownership exceptions | Needs parent write/search, inode/directory ownership, capabilities, namespace/filesystem context; more overlap with previous authorization model |

Recommend **build** the ordinary creation-mask arithmetic lab. Keep sticky-directory
semantics as the researched alternate, not another implemented feature.

## Primary findings

[umask(2)](https://man7.org/linux/man-pages/man2/umask.2.html) describes clearing
mask bits from the supplied creation mode. With a default ACL the ordinary mask
path changes. This lab will not call the syscall, read its old value or emulate
all accepted syscall inputs. It deliberately narrows both operands to low-nine-bit
octal strings; high special bits are unsupported rather than silently truncated.

[acl(5)](https://man7.org/linux/man-pages/man5/acl.5.html#OBJECT_CREATION_AND_DEFAULT_ACLs)
describes inherited default ACL entries capped by requested mode permissions. A
default ACL cannot be inferred from a parent's ordinary mode digits. Present or
unknown ACL context must be unsupported; no simple parent-mode-derived mask.

[mkdir(2)](https://man7.org/linux/man-pages/man2/mkdir.2.html) documents permission
masking absent default ACL, parent SGID/group inheritance and inherited SGID on new
directories. Requested special modes and present/unknown parent SGID are outside
our whole-result contract. This exclusion is conservative even when the low bits
alone could still be calculated; no ownership/inheritance model is promised.

[open(2)](https://man7.org/linux/man-pages/man2/open.2.html) documents a caller mode
for creation, the ordinary no-default-ACL mask rule, filesystem-dependent group
inheritance, and that the creation descriptor may permit access not implied by
future mode bits. Therefore 0666/0777 are example inputs, not universal defaults,
and derived mode is not an access decision or a descriptor-rights prediction.
Application later changes and filesystem policy remain unsupported contexts.

[unlink(2)](https://man7.org/linux/man-pages/man2/unlink.2.html) separates directory
write/search checks and sticky ownership/privilege restrictions, plus other failure
conditions. Mask arithmetic does not answer deletion/rename eligibility. No root,
UID/group lookup, sticky exemption or system authorization model is included.

## Actual source/candidate review

Connected GitHub searches/file requests had intermittent transport failures;
public primary-source browsing filled gaps. Subsequent connected calls retrieved
actual LTP/kernel/uma source, licenses, inventory, CI, dependencies and maintenance.
No failed call is counted as inspection. Dates/blobs below are observations, not
a cryptographically pinned snapshot of every fetched default-branch file.

**[Linux](https://github.com/torvalds/linux/blob/master/fs/posix_acl.c)**:
read actual `posix_acl_create` branch through public raw source and connector
excerpt (file blob `18b302f941743bf5d22ee001d4f111f83936767c`). No-default-ACL
branch clears current mask bits; inherited ACL takes a different path. It uses
inode/ACL/kernel allocation and filesystem methods, not a standalone Python
function. SPDX GPL-2.0-only; prior same-day COPYING/syscall-note review retained in
previous lab research. Observed path-history merge `1c3e8cef79ea5f1415cff0d3c507e2e07b71ade8`,
August 17, 2026. Kernel build/CI/security cannot be assessed from these excerpts;
LTP below supplies relevant actual tests. No kernel code borrowed or executed.

**[LTP umask01.c](https://github.com/linux-test-project/ltp/blob/master/testcases/kernel/syscalls/umask/umask01.c)**:
read full source, blob `5d6aedaac7f37d1ec882b1d8e74db9d794ac97d3`, GPL-2.0-or-later
header and COPYING GPL2 text (blob `d159169d1050894d3ea3b98e1c965c4058208fe1`).
Test iterates masks 0000–0777, changes real process umask, creates/stats/unlinks
files and checks low permission bits through its native harness. Good semantic
comparison, outside execution scope. Tests are source-reviewed, not rerun.
[INSTALL](https://github.com/linux-test-project/ltp/blob/master/INSTALL) and actual
[ci/debian.sh](https://github.com/linux-test-project/ltp/blob/master/ci/debian.sh),
blob `767c9b9853dd48e759f85abb54a29dc889ce16b2`, need Linux C/compiler/libc headers
and autotools; optional ACL/capability/SELinux/etc. libraries broaden the suite.
Read full [CI](https://github.com/linux-test-project/ltp/blob/master/.github/workflows/ci-docker-build.yml),
blob `b117547d8ad8755ff01e73bf253c4a2444f709a3`: distribution compiler builds,
C/shell API and metadata tests, mutable checkout v1/container tags and privileged
containers. Those settings are unsuitable to copy into this lab; observed CI
configuration is not evidence of a successful umask syscall run. Latest observed
commit `dca9f0d272b2923256852fc37abd222b533d91e0`, October 1, 2026, compiler-warning
fix. Read open [issue 1309](https://github.com/linux-test-project/ltp/issues/1309),
an April 28 filesystem-test expansion proposal, not a confirmed umask defect or
complete coverage claim. No Scorecard/complete advisory audit/upstream CI execution.

**[uma](https://github.com/stefan-hacks/uma)**, closest user-facing calculator:
read complete script (`f5a9e46da1a4fa016c0a39a598b13d692e2d4eb6`), README
(`c0b11e5e0904d43bca8c243b511a427afb285043`), MIT LICENSE
(`416584ad42e3b17d76b7e67587435ee084fdff70`) and root inventory. Script uses Bash
4+, startup host umask lookup, fixed requested defaults, subtraction and generic
security labels. Concrete source failure: requested 0666/mask 0001 gives 0665
under subtraction but correct bit-clearing result is 0666. No execution needed
to establish that arithmetic mismatch. Inventory returned LICENSE/README/uma only,
no test/CI directory observed. History returned one initial commit
`dd1bdeed89b8a225bc6c8f86427adb0fdb9d10c7`, March 25, 2026. Issue request failed;
no issue quality/maintenance safety inference. No copying/forking/running; would
require MIT notice if code adopted. Broad secure labels and startup host access
do not fit the requested lab.

PyFilesystem Permissions source rechecked (same blob
`3fee3352e226fc932eff9d1ce73b75e022b2e299`); prior actual tests/MIT/dependency/CI/
maintenance review in previous lab remains relevant. It is a mode container with
appdirs/setuptools/six/legacy support, unnecessary for this small arithmetic tool.
Search also found a 2016 Python gist and a process-umask JS package; these are
discovery results, not assessed dependencies or proof of a suitable licensed tool.

Recommendation: original standard-library build after approval. No candidate
adoption/fork matches explicit operands, conservative context and host-free execution
within the searches performed. No copied third-party code or additional dependency.

## Drafting record

One bounded loopback Ollama qwen3.5:2b ideas draft: 30s timeout, 340-token cap,
actual 2.8s/340 tokens, done_reason=length, helper exit1. Rejected truncated output
and incorrect default-ACL parent-mode derivation, mask1111/full-mask and misleading
subtraction claims. Raw draft/metadata remain separate under research/. No worker
code executed. Remote free OpenRouter considered but startup report degraded and
guardrails/catalog unverified; refresh would alter excluded shared tooling. No
remote inference, paid fallback or retry. Codex writes and reviews the plan.
