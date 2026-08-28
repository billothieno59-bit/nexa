# NEXA Canonical Module Map

| Universal | Canonical Path |
|---|---|
| UCL | core/interaction/communication/ |
| UAL | core/interaction/accessibility/ |
| UPL | core/perception/ |
| USL | core/semantic/ |
| UKL | core/knowledge/ |
| UIL | core/identity/ |
| UOL | core/execution/orchestrator/ |
| UML | core/execution/uml/ |
| UTL | core/governance/trust/ |
| Cognition | core/cognition/ |
| JARVIS Interface | core/interface/jarvis/ |

## Rule

These are the authoritative locations of the corresponding architectural responsibilities.

No duplicate canonical roots should be introduced without an explicit architectural revision.

## Cognition subfolder plan

`core/cognition/` is the permanent name (matches CONSTITUTION.md). `core/cognitive/` must never be created — any reference to "cognitive" as a directory name is an error and should be corrected to "cognition".

Planned subfolders under `core/cognition/`:
- thinking/ (exists)
- brain/
- self_reflection/
- learning/
- skills/
- devices/
- memory/ (exists — session memory)

Session memory lives at core/cognition/memory/, matching CONSTITUTION.md's statement that cognition is responsible for "reasoning, planning, memory, learning, and decision processes."