# Design: Syntagmax DSL Grammar Update

Update the Syntagmax DSL grammar to support conditions, placeholders in schema values, and new rules.

## Proposed Changes

### Grammar Update (server/syntagmax.lark)
- Add `condition` to `rule` and `trace`.
- Add `anchor` and `NOT` for conditions.
- Refactor `schema_value` to support placeholders and quoted/unquoted items.
- Import `INT` from common Lark library.
- Update `rule` to support `condition`.
- Update `trace` to support `condition`.

### LSP Server (server/server.py)
- Update `completions` function to include new keywords: `if`, `not`.

### Syntax Highlighting (syntagmax.tmLanguage.json)
- Add patterns for `if`, `not`.
- Add patterns for placeholders within schema values.

## Testing Strategy
1. Create a `reproduce_new_features.stmx` file with all new features.
2. Run `test_parser.py` (which uses `server/server.py`'s parser) to verify it fails before changes and passes after.
3. Update `test.stmx` with valid examples of the new DSL.
