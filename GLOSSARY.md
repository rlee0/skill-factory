# Skill Factory

This context develops, evaluates, and releases portable agent skills as curated collections.

## Language

**Skill**:
An agent-loadable directory of instructions and optional supporting resources, using the Agent Skills format.
_Avoid_: Prompt, plugin (unless referring to a runtime-specific plugin)

**Skill set**:
A curated, versioned collection of skills with declared membership, runtime compatibility, and evaluation evidence.
_Avoid_: Bundle, pack

**Set release**:
A versioned snapshot of a skill set's descriptor and exact member-skill contents, distributed with its evaluation report.
_Avoid_: Repository release (unless versioning the whole repository)

**Evaluation case**:
A representative prompt and rubric used to assess whether a skill activates appropriately and improves task outcomes.
_Avoid_: Example prompt

**Runtime baseline**:
The runtime's normal environment for the same task without the skill set under evaluation; native runtime capabilities remain available.
_Avoid_: No-skill baseline (unless all skill sources are disabled)

**Runtime matrix**:
The one or more agent runtimes a set intentionally supports and evaluates; only completed evaluations count as tested-runtime claims.
_Avoid_: Universal compatibility
