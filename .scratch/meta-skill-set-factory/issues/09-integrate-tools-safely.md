# 09: Integrate tools safely

**What to build:** A maintainer can design tool-using skills with explicit requirements and safeguards, while preventing unsupported tool behavior from being claimed as tested.

**Blocked by:** 04: Author portable skills from an approved design; 07: Review safety and obtain expert sign-off; 08: Evaluate activation and task outcomes.

**Status:** ready-for-agent

- [ ] Identify required tools, permissions, credentials, environment assumptions, and failure modes before adding an integration.
- [ ] Inspect scripts and supporting resources for unsafe behavior and minimize privileges and sensitive-data exposure.
- [ ] Document runtime-specific requirements and safe behavior when tools or credentials are unavailable.
- [ ] Require an appropriate sandboxed evaluation path before claiming tool behavior as tested; otherwise mark it untested and block unsupported release claims.
- [ ] Do not build a universal sandbox as part of this capability.
- [ ] Include evaluation cases for missing tools, denied permissions, unsafe tool instructions, and honest reporting of untested behavior.
