# Web page adapter (interface)

**Status:** `interface`. Fetches are not enabled (`allow_network` default false).

## Capabilities

- `page_extract`: HTML or pasted markdown → `excerpt` / `claim` with URL locator.

## Mapping rules

- Record access date as `ingested_at`; `observed_at` from Last-Modified or page date if reliable, else omit.
- Distinguish author vs site (press release vs journalist).
- Robots / ToS: if a live fetch is added, honor robots and site terms; skip authenticated-paywall reconstruction.
- Vendor blogs are `single_secondary` assertions until corroborated.

## Safety

Do not fetch LinkedIn HTML as a “web page” workaround. That is scraping.
