# 10: Adapt and validate runtime support

**What to build:** A maintainer can document runtime-specific differences and make precise support claims based only on completed evaluation evidence.

**Blocked by:** 03: Design the set and guide the factory workflow; 08: Evaluate activation and task outcomes.

**Status:** ready-for-agent

- [ ] Keep portable Agent Skills behavior as the default and identify any runtime-specific instructions or requirements explicitly.
- [ ] Select an intentional runtime matrix and define the evidence required for each claimed runtime.
- [ ] Record exact runtime versions, model identifiers, and passing results before marking a runtime as tested.
- [ ] Leave unsupported or unevaluated runtimes untested; never infer universal compatibility from one passing runtime.
- [ ] Include evaluation cases for documenting runtime differences and refusing unsupported compatibility claims.
