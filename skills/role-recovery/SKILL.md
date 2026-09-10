# Skill: role-recovery

Purpose: restore the current working picture for one Staff Office without replaying its whole history.

Inputs: role ID, incumbent identity if known, last reliable checkpoint.

Read: original/current authority pointer, Office CURRENT, unprocessed primary work surface, active pending items and only the project states needed for current duties.

Output: role, incumbent/lifecycle, responsibilities, current projects, pending, blockers, reporting line, authority boundaries, next safe action and source refs.

If incumbent identity or authority conflicts, report the conflict and stop affected execution.
