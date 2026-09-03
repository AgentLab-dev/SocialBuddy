# Contributing

## Principles

- Prefer decision frameworks and checklists over slogans.
- Label examples. Label assumptions. Label mock data.
- Do not add live credentials, scraping, or silent outbound actions.
- Keep the default test path dependency-free (`python3` + stdlib).

## Adding a skill

1. Copy the heading contract in `skills/_schema/skill.schema.json`.
2. Place the file under `skills/<category>/`.
3. Add an entry to `skills/catalog.json`.
4. Run `python3 scripts/validate.py`.

Required H2 sections: Purpose; Activation / Use Cases; Inputs; Procedure; Quality Rubric; Failure Modes; Safety Notes; Example Outputs; Verified vs Assumed.

## Adding an adapter

1. Document the interface in `context/adapters/`.
2. Implement `ContextAdapter` only if you need executable code.
3. Ship mock samples before any live client.
4. Writes go through `socialbuddy.approval`.

## Tests

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```
