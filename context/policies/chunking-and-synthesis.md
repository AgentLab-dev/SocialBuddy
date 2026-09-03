# Chunking and synthesis

## Chunking

Chunk for **retrieval and citation**, not for token folklore.

| Source class | Unit | Notes |
| --- | --- | --- |
| Web / docs | Heading-bounded section | Keep lists with their intro sentence |
| GitHub | File region or PR body section | Do not mix LICENSE with application code |
| Email | Single message; quote history as child chunks | Redact first |
| Calendar | One event | Attendee lists may be restricted |
| CRM | One record field group (e.g. opportunity + stage) | Do not merge accounts |
| LinkedIn export | One experience item or one post | Do not glue About + all jobs into one chunk |
| Transcript | Speaker turn or 2–3 minute topic | Mark speakers |

Hard caps (assumptions — tune later): prefer 200–800 tokens equivalent; never split a table row from its header; never drop the locator.

Each chunk becomes a `document_chunk` or `excerpt` record. The statement should be usable **without** neighboring chunks.

## Synthesis

Synthesis creates `derived` records:

1. Input records listed in `related_ids`.
2. `epistemic_status` is the **min** of inputs unless the operator promotes it.
3. Contradictions are not averaged — see conflict resolution.
4. Public sentences must still cite at least one non-derived parent when challenged.

Do not synthesize a metric (“~2000 connections”) from incomplete exports. Do not synthesize a skill endorsement into a credential.
