# Email adapter (interface)

**Status:** `interface`. Provider-agnostic (Gmail, Exchange, Fastmail, …).

## Capabilities (read)

- `thread_extract` → `excerpt`, `relationship`.

## Mapping rules

- Default sensitivity `restricted` until classified.
- Quote chains become child chunks; the latest message is parent.
- Signatures often contain phone numbers — redact.
- Never use a prospect’s inbound email body in a public post.

## Forbidden

Sending mail, auto-follow-up sequences, harvesting mailing lists for LinkedIn invites.
