# Skill: project-recovery

Purpose: prepare a compact recovery package for a project context after a chat/model/workspace change or other continuity event.

Inputs: project ID, current context identity if known, last reliable checkpoint.

Read: current Project Room/state, active Issue/PR, Project Primary authority pointer, relevant evidence and unresolved pending items.

Output: project, canonical repository, current state, active Issue, last verified ref/SHA, pending, blockers, accepted decisions, do-not-reopen items, authority boundaries, next safe action and evidence refs.

A new chat/model/device alone does not create a new tenure or handoff.
