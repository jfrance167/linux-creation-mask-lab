# Research learning — October 5, 2026

A mask clears bits, not numbers. Requested0666/mask0001 must retain0666 because
the execute bit was never requested; subtraction0665 invents different bits.
Complement alone would grant omitted requested bits. Explicit operands matter.

Default ACL is not a mask inferred from parent mode. Inherited ACL handling and
parent SGID/filesystem/application context limit predictions of complete real modes.
Mask arithmetic is separate from descriptor access and sticky entry restrictions.

The local ideas draft was truncated and confidently invented ACL derivation and
a full-mask1111 example. Source checking rejected it before plan acceptance.
Research findings and hand-derived examples were frozen before implementation.

Verified: ten fixed mode/triplet oracles for both kinds, 8192 independent bit-set
property checks (intentional duplicates, not every512x512 pair), normal/optimized
tests and two assertion-detected logic mutations. Restored regressions pass; no
real filesystem comparison or broad mutation coverage claim.

Whole-common-shape validation prevents earlier excluded context or zero arithmetic
from hiding malformed later cases. A trusted oversized formatter payload tests an
otherwise unreachable output limit; label that seam instead of claiming accepted
input can reach it. Source-only uma arithmetic defect was not executed/fixed.

First test discovery mistakenly ran from the parent directory and failed before
discovery; corrected lab directory invocation passed. Explicit working directories
matter when several independent labs share a workspace.
