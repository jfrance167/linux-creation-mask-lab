# Security policy

Local educational arithmetic over invented non-sensitive records only. Neither a
completed calculation nor supplied context authorizes any real resource operation.
No host umask/permission/identity/path lookup or mutation. Python environment is
not a malware sandbox; untrusted executable code is not an input to this tool.

Boundary: raw bytes/exact API objects -> complete current common validation ->
excluded contexts -> pure low-bit calculation -> escaped capped report. Trusted
harness reads its own configuration/source and writes artifacts separately.

Covered model threats: wrong types, custom key/coercion objects, malformed/duplicate
records, finite parse/resource bounds, subtraction/complement grants, unsupported
context or zero hiding later errors, incomplete batch output, false I/O success.
Reports carry actual_creation/actual_mode/actual_access=unverified. Partial stdout
is possible on I/O failure; exit3 never signals a completed write.

Not covered: actual records/context truth, successful creation, filesystem/ACL/
inheritance/LSM/capability/ownership/race policy, descriptor rights, future application
changes, sticky deletion/rename or host containment. High mask bits excluded even
though the real umask syscall discards them; this is a deliberately narrower model.

For a defect, preserve an invented minimal request, source revision, Python version,
observed report/exit and expected contract behavior. Use an agreed private channel;
no disclosure endpoint or SLA configured. Never attach private credentials,
employer/client data or real private filesystem/user records.
