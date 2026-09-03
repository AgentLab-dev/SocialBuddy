# Calendar adapter (interface)

**Status:** `interface`. Provider-agnostic (Google Calendar, Microsoft 365, CalDAV, …).

## Capabilities (read)

- `event_read` → `event` (title, time range, public vs private calendar).

## Mapping rules

- Private titles → `redacted` or generic “Busy.”
- Attendee emails: redact unless internal and needed for a sourcing/work graph **internal** memo.
- Recurring series: store the series id; do not explode years of instances into the bundle.

## Forbidden

Auto-booking meetings as part of LinkedIn outreach.
