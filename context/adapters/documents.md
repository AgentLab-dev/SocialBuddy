# Document adapter (interface)

**Status:** `interface`. Handles operator-supplied files (Markdown, text, PDF text layer, office docs later).

## Capabilities

- `file_chunk`: bytes or text + filename → `document_chunk`s per chunking policy.

## Mapping rules

- Filename and hash in locator (`file:sha256:...` or path the operator accepts).
- PDFs without a text layer: status `unknown`, do not OCR in this revision.
- Slide decks: one chunk per slide plus title.
- Resumes: treat as `operator_asserted` until corroborated; still redact third-party phone numbers.

## Safety

Skip macros-enabled office files for ingest in v1. Do not execute embedded content.
