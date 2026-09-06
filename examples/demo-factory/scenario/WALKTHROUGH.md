# One fictional Factory, two projects

Everything here is authored fiction. Candidate labels, receipts, review outcomes
and historical notes are not real development/test evidence. This compact
record-based scenario does not create an operational mailbox or a live worker.

## Facilities and their authoritative surfaces

| Facility | Read here | Boundary |
| --- | --- | --- |
| Role/appointment register | [factory.json](factory.json), `assignments` and linked decision | Selected demo role is not the reader's real identity. |
| Project Rooms / current state | [Atlas](projects/atlas.json), [Beacon](projects/beacon.json) | One current state per fictional project. |
| Meeting / candidate / evidence register | [records.json](records.json), `changes` and `evidence` | A review covers its named candidate only. |
| Inbox body / sent and CC references | `records.json`, `messages` and `references` | Each body occurs once; references contain no copy. |
| Portfolio Console | [console.json](console.json) | Reads state pointers, never becomes execution owner. |
| Work Invocation History | `records.json`, `work/atlas-session` | Receipt acknowledges a blocked result, not success. |
| Historical continuity | `records.json`, `history` | Historical notes/handoffs cannot grant current authority. |

## Follow the connected story

The director assigns Atlas, with a bounded prepare/request-review scope. A
management task has one recipient body, one sender reference and Console CC.
A completed fictional change at `fixture:atlas-c1` shows matching evidence,
separate review targets, an explicit integration decision and subsequent readback.

A later change was reviewed at `fixture:atlas-c2` but now stands at
`fixture:atlas-c3`. Atlas's current state points to that active change. Its
result reply goes back to management and preserves Console visibility. The
Console reports the target mismatch from Atlas state; it does not fix or approve
it. The work-session receipt is complete even though the result is BLOCKED.
No live session ID, actual liveness or verified evidence is invented.

Beacon has no current incumbent or assignment. Its historical fictional handoff
cannot fill that gap. The Console reports the vacancy to management, while Atlas
has no authority to appoint a Beacon worker. Atlas's first appointment has no
predecessor handoff; keep the unrelated Beacon history separate.

## What is and is not integrated

The story integrates references and reasoning across the facilities, not the
held implementation branches. It can be read using plain Markdown/JSON on its
own. These compact records are not input to the boot, reply or work-history
CLIs. Wiring their separate schemas into a combined executable acceptance
harness remains later work after authorized integration/revalidation.

Use the [cold-takeover procedure](../../../docs/COLD_TAKEOVER_EXERCISE.md)
for real observed agent behavior. Static fixture checks are not a fresh-agent
run, independent review or permission to merge/publish the framework.
